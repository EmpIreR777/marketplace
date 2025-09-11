import os


def profile_document_path(instance, filename):
    return os.path.join('documents', f'profile_{instance.author_id }', filename)

def logos_document_path(instance, file):
    return f"author/logo_images/{instance.id}/{file}"
