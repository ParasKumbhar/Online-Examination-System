"""
Exam Assignment Models
Manages which students can access which exams
"""

from django.db import models
from django.contrib.auth.models import User
from .models import Exam_Model
import logging

logger = logging.getLogger('app')


class ExamAssignment(models.Model):
    """
    Tracks which students are assigned to which exams.
    Allows professors to restrict exam access to specific students or batches.
    """

    ASSIGNMENT_TYPE = [
        ('individual', 'Individual Student'),
        ('batch', 'Entire Batch/Class'),
        ('public', 'All Students'),
    ]

    exam = models.ForeignKey(Exam_Model, on_delete=models.CASCADE, related_name='assignments')
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={'groups__name': 'Student'},
        related_name='exam_assignments'
    )
    batch_name = models.CharField(max_length=100, blank=True, help_text="e.g., CSE-2024-A")
    assignment_type = models.CharField(max_length=20, choices=ASSIGNMENT_TYPE, default='public')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('exam', 'student', 'batch_name')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['exam', 'is_active']),
            models.Index(fields=['student']),
            models.Index(fields=['batch_name']),
        ]
        verbose_name = 'Exam Assignment'
        verbose_name_plural = 'Exam Assignments'

    def __str__(self):
        if self.assignment_type == 'individual':
            return f"{self.exam.name} → {self.student.username}"
        elif self.assignment_type == 'batch':
            return f"{self.exam.name} → Batch: {self.batch_name}"
        else:
            return f"{self.exam.name} → All Students (Public)"

    @staticmethod
    def is_exam_assigned_to_student(exam, student):
        """
        Check if a student has access to an exam
        """
        # Check if exam has any assignments
        assignments_exist = ExamAssignment.objects.filter(exam=exam, is_active=True).exists()

        if not assignments_exist:
            # No assignments = open to all students
            return True

        # Check if student has direct assignment
        direct_assignment = ExamAssignment.objects.filter(
            exam=exam,
            student=student,
            assignment_type='individual',
            is_active=True
        ).exists()

        if direct_assignment:
            return True

        # Check if exam is assigned to student's batch
        # This would require storing batch info in StudentInfo model
        # For now, we'll just check individual and public assignments
        public_assignment = ExamAssignment.objects.filter(
            exam=exam,
            assignment_type='public',
            is_active=True
        ).exists()

        return public_assignment

    def deactivate(self):
        """Soft delete - deactivate assignment instead of deleting"""
        self.is_active = False
        self.save()
        logger.info(f"Exam assignment deactivated: {self.exam.name} → {self.student or self.batch_name}")
