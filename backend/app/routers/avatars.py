import os
import uuid

from fastapi import APIRouter, UploadFile, HTTPException
from PIL import Image

router = APIRouter(prefix="/avatars", tags=["avatars"])

AVATAR_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "avatars")
AVATAR_SIZE = (128, 128)
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}


@router.post("/upload")
async def upload_avatar(file: UploadFile):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, and WebP images are supported")

    os.makedirs(AVATAR_DIR, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.png"
    filepath = os.path.join(AVATAR_DIR, filename)

    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image too large (max 5MB)")

    img = Image.open(file.file)
    img.thumbnail(AVATAR_SIZE, Image.Resampling.LANCZOS)

    # Center-crop to square
    w, h = img.size
    if w != h:
        side = min(w, h)
        left = (w - side) // 2
        top = (h - side) // 2
        img = img.crop((left, top, left + side, top + side))

    img.save(filepath, "PNG", optimize=True)

    return {"path": f"/avatars/{filename}"}
