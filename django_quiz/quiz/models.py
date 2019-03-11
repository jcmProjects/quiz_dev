from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.CharField(max_length=100)
    question = models.CharField(max_length=100)
    ansA = models.CharField(max_length=100)
    ansB = models.CharField(max_length=100)
    ansC = models.CharField(max_length=100)
    ansD = models.CharField(max_length=100)
    ansE = models.CharField(max_length=100)
    duration = models.IntegerField()
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='no_image.jpg', upload_to='quiz_img')

    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse('quiz-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        # Resize Image
        if img.height>768 or img.width>768:
            output_size = (768, 768)
            img.thumbnail(output_size)
            img.save(self.image.path)
