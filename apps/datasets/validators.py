from django.core.exceptions import ValidationError

ALLOWED_EXTENSIONS = [
    '.csv',
    '.xlsx',
]

def validate_dataset_file(file):
    filename = file.name.lower()

    if not any(
        filename.endswith(ext)
        for ext in ALLOWED_EXTENSIONS
    ):
        raise ValidationError(
            f"Unsupported file type. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )