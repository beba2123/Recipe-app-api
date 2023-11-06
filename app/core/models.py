from django.db import models

# Create your models here.
from django.contrib.auth.models import(
    AbstractBaseUser, BaseUserManager, PermissionsMixin,
)

class UserManager(BaseUserManager):
    """Manager for Users."""

    def create_user(self, email, password=None, **extra_field):
        """Create, save and return a new user."""
        if not email: #incase if the user doesnot have an email adress
            raise ValueError('user must have an email adress!!')  #send a message for not having an email.
        user = self.model(email=self.normalize_email(email), **extra_field) #self.model to call the other model (User class) & pass the email and other things
        user.set_password(password) #incrypt the given password
        user.save(using=self._db) # save it in the database

        return user

    def create_superuser(self, email, password):
        """create and save a superuser with given details"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user




class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'