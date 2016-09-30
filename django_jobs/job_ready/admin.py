from django.contrib import admin

from .models import Category, Video, Article, Year


class ContentAdminMixin(object):
    list_filter = ('category', 'is_premium')
    readonly_fields = ('added_at', 'last_modified_at',
                       'added_by')
    list_display = ('title', 'added_at', 'added_by')


class ArticleAdmin(ContentAdminMixin, admin.ModelAdmin):
    model = Article
    filter_horizontal = ('year',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.added_by = request.user
        super(ArticleAdmin, self).save_model(request, obj, form, change)


class VideoAdmin(ContentAdminMixin, admin.ModelAdmin):
    model = Video
    filter_horizontal = ('year',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.added_by = request.user
        super(VideoAdmin, self).save_model(request, obj, form, change)


admin.site.register(Category)
admin.site.register(Year)
admin.site.register(Video, VideoAdmin)
admin.site.register(Article, ArticleAdmin)
