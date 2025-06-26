from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import numpy as np

client = QdrantClient(":memory:")  

COLLECTION_NAME = "frames"

def setup_collection():
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=512, distance=Distance.COSINE)
    )

def add_vector(id: int, vector: np.ndarray, metadata: dict):
    point = PointStruct(id=id, vector=vector.tolist(), payload=metadata)
    client.upsert(collection_name=COLLECTION_NAME, points=[point])

def search_similar(vector: np.ndarray, top_k: int = 5):
    return client.search(collection_name=COLLECTION_NAME, query_vector=vector.tolist(), limit=top_k)
