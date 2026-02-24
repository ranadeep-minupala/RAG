from dotenv import load_dotenv
load_dotenv()

from src.loader import load
from src.chunker import chunk_texts
from src.embedder import build_vector_store
from src.bot import ask_bot_part3

policies_text, faq_text, business_info = load(
    "data/policies.txt",
    "data/faq.txt",
    "data/get_business_info.json"
)

chunks = chunk_texts(faq_text, policies_text)
vector_store = build_vector_store(chunks)

while True:
    question = input("You: ").strip()
    if not question:
        continue
    if question.lower() == "quit":
        break
    result = ask_bot_part3(question, vector_store, business_info)
    print(f"Bot: {result['answer']}\n")
