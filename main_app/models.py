from django.db import models
from django.contrib.auth.models import AbstractUser
from klin_api.models import User
from autoslug import AutoSlugField
import datetime
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class Schedule(models.Model):
    title = models.CharField(max_length=200)
    start_time = models.DateTimeField(default=datetime.date.today)

    def __str__(self):
        return self.title
    @property
    def get_calendar_url(self):
        url = reverse('schedule_edit', args=(self.id,))
        return f'<p>{self.title}</p><a href="{url}">edit</a>'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    section_points = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user.first_name)


class Blogpost(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    image = models.ImageField(default='default.png', upload_to='blog_pics')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.pk)])


class Comment(models.Model):
    post = models.ForeignKey(Blogpost,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


class Waste(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class PickupTime(models.Model):
    time_range = models.CharField(max_length=50)

    def __str__(self):
        return self.time_range


class PickupRequest(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = PhoneNumberField(null=False, blank=False)
    address = models.CharField(max_length=300)
    date = models.DateField(auto_now_add=False)
    time = models.ForeignKey(PickupTime, on_delete=models.CASCADE)
    waste_type = models.ManyToManyField(Waste)
    quantity = models.IntegerField()
    extra_note = models.TextField(max_length=500)
    is_donor = models.BooleanField(default=False)
    is_collector = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name




