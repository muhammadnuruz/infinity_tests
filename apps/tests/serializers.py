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
    question_number = serializers.CharField(max_length=10, read_only=True)

    class Meta:
        model = Tests
        fields = ['question_number', 'question', 'answers']
        extra_kwargs = {'question': {'read_only': True}, 'answers': {'read_only': True}}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        data = GetTestAnswerSerializer(instance.answers.all(), many=True).data
        random.shuffle(data)
        representation['answers'] = data
        return representation
