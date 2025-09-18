import random
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from focusbjj.models import Aluno, Graduation
from django.db import connection


class Command(BaseCommand):
    help = 'Tests the graduation functionality by updating a student belt/stripe and verifying the changes'

    def add_arguments(self, parser):
        parser.add_argument('--student-id', type=str, help='ID of the student to test with (optional)')
        parser.add_argument('--fix', action='store_true', help='Fix any inconsistencies found')
        parser.add_argument('--all', action='store_true', help='Test all students for belt inconsistencies')

    def handle(self, *args, **options):
        if options['all']:
            self.check_all_students(options['fix'])
            return
            
        # Get a student to test with
        student = None
        if options['student_id']:
            try:
                student = Aluno.objects.get(id=options['student_id'])
                self.stdout.write(f'Using student: {student.nome} {student.surname} (ID: {student.id})')
            except Aluno.DoesNotExist:
                raise CommandError(f'Student with ID {options["student_id"]} does not exist')
        else:
            # Get a random student
            students = list(Aluno.objects.all())
            if not students:
                raise CommandError('No students found in the database')
            student = random.choice(students)
            self.stdout.write(f'Randomly selected student: {student.nome} {student.surname} (ID: {student.id})')
        
        # Show current belt/stripe
        self.stdout.write(f'Current belt: {student.belt}, stripe: {student.stripe}')
        
        # Determine a new belt/stripe
        belts = ['White', 'Blue', 'Purple', 'Brown', 'Black']
        stripes = ['No Stripes', 'Iº Stripe', 'IIº Stripe', 'IIIº Stripe', 'IVº Stripe']
        
        # Choose a different belt
        current_belt_name = student.belt.replace(' Belt', '')
        new_belt_name = current_belt_name
        while new_belt_name == current_belt_name and len(belts) > 1:
            new_belt_name = random.choice(belts)
        
        # Choose a different stripe
        new_stripe = student.stripe
        while new_stripe == student.stripe and len(stripes) > 1:
            new_stripe = random.choice(stripes)
        
        self.stdout.write(f'New belt: {new_belt_name}, stripe: {new_stripe}')
        
        # Create a graduation record
        graduation = Graduation.objects.create(
            aluno=student,
            master='Test Command',
            belt=new_belt_name,
            stripe=new_stripe,
            time_stamp=timezone.now()
        )
        self.stdout.write(f'Created graduation record ID: {graduation.id}')
        
        # Normalize belt format
        new_belt_full = new_belt_name
        if " Belt" not in new_belt_full and new_belt_full in ["White", "Blue", "Purple", "Brown", "Black"]:
            new_belt_full = f"{new_belt_full} Belt"
            self.stdout.write(f'Normalized belt name: {new_belt_name} → {new_belt_full}')
        
        # Update using direct SQL (like in the view)
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE focusbjj_aluno SET belt = %s, stripe = %s WHERE id = %s",
                [new_belt_full, new_stripe, student.id]
            )
            self.stdout.write(f'Direct SQL update executed for student {student.id}')
        
        # Refresh from database
        student.refresh_from_db()
        self.stdout.write(f'After update - belt: {student.belt}, stripe: {student.stripe}')
        
        # Verify the update was successful
        if student.belt != new_belt_full or student.stripe != new_stripe:
            self.stdout.write(self.style.ERROR(
                f'Update failed! Expected belt={new_belt_full}, stripe={new_stripe}, but got belt={student.belt}, stripe={student.stripe}'
            ))
            
            if options['fix']:
                self.stdout.write('Attempting to fix with direct ORM update...')
                student.belt = new_belt_full
                student.stripe = new_stripe
                student.save(update_fields=['belt', 'stripe'])
                
                # Verify again
                student.refresh_from_db()
                if student.belt == new_belt_full and student.stripe == new_stripe:
                    self.stdout.write(self.style.SUCCESS('Fixed with ORM update!'))
                else:
                    self.stdout.write(self.style.ERROR('Failed to fix with ORM update!'))
        else:
            self.stdout.write(self.style.SUCCESS('Graduation test successful! Belt and stripe updated correctly.'))
    
    def check_all_students(self, fix=False):
        """Check all students for belt/stripe consistency compared to their graduation records"""
        self.stdout.write('Checking all students for belt/stripe consistency...')
        
        students = Aluno.objects.all()
        inconsistent_count = 0
        fixed_count = 0
        
        for student in students:
            # Get the latest graduation record
            latest_graduation = Graduation.objects.filter(aluno=student).order_by('-time_stamp').first()
            if not latest_graduation:
                self.stdout.write(f'Student {student.nome} {student.surname} (ID: {student.id}) has no graduation records.')
                continue
            
            # Check if the student's belt/stripe matches the latest graduation
            grad_belt = latest_graduation.belt
            if " Belt" not in grad_belt and grad_belt in ["White", "Blue", "Purple", "Brown", "Black"]:
                grad_belt = f"{grad_belt} Belt"
            
            if student.belt != grad_belt or student.stripe != latest_graduation.stripe:
                inconsistent_count += 1
                self.stdout.write(self.style.WARNING(
                    f'Inconsistency found for {student.nome} {student.surname} (ID: {student.id}):\n'
                    f'  Current: belt={student.belt}, stripe={student.stripe}\n'
                    f'  Graduation: belt={grad_belt}, stripe={latest_graduation.stripe}'
                ))
                
                if fix:
                    # Fix the inconsistency
                    self.stdout.write(f'Fixing inconsistency for student {student.id}...')
                    student.belt = grad_belt
                    student.stripe = latest_graduation.stripe
                    student.save(update_fields=['belt', 'stripe'])
                    fixed_count += 1
        
        if inconsistent_count == 0:
            self.stdout.write(self.style.SUCCESS('All students have consistent belt/stripe information.'))
        else:
            if fix:
                self.stdout.write(self.style.SUCCESS(f'Fixed {fixed_count} out of {inconsistent_count} inconsistencies.'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Found {inconsistent_count} inconsistencies. Run with --fix to correct them.'
                )) 