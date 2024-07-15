import random
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from apps.tests.models import Tests, Answers
from apps.tests.serializers import GetTestsSerializer, CheckAnswersSerializer
from apps.telegram_users.models import TelegramUsers


def send_test_results_email(phone_number: str, full_name: str, correct: int, incorrect: int, answers: dict):
    answers_details = "\n".join([
        f"Question: {Tests.objects.get(id=test_id).question}, Answered Correctly: {result}"
        for test_id, result in answers.items()
    ])
    send_mail(
        subject=f"{full_name} worked the test.",
        message=f"""
{phone_number} - Phone number
{full_name}'s results:

Number of questions: {correct + incorrect}
Correct answers: {correct}
Wrong answers: {incorrect}

Details of answers:
{answers_details}
""",
        from_email=EMAIL_HOST_USER,
        recipient_list=["tulaganow@gmail.com"],
        fail_silently=False,
    )


class GetTestView(GenericAPIView):
    serializer_class = GetTestsSerializer
    permission_classes = [AllowAny]

    def get(self, request, chat_id, *args, **kwargs):
        try:
            telegram_user = TelegramUsers.objects.get(chat_id=chat_id)
        except TelegramUsers.DoesNotExist:
            return Response({"message": "Telegram user not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure step is a dictionary
        if telegram_user.step is None:
            telegram_user.step = {}
            telegram_user.save()

        available_tests = Tests.objects.exclude(id__in=telegram_user.step.keys())

        if not available_tests.exists():
            correct = sum(1 for v in telegram_user.step.values() if v)
            incorrect = sum(1 for v in telegram_user.step.values() if v is False)
            send_test_results_email(full_name=telegram_user.full_name, correct=correct, incorrect=incorrect,
                                    answers=telegram_user.step, phone_number=telegram_user.phone_number)
            telegram_user.step = {}
            telegram_user.save()
            return Response({
                "message": "You have completed all the tests.",
                "number_of_questions": correct + incorrect,
                "correct_questions": correct,
                "wrong_questions": incorrect,
            }, status=status.HTTP_404_NOT_FOUND)

        random_test = random.choice(available_tests)
        telegram_user.step[str(random_test.id)] = None
        telegram_user.save()
        data = {"question_number": len(telegram_user.step)}
        data.update(self.get_serializer(random_test).data)
        return Response(data, status=status.HTTP_200_OK)


class SubmitAnswerView(GenericAPIView):
    serializer_class = CheckAnswersSerializer
    permission_classes = [AllowAny]

    def post(self, request, chat_id, *args, **kwargs):
        try:
            telegram_user = TelegramUsers.objects.get(chat_id=chat_id)
        except TelegramUsers.DoesNotExist:
            return Response({"message": "Telegram user not found"}, status=status.HTTP_404_NOT_FOUND)

        user_answer = request.data.get('answer')
        test_id = next((k for k, v in telegram_user.step.items() if v is None), None)

        if not test_id:
            return Response({"message": "No active test found."}, status=status.HTTP_400_BAD_REQUEST)

        correct_answers = Answers.objects.filter(test_id=test_id, is_correct=True)
        is_correct = any(user_answer == answer.answer for answer in correct_answers)
        telegram_user.step[test_id] = is_correct
        telegram_user.save()

        message = "Correct answer!" if is_correct else "Wrong answer!"
        return Response({"message": message}, status=status.HTTP_200_OK)


class EndTestView(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, chat_id, *args, **kwargs):
        try:
            telegram_user = TelegramUsers.objects.get(chat_id=chat_id)
        except TelegramUsers.DoesNotExist:
            return Response({"message": "Telegram user not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure step is a dictionary
        if telegram_user.step is None:
            telegram_user.step = {}
            telegram_user.save()

        correct = sum(1 for v in telegram_user.step.values() if v)
        incorrect = sum(1 for v in telegram_user.step.values() if v is False)
        send_test_results_email(full_name=telegram_user.full_name, correct=correct, incorrect=incorrect,
                                answers=telegram_user.step, phone_number=telegram_user.phone_number)
        telegram_user.step = {}
        telegram_user.save()
        return Response({
            "message": "You have completed tests.",
            "number_of_questions": correct + incorrect,
            "correct_questions": correct,
            "wrong_questions": incorrect,
        }, status=status.HTTP_200_OK)
