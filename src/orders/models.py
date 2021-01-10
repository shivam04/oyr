from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify
from shop.models import Shop

from items.models import Item


class Order(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    shop = models.ForeignKey(Shop, null=True, on_delete=models.SET_NULL)
    order_number = models.SlugField(unique=True, default=None)
    pickup_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(null=False, blank=False, default="CREATED", max_length=20)


class ItemOrder(models.Model):
    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(1)])


def create_slug(instance, new_slug=None):
    slug = str(int(timezone.now().timestamp() * 1000))
    if new_slug is not None:
        slug = new_slug
    qs = Order.objects.filter(order_number=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = slug + "-" + str(qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_order_slug(sender, instance, *args, **kwargs):
    if not instance.order_number:
        instance.order_number = create_slug(instance)


pre_save.connect(pre_save_order_slug, sender=Order)
