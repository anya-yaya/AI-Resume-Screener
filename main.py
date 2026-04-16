import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

from prompts.extract_prompt import extract_prompt
from prompts.explain_prompt import explain_prompt

from chains.extraction_chain import extraction_chain
from chains.explanation_chain import explanation_chain


# -------------------------------
# Safe JSON Loader (VERY IMPORTANT)
# -------------------------------
def safe_json_loads(text):
    try:
        return json.loads(text)
    except:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass
    return {}


# -------------------------------
# Python Matching + Scoring Logic
# -------------------------------
def compute_match_and_score(extracted_json):

    required_skills = ["Python", "Machine Learning", "SQL", "Data Analysis", "Statistics"]

    skills = extracted_json.get("skills", [])
    experience = extracted_json.get("experience", "0")

    try:
        experience = float(experience)
    except:
        experience = 0

    # Matching
    matching_skills = [s for s in required_skills if s in skills]
    missing_skills = [s for s in required_skills if s not in skills]

    # Experience Match
    if experience >= 2:
        exp_match = "High"
        exp_score = 20
    elif experience >= 1:
        exp_match = "Medium"
        exp_score = 10
    else:
        exp_match = "Low"
        exp_score = 5

    # Scoring
    skill_score = (len(matching_skills) / 5) * 50
    penalty = (len(missing_skills) / 5) * 30

    final_score = skill_score + exp_score - penalty

    return {
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "experience_match": exp_match,
        "score": round(final_score)
    }


# -------------------------------
# Main Pipeline
# -------------------------------
def run_pipeline(resume, jd):

    extract = extraction_chain(extract_prompt)
    explain = explanation_chain(explain_prompt)

    # Step 1: Extraction
    extracted = extract.invoke({"resume": resume})
    extracted_json = safe_json_loads(extracted)

    print("\n--- Extracted ---\n", extracted_json)

    # Step 2 + 3: Python Matching + Scoring
    result = compute_match_and_score(extracted_json)

    print("\n--- Matching ---\n", {
        "matching_skills": result["matching_skills"],
        "missing_skills": result["missing_skills"],
        "experience_match": result["experience_match"]
    })

    print("\n--- Score ---\n", {"score": result["score"]})

    # Step 4: Explanation (LLM)
    explanation = explain.invoke({
        "match_data": result,
        "score": result["score"]
    })

    print("\n--- Explanation ---\n", explanation)

    return {
        "extracted": extracted_json,
        "result": result,
        "explanation": explanation
    }


# -------------------------------
# Run for 3 candidates
# -------------------------------
if __name__ == "__main__":

    with open("data/strong_resume.txt") as f:
        strong = f.read()

    with open("data/average_resume.txt") as f:
        average = f.read()

    with open("data/weak_resume.txt") as f:
        weak = f.read()

    with open("data/job_description.txt") as f:
        jd = f.read()

    print("\n========= STRONG =========")
    run_pipeline(strong, jd)

    print("\n========= AVERAGE =========")
    run_pipeline(average, jd)

    print("\n========= WEAK =========")
    run_pipeline(weak, jd)