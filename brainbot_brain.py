from formulas import solve_formula
from openai_api import ask_llm
import json

# Load general responses
with open("C:/Users/bharg/OneDrive/Documents/New folder/test/project/general_response.json") as f:
    general_responses = json.load(f)

def brainbot_brain(question):
    print(f"User asked: {question}")  # 🟡 Bonus Debug Print

    question_lower = question.lower()

    # 1. Check general predefined responses
    for key in general_responses:
        if key in question_lower:
            print("Matched general response.")
            return general_responses[key]

    # 2. Check formula solving
    formula_response = solve_formula(question_lower)
    if formula_response:
        print("Matched formula logic.")
        return formula_response

    # 3. Try LLM
    try:
        llm_response = ask_llm(question)
        if llm_response:
            print("Matched LLM logic.")
            return llm_response
    except Exception as e:
        print("LLM Error:", e)

    # 4. Static fallback
    print("No match found. Sending fallback response.")
    return f"Sorry, I couldn't find an answer to: '{question}'. But I'm learning more every day!"
