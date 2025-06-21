from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from focusbjj.models import Aluno, GetAttendance
import datetime


class Command(BaseCommand):
    help = 'Add test attendance records for a student'

    def add_arguments(self, parser):
        parser.add_argument('student_id', type=str, help='ID of the student to add attendance for')
        parser.add_argument('--count', type=int, default=1, help='Number of attendance records to add')
        parser.add_argument('--days-back', type=int, default=0, help='Days in the past to start from')

    def handle(self, *args, **options):
        student_id = options['student_id']
        count = options['count']
        days_back = options['days_back']
        
        try:
            student = Aluno.objects.get(id=student_id)
        except Aluno.DoesNotExist:
            raise CommandError(f"Student with ID {student_id} not found")
        
        self.stdout.write(f"Adding {count} attendance records for {student.nome} {student.surname} (ID: {student.id})")
        
        # Get current time
        now = timezone.now()
        
        # Create attendance records
        for i in range(count):
            # Calculate attendance time (starting from days_back days ago)
            days_offset = days_back - i
            hours_offset = i * 2  # Spread out the attendance records by 2 hours
            
            attendance_time = now - datetime.timedelta(days=days_offset, hours=hours_offset)
            
            # Create the attendance record
            attendance = GetAttendance.objects.create(
                aluno=student,
                attendance=attendance_time
            )
            
            self.stdout.write(f"Created attendance record: {attendance.attendance}")
        
        self.stdout.write(self.style.SUCCESS(f"Successfully added {count} attendance records"))
        
        # Show updated attendance counts
        total_attendance = GetAttendance.objects.filter(aluno=student).count()
        self.stdout.write(f"Total attendance count: {total_attendance}")
        
        # Run check_attendance to show detailed information
        from django.core.management import call_command
        self.stdout.write("\nDetailed attendance information:")
        call_command('check_attendance', student_id) 