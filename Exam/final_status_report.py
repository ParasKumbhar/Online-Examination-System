#!/usr/bin/env python
"""
Final Verification and Status Report
Checks complete groups and permissions implementation
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'examProject.settings')
django.setup()

from django.contrib.auth.models import Group, Permission, User
from django.core.management import call_command


def print_divider(char="="):
    print(char * 80)


def status_report():
    print_divider()
    print("GROUPS AND PERMISSIONS - FINAL STATUS REPORT")
    print_divider()
    
    # Check if groups exist
    print("\n1. GROUP STATUS")
    print("-" * 80)
    
    prof_exists = Group.objects.filter(name='Professor').exists()
    student_exists = Group.objects.filter(name='Student').exists()
    
    print(f"Professor group: {'FOUND' if prof_exists else 'MISSING'}")
    print(f"Student group: {'FOUND' if student_exists else 'MISSING'}")
    
    if not (prof_exists and student_exists):
        print("\n[ACTION] Groups not found. Run: python manage.py migrate")
        return False
    
    prof = Group.objects.get(name='Professor')
    student = Group.objects.get(name='Student')
    
    prof_count = prof.permissions.count()
    student_count = student.permissions.count()
    
    print(f"\nProfessor permissions: {prof_count}/81")
    print(f"Student permissions: {student_count}/49")
    
    prof_ok = prof_count == 81
    student_ok = student_count == 49
    
    print(f"Professor status: {'OK' if prof_ok else 'INCOMPLETE'}")
    print(f"Student status: {'OK' if student_ok else 'INCOMPLETE'}")
    
    # Check user group assignments
    print("\n2. USER GROUP ASSIGNMENTS")
    print("-" * 80)
    
    try:
        prof_users = User.objects.filter(groups=prof).count()
        student_users = User.objects.filter(groups=student).count()
        
        print(f"Users in Professor group: {prof_users}")
        print(f"Users in Student group: {student_users}")
        print(f"Total users with groups: {User.objects.filter(groups__isnull=False).distinct().count()}")
    except Exception as e:
        print(f"Error checking user assignments: {e}")
    
    # Check critical permissions exist
    print("\n3. CRITICAL PERMISSIONS CHECK")
    print("-" * 80)
    
    critical_perms = [
        ('questions', 'add_question_db'),
        ('questions', 'change_question_paper'),
        ('course', 'view_course'),
        ('student', 'view_studentinfo'),
    ]
    
    all_exist = True
    for app, perm in critical_perms:
        exists = Permission.objects.filter(
            codename=perm,
            content_type__app_label=app
        ).exists()
        status = "OK" if exists else "MISSING"
        print(f"  {app}.{perm}: {status}")
        if not exists:
            all_exist = False
    
    # Final summary
    print("\n" + "=" * 80)
    print("FINAL STATUS")
    print("=" * 80)
    
    all_ok = prof_ok and student_ok and all_exist
    
    if all_ok:
        print("STATUS: OK")
        print("")
        print("All groups are properly configured:")
        print("  [OK] Professor group with 81 permissions")
        print("  [OK] Student group with 49 permissions")
        print("  [OK] All critical permissions present")
        print("")
        print("NEXT STEPS:")
        print("  1. Go to Django Admin: http://localhost:8000/admin/")
        print("  2. Navigate to Users")
        print("  3. Select a user and assign them to groups")
        print("  4. Save")
        print("")
        print("VERIFICATION:")
        print("  Run: python verify_groups.py")
        print("")
        return True
    else:
        print("STATUS: INCOMPLETE")
        print("")
        if not prof_ok:
            print(f"  [ERROR] Professor group has {prof_count}/81 permissions")
        if not student_ok:
            print(f"  [ERROR] Student group has {student_count}/49 permissions")
        if not all_exist:
            print("  [ERROR] Some critical permissions are missing")
        print("")
        print("FIX:")
        print("  Run: python manage.py migrate")
        print("  Then: python manage.py create_groups")
        print("")
        return False


if __name__ == '__main__':
    try:
        success = status_report()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
