import os
import json
from groq import Groq
from src.router import classify_question
from src.tool import TOOLS, get_business_info


def ask_bot_part3(question, vector_store, business_info, model="llama-3.1-8b-instant"):
    api_key = os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=api_key)

    route = classify_question(question)

    if route == "CLARIFY":
        return {
            "route": "CLARIFY",
            "answer": "Could you clarify the question?",
            "tool_used": None
        }

    if route == "TOOL":
        messages = [
            {
                "role": "system",
                "content": "You are an expense policy assistant. Use the get_business_info tool when users ask about contact information, specific limits/rates, deadlines, or timelines. For questions about policies, procedures, or 'how to' questions, search the policy documents instead."
            },
            {
                "role": "user",
                "content": question
            }
        ]

        response = client.chat.completions.create(
            messages=messages,
            model=model,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        if tool_calls:
            messages.append(response_message)

            for tool_call in tool_calls:
                function_args = json.loads(tool_call.function.arguments)
                function_response = get_business_info(
                    business_info,
                    field=function_args.get("field")
                )
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "get_business_info",
                    "content": json.dumps(function_response)
                })

            final_response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0
            )

            return {
                "route": "TOOL",
                "answer": final_response.choices[0].message.content,
                "tool_used": {
                    "name": "get_business_info",
                    "arguments": function_args,
                    "result": function_response
                }
            }

    docs = vector_store.similarity_search(question, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    rag_messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Answer ONLY using the provided context from FAQ and Policy documents. If the context doesn't contain the answer, say 'I don't know based on the available documents.'"
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}"
        }
    ]

    rag_response = client.chat.completions.create(
        model=model,
        messages=rag_messages,
        temperature=0
    )

    return {
        "route": "RAG",
        "answer": rag_response.choices[0].message.content,
        "tool_used": None
    }