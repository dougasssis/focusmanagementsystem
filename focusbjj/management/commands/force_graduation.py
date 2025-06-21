from django.core.management.base import BaseCommand
from focusbjj.models import Aluno, Graduation
from django.utils import timezone
from django.db import connection

class Command(BaseCommand):
    help = 'Directly graduates a student by ID using direct database access'

    def add_arguments(self, parser):
        parser.add_argument('student_id', type=str, help='Student ID to graduate')
        parser.add_argument('--belt', type=str, default='Blue', help='New belt (default: Blue)')
        parser.add_argument('--stripe', type=str, default='No Stripes', help='New stripe (default: No Stripes)')

    def handle(self, *args, **options):
        student_id = options['student_id']
        new_belt = options['belt']
        new_stripe = options['stripe']
        
        # Normalize belt format
        if " Belt" not in new_belt and new_belt in ["White", "Blue", "Purple", "Brown", "Black"]:
            new_belt = f"{new_belt} Belt"
        
        try:
            # Get the student
            student = Aluno.objects.get(id=student_id)
            self.stdout.write(f"Found student: {student.nome} {student.surname}")
            self.stdout.write(f"Current belt: {student.belt}, Current stripe: {student.stripe}")
            
            # Create graduation record
            graduation = Graduation.objects.create(
                aluno=student,
                belt=new_belt.replace(' Belt', ''),  # Store without 'Belt' in Graduation
                stripe=new_stripe,
                master="Force Graduation Command",
                time_stamp=timezone.now()
            )
            self.stdout.write(f"Created graduation record: ID={graduation.id}")
            
            # Update student directly with SQL
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE focusbjj_aluno SET belt = %s, stripe = %s WHERE id = %s",
                    [new_belt, new_stripe, student_id]
                )
                self.stdout.write(self.style.SUCCESS(f"Direct SQL update executed for student {student_id}"))
            
            # Verify update
            updated_student = Aluno.objects.get(id=student_id)
            self.stdout.write(f"Updated student belt: {updated_student.belt}, stripe: {updated_student.stripe}")
            
            if updated_student.belt == new_belt and updated_student.stripe == new_stripe:
                self.stdout.write(self.style.SUCCESS("Update successful!"))
            else:
                self.stdout.write(self.style.ERROR(f"Update verification failed! Student has belt={updated_student.belt}, stripe={updated_student.stripe}"))
                
        except Aluno.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Student with ID {student_id} not found!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}")) 