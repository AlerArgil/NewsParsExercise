from django.contrib import admin

from news_pars_exercise.news.models import Tag, New


class NewAdmin(admin.ModelAdmin):
    pass


admin.site.register(New, NewAdmin)


class TagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag, TagAdmin)