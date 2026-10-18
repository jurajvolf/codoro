from django.contrib import admin
from .models import Module, Lesson, Exercise, TestCase, Submission, QuizQuestion, LessonProgress

admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Exercise)
admin.site.register(TestCase)
admin.site.register(Submission)
admin.site.register(QuizQuestion)
admin.site.register(LessonProgress)