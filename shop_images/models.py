from django.db import models

class HeroImage(models.Model):
    image = models.ImageField(upload_to='hero_images/')  # This field stores the image
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is created

    def __str__(self):
        return f"Hero Image uploaded at {self.uploaded_at}"