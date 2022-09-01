from django.db import models


class New(models.Model):
    """
    Model of news
    """
    YANDEX = 'y'
    OZON = 'o'
    SOURCES = [
        YANDEX,
        OZON
    ]

    id = models.PositiveBigIntegerField(primary_key=True)
    source = models.CharField(max_length=1, choices=SOURCES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    publish_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)


class Tags(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)


class NewTags(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    new = models.ForeignKey(New, related_name='newtags', on_delete=models.CASCADE)
    tag = models.ForeignKey(New, related_name='newtags', on_delete=models.CASCADE)
