from focusbjj.models import Aluno, GetAttendance
from django.utils import timezone
from datetime import timedelta

def get_students_absent(qs):
    absent_ids = []
    for aluno in qs:
        att = GetAttendance.objects.filter(aluno_id=aluno.id).order_by('-attendance')
        if not att.exists() or att[0].attendance + timedelta(days=30) < timezone.now():
            absent_ids.append(aluno.id)
    return qs.filter(id__in=absent_ids)

def get_students_active(qs):
    active_ids = []
    for aluno in qs:
        att = GetAttendance.objects.filter(aluno_id=aluno.id).order_by('-attendance')
        if att.exists() and att[0].attendance + timedelta(days=30) >= timezone.now():
            active_ids.append(aluno.id)
    return qs.filter(id__in=active_ids) 