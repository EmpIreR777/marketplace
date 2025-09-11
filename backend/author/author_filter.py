import django_filters
from author.models import Author, AuthorType


class AuthorFilter(django_filters.FilterSet):
    author_type = django_filters.ChoiceFilter(choices=AuthorType.choices, label='Author Type')

    class Meta:
        model = Author
        fields = ['author_type']
