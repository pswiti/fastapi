import uuid
from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from azure.storage.blob import BlobServiceClient
from app.auth import get_api_key
import os

app = FastAPI()

AZURE_STORAGE_CONNECTION_STRING = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
CONTAINER_NAME = "fastapi"
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

@app.post("/api/v1/test/upload")
async def upload_file(
    file: UploadFile = File(...),
    api_key: str = Depends(get_api_key)
):
    contents = await file.read()
    file_id = str(uuid.uuid4())
    blob_name = f"{file_id}_{file.filename}"

    # Upload to Azure Blob Storage
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(contents, overwrite=True)

    return JSONResponse(content={
        "file_id": file_id,
        "message": "Upload successful"
    })
