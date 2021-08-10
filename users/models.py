from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.db import models
from knox.models import AuthToken


class StaffManager(BaseUserManager):
    def create_user(self, email, user_role, first_name, last_name, contact_no, profile_picture, password=None):
        if email is None:
            raise TypeError('User should have a email')

        user = self.model(email=self.normalize_email(email), user_role=user_role, first_name=first_name,
                          last_name=last_name,
                          contact_no=contact_no, profile_picture=profile_picture)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, password=None):
        if password is None:
            raise TypeError('password can not be empty')
        if email is None:
            raise TypeError('User should have an email')
        user = self.create_user(email, '', first_name, '', '', '', password)
        user.is_superuser = True
        user.is_approved = True
        user.is_staff = True
        user.save()
        return user


# Create your models here.
class Staff(AbstractBaseUser, PermissionsMixin):
    USER_ROLES = {
        ('SALESPERSON', 'Salesperson'),
        ('OFFICER', 'Distribution Officer'),
        ('MANAGER', 'Operations Manager')
    }
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    user_role = models.CharField(choices=USER_ROLES, max_length=50)
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    contact_no = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='staff/')
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']
    objects = StaffManager()

    def __str__(self):
        return self.email

    def token(self):
        token = AuthToken.objects.create(self)[1]
        return str(token)
