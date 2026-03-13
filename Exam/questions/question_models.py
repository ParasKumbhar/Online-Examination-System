from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms

class Question_DB(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    professor = models.ForeignKey(User, limit_choices_to={'groups__name': "Professor"}, on_delete=models.CASCADE, null=True)
    qno = models.AutoField(primary_key=True)
    question = models.CharField(max_length=500)  # Increased from 100 to 500
    optionA = models.CharField(max_length=200)
    optionB = models.CharField(max_length=200)
    optionC = models.CharField(max_length=200)
    optionD = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    max_marks = models.IntegerField(default=0)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['professor', 'difficulty']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'Question No.{self.qno}: {self.question} \t\t Options: \nA. {self.optionA} \nB.{self.optionB} \nC.{self.optionC} \nD.{self.optionD} '


class QForm(ModelForm):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    answer = forms.ChoiceField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], widget=forms.Select(attrs={'class': 'w-full rounded-lg border-slate-300 text-slate-900 focus:ring-primary focus:border-primary'}))
    difficulty = forms.ChoiceField(choices=DIFFICULTY_CHOICES, widget=forms.Select(attrs={'class': 'w-full rounded-lg border-slate-300 text-slate-900 focus:ring-primary focus:border-primary'}))

    class Meta:
        model = Question_DB
        fields = '__all__'
        exclude = ['qno', 'professor', 'created_at', 'updated_at']
        widgets = {
            'question': forms.Textarea(attrs = {'class':'w-full rounded-lg border-slate-300 text-slate-900 focus:ring-primary focus:border-primary', 'rows': 4}),
            'optionA': forms.TextInput(attrs = {'class':'w-full rounded-lg border-slate-300 text-slate-900 focus:ring-primary focus:border-primary'}),
            'optionB': forms.TextInput(attrs = {'class':'w-full rounded-lg border-slate-300 text-slate-900 focus:ring-primary focus:border-primary'}),
            'optionC': forms.TextInput(attrs = {'class':'w-full rounded-lg border-slate-300 text-slate-900 focus:ring-primary focus:border-primary'}),
            'optionD': forms.TextInput(attrs = {'class':'w-full rounded-lg border-slate-300 text-slate-900 focus:ring-primary focus:border-primary'}),
            'max_marks': forms.NumberInput(attrs = {'class':'w-full rounded-lg border-slate-300 text-slate-900 focus:ring-primary focus:border-primary', 'step': '1', 'min': '0'}),
        }