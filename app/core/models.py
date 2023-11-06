from django.db import models

# Create your models here.
from django.contrib.auth.models import(
    AbstractBaseUser, BaseUserManager, PermissionsMixin,
)

class UserManager(BaseUserManager):
    """Manager for Users."""

    def create_user(self, email, password=None, **extra_field):
        """Create, save and return a new user."""
        user = self.model(email=self.normalize_email(email), **extra_field) #self.model to call the other model (User class) & pass the email and other things
        user.set_password(password) #incrypt the given password
        user.save(using=self._db) # save it in the database

        return user




class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'