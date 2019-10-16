from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
# Create your models here.

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    #specify functions that can be used to manipulate objects
    def create_user(self,email,name,password=None):
        #password will set to None if not specified
        """create a new user profile"""
        if not email:
            raise ValueError('User NEEd email address')

        email = self.normalize_email(email)
        user = self.model(email=email,name=name,)

        user.set_password(password)
        user.save(using=self._db) #standard procedure to save objects in djangoproject

        return user

    def create_superuser(self,email,name,password):
        """create and save a superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True #PermissionsMixin creates the is_ automatically
        user.is_staff = True
        user.save(using=self._db)

        return user
#class- User Profile.
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """database model for users in the system"""
    email = models.EmailField(max_length=50,unique=True)
    name = models.CharField(max_length=50,unique=True)
    #determine if user's profile is activated or not, by default its set to True
    is_active = models.BooleanField(default = True)
    #deterine if user is a staff user which means admin access or not, by default they are not members
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name'] #add all the other attributes AuthenticationMiddleware

    #functions for django to interact with custom user model
    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    #string representation of our model, we want this to return when user profile object is returned as string
    def __str__(self):
        """Return string representation of our user"""
        return self.email
