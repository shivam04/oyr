from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db.models.signals import pre_save
from django.utils.text import slugify


class Shop(models.Model):
    name = models.CharField(max_length=200)
    lisence_number = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, default=None)

    def user_detail(self):
        return User.objects.filter(username=self.user.username)


def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Shop.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = slug + "-" + str(qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_shop_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_shop_slug, sender=Shop)
