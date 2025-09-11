from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from questions.models import Question
from questions.serializers import QuestionSerializer, QuizSerializer


class QuizView(GenericAPIView):
    serializer_class = QuizSerializer

    @action(methods=['post'], detail=False)
    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        url = serializer.get_courses_url()
        return Response(data={'url': url})


class QuestionViewSet(ReadOnlyModelViewSet):
    queryset = Question.objects.all().prefetch_related('answers')
    serializer_class = QuestionSerializer
