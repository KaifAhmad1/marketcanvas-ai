from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from fastapi.responses import FileResponse
import os
from typing import List, Optional

from ..models.responses import UploadResponse, AssetListResponse, ErrorResponse, GenericResponse
from ...utils.file_handler import FileHandler

router = APIRouter()
file_handler = FileHandler(base_upload_dir="uploads", workflow_subdir="assets_library")

@router.post("/upload", response_model=UploadResponse, responses={400: {"model": ErrorResponse}})
async def upload_asset(file: UploadFile = File(...), category: Optional[str] = Form("general")):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")

    safe_category = "".join(c if c.isalnum() or c in ['_', '-'] else '_' for c in category)
    if not safe_category:
        safe_category = "general"

    try:
        saved_filepath = await file_handler.save_uploaded_file(file, sub_dir=safe_category)

        asset_url = file_handler.get_url_for_file(saved_filepath)

        return UploadResponse(
            filename=file.filename,
            file_url=asset_url,
            content_type=file.content_type,
            size=file.size,
            message="Asset uploaded successfully."
        )
    except Exception as e:
        print(f"Asset upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Asset upload failed: {str(e)}")

@router.get("/", response_model=AssetListResponse)
async def list_assets(category: Optional[str] = None, file_type: Optional[str] = None):
    assets = []
    asset_storage_root = file_handler.base_upload_dir

    search_dir = asset_storage_root
    if category:
        safe_category = "".join(c if c.isalnum() or c in ['_', '-'] else '_' for c in category)
        search_dir = os.path.join(asset_storage_root, safe_category)

    if not os.path.isdir(search_dir):
        return AssetListResponse(assets=[])

    for dirname, _, filenames in os.walk(search_dir):
        for filename in filenames:
            if filename.startswith('.'):
                continue

            if file_type:
                ext = os.path.splitext(filename)[1].lower()
                if file_type == "image" and ext not in [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"]:
                    continue
                elif file_type == "template" and ext not in [".json", ".yaml"]:
                    continue

            filepath = os.path.join(dirname, filename)
            file_url = file_handler.get_url_for_file(filepath)

            current_category = "general"
            if dirname != asset_storage_root:
                current_category = os.path.basename(dirname)

            assets.append({
                "filename": filename,
                "url": file_url,
                "path": filepath,
                "category": current_category,
                "type": os.path.splitext(filename)[1].lower().strip('.')
            })

    return AssetListResponse(assets=assets, message=f"Found {len(assets)} assets.")

@router.get("/download/{category}/{filename:path}", response_class=FileResponse)
async def download_asset(category: str, filename: str):
    safe_category = "".join(c if c.isalnum() or c in ['_', '-'] else '_' for c in category)
    safe_filename = os.path.basename(filename)
    filepath = os.path.join(file_handler.base_upload_dir, safe_category, safe_filename)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Asset not found.")
    return FileResponse(filepath, filename=safe_filename)

@router.delete("/{category}/{filename:path}", response_model=GenericResponse)
async def delete_asset(category: str, filename: str):
    safe_category = "".join(c if c.isalnum() or c in ['_', '-'] else '_' for c in category)
    safe_filename = os.path.basename(filename)
    filepath = os.path.join(file_handler.base_upload_dir, safe_category, safe_filename)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Asset not found.")
    try:
        os.remove(filepath)
        return GenericResponse(message=f"Asset '{filename}' in category '{category}' deleted successfully.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete asset: {str(e)}")
