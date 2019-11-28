from apps.web import models
from rest_framework import generics, permissions

from . import serializers, utils


class QuestionList(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    pagination_class = utils.SmallResultsSetPagination

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category=category)
        return queryset
