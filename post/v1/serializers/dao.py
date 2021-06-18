from rest_framework import serializers


class AddPostDao(serializers.Serializer):
    caption = serializers.CharField(max_length=255)
    image_url = serializers.CharField(max_length=255)
    video_url = serializers.CharField(max_length=255)
    topic = serializers.CharField(max_length=45)
    user_uuid = serializers.CharField(max_length=45)


class UpdatePostDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100)
    caption = serializers.CharField(max_length=255)
    image_url = serializers.CharField(max_length=255)
    video_url = serializers.CharField(max_length=255)


class UpdateVoteDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100)
    increment = serializers.IntegerField()


class GetVoteDao(serializers.Serializer):
    post_uuid = serializers.CharField(max_length=100)
    user_uuid = serializers.CharField(max_length=100)


class AddTopicDao(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    desc = serializers.CharField(max_length=255)
    url = serializers.CharField(max_length=255)
    category = serializers.CharField(max_length=45)
    source_name = serializers.CharField(max_length=45)


class UpdateTopicDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255)
    desc = serializers.CharField(max_length=255)
    url = serializers.CharField(max_length=255)
    category = serializers.CharField(max_length=45)
    source_name = serializers.CharField(max_length=45)
    user_uuid = serializers.CharField(max_length=100)


class CommentListDao(serializers.Serializer):
    post_uuid = serializers.CharField(max_length=255)
    page = serializers.IntegerField()