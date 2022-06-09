from pathlib import Path
from time import time

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from mainapp.models import NULLABLE


def user_avatars_path(instance, filename):
    # file will be uploaded to
    #    MEDIA_ROOT / user_ < username > / avatars / < filename >
    num = int(time() * 1000)
    suff = Path(filename).suffix
    return f'user_{instance.username}/avatars/pic_{num}{suff}'


class CustomUser(AbstractUser):
    email = models.EmailField(**NULLABLE, verbose_name=_('email'), unique=True)
    age = models.PositiveIntegerField(**NULLABLE, verbose_name=_('age'))
    avatar = models.ImageField(upload_to=user_avatars_path, **NULLABLE, verbose_name=_('avatar'))

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
