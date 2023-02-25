from rest_framework import serializers

from apps.users.models import Post


class PostSerializer(serializers.ModelSerializer):
    user=serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Post
        fields = "__all__"