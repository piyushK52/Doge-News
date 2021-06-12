from django.db import models
import uuid


class TinyIntegerField(models.SmallIntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint"
        else:
            return super(TinyIntegerField, self).db_type(connection)


class BaseModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_disabled = TinyIntegerField(default=0)

    class Meta:
        abstract = True


class User(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=255, default=None)
    email = models.CharField(max_length=255, default=None)
    password = models.CharField(max_length=45, default=None)
    image_url = models.CharField(max_length=255, default=None)

