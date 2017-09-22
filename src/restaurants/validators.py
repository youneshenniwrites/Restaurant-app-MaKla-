from django.core.exceptions import ValidationError

CATEGORIES = ['Kebab', 'Tacos', 'Chinese', 'Thai', 'Burgers', 'Pizza', 'Sandwichs', 'Sushi']


def validate_category(value):
    cat = value.capitalize()
    if not value in CATEGORIES and not cat in CATEGORIES:
        raise ValidationError(f"{value} is not a valid category")