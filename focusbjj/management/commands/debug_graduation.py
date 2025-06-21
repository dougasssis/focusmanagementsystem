from django.core.management.base import BaseCommand
from django.utils import timezone
from focusbjj.models import Aluno, Graduation
from focusbjj.forms import GraduateForm
from django.db import connection


class Command(BaseCommand):
    help = 'Debugs the graduation form submission process'

    def add_arguments(self, parser):
        parser.add_argument('student_id', type=str, help='ID of the student to test graduation')
        parser.add_argument('--belt', type=str, default='Blue', help='New belt color')
        parser.add_argument('--stripe', type=str, default='No Stripes', help='New stripe')

    def handle(self, *args, **options):
        student_id = options['student_id']
        belt = options['belt']
        stripe = options['stripe']
        
        try:
            student = Aluno.objects.get(id=student_id)
        except Aluno.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Student with ID {student_id} not found"))
            return
        
        self.stdout.write(f"Student: {student.nome} {student.surname}")
        self.stdout.write(f"Current belt: {student.belt}, stripe: {student.stripe}")
        
        # Create form data
        form_data = {
            'belt': belt,
            'stripe': stripe,
            'master': 'Debug Test',
            'time_stamp': timezone.now().date()
        }
        
        self.stdout.write("\nForm data:")
        for key, value in form_data.items():
            self.stdout.write(f"  {key}: {value}")
        
        # Initialize the form
        form = GraduateForm(data=form_data)
        
        # Check form validity
        if form.is_valid():
            self.stdout.write(self.style.SUCCESS("\nForm is valid!"))
            
            # Create graduation record manually
            graduation = Graduation(
                aluno=student,
                master=form.cleaned_data['master'],
                belt=form.cleaned_data['belt'],
                stripe=form.cleaned_data['stripe'],
                time_stamp=form.cleaned_data['time_stamp']
            )
            graduation.save()
            self.stdout.write(f"Created graduation record ID: {graduation.id}")
            
            # Normalize belt format
            new_belt = form.cleaned_data['belt']
            if " Belt" not in new_belt and new_belt in ["White", "Blue", "Purple", "Brown", "Black"]:
                new_belt = f"{new_belt} Belt"
            
            # Update student using direct SQL
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE focusbjj_aluno SET belt = %s, stripe = %s WHERE id = %s",
                    [new_belt, form.cleaned_data['stripe'], student_id]
                )
            
            # Refresh student from database
            student.refresh_from_db()
            self.stdout.write(f"After update - belt: {student.belt}, stripe: {student.stripe}")
            
            if student.belt == new_belt and student.stripe == form.cleaned_data['stripe']:
                self.stdout.write(self.style.SUCCESS("Student record updated successfully!"))
            else:
                self.stdout.write(self.style.ERROR("Student record not updated correctly!"))
        else:
            self.stdout.write(self.style.ERROR("\nForm is invalid!"))
            self.stdout.write("Errors:")
            for field, errors in form.errors.items():
                self.stdout.write(f"  {field}: {', '.join(errors)}") 