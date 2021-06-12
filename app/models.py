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
    name = models.CharField(max_length=255, default="")
    email = models.CharField(max_length=255, default="")
    password = models.CharField(max_length=45, default="")
    image_url = models.CharField(max_length=255, default="")


class Topic(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=255, default="")
    desc = models.CharField(max_length=255, default="")
    url = models.CharField(max_length=255, default=None, null=True)
    category = models.CharField(max_length=45, default=None)
    source_name = models.CharField(max_length=45)
    user = models.ForeignKey(User)


class Post(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4)
    caption = models.TextField(default="", null=True)
    image_url = models.CharField(max_length=255, default=None, null=True)
    video_url = models.CharField(max_length=255, default=None, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4)
    content = models.TextField(default="")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.IntegerField(default=0, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Like(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4)
    value = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User)