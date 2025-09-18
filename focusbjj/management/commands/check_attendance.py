from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from focusbjj.models import Aluno, Graduation, GetAttendance
from focusbjj.templatetags.attendance_tags import new_attendance, get_count_att_aluno


class Command(BaseCommand):
    help = 'Check attendance information for a student, including classes since last graduation'

    def add_arguments(self, parser):
        parser.add_argument('student_id', type=str, help='ID of the student to check')

    def handle(self, *args, **options):
        student_id = options['student_id']
        
        try:
            student = Aluno.objects.get(id=student_id)
        except Aluno.DoesNotExist:
            raise CommandError(f"Student with ID {student_id} not found")
        
        self.stdout.write(f"Student: {student.nome} {student.surname} (ID: {student.id})")
        self.stdout.write(f"Current belt: {student.belt}, stripe: {student.stripe}")
        
        # Get all attendance records
        attendance_records = GetAttendance.objects.filter(aluno=student).order_by('attendance')
        total_classes = attendance_records.count()
        
        self.stdout.write(f"\nTotal classes attended: {total_classes}")
        
        # Get all graduation records
        graduation_records = Graduation.objects.filter(aluno=student).order_by('-time_stamp')
        
        if graduation_records.exists():
            latest_graduation = graduation_records.first()
            self.stdout.write(f"\nLatest graduation:")
            self.stdout.write(f"  Date: {latest_graduation.time_stamp}")
            self.stdout.write(f"  Belt: {latest_graduation.belt}")
            self.stdout.write(f"  Stripe: {latest_graduation.stripe}")
            
            # Count classes since latest graduation
            classes_since_graduation = GetAttendance.objects.filter(
                aluno=student,
                attendance__gt=latest_graduation.time_stamp
            ).count()
            
            self.stdout.write(f"\nClasses since latest graduation: {classes_since_graduation}")
            
            # List attendance dates since graduation
            if classes_since_graduation > 0:
                self.stdout.write("\nAttendance dates since graduation:")
                for attendance in GetAttendance.objects.filter(
                    aluno=student,
                    attendance__gt=latest_graduation.time_stamp
                ).order_by('attendance'):
                    self.stdout.write(f"  {attendance.attendance}")
            
            # Check if new_attendance template filter gives the correct value
            template_new_attendance = new_attendance(student)
            if template_new_attendance == classes_since_graduation:
                self.stdout.write(self.style.SUCCESS(
                    f"\nTemplateTags.new_attendance is working correctly: {template_new_attendance}"
                ))
            else:
                self.stdout.write(self.style.ERROR(
                    f"\nTemplateTags.new_attendance returned {template_new_attendance}, " +
                    f"but expected {classes_since_graduation}"
                ))
        else:
            self.stdout.write("\nNo graduation records found")
            
            # Check if new_attendance template filter gives None as expected
            template_new_attendance = new_attendance(student)
            if template_new_attendance is None:
                self.stdout.write(self.style.SUCCESS(
                    "\nTemplateTags.new_attendance correctly returned None (no graduation records)"
                ))
            else:
                self.stdout.write(self.style.ERROR(
                    f"\nTemplateTags.new_attendance returned {template_new_attendance}, " +
                    "but expected None"
                ))
                
        # Check total attendance count from template tag
        template_total_attendance = get_count_att_aluno(student)
        if template_total_attendance == total_classes:
            self.stdout.write(self.style.SUCCESS(
                f"\nTemplateTags.get_count_att_aluno is working correctly: {template_total_attendance}"
            ))
        else:
            self.stdout.write(self.style.ERROR(
                f"\nTemplateTags.get_count_att_aluno returned {template_total_attendance}, " +
                f"but expected {total_classes}"
            )) 