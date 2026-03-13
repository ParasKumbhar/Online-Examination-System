from django.contrib import admin
from .models import Exam_Model
from .questionpaper_models import Question_Paper
from .question_enhancements import QuestionTag
from .anticheating_models import ExamFocusLog, FocusLossEvent, ExamSecurityAlert
from .exam_assignment_models import ExamAssignment

admin.site.register(QuestionTag)
admin.site.register(Question_Paper)
@admin.register(Exam_Model)
class ExamModelAdmin(admin.ModelAdmin):
    # Hide the internal soft-delete flag from the admin form
    exclude = ('is_active',)


@admin.register(ExamFocusLog)
class ExamFocusLogAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'focus_loss_count', 'is_suspicious', 'last_focus_loss_time']
    list_filter = ['is_suspicious', 'created_at', 'exam']
    search_fields = ['student__username', 'exam__name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Exam Info', {
            'fields': ('student', 'exam')
        }),
        ('Focus Loss Data', {
            'fields': ('focus_loss_count', 'max_focus_losses', 'last_focus_loss_time')
        }),
        ('Security', {
            'fields': ('is_suspicious', 'reason')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(FocusLossEvent)
class FocusLossEventAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'event_type', 'timestamp']
    list_filter = ['event_type', 'timestamp', 'exam']
    search_fields = ['student__username', 'exam__name']
    readonly_fields = ['timestamp', 'student', 'exam', 'event_type']

    fieldsets = (
        ('Event Info', {
            'fields': ('student', 'exam', 'event_type', 'timestamp')
        }),
        ('Client Data', {
            'fields': ('browser_timestamp', 'ip_address')
        }),
        ('Browser Info', {
            'fields': ('user_agent',),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return False  # Events are recorded by the system only


@admin.register(ExamSecurityAlert)
class ExamSecurityAlertAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'alert_type', 'level', 'created_at', 'is_resolved']
    list_filter = ['level', 'created_at', 'exam', 'is_resolved']
    search_fields = ['student__username', 'exam__name', 'alert_type']
    readonly_fields = ['created_at']

    fieldsets = (
        ('Alert Info', {
            'fields': ('student', 'exam', 'alert_type', 'level')
        }),
        ('Details', {
            'fields': ('message', 'is_resolved')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ExamAssignment)
class ExamAssignmentAdmin(admin.ModelAdmin):
    list_display = ['exam', 'assignment_type', 'student', 'batch_name', 'is_active', 'created_at']
    list_filter = ['assignment_type', 'is_active', 'created_at', 'exam']
    search_fields = ['student__username', 'exam__name', 'batch_name']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Assignment Details', {
            'fields': ('exam', 'assignment_type')
        }),
        ('Individual Assignment', {
            'fields': ('student',),
            'classes': ('collapse',),
            'description': 'Assign exam to a specific student'
        }),
        ('Batch Assignment', {
            'fields': ('batch_name',),
            'classes': ('collapse',),
            'description': 'Assign exam to an entire batch/class (e.g., CSE-2024-A)'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['deactivate_assignments']

    def deactivate_assignments(self, request, queryset):
        """Admin action to deactivate multiple assignments at once"""
        count = 0
        for assignment in queryset:
            assignment.deactivate()
            count += 1
        self.message_user(request, f"{count} assignment(s) deactivated successfully")

    deactivate_assignments.short_description = "Deactivate selected assignments"