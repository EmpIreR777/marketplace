from django.core.management.base import BaseCommand
from author.models import Author, AuthorType, LLCAuthor, FIZAuthor, FOPAuthor


class Command(BaseCommand):
    help = "Создаёт записи LLCAuthor для всех авторов-организаций, у которых их нет"

    def handle(self, *args, **options):
        authors_without_llc = Author.objects.filter(author_type=AuthorType.ORGANIZATION, llc_author__isnull=True)
        authors_without_fop = Author.objects.filter(author_type=AuthorType.INDIVIDUAL_ENTREPRENEUR, fop_author__isnull=True)
        authors_without_fiz = Author.objects.filter(author_type=AuthorType.INDIVIDUAL, fiz_author__isnull=True)
        count_llc = 0
        count_fop = 0
        count_fiz = 0

        for author in authors_without_llc:
            LLCAuthor.objects.create(author=author)
            count_llc += 1
            
        for author in authors_without_fop:
            FOPAuthor.objects.create(author=author)
            count_fop += 1

        for author in authors_without_fiz:
            FIZAuthor.objects.create(author=author)
            count_fiz += 1

        self.stdout.write(self.style.SUCCESS(f"Создано {count_llc} LLCAuthor для организаций, "
                                             f"{count_fop} LLCAuthor для ФОП, {count_fiz} LLCAuthor для ФИЗ"))