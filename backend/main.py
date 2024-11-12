import sys
#sys.path.append("C:\\Users\\Saba Gul\Desktop\\Celeb-Twin")
from fastapi import FastAPI, File, UploadFile, HTTPException
import numpy as np
import os
from pydantic import BaseModel
from qdrant_client import QdrantClient
from embeddings import generate_embedding  # Ensure this function works correctly
from auth import verify_user
from qdrant_client.models import Distance, VectorParams, PointStruct

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, Vector Twin!"}
# Qdrant connection
client = QdrantClient(
    url=os.getenv("QDRANT_API_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

collection_name = "celebrity_embeddings"
vector_size = 512

# Ensure the collection exists and is configured with the correct vector parameters
def ensure_collection():
    """Ensure the collection exists and is configured properly"""
    try:
        if not client.collection_exists(collection_name):
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
            print(f"Created collection: {collection_name}")
        else:
            print(f"Collection '{collection_name}' already exists.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ensuring collection exists: {str(e)}")

ensure_collection()  # Call this to ensure collection is set up properly

class MatchResponse(BaseModel):
    name: str
    score: float


@app.post("/upload-image/", response_model=list[MatchResponse])
async def upload_image(file: UploadFile = File(...)):
    try:
        # Read image and generate embedding
        image_bytes = await file.read()
        embedding = generate_embedding(image_bytes)  # Ensure this function is working properly

        if embedding is None:
            raise HTTPException(status_code=400, detail="Error generating embedding")

        # Convert embedding to float32 and handle NaN values
        embedding = np.nan_to_num(embedding.astype(np.float32))

        # Search Qdrant for similar embeddings
        results = client.search(
            collection_name=collection_name,
            query_vector=embedding.tolist(),
            limit=10
        )

        if not results:
            return []

        matches = [
            MatchResponse(
                name=result.payload['celebrity'],
                score=float(result.score)
            )
            for result in results
        ]
        return matches

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
