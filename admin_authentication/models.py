from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models

class ShopAdminAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Admins must have an email address')
        if not username:
            raise ValueError('Admins must have a username')

        email = self.normalize_email(email)
        admin = self.model(email=email, username=username)
        admin.set_password(password)
        admin.save(using=self._db)
        return admin

    def create_superuser(self, email, username, password=None):
        admin = self.create_user(email, username, password)
        admin.is_superuser = True
        admin.is_staff = True
        admin.save(using=self._db)
        return admin

class ShopAdminAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Admin user has access to admin site
    is_superuser = models.BooleanField(default=False)

    objects = ShopAdminAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    # By default, related_name is 'user_set'
    groups = models.ManyToManyField(Group, blank=True)
    user_permissions = models.ManyToManyField(Permission, blank=True)
