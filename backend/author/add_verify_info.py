from author.models import AuthorType, FIZAuthor, FOPAuthor, LLCAuthor, VerificationProfileType
from author.serializers import FIZAuthorSerializer, FOPAuthorSerializer, LLCAuthorSerializer
from rest_framework.exceptions import ValidationError


def update_verify_fields(profile, full_data):
    if not full_data.get('verify_fields'):
        return

    if profile.author_type == AuthorType.INDIVIDUAL:
        fiz_author = getattr(profile, 'fiz_author', None)
        if not fiz_author:
            fiz_author = FIZAuthor.objects.create(author=profile)

        fiz_author_serializer = FIZAuthorSerializer(fiz_author, data=full_data['verify_fields'], partial=True)
        fiz_author_serializer.is_valid(raise_exception=True)
        fiz_author_serializer.save()
        profile.verification_status = VerificationProfileType.ON_VERIFICATION
        profile.save()

    elif profile.author_type == AuthorType.INDIVIDUAL_ENTREPRENEUR:
        fop_author = getattr(profile, 'fop_author', None)
        if not fop_author:
            fop_author = FOPAuthor.objects.create(author=profile)

        fop_author_serializer = FOPAuthorSerializer(fop_author, data=full_data['verify_fields'], partial=True)
        fop_author_serializer.is_valid(raise_exception=True)
        fop_author_serializer.save()
        profile.verification_status = VerificationProfileType.ON_VERIFICATION
        profile.save()

    elif profile.author_type == AuthorType.ORGANIZATION:
        llc_author = getattr(profile, 'llc_author', None)
        if not llc_author:
            llc_author = LLCAuthor.objects.create(author=profile)

        llc_author_serializer = LLCAuthorSerializer(llc_author, data=full_data['verify_fields'], partial=True)
        llc_author_serializer.is_valid(raise_exception=True)
        llc_author_serializer.save()
        profile.verification_status = VerificationProfileType.ON_VERIFICATION
        profile.save()

    else:
        raise ValidationError({"error": "Неверный тип автора."})

    return
