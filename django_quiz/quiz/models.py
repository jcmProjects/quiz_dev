from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.CharField(max_length=100)
    question = models.CharField(max_length=100)
    ansA = models.CharField(max_length=50)
    ansB = models.CharField(max_length=50)
    ansC = models.CharField(max_length=50)
    ansD = models.CharField(max_length=50)
    ansE = models.CharField(max_length=50)
    duration = models.IntegerField()
    date_created = models.DateTimeField(default=timezone.now)
    execution_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='no_image.jpg', upload_to='quiz_img')

    # Right Answer
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    RIGHT_ANSWER_CHOICES = (
        (A, 'a)'),
        (B, 'b)'),
        (C, 'c)'),
        (D, 'd)'),
        (E, 'e)'),
    )
    right_ans = models.CharField(
        max_length=1,
        choices=RIGHT_ANSWER_CHOICES,
        default=A,
    )

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


class Results(models.Model):
    id = models.AutoField(primary_key=True)
    quiz_id = models.ForeignKey('Quiz', on_delete=models.DO_NOTHING)
    student = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    date_time = models.DateTimeField(default=timezone.now)