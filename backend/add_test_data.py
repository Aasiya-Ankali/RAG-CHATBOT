"""
Add test data to ChromaDB
"""

import chromadb
from app.services.siemens_client import siemens_client
from app.config import CHROMA_DB_PATH, COLLECTION_NAME

print("="*50)
print("Adding Test Data to ChromaDB")
print("="*50)

# Connect to ChromaDB
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

# Get or create collection
collection = client.get_or_create_collection(name=COLLECTION_NAME)

print(f"Collection: {COLLECTION_NAME}")
print(f"Current count: {collection.count()}")

# Test data about power plants
test_documents = [
    "Solar power plants convert sunlight into electricity using photovoltaic panels. They are renewable and produce no emissions during operation.",
    "Wind power plants use large turbines to convert wind energy into electricity. Modern wind farms can generate significant amounts of clean energy.",
    "Nuclear power plants generate electricity through controlled nuclear fission reactions. They produce large amounts of power with minimal carbon emissions.",
    "Hydroelectric power plants harness the energy of flowing water to generate electricity. Dams are commonly used to control water flow and maximize power generation.",
    "Coal power plants burn coal to produce steam that drives turbines. They are being phased out in many countries due to environmental concerns.",
    "Natural gas power plants are more efficient and cleaner than coal plants. They can quickly ramp up or down to meet electricity demand.",
    "Geothermal power plants use heat from the Earth's core to generate electricity. They provide reliable baseload power in geologically active regions.",
    "Biomass power plants burn organic materials like wood chips or agricultural waste to generate electricity. They are considered carbon-neutral when sustainably managed.",
]

print(f"\nAdding {len(test_documents)} test documents...")

# Generate embeddings and add to ChromaDB
ids = []
embeddings = []
documents = []
metadatas = []

for i, doc in enumerate(test_documents):
    print(f"  Processing {i+1}/{len(test_documents)}...", end="\r")
    
    # Generate embedding
    embedding = siemens_client.embeddings(doc)
    
    ids.append(f"test_doc_{i}")
    embeddings.append(embedding)
    documents.append(doc)
    metadatas.append({
        "source": "test_data",
        "doc_id": i,
        "type": "power_plant_info"
    })

# Add all at once
collection.add(
    ids=ids,
    embeddings=embeddings,
    documents=documents,
    metadatas=metadatas
)

print(f"\n✅ Successfully added {len(test_documents)} documents!")
print(f"Total documents in collection: {collection.count()}")
print("="*50)