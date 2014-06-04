from rest_framework import viewsets

from . import serializers

from .permissions import Or, IsReadOnly, IsStaff, IsCreateOnly, IsAuthor
from . import models


"""
ModelViewSet automatically sets up retrieve, update, create, delete, list,
operations for the resource. 5 views in 1!
"""

class PostViewSet(viewsets.ModelViewSet):
    model = models.Post
    serializer_class = serializers.PostSerializer
    permission_classes = [ # permission_classes ANDs everything in the list.
        Or(IsReadOnly, IsStaff), # Custom OR operator.
        Or(IsReadOnly, IsAuthor)
        # Authors can, if they are also staff, can update their own comments.
    ]


class CommentViewSet(viewsets.ModelViewSet):
    model = models.Comment
    serializer_class = serializers.CommentSerializer
    permission_classes = [
        Or(IsReadOnly, IsCreateOnly, IsAuthor)
        # Only authors can update their own comments.
    ]

    # `get_queryset` can be overridden to apply permissions retrieve list,
    # so that the list can be filtered for users only authorised to view the
    # existence of some, but not all, objects.

    # def get_queryset(self):
    #   return Comment.objects.filter(...)
