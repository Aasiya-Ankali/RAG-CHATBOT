# import chromadb

# # Connect to your ACTUAL data folder
# client = chromadb.PersistentClient(path="./chroma_data")

# # List collections
# collections = client.list_collections()

# print("Collections in chroma_data:")
# for col in collections:
#     print(f"  - {col.name}: {col.count()} documents")
# """
# Test the complete RAG pipeline
# """

# from app.services.siemens_client import siemens_client
# from app.services.chroma_service import chroma_service

# print("="*70)
# print("TESTING RAG PIPELINE")
# print("="*70)

# # Test query
# query = "list powerplants in india"

# print(f"\n❓ Query: {query}")
# print("-"*70)

# # Step 1: Generate query embedding
# print("\n1️⃣ Generating query embedding...")
# query_embedding = siemens_client.embeddings(query)
# print(f"   ✅ Embedding dimension: {len(query_embedding)}")

# # Step 2: Search ChromaDB
# print("\n2️⃣ Searching ChromaDB...")
# try:
#     results = chroma_service.collection.query(
#         query_embeddings=[query_embedding],
#         n_results=5
#     )
    
#     print(f"   ✅ Found {len(results['documents'][0])} results")
    
#     # Show results
#     print("\n📄 Retrieved documents:")
#     for i, doc in enumerate(results['documents'][0]):
#         distance = results['distances'][0][i] if 'distances' in results else 'N/A'
#         print(f"\n   Result {i+1} (distance: {distance}):")
#         print(f"   {doc[:300]}...")
        
#     # Step 3: Build context
#     print("\n3️⃣ Building context...")
#     context = "\n\n".join(results['documents'][0])
#     print(f"   ✅ Context length: {len(context)} characters")
    
#     # Step 4: Generate answer
#     print("\n4️⃣ Generating answer with LLM...")
    
#     prompt = f"""You are a helpful assistant. Answer the question based on the context provided.

# Context:
# {context}

# Question: {query}

# Answer:"""
    
#     answer = siemens_client.rag_chat(prompt)
    
#     print(f"\n💬 Answer:")
#     print(f"   {answer}")
    
# except Exception as e:
#     print(f"   ❌ Error: {e}")
#     import traceback
#     traceback.print_exc()

# print("\n" + "="*70)
# """
# Verify ChromaDB and embedding setup
# """

# import chromadb
# from app.services.siemens_client import siemens_client
# from app.config import CHROMA_DB_PATH, COLLECTION_NAME, EMBED_MODEL

# print("="*70)
# print("VERIFYING RAG SETUP")
# print("="*70)

# # 1. Check config
# print("\n📋 Configuration:")
# print(f"   ChromaDB Path: {CHROMA_DB_PATH}")
# print(f"   Collection Name: {COLLECTION_NAME}")
# print(f"   Embedding Model: {EMBED_MODEL}")

# # 2. Check embedding dimension
# print("\n🔍 Testing embedding...")
# test_embedding = siemens_client.embeddings("test query")
# print(f"   ✅ Embedding dimension: {len(test_embedding)}")

# # 3. Check ChromaDB
# print("\n💾 Checking ChromaDB...")
# client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# try:
#     collection = client.get_collection(name=COLLECTION_NAME)
#     count = collection.count()
#     print(f"   ✅ Collection '{COLLECTION_NAME}' found")
#     print(f"   ✅ Document count: {count}")
    
#     if count > 0:
#         # Check stored embedding dimension
#         sample = collection.peek(limit=1)
#         stored_dim = len(sample['embeddings'][0])
#         print(f"   ✅ Stored embedding dimension: {stored_dim}")
        
#         # Show sample document
#         print(f"\n📄 Sample document:")
#         print(f"   {sample['documents'][0][:200]}...")
        
#         # Test search
#         print(f"\n🔎 Testing search...")
#         query_embedding = siemens_client.embeddings("power plant")
#         results = collection.query(
#             query_embeddings=[query_embedding],
#             n_results=2
#         )
        
