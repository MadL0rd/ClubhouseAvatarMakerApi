from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def get_border_path(instance, filename):
    return f"borders/{instance.id}/{filename}"


class SettingJson(models.Model):
    data = models.JSONField()


class Brand(models.Model):
    title = models.CharField(verbose_name='Название', max_length=20, unique=True)

    def __str__(self):
        return self.title


class Code(models.Model):
    brand = models.ForeignKey(Brand, verbose_name='Бренд', on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    name = models.CharField(unique=True, verbose_name='Промокод', max_length=20)
    start_date = models.DateField(verbose_name='Начало действия промокода', blank=True, null=True)
    end_date = models.DateField(verbose_name='Конец действия промокода', blank=True, null=True)
    max_users_count = models.IntegerField(verbose_name='Начальное количество пользователей',)
    users = models.ManyToManyField(User, verbose_name='Пользователи, использующие промокод', related_name='codes', blank=True)

    @property
    def current_users_count(self):
        return self.users.count()

    @property
    def available_users_count(self):
        return self.max_users_count-self.current_users_count

    def __str__(self):
        return self.name


class Border(models.Model):
    brand = models.ForeignKey(Brand, verbose_name='Организация', blank=True, null=True, on_delete=models.CASCADE)
    code = models.ForeignKey(Code, verbose_name='Промокод', blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Название', max_length=20, blank=True)
    image = models.ImageField(verbose_name='Изображение', upload_to=get_border_path)
    colorable = models.BooleanField(verbose_name='Изменяем ли цвет', default=False)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Border)
def handle_new_border(sender, instance, **kwargs):
    if not instance:
        return

    if hasattr(instance, '_dirty'):
        return

    if instance.code is not None:
        instance.brand = instance.code.brand

    try:
        instance._dirty = True
        instance.save()
    finally:
        del instance._dirty
