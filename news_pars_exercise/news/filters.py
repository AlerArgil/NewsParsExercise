import django_filters

from news_pars_exercise.news.models import New


class NewsFilter(django_filters.FilterSet):

    class Meta:
        model = New
        fields = {
            'publish_at': ['exact', 'in', 'gte', 'lte']
        }
