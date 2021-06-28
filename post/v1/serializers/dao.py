from rest_framework import serializers


class AddPostDao(serializers.Serializer):
    caption = serializers.CharField(max_length=255)
    image_url = serializers.CharField(max_length=255, allow_blank=True)
    video_url = serializers.CharField(max_length=255, allow_blank=True)
    topic_uuid = serializers.CharField(max_length=45)


class UpdatePostDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100)
    caption = serializers.CharField(max_length=255)
    image_url = serializers.CharField(max_length=255, required=False, allow_blank=True)
    video_url = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate(self, data):
        if 'image_url' not in data and 'video_url' not in data:
            raise serializers.ValidationError("Must include either image_url or video_url")
        return data


class UpdateVoteDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100)
    increment = serializers.IntegerField()


class CommentVoteDao(serializers.Serializer):
    uuid = serializers.CharField(max_length=100)
    increment = serializers.IntegerField()


class GetVoteDao(serializers.Serializer):
    post_uuid = serializers.CharField(max_length=100)


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


class CommentListDao(serializers.Serializer):
    post_uuid = serializers.CharField(max_length=255)
    page = serializers.IntegerField()


class PostListDao(serializers.Serializer):
    page = serializers.IntegerField()


class AddCommentDao(serializers.Serializer):
    content = serializers.CharField()
    post_uuid = serializers.CharField(max_length=45)
    parent_comment_uuid = serializers.CharField(max_length=45, allow_null=True,)
