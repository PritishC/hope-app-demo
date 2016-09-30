from django.db.models import Q

from rest_framework import viewsets, permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_extensions.cache.decorators import cache_response

from job_ready.serializers import VideoSerializer, ArticleSerializer
from job_ready.models import Video, Article


class VideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VideoSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, BasicAuthentication)

    @cache_response()
    def list(self, request, *args, **kwargs):
        return super(VideoViewSet, self).list(request, *args, **kwargs)

    def get_queryset(self):
        """
        Return content based on the year of college of the user
        requesting.
        """
        return Video.objects\
            .filter(Q(year__year_integer=self.request.user.college_year) |
                    Q(year__year_integer=None))\
            .order_by('category')


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, BasicAuthentication)

    @cache_response()
    def list(self, request, *args, **kwargs):
        return super(ArticleViewSet, self).list(request, *args, **kwargs)

    def get_queryset(self):
        """
        Return content based on the year of college of the user
        requesting.
        """
        return Article.objects\
            .filter(Q(year__year_integer=self.request.user.college_year) |
                    Q(year__year_integer=None))\
            .order_by('category')
