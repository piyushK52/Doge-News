import hashlib
import os
from django.db import models
from util.hash import PBKDF2PasswordHasher
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


class UserProfile(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4)
    name = models.CharField(max_length=255, default="")
    email = models.CharField(max_length=255, default="")
    password = models.CharField(max_length=225, default="")
    image_url = models.CharField(max_length=255, default="")
    bio = models.CharField(max_length=255, default="")

    class Meta:
        db_table = 'UserProfile'

    def save(self, *args, **kwargs):
        if not self.id:
            password = ""
            if self.password:
                password = self.password
            self.password = PBKDF2PasswordHasher().encode(password)
        super(UserProfile, self).save(*args, **kwargs)


class Topic(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=255, default="")
    desc = models.CharField(max_length=255, default="")
    url = models.CharField(max_length=255, default=None, null=True)
    category = models.CharField(max_length=45, default=None)
    source_name = models.CharField(max_length=45)
    user = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'topic'


class Post(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4)
    caption = models.TextField(default="", null=True)
    image_url = models.CharField(max_length=255, default=None, null=True)
    video_url = models.CharField(max_length=255, default=None, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = 'post'


class Comment(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4)
    content = models.TextField(default="")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, default=0, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = 'comment'


class Vote(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4)
    value = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = 'vote'


class CommentVote(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4)
    value = models.IntegerField(default=0)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = 'comment_vote'


class Session(BaseModel):
    token = models.CharField(max_length=255)
    uuid = models.CharField(max_length=255)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = 'session'

    def save(self, *args, **kwargs):
        self.token = str(hashlib.sha1(os.urandom(128)).hexdigest())[:26]
        super(Session, self).save(*args, **kwargs)


class Relationship(BaseModel):
    uuid = models.CharField(max_length=45)
    follower_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='follower')
    followed_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='followed')

    class Meta:
        db_table = 'relationship'
