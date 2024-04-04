from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractBaseUser, PermissionsMixin):
    """
    https://testdriven.io/blog/django-custom-user-model/
    """

    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=128,
        unique=True,
        blank=True, null=True,
        help_text=_("Required. 128 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _("email address"),
        null=True, blank=True,
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists.")
        }
    )
    phone = PhoneNumberField(
        _("Phone"),
        null=True, blank=True,
        unique=True,
        error_messages={"unique": _("A user with that phone already exists.")}
    )
    first_name = models.CharField(
        _("first name"),
        max_length=100,
        blank=True
    )
    last_name = models.CharField(
        _("last name"),
        max_length=100,
        blank=True
    )
    # pip install Pillow
    photo = models.ImageField(
        upload_to='accounts/',
        null=True,
        blank=True,
        default="accounts/profile_default.png"
    )
    bio = models.TextField(_("Bio"), max_length=300, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email",]

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()