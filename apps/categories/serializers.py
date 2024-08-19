from apps.categories.models import Categories
from rest_framework import serializers
from apps.words.serializers import WordsSerializer


class CategoriesSerializer(serializers.ModelSerializer):
    words_count = serializers.IntegerField(source='words.count', read_only=True)
    words = WordsSerializer(many=True, read_only=True)

    class Meta:
        model = Categories
        fields = ['id', 'name', 'words_count', 'created_at', 'words']
