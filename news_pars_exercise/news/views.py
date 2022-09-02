import django_filters
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from news_pars_exercise.news.filters import NewsFilter
from news_pars_exercise.news.models import Tag, New
from news_pars_exercise.news.parsers import YandexParsing, OzonParsing
from news_pars_exercise.news.serializers import TagNewsSerializer, NewsSerializer


class TagWithNewView(generics.RetrieveAPIView):
    """
    View tag with news
    """
    queryset = Tag.objects.prefetch_related('news').all()
    serializer_class = TagNewsSerializer
    lookup_field = 'name'


class ListNewView(generics.ListAPIView):
    """
    View news list
    """
    queryset = New.objects.all()
    serializer_class = NewsSerializer
    filterset_class = NewsFilter


class RunParsingView(GenericViewSet):
    permission_classes = AllowAny,

    def parsing(self, request):
        y_p = YandexParsing()
        y_p.parse_news()
        o_p = OzonParsing()
        o_p.parse_news()
        return JsonResponse(dict(result='success'))
