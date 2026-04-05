# Generated migration to create default groups with permissions

from django.db import migrations
from django.core.management import call_command


def create_groups(apps, schema_editor):
    """Create default groups with proper permissions"""
    call_command('create_groups', verbosity=0)


def delete_groups(apps, schema_editor):
    """Remove default groups (rollback)"""
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Professor', 'Student']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_otpsession_otpattempt_and_more'),
    ]

    operations = [
        migrations.RunPython(create_groups, delete_groups),
    ]
