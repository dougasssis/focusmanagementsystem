from django.core.management.base import BaseCommand
from focusbjj.models import Aluno, Graduation
from django.db.models import Count


class Command(BaseCommand):
    help = 'Finds and fixes belt/stripe mismatches between student records and their latest graduation'

    def handle(self, *args, **options):
        # Get all students
        students = Aluno.objects.all()
        processed = 0
        updated = 0
        
        self.stdout.write(self.style.SUCCESS(f'Processing {students.count()} students...'))
        
        # Process each student
        for student in students:
            processed += 1
            
            # Get the latest graduation
            latest_graduation = Graduation.objects.filter(aluno=student).order_by('-time_stamp').first()
            
            if latest_graduation:
                # Normalize belt format
                grad_belt = latest_graduation.belt
                if " Belt" not in grad_belt and grad_belt in ["White", "Blue", "Purple", "Brown", "Black"]:
                    grad_belt = f"{grad_belt} Belt"
                    self.stdout.write(f"Normalized graduation belt: {latest_graduation.belt} → {grad_belt}")
                
                # Check if there's a mismatch
                belt_mismatch = student.belt != grad_belt
                stripe_mismatch = student.stripe != latest_graduation.stripe
                
                if belt_mismatch or stripe_mismatch:
                    # Create message about the mismatch
                    mismatch_str = []
                    if belt_mismatch:
                        mismatch_str.append(f"belt: '{student.belt}' → '{grad_belt}'")
                    if stripe_mismatch:
                        mismatch_str.append(f"stripe: '{student.stripe}' → '{latest_graduation.stripe}'")
                    
                    # Update student record
                    old_belt = student.belt
                    old_stripe = student.stripe
                    student.belt = grad_belt
                    student.stripe = latest_graduation.stripe
                    student.save()
                    updated += 1
                    
                    self.stdout.write(self.style.WARNING(
                        f"Updated student #{student.id} {student.nome} {student.surname}: {', '.join(mismatch_str)}"
                    ))
            
            # Show progress for large datasets
            if processed % 50 == 0:
                self.stdout.write(f"Processed {processed}/{students.count()} students...")
        
        # Final statistics
        self.stdout.write(self.style.SUCCESS(
            f"Completed! Processed {processed} students, updated {updated} mismatches."
        )) 