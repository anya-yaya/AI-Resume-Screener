from langchain_core.prompts import PromptTemplate

extract_prompt = PromptTemplate.from_template("""
Extract ONLY exact data from resume.

Return JSON ONLY:
{{
  "skills": [],
  "tools": [],
  "experience": ""
}}

Rules:
- Extract exact words only
- Experience:
  - "3 years" → "3"
  - "1.5 years" → "1.5"
  - "Fresher" → "0"
- No guessing

Resume:
{resume}
""")