from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from apps.words.models import Words
from apps.words.serializers import WordsSerializer, WordsCreateSerializer


class WordsListViewSet(ListAPIView):
    queryset = Words.objects.all()
    serializer_class = WordsSerializer


class WordsCreateViewSet(CreateAPIView):
    queryset = Words.objects.all()
    serializer_class = WordsCreateSerializer
    permission_classes = [AllowAny]


class WordsUpdateViewSet(UpdateAPIView):
    queryset = Words.objects.all()
    serializer_class = WordsCreateSerializer
    permission_classes = [AllowAny]


class WordsDetailViewSet(RetrieveAPIView):
    queryset = Words.objects.all()
    serializer_class = WordsSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        random_words = Words.objects.exclude(id=instance.id).order_by('?')[:3]
        random_words_names = [word.name for word in random_words]

        data = {
            'word': serializer.data,
            'random_words': random_words_names
        }
        return Response(data)

