from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)   # one to one relation with our user model
    course = models.ManyToManyField('Course', through='ProfileCourse')
    image = models.ImageField(default='default_profile_pic.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image)

        # Resize Image
        if img.height>300 or img.width>300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image)



class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.course_name)


class ProfileCourse(models.Model):
    id = models.AutoField(primary_key=True)
    profile = models.ForeignKey('Profile', on_delete=models.DO_NOTHING)
    course = models.ForeignKey('Course', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'Course: {self.course}, User: {self.profile}'
