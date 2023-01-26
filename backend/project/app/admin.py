from django.contrib import admin
from . models import Subject, Question

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):

    search_fields = ('en_lang', 'ru_lang')
