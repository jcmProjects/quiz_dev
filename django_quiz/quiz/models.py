from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from users.models import Course, ProfileCourse, Session

from datetime import datetime
from time import strftime

from unixtimestampfield.fields import UnixTimeStampField

class UnixTimestampField(models.DateTimeField):
    # UnixTimestampField: creates a DateTimeField that is represented on the
    # database as a TIMESTAMP field rather than the usual DATETIME field.
    # https://stackoverflow.com/questions/11332107/timestamp-fields-in-django/11332150

    def __init__(self, null=False, blank=False, **kwargs):
        super(UnixTimestampField, self).__init__(**kwargs)
        # default for TIMESTAMP is NOT NULL unlike most fields, so we have to
        # cheat a little:
        self.blank, self.isnull = blank, null
        self.null = True # To prevent the framework from shoving in "not null".

    def db_type(self, connection):
        typ=['TIMESTAMP']
        # See above!
        if self.isnull:
            typ += ['NULL']
        if self.auto_created:
            typ += ['default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP']
        return ' '.join(typ)

    def to_python(self, value):
        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        else:
            return models.DateTimeField.to_python(self, value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value==None:
            return None
        # Use '%Y%m%d%H%M%S' for MySQL < 4.1
        return strftime('%Y-%m-%d %H:%M:%S',value.timetuple())


class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ManyToManyField(Course)
    title = models.CharField(max_length=100, default=' ')
    question = models.CharField(max_length=100)
    ansA = models.CharField(max_length=50)
    ansB = models.CharField(max_length=50)
    ansC = models.CharField(max_length=50)
    ansD = models.CharField(max_length=50)
    ansE = models.CharField(max_length=50)
    duration = models.IntegerField()
    date_created = models.DateTimeField(default=timezone.now)
    #start_date = models.DateTimeField(default=timezone.now)
    start_date = UnixTimestampField(auto_created=True)
    #start_date = UnixTimeStampField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='no_image.jpg', upload_to='quiz_img')
    #anonymous = models.BooleanField(default=False)

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

    # ANONYMOUS
    Y = 'Yes'
    N = 'No'
    ANONYMOUS_CHOICES = (
        (Y, 'Yes'),
        (N, 'No'),
    )
    anonymous = models.CharField(
        max_length=3,
        choices=ANONYMOUS_CHOICES,
        default=N,
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
    quiz_id = models.ForeignKey('Quiz', on_delete=models.DO_NOTHING)            # DO_NOTHING
    student = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    time = models.CharField(max_length=100, default="")
    evaluation = models.CharField(max_length=100, default="")
    date_time = models.DateTimeField(default=timezone.now)
    session = models.ForeignKey(Session, default=1, on_delete=models.CASCADE)   # DO_NOTHING
    anonymous = models.CharField(max_length=3, default="No")

    def __str__(self):
        return f'Question: {self.quiz_id.id}, Student: {self.student}'  # {self.quiz_id.id} to return ID or {self.quiz_id} to return Question


class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    #nmec = models.CharField(max_length=100)
    uid = models.CharField(max_length=100, default='00 00 00 00 00 00 00')
    mac = models.CharField(max_length=100)
    ans = models.CharField(max_length=100)
    date_time = models.DateTimeField(default=timezone.now)
    #date_time = UnixTimestampField(auto_created=True)

    def __str__(self):
        return f'{self.uid}, {self.ans}'


class AnswerProcessing(models.Model):
    id = models.AutoField(primary_key=True)
    nmec = models.CharField(max_length=100)
    mac = models.CharField(max_length=100)
    ans = models.CharField(max_length=100)
    date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nmec


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=100)
    nmec = models.CharField(max_length=100)

    def __str__(self):
        return self.nmec


class Terminal(models.Model):
    id = models.AutoField(primary_key=True)
    mac = models.CharField(max_length=100)

    def __str__(self):
        return self.mac