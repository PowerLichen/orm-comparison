from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from models import Post
from serializers import PostEditInputSerializer, PostEditOutputSerializer


class PostEditViewSet(ListModelMixin, GenericViewSet):
    serializer_class = PostEditOutputSerializer

    def get_queryset(self):
        path_params = self.kwargs

        blog_id = path_params["blog_id"]
        serializer = PostEditInputSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)

        return Post.service_objects.get_valid_post(
            blog_id, data=serializer.validated_data
        )

    @extend_schema(
        operation_id="api_post_edit_list",
        description="Post 수정 시, 수정 가능한 Post 목록을 가져옵니다.",
        parameters=[PostEditInputSerializer],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
