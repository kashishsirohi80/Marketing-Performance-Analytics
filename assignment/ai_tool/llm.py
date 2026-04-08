from google import genai
from config import GEMINI_API_KEY
from prompt import SQL_PROMPT

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_sql_and_explanation(question, memory=[]):
    context = "\n".join(
        [f"Q: {m['question']}\nA: {m['answer']}" for m in memory]
    )

    prompt = f"""
Previous conversation:
{context}

{SQL_PROMPT.format(question=question)}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    return response.text.strip()