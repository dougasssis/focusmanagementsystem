from django.core.management.base import BaseCommand
from django.utils import timezone
from focusbjj.models import Aluno, Graduation
from django.db.models import Max, F


class Command(BaseCommand):
    help = 'Fix graduation record timestamps to ensure proper attendance tracking'

    def add_arguments(self, parser):
        parser.add_argument('--student-id', type=str, help='ID of a specific student to fix (optional)')
        parser.add_argument('--fix', action='store_true', help='Apply fixes (otherwise just reports issues)')

    def handle(self, *args, **options):
        student_id = options.get('student_id')
        fix = options.get('fix', False)
        
        # Get students to process
        if student_id:
            try:
                students = [Aluno.objects.get(id=student_id)]
                self.stdout.write(f"Processing single student: {students[0].nome} {students[0].surname} (ID: {students[0].id})")
            except Aluno.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Student with ID {student_id} not found"))
                return
        else:
            students = Aluno.objects.all()
            self.stdout.write(f"Processing all students ({students.count()} total)")
        
        # Track statistics
        total_students = len(students)
        students_with_graduations = 0
        students_with_issues = 0
        students_fixed = 0
        
        # Process each student
        for student in students:
            graduations = Graduation.objects.filter(aluno=student).order_by('-time_stamp')
            
            if not graduations.exists():
                continue
                
            students_with_graduations += 1
            
            # Get the latest graduation by ID (most recently created)
            latest_by_id = graduations.order_by('-id').first()
            
            # Get the latest graduation by timestamp
            latest_by_timestamp = graduations.first()
            
            if latest_by_id.id != latest_by_timestamp.id:
                students_with_issues += 1
                self.stdout.write(f"\nIssue found for {student.nome} {student.surname} (ID: {student.id}):")
                self.stdout.write(f"  Latest by ID: #{latest_by_id.id}, {latest_by_id.belt} {latest_by_id.stripe}, {latest_by_id.time_stamp}")
                self.stdout.write(f"  Latest by timestamp: #{latest_by_timestamp.id}, {latest_by_timestamp.belt} {latest_by_timestamp.stripe}, {latest_by_timestamp.time_stamp}")
                
                if fix:
                    # Update the timestamp of the latest graduation by ID to be now
                    now = timezone.now()
                    latest_by_id.time_stamp = now
                    latest_by_id.save(update_fields=['time_stamp'])
                    self.stdout.write(self.style.SUCCESS(f"  Fixed: Updated timestamp for graduation #{latest_by_id.id} to {now}"))
                    students_fixed += 1
        
        # Summary
        self.stdout.write(f"\nSummary:")
        self.stdout.write(f"  Total students processed: {total_students}")
        self.stdout.write(f"  Students with graduation records: {students_with_graduations}")
        self.stdout.write(f"  Students with timestamp issues: {students_with_issues}")
        
        if fix:
            self.stdout.write(self.style.SUCCESS(f"  Students fixed: {students_fixed}"))
        elif students_with_issues > 0:
            self.stdout.write(self.style.WARNING(f"  Run with --fix to apply fixes")) 