#         print(f"   ✅ Search successful!")
#         print(f"   Found {len(results['documents'][0])} results")
#         print(f"   Top result: {results['documents'][0][0][:150]}...")
        
#     else:
#         print(f"   ⚠️ Collection is EMPTY!")
#         print(f"   You need to add data to the collection.")
        
# except Exception as e:
#     print(f"   ❌ Error: {e}")

# print("\n" + "="*70)
# """
# Test the complete RAG pipeline
# """

# from app.services.siemens_client import siemens_client
# from app.services.chroma_service import chroma_service

# print("="*70)
# print("TESTING RAG PIPELINE")
# print("="*70)

# # Test query
# query = "list powerplants in india"

# print(f"\n❓ Query: {query}")
# print("-"*70)

# # Step 1: Generate query embedding
# print("\n1️⃣ Generating query embedding...")
# query_embedding = siemens_client.embeddings(query)
# print(f"   ✅ Embedding dimension: {len(query_embedding)}")

# # Step 2: Search ChromaDB
# print("\n2️⃣ Searching ChromaDB...")
# try:
#     results = chroma_service.collection.query(
#         query_embeddings=[query_embedding],
#         n_results=5
#     )
    
#     print(f"   ✅ Found {len(results['documents'][0])} results")
    
#     # Show results
#     print("\n📄 Retrieved documents:")
#     for i, doc in enumerate(results['documents'][0]):
#         distance = results['distances'][0][i] if 'distances' in results else 'N/A'
#         print(f"\n   Result {i+1} (distance: {distance}):")
#         print(f"   {doc[:300]}...")
        
#     # Step 3: Build context
#     print("\n3️⃣ Building context...")
#     context = "\n\n".join(results['documents'][0])
#     print(f"   ✅ Context length: {len(context)} characters")
    
#     # Step 4: Generate answer
#     print("\n4️⃣ Generating answer with LLM...")
    
#     prompt = f"""You are a helpful assistant. Answer the question based on the context provided.

# Context:
# {context}

# Question: {query}

# Answer:"""
    
#     answer = siemens_client.rag_chat(prompt)
    
#     print(f"\n💬 Answer:")
#     print(f"   {answer}")
    
# except Exception as e:
#     print(f"   ❌ Error: {e}")
#     import traceback
#     traceback.print_exc()

# print("\n" + "="*70)
"""
Test simple chat (no persistence)
"""

import requests

BASE_URL = "http://localhost:8000/api/chat"

def test_conversation():
    print("="*70)
    print("TESTING SIMPLE CHAT")
    print("="*70)
    
    # Message 1 - No session_id
    print("\n1️⃣ First message (no session)...")
    r1 = requests.post(f"{BASE_URL}/message", json={
        "message": "What are the largest power plants in India?"
    })
    data1 = r1.json()
    session_id = data1['session_id']
    
    print(f"✅ Session created: {session_id}")
    print(f"Answer: {data1['answer'][:150]}...")
    
    # Message 2 - With session_id (tests history)
    print("\n2️⃣ Follow-up (tests conversation memory)...")
    r2 = requests.post(f"{BASE_URL}/message", json={
        "session_id": session_id,
        "message": "What about their capacity?"
    })
    data2 = r2.json()
    
    print(f"Answer: {data2['answer'][:150]}...")
    
    # Message 3 - Another follow-up
    print("\n3️⃣ Another follow-up...")
    r3 = requests.post(f"{BASE_URL}/message", json={
        "session_id": session_id,
        "message": "Which one is the biggest?"
    })
    data3 = r3.json()
    
    print(f"Answer: {data3['answer'][:150]}...")
    
    print("\n" + "="*70)
    print("✅ TEST COMPLETE!")
    print("="*70)

if __name__ == "__main__":
    test_conversation()