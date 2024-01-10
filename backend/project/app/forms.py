from django import forms
from .models import Subject, Question

class SubjectCreateForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Subject name'}),
        }
 
class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        widgets = {
            'name': forms.Select(attrs={'class': 'select'}),
            'en_lang': forms.TextInput(attrs={'class': 'input', 'placeholder': 'English question'}),
            'ru_lang': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Russian question'}),
            'en_answer': forms.Textarea(attrs={'class': 'textarea is-primary', 'placeholder': 'Type english answer'}),
            'ru_answer': forms.Textarea(attrs={'class': 'textarea is-primary', 'placeholder': 'Type russian answer'}),
        }