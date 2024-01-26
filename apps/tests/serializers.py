import random

from apps.tests.models import Tests, Answers
from rest_framework import serializers


class CheckAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ['answer']


class GetTestAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ['answer']


class GetTestsSerializer(serializers.ModelSerializer):
    topic_id = serializers.IntegerField(write_only=True)
    question_number = serializers.CharField(max_length=10, read_only=True)

    class Meta:
        model = Tests
        fields = ['topic', 'question_number', 'question', 'answers', 'topic_id']
        extra_kwargs = {'topic': {'read_only': True}, 'question': {'read_only': True}, 'answers': {'read_only': True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['topic'] = instance.topic.name
        data = GetTestAnswerSerializer(instance.answers.all(), many=True).data
        random.shuffle(data)
        representation['answers'] = data
        return representation
