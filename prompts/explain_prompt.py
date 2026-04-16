from langchain_core.prompts import PromptTemplate

explain_prompt = PromptTemplate.from_template("""
Explain in 3 lines:

- matched skills count
- missing skills
- experience level

Match Data:
{match_data}

Score:
{score}
""")