from django.db import models
from core import constants


'''
class Message(models.Model):

    message_id = models.IntegerField(null=False, primary_key=True)
    from_user = models.ForeignKey('User', null=False, on_delete=models.CASCADE)
    date = models.DateTimeField(null=False)
    text = models.TextField(default="")
    location = models.OneToOneField('Location', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "DATE: {}\n, USER: {}\n, TEXT: {}\n".format(str(self.date), str(self.from_user), str(self.text))

    class Meta:
        ordering = ['date']
'''


class User(models.Model):

    id = models.IntegerField(null=False, primary_key=True)
    is_bot = models.BooleanField(default=False)
    first_name = models.CharField(max_length=32, null=True)
    username = models.CharField(max_length=32, null=True)
    last_name = models.CharField(max_length=32, null=True)
    language_code = models.CharField(max_length=3, null=True)

    @property
    def locations(self):
        if self.location_set:
            return self.location_set.all()
        return None

    def __str__(self):
        return str(self.username)


class Location(models.Model):

    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)

    text = models.CharField(max_length=256, default='')

    is_editable = models.BooleanField(default=True)

    @property
    def photos(self):
        if self.photo_set:
            return self.photo_set.all()
        return None

    def __str__(self):
        return "({}, {}) {}".format(self.latitude, self.longitude, self.text)


class Photo(models.Model):

    link = models.TextField(null=True)
    upload = models.ImageField(upload_to='places/', null=True)
    location = models.ForeignKey(Location, null=True, on_delete=models.CASCADE)
