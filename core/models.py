from django.db import models

class Message(models.Model):

    message_id = models.IntegerField(null=False, primary_key=True)
    from_user = models.ForeignKey('User', null=False, on_delete=models.CASCADE)
    date = models.DateTimeField(null=False)
    text = models.TextField(default="")
    location = models.OneToOneField('Location', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "DATE: {}\n, USER: {}\n, TEXT: {}\n".format(str(self.date), str(self.from_user), str(self.text))

class User(models.Model):

    id = models.IntegerField(null=False, primary_key=True)
    is_bot = models.BooleanField(default=False)
    first_name = models.CharField(max_length=32, null=True)
    username = models.CharField(max_length=32, null=True)
    last_name = models.CharField(max_length=32, null=True)
    language_code = models.CharField(max_length=3, null=True)

    @property
    def messages(self):
        return self.message_set.all()

    def __str__(self):
        return str(self.username)

class Location(models.Model):

    longitude = models.FloatField(default=0.0)
    latitude = models.FloatField(default=0.0)

    def __str__(self):
        return "LAT {}, LON: {}".format(self.latitude, self.longitude)
