from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        values = [email]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError("The {} value must be set".format(field_name))

        email = self.normalize_email(email)
        extra_fields.setdefault("username", email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("username", email)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(unique=True, max_length=200)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    address = models.TextField(max_length=200, null=True)
    lat = models.DecimalField(decimal_places=10, default=27.7172, max_digits=15)
    lng = models.DecimalField(decimal_places=10, default=85.3240, max_digits=15)
    dob = models.DateTimeField(null=True, blank=True, default=timezone.now)
    phone = models.CharField(max_length=200, blank=True)
    phone_activated = models.BooleanField(default=False)
    phone_activation_code = models.CharField(max_length=200)
    genderChoices = [("Male", "Male"), ("Female", "Female"), ("Other", "Other")]
    gender = models.CharField(max_length=200, choices=genderChoices, default="Male")
    profile_image = models.ImageField(blank=True)
    cover_photo = models.ImageField(blank=True)
    facebook_link = models.CharField(max_length=200, blank=True)
    twitter_link = models.CharField(max_length=200, blank=True)
    instagram_link = models.CharField(max_length=200, blank=True)
    youtube_link = models.CharField(max_length=200, blank=True)
    linkedin_link = models.CharField(max_length=200, blank=True)
    sendEmail = models.BooleanField(default=True)
    sendSMS = models.BooleanField(default=True)
    activation = models.CharField(max_length=200)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def fromdict(self, datadict):
        if datadict:
            for dict_key, value in datadict.items():
                self.dict_key = value
                print(self.dict_key)
        print(self)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        if not self.dob:
            self.dob = timezone.now()
        if not self.date_joined:
            self.date_joined = timezone.now()
        if not self.last_login:
            self.last_login = timezone.now()
        self.last_login = timezone.now()
        try:
            super(CustomUser, self).save(*args, **kwargs)
            return self.pk
        except Exception as e:
            print(e)
            return 0
