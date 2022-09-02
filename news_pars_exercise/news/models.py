from django.db import models


class New(models.Model):
    """
    Model of news
    """
    YANDEX = 'y'
    OZON = 'o'
    SOURCES = [
        (YANDEX, 'yandex'),
        (OZON, 'ozon')
    ]
    source = models.CharField(max_length=1, choices=SOURCES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    publish_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(through='NewTags', to='Tag')


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    news = models.ManyToManyField(through='NewTags', to='New')


class NewTags(models.Model):
    new = models.ForeignKey(New, related_name='newtags', on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, related_name='newtags', on_delete=models.CASCADE)
