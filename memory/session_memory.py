import hashlib

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance


# Init Qdrant client
qdrant = QdrantClient(path="./qdrant_data")
collection_name = "session_memory"

if not qdrant.collection_exists(collection_name=collection_name):
    qdrant.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=64, distance=Distance.COSINE)

    )

#embedding the text
def embed_text(text: str) -> list:
    return [float(int(hashlib.sha256((text + str(i)).encode()).hexdigest(), 16) % 100) / 100 for i in range(64)]

