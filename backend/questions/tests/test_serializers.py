from unittest.mock import patch

from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from courses.models import LearningType, Course
from questions.models import Question, Answer, AnswerCategory, OpennessChoices
from questions.serializers import QuizSerializer


class TestQuizSerializer(APITestCase):
    serializer_class = QuizSerializer

    def setUp(self):
        self.test_question = Question.objects.create(title='test_question', text='Who are you?')
        LearningType.objects.bulk_create(
            [LearningType(name=name)
             for name in ('typeProgramming', 'typeDesign', 'typeAnalytics', 'typeCreativity', 'typeArt',
                          'typeSoftSkills', 'typePsychology', 'typePedagogy', 'typeSport', 'typeFinance',
                          'typeManagement', 'typePO', 'typeDataScience')]
        )
        self.test_points = {
            'IT': 1,
            'CREATIVITY': 2,
            'SOCIAL_SCIENCE': 3,
            'ECONOMICS': 4,
            'ANALYTICS': 5,
        }

        self.it_course = Course.objects.create(name='It course')
        self.it_course.learning_types.set([LearningType.objects.get(name='typeProgramming')])
        self.analytic_course = Course.objects.create(name='Analytic course')
        self.analytic_course.learning_types.set([LearningType.objects.get(name='typeAnalytics')])

    def test_serializer_raises_error_if_question_cant_have_multiple_answers_but_data_have_some_answers(self):
        self.test_question.has_multiple_answers = False
        self.test_question.save()
        Answer.objects.bulk_create(
            [Answer(question=self.test_question, text=f'answer_{i}', answer_category=AnswerCategory.IT.value)
             for i in range(3)]
        )
        test_data = {self.test_question.pk: Answer.objects.values_list('id', flat=True)}

        serializer = self.serializer_class(data={'quiz': test_data})
        with self.assertRaisesRegex(ValidationError, r"can't have multiple answers."):
            serializer.is_valid(raise_exception=True)

    @patch.object(Answer, 'full_clean', return_value=True)
    def test_process_answer_method_raises_error_if_answer_have_no_at_least_one_of_expected_fields(self, mock):
        Answer.objects.create(question=self.test_question, text='Cucu jopta.')

        serializer = self.serializer_class()
        with self.assertRaisesRegex(ValidationError, 'have no "openness_priority" and "answer_category"'):
            serializer._process_answers(Answer.objects.all())

    def test_process_answer_method_returns_expected_points(self):
        expected_points = self.test_points
        for i, category in enumerate(AnswerCategory, start=1):
            for _ in range(i):
                Answer.objects.create(
                    question=self.test_question,
                    text=f'answer_{i}',
                    answer_category=category
                )

        _, points = self.serializer_class()._process_answers(Answer.objects.all())
        self.assertEqual(expected_points, points)

    def test_process_answer_method_returns_expected_openness(self):
        Answer.objects.create(
            question=self.test_question,
            text='answer',
            openness_priority=OpennessChoices.MEDIUM,
        )

        openness, _ = self.serializer_class()._process_answers(Answer.objects.all())
        self.assertEqual(openness, OpennessChoices.MEDIUM)

    def test_get_top_learning_types_method_returns_analytics_learning_types(self):
        serializer = self.serializer_class()
        types = ('typeAnalytics', 'typeDataScience', 'typeFinance')
        expected_qs = LearningType.objects.filter(name__in=types).order_by('id')
        qs = serializer._get_top_learning_types(self.test_points, None).order_by('id')
        self.assertQuerySetEqual(expected_qs, qs)

    def test_get_top_learning_types_method_returns_analytics_and_it_learning_types(self):
        self.test_points['IT'] = 5
        serializer = self.serializer_class()
        types = ('typeAnalytics', 'typeDataScience', 'typeFinance', 'typeProgramming', 'typeDesign',
                 'typeAnalytics')
        expected_qs = LearningType.objects.filter(name__in=types).order_by('id')
        qs = serializer._get_top_learning_types(self.test_points, None).order_by('id')
        self.assertQuerySetEqual(expected_qs, qs)

    def test_get_top_learning_types_method_returns_all_learning_types_except_analytics_if_openness_is_high(
        self
    ):
        serializer = self.serializer_class()
        types = ('typeAnalytics', 'typeDataScience', 'typeFinance')
        expected_qs = LearningType.objects.exclude(name__in=types).order_by('id')
        qs = serializer._get_top_learning_types(self.test_points, OpennessChoices.HIGH).order_by('id')
        self.assertQuerySetEqual(expected_qs, qs)

    def test_get_courses_url_method_returns_expected_url(self):
        types = ('typeAnalytics', 'typeDataScience', 'typeFinance')
        expected_url = f'{reverse('courses-list')}?{'&'.join([f'learning_types={type_}' for type_ in types])}'
        learning_types = LearningType.objects.filter(name__in=types)

        url = self.serializer_class()._get_courses_url(learning_types)
        self.assertEqual(expected_url, url)
