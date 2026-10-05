# ============================================
# AI Interview System - AI Prompts
# ============================================
# Yeh file saare AI prompts store karti hai.
# Har prompt ek template hai jo AI ko instruction deta hai.
# ============================================


# ============================================
# 1. QUESTION GENERATION PROMPT
# ============================================

QUESTION_GENERATION_PROMPT = """
You are an expert technical interviewer with 10+ years of experience.

Generate exactly {num_questions} interview questions for the following:

**Job Role:** {job_role}
**Candidate Skills:** {skills}
**Difficulty Level:** {difficulty}

**Rules:**
1. Questions should be a mix of:
   - Technical (concept-based)
   - Practical (problem-solving)
   - Behavioral (situational)
2. Each question should be clear and specific
3. Avoid yes/no questions
4. Make questions relevant to the role and skills
5. If difficulty is "easy", focus on basics
6. If difficulty is "medium", include intermediate concepts
7. If difficulty is "hard", include advanced + system design

**Output Format (STRICT):**
Return ONLY a valid JSON array of strings. No extra text, no markdown.
Example:
["Question 1 text here?", "Question 2 text here?", "Question 3 text here?"]
"""


# ============================================
# 2. ANSWER EVALUATION PROMPT
# ============================================

ANSWER_EVALUATION_PROMPT = """
You are an expert technical interviewer evaluating a candidate's answer.

**Question:** {question}

**Candidate's Answer:** {answer}

**Evaluation Criteria:**
1. **Technical Accuracy** (0-10): Is the answer factually correct?
2. **Clarity** (0-10): Is the answer well-structured and easy to understand?
3. **Completeness** (0-10): Does it cover all important points?
4. **Overall Score** (0-10): Weighted average of the above

**Output Format (STRICT):**
Return ONLY a valid JSON object with this exact structure. No markdown, no extra text:
{{
    "score": <integer 0-10>,
    "technical_accuracy": <integer 0-10>,
    "clarity": <integer 0-10>,
    "completeness": <integer 0-10>,
    "strengths": "<1-2 sentences about what was good>",
    "weaknesses": "<1-2 sentences about what was missing or wrong>",
    "improvement_tips": "<1-2 actionable suggestions to improve>"
}}
"""


# ============================================
# 3. FOLLOW-UP QUESTION PROMPT
# ============================================

FOLLOWUP_QUESTION_PROMPT = """
You are an expert interviewer. Based on the candidate's answer, generate ONE relevant follow-up question.

**Original Question:** {question}

**Candidate's Answer:** {answer}

**Rules:**
1. The follow-up should dig deeper into the same topic
2. It should test the candidate's depth of understanding
3. Avoid repeating the original question
4. Make it conversational and natural

**Output Format (STRICT):**
Return ONLY the follow-up question as plain text. No JSON, no quotes, no extra text.
"""


# ============================================
# 4. RESUME PARSING PROMPT
# ============================================

RESUME_PARSING_PROMPT = """
You are an expert resume parser. Extract structured information from the resume text below.

**Resume Text:**
{resume_text}

**Extract the following:**
1. List of technical skills
2. Years of experience (approximate)
3. A brief professional summary (1-2 sentences)

**Output Format (STRICT):**
Return ONLY a valid JSON object with this exact structure. No markdown, no extra text:
{{
    "skills": ["skill1", "skill2", "skill3", ...],
    "experience_years": <integer>,
    "summary": "<brief professional summary>"
}}
"""


# ============================================
# 5. OVERALL INTERVIEW FEEDBACK PROMPT
# ============================================

OVERALL_FEEDBACK_PROMPT = """
You are an expert interviewer. Based on the candidate's performance across multiple questions, provide overall feedback.

**Job Role:** {job_role}
**Total Questions:** {total_questions}
**Average Score:** {avg_score}/10

**All Questions & Answers:**
{qa_summary}

**Output Format (STRICT):**
Return ONLY a valid JSON object with this exact structure. No markdown, no extra text:
{{
    "overall_rating": "<Excellent/Good/Average/Needs Improvement>",
    "summary": "<2-3 sentences summarizing overall performance>",
    "key_strengths": ["strength1", "strength2", "strength3"],
    "areas_to_improve": ["area1", "area2", "area3"],
    "recommendation": "<Should this candidate move forward? Why?>"
}}
"""