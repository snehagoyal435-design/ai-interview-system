# ============================================
# AI Interview System - AI Prompts
# ============================================


QUESTION_GENERATION_PROMPT = """
You are an expert technical interviewer with 10+ years of experience.

Generate exactly {num_questions} interview questions for the following:

**Job Role:** {job_role}
**Candidate Skills:** {skills}
**Difficulty Level:** {difficulty}
**Session ID:** {session_id}
**Timestamp:** {timestamp}

**CRITICAL INSTRUCTIONS:**
1. Every generation MUST produce COMPLETELY DIFFERENT questions.
2. Do NOT repeat questions you might have generated before.
3. Use the Session ID and Timestamp to ensure uniqueness.
4. Randomly pick from these topic areas:
   - Core concepts and definitions
   - Real-world scenarios
   - Debugging and troubleshooting
   - Code optimization
   - System design
   - Best practices
   - Framework-specific questions
   - Database queries and optimization
   - API design and REST
   - Security best practices
   - Testing and quality assurance
   - Version control scenarios

**Rules:**
1. Mix: Technical (60%), Practical (25%), Behavioral (15%)
2. Clear and specific
3. No yes/no questions
4. Relevant to role and skills
5. Adjust complexity based on difficulty level

**Output Format (STRICT):**
Return ONLY a valid JSON array of strings. No extra text, no markdown.
Example:
["Question 1 text here?", "Question 2 text here?"]
"""


ANSWER_EVALUATION_PROMPT = """
You are a senior technical interviewer evaluating a candidate's answer.

**Question:** {question}
**Candidate's Answer:** {answer}

**Evaluation Guidelines:**
- EMPTY / IRRELEVANT / "I don't know" → score = 0
- PARTIAL (some correct points) → score = 3-6
- GOOD (mostly correct) → score = 7-8
- EXCELLENT (complete, accurate) → score = 9-10

**Scoring Criteria:**
1. Technical Accuracy (0-10)
2. Clarity (0-10)
3. Completeness (0-10)
4. Overall Score (0-10)

**Be STRICT:**
- Wrong → 0-2
- Vague → 3-4
- Partial → 5-6
- Good → 7-8
- Excellent → 9-10

**Output Format (STRICT):**
Return ONLY valid JSON:
{{
    "score": <0-10>,
    "technical_accuracy": <0-10>,
    "clarity": <0-10>,
    "completeness": <0-10>,
    "strengths": "<text>",
    "weaknesses": "<text>",
    "improvement_tips": "<text>"
}}
"""


FOLLOWUP_QUESTION_PROMPT = """
Generate ONE relevant follow-up question.

**Original Question:** {question}
**Candidate's Answer:** {answer}

**Rules:**
1. Dig deeper into the same topic
2. Test depth of understanding
3. Avoid repeating
4. Natural and conversational

**Output Format:**
Return ONLY the follow-up question as plain text.
"""


RESUME_PARSING_PROMPT = """
Extract structured information from this resume.

**Resume:**
{resume_text}

**Output Format (STRICT):**
Return ONLY valid JSON:
{{
    "skills": ["skill1", "skill2"],
    "experience_years": <integer>,
    "summary": "<brief summary>"
}}
"""


OVERALL_FEEDBACK_PROMPT = """
Provide overall feedback based on performance.

**Job Role:** {job_role}
**Total Questions:** {total_questions}
**Average Score:** {avg_score}/10

**Q&A Summary:**
{qa_summary}

**Output Format (STRICT):**
Return ONLY valid JSON:
{{
    "overall_rating": "<Excellent/Good/Average/Needs Improvement>",
    "summary": "<2-3 sentences>",
    "key_strengths": ["strength1", "strength2"],
    "areas_to_improve": ["area1", "area2"],
    "recommendation": "<text>"
}}
"""