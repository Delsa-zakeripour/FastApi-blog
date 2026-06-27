import uuid
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageOps

PROFILE_PIC_DIR = Path("media/profile_pics")


def process_profile_image(content: bytes) -> tuple[bytes, str]:
    with Image.open(BytesIO(content)) as original:
        img = ImageOps.exif_transpose(original)

        img = ImageOps.fit(img, (300, 300), method=Image.Resampling.LANCZOS)

        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")

        filename = f"{uuid.uuid4().hex}.jpg"

        output = BytesIO()
        img.save(output, "JPEG", quality=85, optimize=True)
        output.seek(0)

    return output.read(), filename


def save_profile_image(content: bytes, filename: str) -> None:
    PROFILE_PIC_DIR.mkdir(parents=True, exist_ok=True)
    (PROFILE_PIC_DIR / filename).write_bytes(content)


async def delete_profile_image(filename: str | None) -> None:
    if filename is None:
        return
    file_path = PROFILE_PIC_DIR / filename
    if file_path.exists():
        file_path.unlink()
