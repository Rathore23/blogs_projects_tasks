from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.serializers import UserSerializer
from category.serializers import CategorySerializer
from posts.models import Post, PostPhoto


class PostPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostPhoto
        fields = ('id', 'image', 'width', 'height',)
        _required = {'required': True}
        _not_required = {'required': False}
        extra_kwargs = {
            'image': _required,
            'width': _not_required,
            'height': _not_required,
        }

    def create(self, validated_data):
        # converting in dict and get all image with key name
        images = dict(self.context['request'].data)["image"]
        post_id = self.context['view'].kwargs.get('nested_1_pk')
        if len(images) and images[0] == '':
            raise ValidationError("Images filed is required.")

        bulk_images = [
            PostPhoto(post_id=post_id, image=images[img]) for img in range(len(images))
        ]

        return PostPhoto.objects.bulk_create(bulk_images)[0]


class PostSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    # child (Post) to parent(Category) => Source name is field name
    category_details = CategorySerializer(source='category', read_only=True)
    # parent(Post) to child (PostPhoto) => Source name is related_name
    photos = PostPhotoSerializer(source='post_photos', read_only=True, many=True)
    like_count = serializers.CharField(read_only=True,)

    class Meta:
        model = Post
        fields = (
            "id", "category", "category_details", "title",
            "content", "user_details", "user", "photos",
            "like_count",
        )
        extra_kwargs = {
            "category": {
                "required": True,
            },
            "title": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            },
            "content": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            }
        }

    # def validate(self, attrs):
    #     validated_data = super().validated_data(attrs)
    #     if self.context["request"].user != self.validated_data.get('user'):
    #         raise serializers.ValidationError("You do not have permission.")
    #     return validated_data

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        post = super().create(validated_data)
        return post
