def search_semantic_libraries(query: str) -> str:
    data = [
        "FAISS – efficient vector similarity search",
        "Chroma – open-source embedding database",
        "Pinecone – managed vector database",
        "Weaviate – vector search engine with schema"
    ]
    return "\n".join(data)

def calculator_tool(expression: str) -> str:
    try:
        return str(eval(expression))
    except Exception:
        return "Invalid expression"
