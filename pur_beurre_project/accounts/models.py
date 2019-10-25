'''
This file contains the models for the custom User and its manager.
'''


from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.translation import ugettext_lazy as _

from substituter.models import Product


class UserManager(BaseUserManager):
    '''
    The user manager contains the required method to create a new user
    '''

    def create_user(self, email, first_name, password=None):
        '''
        Creates and saves a User with the given email and password.
        '''
        if not email:
            raise ValueError('Une adresse mail est nécessaire')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password):
        '''
        Creates and saves a User with the given email and password.
        '''
        if not email:
            raise ValueError('Une adresse mail est nécessaire')

        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    '''
    Users in this app use their mail address as their username.
    They also require a first_name, for aesthetic reasons.
    The model stores the products that were bookmarked by the user
    using many-to-many relations with the substituter_products table.
    '''

    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(_('Prénom'), max_length=30)
    is_active = models.BooleanField(default=True)
    bookmarks = models.ManyToManyField(Product)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')