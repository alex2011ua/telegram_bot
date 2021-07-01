from django.forms import ModelForm
from .models import Author


class AuthorCreationForm(ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
