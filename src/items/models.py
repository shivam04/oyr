from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.utils.text import slugify
from shop.models import Shop
from django.core.validators import MinValueValidator


class Item(models.Model):
    name = models.CharField(max_length=200)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(null=False, blank=False)
    cost = models.FloatField(null=False, blank=False, validators=[MinValueValidator(0)])
    slug = models.SlugField(unique=True, default=None)

    def shop_detail(self):
        return Shop.objects.filter(slug=self.shop.slug)


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


pre_save.connect(pre_save_shop_slug, sender=Item)