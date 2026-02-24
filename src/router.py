import os
from groq import Groq

def classify_question(question):
    api_key = os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=api_key)
    classify_messages = [
        {
            "role": "system",
            "content": """You are a question classifier for an expense policy assistant.
Classify the user's question into exactly ONE of these routes:

TOOL     → user asks about specific facts: contacts, phone, email, spending limits, mileage rate, deadlines, reimbursement timelines
RETRIEVE → user asks about policies, procedures, how-to, rules, what is allowed
CLARIFY  → question is too vague, too short, unrelated to expense policy, or needs more context

Examples:
Q: "what is the mileage rate?"         → TOOL
Q: "hr contact"                         → TOOL
Q: "how do I submit an expense?"        → RETRIEVE
Q: "what is the hotel limit?"           → TOOL
Q: "can I expense alcohol?"             → RETRIEVE
Q: "help"                               → CLARIFY
Q: "what about that thing?"             → CLARIFY
Q: "how is the weather?"                → CLARIFY

Reply with ONLY one word: TOOL, RETRIEVE, or CLARIFY"""
        },
        {
            "role": "user",
            "content": question
        }
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=classify_messages
    )

    route = response.choices[0].message.content.strip().upper()

    # Safeguard: extract keyword in case LLM returns extra text
    for keyword in ["TOOL", "RETRIEVE", "CLARIFY"]:
        if keyword in route:
            return keyword

    return "CLARIFY"  