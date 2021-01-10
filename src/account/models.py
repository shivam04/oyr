from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    aadhar_card = models.CharField(max_length=16, blank=False)
    contact_no = models.CharField(max_length=11)
    is_customer = models.BooleanField(default=True)

    def user_detail(self):
        return User.objects.filter(username=self.user.username)
