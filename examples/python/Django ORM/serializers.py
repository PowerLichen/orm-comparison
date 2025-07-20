from rest_framework import serializers

from models import Post


class PostEditInputSerializer(serializers.Serializer):
    offset = serializers.IntegerField(required=False, min_value=0)
    limit = serializers.IntegerField(required=False, min_value=1)
    author_ids = serializers.CharField(
        required=False, help_text="author의 id 리스트. `,`으로 구분"
    )
    section_code = serializers.CharField(
        required=False, help_text="PostSection의 section code"
    )


class PostEditOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
