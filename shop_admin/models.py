from django.db import models
from django.contrib.auth.hashers import make_password, check_password as django_check_password
from django.utils import timezone

class ShopAdminAccount(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Will store the hashed password
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # If the password is not already hashed, hash it before saving
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        """Check if the provided raw password matches the hashed password."""
        return django_check_password(raw_password, self.password)

    def __str__(self):
        return self.username
