from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from focusbjj.models import Aluno, Graduation
from focusbjj.forms import GraduateForm
from django.db import connection


class Command(BaseCommand):
    help = 'Performs a full student graduation simulation'

    def add_arguments(self, parser):
        parser.add_argument('student_id', type=str, help='ID of the student to graduate')
        parser.add_argument('--belt', type=str, default='Purple', help='New belt color (default: Purple)')
        parser.add_argument('--stripe', type=str, default='Iº Stripe', help='New stripe (default: Iº Stripe)')
        parser.add_argument('--master', type=str, default='Test Professor', help='Graduating professor name')

    def handle(self, *args, **options):
        student_id = options['student_id']
        belt = options['belt']
        stripe = options['stripe']
        master = options['master']
        
        try:
            student = Aluno.objects.get(id=student_id)
        except Aluno.DoesNotExist:
            raise CommandError(f"Student with ID {student_id} not found")
        
        self.stdout.write(f"STEP 1: Identified student {student.nome} {student.surname} (ID: {student.id})")
        self.stdout.write(f"Current belt: {student.belt}, stripe: {student.stripe}")
        
        # Initialize form with data
        form_data = {
            'belt': belt,
            'stripe': stripe,
            'master': master,
            'time_stamp': timezone.now().date()
        }
        
        self.stdout.write(f"\nSTEP 2: Preparing form data: {form_data}")
        
        # Create the form
        form = GraduateForm(data=form_data)
        
        # Validate the form
        self.stdout.write("\nSTEP 3: Validating form")
        if not form.is_valid():
            self.stdout.write(self.style.ERROR(f"Form validation failed: {form.errors}"))
            return
        
        self.stdout.write(self.style.SUCCESS("Form validated successfully"))
        
        # Create graduation record
        self.stdout.write("\nSTEP 4: Creating graduation record")
        try:
            graduation = Graduation(
                aluno=student,
                master=form.cleaned_data['master'],
                belt=form.cleaned_data['belt'],
                stripe=form.cleaned_data['stripe'],
                time_stamp=timezone.now()
            )
            graduation.save()
            self.stdout.write(self.style.SUCCESS(f"Created graduation record ID: {graduation.id}, Time: {graduation.time_stamp}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to create graduation record: {str(e)}"))
            return
        
        # Normalize belt format
        self.stdout.write("\nSTEP 5: Normalizing belt format")
        new_belt = graduation.belt
        if " Belt" not in new_belt and new_belt in ["White", "Blue", "Purple", "Brown", "Black"]:
            new_belt = f"{new_belt} Belt"
            self.stdout.write(f"Normalized belt name: {graduation.belt} → {new_belt}")
        
        # Update student's belt and stripe using direct SQL
        self.stdout.write("\nSTEP 6: Updating student record using SQL")
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE focusbjj_aluno SET belt = %s, stripe = %s WHERE id = %s",
                    [new_belt, graduation.stripe, student.id]
                )
                self.stdout.write(f"SQL executed: UPDATE focusbjj_aluno SET belt = '{new_belt}', stripe = '{graduation.stripe}' WHERE id = '{student.id}'")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to execute SQL: {str(e)}"))
            return
        
        # Verify the update
        self.stdout.write("\nSTEP 7: Verifying update")
        # Refresh from database
        student.refresh_from_db()
        self.stdout.write(f"Updated student record - belt: {student.belt}, stripe: {student.stripe}")
        
        if student.belt != new_belt or student.stripe != graduation.stripe:
            self.stdout.write(self.style.ERROR(
                "Update verification failed! " +
                f"Expected belt={new_belt}, stripe={graduation.stripe}, " +
                f"got belt={student.belt}, stripe={student.stripe}"
            ))
            
            # Try ORM update as fallback
            self.stdout.write("\nSTEP 8: Attempting ORM update as fallback")
            student.belt = new_belt
            student.stripe = graduation.stripe
            student.save(update_fields=['belt', 'stripe'])
            
            # Verify again
            student.refresh_from_db()
            if student.belt == new_belt and student.stripe == graduation.stripe:
                self.stdout.write(self.style.SUCCESS("Fixed with ORM update!"))
            else:
                self.stdout.write(self.style.ERROR("Failed to fix with ORM update!"))
        else:
            self.stdout.write(self.style.SUCCESS("\nGraduation completed successfully!"))
            self.stdout.write(f"Student {student.nome} {student.surname} (ID: {student.id}) is now:")
            self.stdout.write(f"Belt: {student.belt}, Stripe: {student.stripe}")
            self.stdout.write(f"Graduated by: {graduation.master}")
            self.stdout.write(f"Date: {graduation.time_stamp}") 