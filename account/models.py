from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        # email = self.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)
    # def create_user(self, phone_number, password, **extra_fields):
    #     if not phone_number:
    #         raise ValueError('Phone number must be given')
    #     user = self.model(phone_number=phone_number, **extra_fields)
    #     user.set_password(password)
    #     user.create_activation_code()
    #     user.save(using=self._db)
    #     return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is False:
            raise ValueError('Super users must have is_superuser=True')
        return self._create_user(username, password, **extra_fields)
        # if not username:
        #     raise ValueError('Username must be given')
        # user = self.model(username=username, **extra_fields)
        # user.set_password(password)
        # print(password)
        # user.is_superuser = True
        # user.is_active = True
        # user.is_staff = True
        # user.save(using=self._db)
        # return user


class MyUser(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    username = models.CharField(max_length=155, unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=6, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    objects = MyUserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_staff

    def __str__(self):
        return f'{self.username} {self.phone_number}'

    def create_activation_code(self):
        code = get_random_string(6, allowed_chars='123456789')
        self.activation_code = code
        return code

