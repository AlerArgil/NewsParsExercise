from rest_framework import serializers

from news_pars_exercise.news.models import Tag, New


class NativeNewsSerializer(serializers.ModelSerializer):
    """
    New Serializer with all default field
    """
    class Meta:
        model = New
        fields = ('id', 'source', 'title', 'description', 'publish_at', 'created_at', 'edited_at')


class NewsSerializer(NativeNewsSerializer):
    """
    News Serializer with news
    """
    pass


class NativeTagsSerializer(serializers.ModelSerializer):
    """
    Tag Serializer with all default field
    """
    class Meta:
        model = Tag
        fields = ('id', 'name')


class TagNewsSerializer(NativeTagsSerializer):
    """
    Tag Serializer with news
    """
    news = NewsSerializer(many=True, read_only=True)

    class Meta(NativeTagsSerializer.Meta):
        fields = NativeTagsSerializer.Meta.fields + ('news',)
