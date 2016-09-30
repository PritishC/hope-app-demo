import mimetypes

from rest_framework import serializers

from job_ready.models import Video, Article


class VideoSerializer(serializers.ModelSerializer):
    video_file = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    mimetype = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ('title', 'category', 'icon',
                  'is_premium', 'video_file',
                  'description', 'mimetype')

    def get_video_file(self, obj):
        """
        Arguably not the best way to go about it,
        will perhaps go in the future with Permission+
        separate Serializers+separate Views.
        """
        request = self.context['request']

        if obj.is_premium and \
                not request.user.subscribed:
            return

        # Return S3 presigned url
        return obj.generate_url()

    def get_category(self, obj):
        return obj.category.name

    def get_mimetype(self, obj):
        return mimetypes.guess_type(obj.video_file.name)[0]


class ArticleSerializer(serializers.ModelSerializer):
    article_content = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('title', 'category', 'icon',
                  'is_premium', 'article_content')

    def get_article_content(self, obj):
        request = self.context['request']

        if obj.is_premium and \
                not request.user.subscribed:
            return

        return obj.article_content

    def get_category(self, obj):
        return obj.category.name
