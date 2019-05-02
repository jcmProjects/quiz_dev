from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.apps import apps
from PIL import Image


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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)   # one to one relation with our user model
    course = models.ManyToManyField('Course', through='ProfileCourse')
    image = models.ImageField(default='default_profile_pic.jpg', upload_to='profile_pics')

    # Valid Answer
    First = 'First'
    Last = 'Last'
    VALID_ANSWER_CHOICES = (
        (First, 'First'),
        (Last, 'Last'),
    )
    valid_ans = models.CharField(
        max_length=10,
        choices=VALID_ANSWER_CHOICES,
        default=Last,
    )

    def __str__(self):
        #return f'{self.user}'
        return f'{self.user.first_name} {self.user.last_name}'

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


# class Session(models.Model):
#     id = models.AutoField(primary_key=True)
#     quiz = models.ForeignKey('quiz.Quiz', on_delete=models.CASCADE)
#     date_created = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f'Quiz ID: {self.quiz.id}, User: {self.quiz.author}, Date: {self.date_created}'
