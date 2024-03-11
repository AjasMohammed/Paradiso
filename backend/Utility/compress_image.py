from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def compress_image(image):
    if image.size > 1000000:
        
        # Open the image using Pillow
        img = Image.open(image)
        # Set the compression level (0-100, 100 being the best quality)
        quality = 40
        # Create a BytesIO buffer to store the compressed image
        buffer = BytesIO()
        # Save the image to the buffer with compression
        try:
            img.save(buffer, format='JPEG', quality=quality, optimize=True)
            # Get the size of the compressed image
            compressed_size = buffer.tell()
            # Rewind the buffer to the beginning
            buffer.seek(0)
            # Create an InMemoryUploadedFile from the buffer
            compressed_image = InMemoryUploadedFile(
                buffer,
                'ImageField',
                image.name,
                'image/jpeg',
                compressed_size,
                None
            )
            return compressed_image
        except Exception as e:
            print("Error:", e)
            return image
    return image
