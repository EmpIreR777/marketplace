from collections import defaultdict

from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

from courses.models import LearningType
from questions.models import Answer, Question, OpennessChoices, AnswerCategory

TOpenness = OpennessChoices | None


class AnswerListField(serializers.ListField):
    child = serializers.IntegerField()


class QuestionDictField(serializers.DictField):
    child = AnswerListField()

    def run_child_validation(self, data):
        result = {}
        errors = {}

        for key, value in data.items():
            key = int(key)

            try:
                result[key] = self.child.run_validation(value)
            except ValidationError as e:
                errors[key] = e.detail

        if not errors:
            return result
        raise ValidationError(errors)


class QuizSerializer(serializers.Serializer):
    quiz = QuestionDictField(allow_empty=False)

    default_error_messages = {
        'cant_have_multiple_answer': "Questions with ID: {ids} can't have multiple answers.",
        'invalid_answer': 'Answer(id={id}) have no "openness_priority" and "answer_category".'
    }

    def validate_quiz(self, quiz: dict[int, list[int]]):
        questions = Question.objects.filter(pk__in=quiz)

        invalid_questions: list[str] = []
        for question in questions:
            raw_answer_ids = quiz[question.pk]
            if len(raw_answer_ids) > 1 and not question.has_multiple_answers:
                invalid_questions.append(str(question.pk))

        if invalid_questions:
            self.fail('cant_have_multiple_answer', ids=', '.join(invalid_questions))

        return quiz

    def get_courses_url(self) -> str:
        raw_answer_ids = sum(self.validated_data['quiz'].values(), start=[])
        answers = Answer.objects.filter(pk__in=raw_answer_ids)
        openness, category_points = self._process_answers(answers)
        top_learning_types = self._get_top_learning_types(category_points, openness)
        url_piece = self._get_courses_url(top_learning_types)
        return self.context['request'].build_absolute_uri(url_piece)

    def _process_answers(self, answers: QuerySet[Answer]) -> tuple[TOpenness, dict[AnswerCategory, int]]:
        openness: OpennessChoices | None = None
        category_points: dict[AnswerCategory, int] = defaultdict(int)
        for answer in answers:
            if answer.answer_category:
                category_points[answer.answer_category] += 1
            elif answer.openness_priority:
                openness = answer.openness_priority
            else:
                self.fail('invalid_answer', id=answer.id)
        return openness, category_points

    def _get_top_learning_types(
        self, points: dict[AnswerCategory, int], openness: OpennessChoices
    ) -> QuerySet[LearningType]:
        categories = {
            'IT': ['typeProgramming', 'typeDesign', 'typeAnalytics'],
            'CREATIVITY': ['typeCreativity', 'typeArt', 'typeDesign', 'typeSoftSkills'],
            'SOCIAL_SCIENCE': ['typePsychology', 'typePedagogy', 'typeSport'],
            'ECONOMICS': ['typeFinance', 'typeManagement', 'typePO'],
            'ANALYTICS': ['typeAnalytics', 'typeDataScience', 'typeFinance'],
        }
        max_point = max([0, *points.values()])
        top_categories_with_types: dict[AnswerCategory, list[str]] = {
            category: categories[category] for category in points if points[category] == max_point
        }
        top_learning_types = sum(top_categories_with_types.values(), start=[])
        if openness == OpennessChoices.HIGH:
            result = LearningType.objects.exclude(name__in=top_learning_types)
        else:
            result = LearningType.objects.filter(name__in=top_learning_types)
        return result

    def _get_courses_url(self, learning_types: QuerySet[LearningType]) -> str:
        url = reverse('courses-list')
        learning_type_names = learning_types.values_list('name', flat=True)
        learning_type_filter_params = '&'.join([f'learning_types={type_}' for type_ in learning_type_names])
        return f'{url}?{learning_type_filter_params}'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'answer_category', 'openness_priority']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'text', 'has_multiple_answers', 'answers']


class AnswerUserSerializer(serializers.Serializer):
    answer_ids = serializers.ListField(child=serializers.IntegerField())
