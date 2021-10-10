from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **kwargs):
        if not username:
            raise ValueError("The given email must be set")
        # email = self.normalize_email(email=email)
        user = self.model(username=username, **kwargs)
        user.create_activation_code()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(username, password, **kwargs)

    def create_superuser(self, username, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have status is_staff=True')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have status is_superuser=True')
        return self._create_user(username, password, **kwargs)





class MyUser(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    username = models.CharField(max_length=155, unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=6, blank=True)
    # is_staff = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = MyUserManager()



    def __str__(self):
        return f'{self.username} {self.phone_number}'

    def create_activation_code(self):
        code = get_random_string(6, allowed_chars='123456789')
        self.activation_code = code
        return code

