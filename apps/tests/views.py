import random

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.tests.models import Tests, Answers
from apps.tests.serializers import GetTestsSerializer, CheckAnswersSerializer
from apps.users.permissions import UserPermission


class GetTestView(GenericAPIView):
    serializer_class = GetTestsSerializer
    permission_classes = [UserPermission]

    def get(self, request, *args, **kwargs):
        topic_id = self.kwargs.get('topic_id')
        available_tests = Tests.objects.filter(topic=topic_id).exclude(id__in=request.user.step.keys())

        if not available_tests.exists():
            tr, fl = 0, 0
            for k, v in request.user.step.items():
                if v is True:
                    tr += 1
                elif v is False:
                    fl += 1
                else:
                    request.user.step.pop(k)
            request.user.step = {}
            request.user.save()
            return Response(data={
                "message": "You have completed all the tests for this topic.",
                "number_of_questions": tr + fl,
                "true_questions": tr,
                "false_questions": fl,
            },
                status=status.HTTP_404_NOT_FOUND)
        random_test = random.choice(available_tests)
        user_step = request.user.step
        user_step[str(random_test.id)] = None
        request.user.step = user_step
        request.user.save()
        data = {"question_number": len(request.user.step)}
        data.update(self.get_serializer(random_test).data)
        return Response(data, status=status.HTTP_200_OK)


class SubmitAnswerView(GenericAPIView):
    serializer_class = CheckAnswersSerializer
    permission_classes = [UserPermission]

    def post(self, request, *args, **kwargs):
        user_answer = request.data.get('answer')
        test_id = None
        for k, v in request.user.step.items():
            if v is None:
                test_id = k
                break
        if not test_id:
            return Response(data={"message": "No active test found or all tests completed."},
                            status=status.HTTP_400_BAD_REQUEST)
        correct_answers = Answers.objects.filter(test_id=test_id, is_correct=True)
        is_correct = any(user_answer == answer.answer for answer in correct_answers)
        request.user.step[test_id] = is_correct
        request.user.save()
        if is_correct:
            return Response(data={"message": "Correct answer!"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Wrong answer, try again!"}, status=status.HTTP_200_OK)


class EndTestView(GenericAPIView):
    permission_classes = [UserPermission]

    def get(self, request, *args, **kwargs):
        tr, fl, no = 0, 0, 0
        for k, v in request.user.step.items():
            if v is True:
                tr += 1
            elif v is False:
                fl += 1
        request.user.step = {}
        request.user.save()
        return Response(data={
            "message": "You have completed all the tests for this topic.",
            "number_of_questions": tr + fl,
            "true_questions": tr,
            "false_questions": fl,
        },
            status=status.HTTP_404_NOT_FOUND)
