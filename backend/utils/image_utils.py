import aiofiles
import os
import base64
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from client.models import ImageData


async def save_image(base64_encoded_image: str, plate_number: str, gate: str) -> str:
    """
    Saves the base64-encoded image to a file asynchronously.
    """
    # Decode the base64 image
    image_data = base64.b64decode(base64_encoded_image)

    # Create the directory based on the current date and gate
    timestamp = datetime.now()
    directory = f"images/{timestamp.year}/{timestamp.month}/{timestamp.day}/{gate}"
    os.makedirs(directory, exist_ok=True)

    # Define the image file path
    file_name = f"{timestamp.strftime('%Y%m%d_%H%M%S')}_{plate_number}.jpg"
    file_path = os.path.join(directory, file_name)

    # Save the image asynchronously
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(image_data)

    return file_path


async def save_image_metadata(db_session: AsyncSession, file_path: str, plate_number: str, gate: str):
    """
    Saves the metadata of the image to the database.
    """
    new_image_data = ImageData(
        plate_number=plate_number,
        gate=gate,
        file_path=file_path
    )
    try:
        db_session.add(new_image_data)
        await db_session.commit()
        print(f"[INFO] Saved image metadata for file: {file_path}")
    except SQLAlchemyError as e:
        await db_session.rollback()
        print(f"[ERROR] Could not save image metadata: {str(e)}")
