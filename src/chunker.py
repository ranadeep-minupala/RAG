from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_texts(faq_text, policies_text):
    faq_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\nQ", "\n\n", "\n", " "],
    )

    policy_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " "],
    )

    faq_chunks = faq_splitter.create_documents([faq_text])
    policies_chunks = policy_splitter.create_documents([policies_text])

    return faq_chunks + policies_chunks