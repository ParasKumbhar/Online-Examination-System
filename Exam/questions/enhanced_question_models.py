"""
Enhanced Question Management Models
Adds difficulty, search, versioning, and CSV support
"""

from django.db import models
from django.contrib.auth.models import User
import csv
import logging

logger = logging.getLogger('app')


class QuestionDifficultyManager(models.Manager):
    """Custom manager for difficulty-based question filtering"""

    def easy(self):
        return self.filter(difficulty='easy')

    def medium(self):
        return self.filter(difficulty='medium')

    def hard(self):
        return self.filter(difficulty='hard')

    def by_difficulty(self, difficulty):
        return self.filter(difficulty=difficulty)


class QuestionVersion(models.Model):
    """Track question revisions and versions"""

    CHANGE_TYPE = [
        ('CREATED', 'Question Created'),
        ('EDITED', 'Question Edited'),
        ('DELETED', 'Question Deleted'),
        ('RESTORED', 'Question Restored'),
    ]

    question_id = models.IntegerField()  # Original question ID
    professor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    question_text = models.CharField(max_length=500)
    optionA = models.CharField(max_length=200)
    optionB = models.CharField(max_length=200)
    optionC = models.CharField(max_length=200)
    optionD = models.CharField(max_length=200)
    answer = models.CharField(max_length=10)
    max_marks = models.IntegerField()
    difficulty = models.CharField(max_length=10)
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPE)
    change_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['question_id', 'created_at']),
            models.Index(fields=['professor']),
        ]

    def __str__(self):
        return f"v{self.id}: {self.change_type} - Q{self.question_id}"


class QuestionDuplicate(models.Model):
    """Detect and track duplicate questions"""

    original_question_id = models.IntegerField()
    duplicate_question_id = models.IntegerField()
    similarity_score = models.FloatField(default=0.0)  # 0-1
    is_resolved = models.BooleanField(default=False)
    resolution = models.CharField(
        max_length=50,
        choices=[
            ('MERGE', 'Merged'),
            ('DELETE', 'Deleted duplicate'),
            ('BOTH_VALID', 'Both valid'),
        ],
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-similarity_score']
        unique_together = ('original_question_id', 'duplicate_question_id')

    def __str__(self):
        return f"Duplicate: Q{self.original_question_id} ≈ Q{self.duplicate_question_id} ({self.similarity_score:.2%})"


def calculate_text_similarity(text1, text2):
    """
    Simple text similarity calculation using word overlap
    Returns value between 0 and 1
    """
    from difflib import SequenceMatcher

    # Normalize text
    text1 = text1.lower().strip()
    text2 = text2.lower().strip()

    # Use SequenceMatcher for string similarity
    matcher = SequenceMatcher(None, text1, text2)
    return matcher.ratio()


class QuestionCSVImporter:
    """Handle CSV import/export for questions"""

    @staticmethod
    def export_to_csv(professor, filename=None):
        """
        Export all questions from a professor to CSV file
        """
        from questions.question_models import Question_DB

        try:
            questions = Question_DB.objects.filter(professor=professor)

            if filename is None:
                from django.utils import timezone
                filename = f"questions_{professor.username}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.csv"

            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                # Header
                writer.writerow([
                    'Question Text',
                    'Option A',
                    'Option B',
                    'Option C',
                    'Option D',
                    'Correct Answer',
                    'Max Marks',
                    'Difficulty'
                ])

                # Data rows
                for q in questions:
                    writer.writerow([
                        q.question,
                        q.optionA,
                        q.optionB,
                        q.optionC,
                        q.optionD,
                        q.answer,
                        q.max_marks,
                        getattr(q, 'difficulty', 'medium'),
                    ])

            logger.info(f"Exported {questions.count()} questions to {filename}")
            return True, filename

        except Exception as e:
            logger.error(f"Error exporting questions: {str(e)}")
            return False, str(e)

    @staticmethod
    def import_from_csv(professor, csv_file):
        """
        Import questions from CSV file
        CSV format:
        Question Text,Option A,Option B,Option C,Option D,Correct Answer,Max Marks,Difficulty
        """
        from questions.question_models import Question_DB
        from django.db import transaction

        try:
            imported_count = 0
            errors = []

            with transaction.atomic():
                reader = csv.DictReader(csv_file)

                for i, row in enumerate(reader, start=2):  # start=2 because row 1 is header
                    try:
                        # Validate required fields
                        if not all(row.get(field) for field in ['Question Text', 'Option A', 'Option B', 'Option C', 'Option D', 'Correct Answer']):
                            errors.append(f"Row {i}: Missing required field")
                            continue

                        # Validate answer is A-D
                        answer = row.get('Correct Answer', '').upper()
                        if answer not in ['A', 'B', 'C', 'D']:
                            errors.append(f"Row {i}: Answer must be A, B, C, or D")
                            continue

                        # Validate marks is integer
                        try:
                            max_marks = int(row.get('Max Marks', 1))
                        except ValueError:
                            errors.append(f"Row {i}: Max Marks must be a number")
                            continue

                        # Create question
                        question = Question_DB.objects.create(
                            professor=professor,
                            question=row['Question Text'],
                            optionA=row['Option A'],
                            optionB=row['Option B'],
                            optionC=row['Option C'],
                            optionD=row['Option D'],
                            answer=answer,
                            max_marks=max_marks,
                        )

                        # Save difficulty if provided
                        if 'Difficulty' in row and row['Difficulty'] in ['easy', 'medium', 'hard']:
                            question.difficulty = row['Difficulty']
                            question.save()

                        imported_count += 1

                    except Exception as e:
                        errors.append(f"Row {i}: {str(e)}")

            logger.info(f"Imported {imported_count} questions for {professor.username}")
            return imported_count, errors

        except Exception as e:
            logger.error(f"Error importing questions: {str(e)}")
            return 0, [str(e)]
