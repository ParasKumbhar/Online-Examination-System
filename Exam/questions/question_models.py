from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from django.core.validators import FileExtensionValidator

class Question_DB(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    professor = models.ForeignKey(User, limit_choices_to={'groups__name': "Professor"}, on_delete=models.CASCADE, null=True)
    qno = models.AutoField(primary_key=True)
    question = models.CharField(max_length=500, blank=True, null=True)  # Allow null text when image exists
    question_image = models.ImageField(upload_to='questions/', blank=True, null=True,
                                       validators=[FileExtensionValidator(['jpg','jpeg','png','gif'])])
    optionA = models.CharField(max_length=200, blank=True, null=True)
    optionA_image = models.ImageField(upload_to='options/', blank=True, null=True,
                                      validators=[FileExtensionValidator(['jpg','jpeg','png','gif'])])
    optionB = models.CharField(max_length=200, blank=True, null=True)
    optionB_image = models.ImageField(upload_to='options/', blank=True, null=True,
                                      validators=[FileExtensionValidator(['jpg','jpeg','png','gif'])])
    optionC = models.CharField(max_length=200, blank=True, null=True)
    optionC_image = models.ImageField(upload_to='options/', blank=True, null=True,
                                      validators=[FileExtensionValidator(['jpg','jpeg','png','gif'])])
    optionD = models.CharField(max_length=200, blank=True, null=True)
    optionD_image = models.ImageField(upload_to='options/', blank=True, null=True,
                                      validators=[FileExtensionValidator(['jpg','jpeg','png','gif'])])
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
            'question': forms.Textarea(attrs = {'class':'w-full max-w-2xl rounded-lg border-slate-300 text-slate-900 focus:ring-primary focus:border-primary pr-3', 'rows': 4, 'placeholder': 'Enter question text (or upload image)'}),
            'optionA': forms.TextInput(attrs = {'class':'w-full max-w-lg rounded-lg border-slate-300 text-slate-900 focus:ring-primary focus:border-primary pr-3', 'placeholder': 'Option A text'}),
            'optionB': forms.TextInput(attrs = {'class':'w-full max-w-lg rounded-lg border-slate-300 text-slate-900 focus:ring-primary focus:border-primary pr-3', 'placeholder': 'Option B text'}),
            'optionC': forms.TextInput(attrs = {'class':'w-full max-w-lg rounded-lg border-slate-300 text-slate-900 focus:ring-primary focus:border-primary pr-3', 'placeholder': 'Option C text'}),
            'optionD': forms.TextInput(attrs = {'class':'w-full max-w-lg rounded-lg border-slate-300 text-slate-900 focus:ring-primary focus:border-primary pr-3', 'placeholder': 'Option D text'}),
            'max_marks': forms.NumberInput(attrs = {'class':'w-full rounded-lg border-slate-300 text-slate-900 focus:ring-primary focus:border-primary', 'step': '1', 'min': '0'}),
            'question_image': forms.ClearableFileInput(attrs={'class': 'hidden', 'accept':'image/*'}),
            'optionA_image': forms.ClearableFileInput(attrs={'class': 'hidden', 'accept':'image/*'}),
            'optionB_image': forms.ClearableFileInput(attrs={'class': 'hidden', 'accept':'image/*'}),
            'optionC_image': forms.ClearableFileInput(attrs={'class': 'hidden', 'accept':'image/*'}),
            'optionD_image': forms.ClearableFileInput(attrs={'class': 'hidden', 'accept':'image/*'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        q_text = cleaned_data.get('question')
        q_img = cleaned_data.get('question_image')

        if not q_text and not q_img:
            raise forms.ValidationError('Question must contain text or an image.')

        for opt in ['A', 'B', 'C', 'D']:
            text = cleaned_data.get(f'option{opt}')
            img = cleaned_data.get(f'option{opt}_image')
            if not text and not img:
                raise forms.ValidationError(f'Option {opt} must contain text or an image.')

        answer = cleaned_data.get('answer')
        if answer not in ['A', 'B', 'C', 'D']:
            raise forms.ValidationError('Valid correct answer is required (A, B, C, D).')

        return cleaned_data