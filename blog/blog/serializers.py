from rest_framework import serializers

from .models import Post, Comment

"""
The `HyperlinkedModelSerializer` is like a `ModelSerializer`, except uses url
instead of using a model instance's `id` attribute to identify resources
as well as in relationships.
"""

class PostSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the `Post` model.
    """

    author = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Post
        read_only_fields = ('date_created',)

    # Like Django's Form's clean_XXX.
    # `source` is the attribute name.
    def validate_author(self, attrs, source):
        if source not in attrs:
            return attrs

        request = self.context['request']

        if request.user.is_superuser and attrs[source] == None or \
                request.user.is_authenticated():
            # Make sure the author cannot reverse plagarise and set the author
            # to someone else.
            attrs[source] = request.user

        return attrs


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the `Comment` model.
    """

    author = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Comment
        read_only_fields = ('date_created',)

    def validate_author(self, attrs, source):
        if source not in attrs:
            return attrs

        request = self.context['request']

        if request.user.is_superuser and attrs[source] == None or \
                request.user.is_authenticated():
            # Make sure the author cannot reverse plagarise and set the author
            # to someone else.
            attrs[source] = request.user

        return attrs
