from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "email",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "username",
                )
            },
        ),

        (
            "Profile Information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "dob",
                    "gender",
                    "address",
                    "lat",
                    "lng",
                    "phone",
                )
            },
        ),
        (
            "Images",
            {
                "fields": (
                    "profile_image",
                    "cover_photo",
                )
            },
        ),
        (
            "Social links",
            {
                "fields": (
                    "facebook_link",
                    "twitter_link",
                    "instagram_link",
                    "youtube_link",
                    "linkedin_link",
                )
            },
        ),
        (
            "Advanced options",
            {
                "fields": (
                    "date_joined",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "phone_activated",
                    "sendEmail",
                    "sendSMS",
                ),
            },
        ),
        ("Permissions", {"fields": ("groups", "user_permissions")})
    )
    add_fieldsets = (
        (

            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ()
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
