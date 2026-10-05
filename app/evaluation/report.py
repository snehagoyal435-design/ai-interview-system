# ============================================
# AI Interview System - Report Generator
# ============================================
# Yeh file interview ka PDF report banati hai.
# ReportLab use kar rahe hain.
# ============================================

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
from sqlalchemy.orm import Session

from app.models import Interview, Question, User


# ============================================
# 1. OUTPUT FOLDER
# ============================================

REPORT_OUTPUT_DIR = "reports"


def ensure_report_dir():
    """Reports folder banao agar nahi hai."""
    os.makedirs(REPORT_OUTPUT_DIR, exist_ok=True)


# ============================================
# 2. RATING NIKALO SCORE SE
# ============================================

def get_rating(score: float) -> str:
    """Score ke basis pe rating string return karta hai."""
    if score >= 9:
        return "Excellent"
    elif score >= 7:
        return "Good"
    elif score >= 5:
        return "Average"
    else:
        return "Needs Improvement"


# ============================================
# 3. PDF REPORT GENERATE KARO
# ============================================

def generate_pdf_report(interview_id: int, db: Session) -> dict:
    """
    Interview ka complete PDF report banata hai.
    
    Returns:
        dict with:
        - success: True/False
        - file_path: PDF file ka path
        - error: error message
    """
    # Step 1: Interview + User + Questions fetch karo
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        return {"success": False, "file_path": None, "error": "Interview not found"}
    
    user = db.query(User).filter(User.id == interview.user_id).first()
    questions = (
        db.query(Question)
        .filter(Question.interview_id == interview_id)
        .all()
    )
    
    if not questions:
        return {"success": False, "file_path": None, "error": "No questions found"}
    
    # Step 2: Folder banao
    ensure_report_dir()
    
    # Step 3: File path
    filename = f"report_interview_{interview_id}.pdf"
    file_path = os.path.join(REPORT_OUTPUT_DIR, filename)
    
    # Step 4: PDF document banao
    try:
        doc = SimpleDocTemplate(
            file_path,
            pagesize=A4,
            rightMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            topMargin=0.5 * inch,
            bottomMargin=0.5 * inch,
        )
        
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            "TitleStyle",
            parent=styles["Title"],
            fontSize=22,
            textColor=colors.HexColor("#1a237e"),
            spaceAfter=20,
        )
        heading_style = ParagraphStyle(
            "HeadingStyle",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=colors.HexColor("#283593"),
            spaceBefore=15,
            spaceAfter=8,
        )
        body_style = ParagraphStyle(
            "BodyStyle",
            parent=styles["BodyText"],
            fontSize=10,
            leading=14,
        )
        
        # Content build karo
        elements = []
        
        # Title
        elements.append(Paragraph("AI Interview Report", title_style))
        elements.append(Spacer(1, 10))
        
        # Candidate info
        info_data = [
            ["Candidate:", user.email if user else "N/A"],
            ["Job Role:", interview.job_role],
            ["Date:", interview.created_at.strftime("%Y-%m-%d %H:%M")],
            ["Status:", interview.status.title()],
        ]
        info_table = Table(info_data, colWidths=[1.5 * inch, 5 * inch])
        info_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e8eaf6")),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("PADDING", (0, 0), (-1, -1), 6),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 20))
        
        # Summary section
        elements.append(Paragraph("Performance Summary", heading_style))
        
        scored_questions = [q for q in questions if q.score is not None]
        if scored_questions:
            avg_score = sum(q.score for q in scored_questions) / len(scored_questions)
            rating = get_rating(avg_score)
        else:
            avg_score = 0
            rating = "Not Evaluated"
        
        summary_data = [
            ["Total Questions:", str(len(questions))],
            ["Evaluated:", str(len(scored_questions))],
            ["Average Score:", f"{avg_score:.1f}/10"],
            ["Overall Rating:", rating],
        ]
        summary_table = Table(summary_data, colWidths=[2 * inch, 4.5 * inch])
        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#fff3e0")),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 11),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Question-wise analysis
        elements.append(PageBreak())
        elements.append(Paragraph("Question-wise Analysis", heading_style))
        elements.append(Spacer(1, 10))
        
        for i, q in enumerate(questions, 1):
            # Question number + text
            q_text = f"<b>Q{i}:</b> {q.question_text}"
            elements.append(Paragraph(q_text, body_style))
            elements.append(Spacer(1, 5))
            
            # Answer
            answer_text = q.answer_text or "(Not answered)"
            ans_text = f"<b>Your Answer:</b> {answer_text[:500]}"
            elements.append(Paragraph(ans_text, body_style))
            elements.append(Spacer(1, 5))
            
            # Score
            score_text = f"<b>Score:</b> {q.score}/10" if q.score is not None else "<b>Score:</b> Not evaluated"
            elements.append(Paragraph(score_text, body_style))
            elements.append(Spacer(1, 5))
            
            # Feedback
            if q.feedback:
                feedback_clean = q.feedback.replace("\n", "<br/>")
                elements.append(Paragraph(f"<b>Feedback:</b>", body_style))
                elements.append(Paragraph(feedback_clean, body_style))
            
            elements.append(Spacer(1, 15))
        
        # Footer note
        elements.append(Spacer(1, 30))
        elements.append(Paragraph(
            "<i>Generated by AI Interview System</i>",
            ParagraphStyle("Footer", parent=body_style, textColor=colors.grey, fontSize=9),
        ))
        
        # Build PDF
        doc.build(elements)
        
        return {
            "success": True,
            "file_path": file_path,
            "error": None,
        }
    
    except Exception as e:
        return {
            "success": False,
            "file_path": None,
            "error": f"PDF generation failed: {str(e)}",
        }


# ============================================
# 4. TEXT SUMMARY
# ============================================

def get_text_report(interview_id: int, db: Session) -> dict:
    """
    Simple text-based report return karta hai (frontend ke liye).
    """
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        return {"success": False, "error": "Interview not found"}
    
    user = db.query(User).filter(User.id == interview.user_id).first()
    questions = db.query(Question).filter(Question.interview_id == interview_id).all()
    
    scored = [q for q in questions if q.score is not None]
    avg_score = sum(q.score for q in scored) / len(scored) if scored else 0
    
    return {
        "success": True,
        "candidate": user.email if user else "N/A",
        "job_role": interview.job_role,
        "status": interview.status,
        "total_questions": len(questions),
        "evaluated": len(scored),
        "average_score": round(avg_score, 1),
        "rating": get_rating(avg_score),
        "questions": [
            {
                "number": i,
                "question": q.question_text,
                "answer": q.answer_text,
                "score": q.score,
                "feedback": q.feedback,
            }
            for i, q in enumerate(questions, 1)
        ],
        "error": None,
    }