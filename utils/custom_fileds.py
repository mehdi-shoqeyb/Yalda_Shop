from django.db import models
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image

class WebPImageField(models.ImageField):
    def __init__(self, *args, quality=90, **kwargs):
        self.quality = quality
        super().__init__(*args, **kwargs)

    def save_form_data(self, instance, data):
        # Call the super method to handle the file upload
        super().save_form_data(instance, data)
        
        # If data is not None and not already in WebP format, convert it
        if data and not data.name.lower().endswith('.webp'):
            try:
                img = Image.open(data)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                img_io = BytesIO()
                img.save(img_io, format='WEBP', quality=self.quality)

                webp_filename = f'{data.name.rsplit(".", 1)[0]}.webp'
                webp_file = ContentFile(img_io.getvalue(), webp_filename)

                # Save the new file to the model instance
                field = getattr(instance, self.attname)
                field.save(webp_filename, webp_file, save=False)

                # Update the field value on the model instance
                setattr(instance, self.attname, webp_file)

            except Exception as e:
                print(f"Error processing image: {e}")