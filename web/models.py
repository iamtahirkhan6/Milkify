from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager

#############################################################

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#############################################################

class Locality(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length = 200, null = True, blank = True, unique=True)

    class Meta:
        verbose_name_plural = "Localities"

    def __str__(self):
        return self.name

#############################################################

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.ForeignKey('Product', on_delete=models.CASCADE, blank=False)
    seller = models.ForeignKey('CustomUser', on_delete=models.CASCADE, blank=False)
    locality = models.ManyToManyField(Locality, blank=False)
    price = models.FloatField(blank=False)

    class Meta:
        verbose_name_plural = "Listings"

    def __str__(self):
        return str(self.name.__str__() + str(' (') + self.seller.__str__() + str(') - ₹') + self.price.__str__())

#############################################################

class Subscription(models.Model):
    TIMING_CHOICES = (
      (1, '7AM'),
      (2, '8AM'),
      (3, '9AM'),
      (4, '10AM'),
      (5, '4PM'),
      (6, '5PM'),
      (7, '6PM'),
      (8, '7PM'),
    )
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey('CustomUser', on_delete=models.CASCADE, blank=False)
    buyer = models.ForeignKey('CustomUser', on_delete=models.CASCADE, blank=False, related_name="consumer")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=False, default='', null=True)
    price = models.FloatField(blank=False)
    timing = models.PositiveSmallIntegerField(_('timing'), choices=TIMING_CHOICES, null=True, blank=True)
    duration_from = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    duration_till = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    total_amount = models.FloatField(blank=False)

    address_1 = models.CharField(_('address 1'), max_length=500, blank=True)
    address_2 = models.CharField(_('address 2'), max_length=500, blank=True)
    locality = models.ForeignKey('Locality', on_delete=models.CASCADE, null=True, blank=True)
    mobile = models.CharField(_('mobile number'), max_length=250, blank=True)

    def __str__(self):
        return str("Subscription #" + str(self.id.__str__()))

#############################################################

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
      (1, 'Consumer'),
      (2, 'Farmer'),
    )
    id = models.AutoField(primary_key=True)
    email = models.EmailField(_('Email Address'), unique=True)
    first_name = models.CharField(_('First Name'), max_length=30, blank=True)
    last_name = models.CharField(_('Last Name'), max_length=30, blank=True)
    user_type = models.PositiveSmallIntegerField(_('user_type'), choices=USER_TYPE_CHOICES, null=True, blank=True)
    account_balance = models.FloatField(blank=True, null=True)
    date_joined = models.DateTimeField(_('Date Joined'), auto_now_add=True)
    is_active = models.BooleanField(_('Active'), default=True)
    is_staff = models.BooleanField(_('Staff'), default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name
