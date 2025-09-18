from django import template
from django.db.models import Sum, Q, Count
from focusbjj.models import GetAttendance, Graduation, Aluno, GraduationRequirement
from datetime import timedelta
from django.utils import timezone
import re
from focusbjj.utils import get_students_absent as utils_get_students_absent, get_students_active as utils_get_students_active

register = template.Library()


@register.filter
def get_count_att_aluno(aluno_instance):
    return len(GetAttendance.objects.filter(aluno_id=aluno_instance.id))


@register.filter
def att_list(aluno_instance):
    return GetAttendance.objects.filter(aluno_id=aluno_instance.id)


@register.filter
def last_att_aluno(aluno_instance):
    att = GetAttendance.objects.filter(aluno_id=aluno_instance.id).order_by('-attendance')
    if not att.exists():
        return None
    if att[0].attendance + timedelta(days=15) < timezone.now():
        tempo = timezone.now() - att[0].attendance
        return tempo
    else:
        return ''
    
@register.filter
def days_since_last_attendance(aluno_instance):
    att = last_att_aluno(aluno_instance)
    if att is None:
        return 0
    return (timezone.now() - att).days

@register.filter
def is_student_absent(aluno_instance):
    att = GetAttendance.objects.filter(aluno_id=aluno_instance.id).order_by('-attendance')
    if att is None:
        return False
    if att[0].attendance + timedelta(days=30) < timezone.now():
        return True
    return False

@register.filter
def get_students_absent(qs):
    return utils_get_students_absent(qs)

@register.filter
def get_students_active(qs):
    return utils_get_students_active(qs)

@register.filter
def graduacoes(aluno_instance):
    return Graduation.objects.filter(aluno_id=aluno_instance.id).order_by('-time_stamp')


@register.filter
def current_belt(aluno_instance):
    """
    Get the current belt of a student, prioritizing their most recent graduation record.
    If no graduation record exists, fall back to the student's belt field.
    
    Ensures consistent belt display across all views.
    """
    try:
        # Check for graduation records
        graduations = Graduation.objects.filter(aluno_id=aluno_instance.id).order_by('-time_stamp')
        
        if graduations.exists():
            # Get the most recent graduation
            latest_graduation = graduations.first() 
            
            # Get belt from graduation and ensure proper formatting
            current = latest_graduation.belt
            
            # Normalize belt name (add "Belt" suffix if missing)
            if " Belt" not in current and current in ["White", "Blue", "Purple", "Brown", "Black"]:
                current = f"{current} Belt"
                
            return current
        else:
            # No graduation record, use the student model field
            current = aluno_instance.belt
            return current
            
    except Exception as e:
        return aluno_instance.belt or "White Belt"


@register.filter
def current_stripe(aluno_instance):
    """
    Get the current stripe of a student, prioritizing their most recent graduation record.
    If no graduation record exists, fall back to the student's stripe field.
    
    Ensures consistent stripe display across all views.
    """
    try:
        # Check for graduation records
        graduations = Graduation.objects.filter(aluno_id=aluno_instance.id).order_by('-time_stamp')
        
        if graduations.exists():
            # Get the most recent graduation
            latest_graduation = graduations.first()
            return latest_graduation.stripe
        else:
            # No graduation record, use the student model field
            return aluno_instance.stripe
            
    except Exception as e:
        return aluno_instance.stripe or "No Stripes"


@register.filter
def last_graduation(aluno_instance):
    last_grad = Graduation.objects.filter(aluno_id=aluno_instance.id).order_by('-time_stamp')
    if last_grad:
        date = last_grad[0].time_stamp
    else:
        date = 'Not Graduated'
    return date


@register.filter
def new_attendance(aluno_instance):
    """
    Count the number of classes attended since the last graduation.
    Returns None if no graduation records exist.
    """
    last_grad = Graduation.objects.filter(aluno_id=aluno_instance.id).order_by('-time_stamp')
    
    if not last_grad.exists():
        # No graduation records, return None to indicate this
        return None
    
    # Get the date/time of the last graduation
    last_grad_date = last_grad[0].time_stamp
    
    # Count attendance records since last graduation
    attendance_since_graduation = GetAttendance.objects.filter(
        aluno_id=aluno_instance.id,
        attendance__gt=last_grad_date
    ).count()
    
    # Return the count (will be 0 immediately after graduation)
    return attendance_since_graduation

#GENDER TAGS

@register.filter
def male_total(gender_instance):
    men = Aluno.objects.filter(gender='Male').annotate(male=Count('pk', filter=Q(gender='Male')))
    return len(men)


@register.filter
def female_total(aluno_instance):
    girls = Aluno.objects.filter(gender='Female').annotate(female=Count('pk', filter=Q(gender='Female')))
    return len(girls)


@register.filter
def male(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    gender = 0
    for aluno in alunos:
        if aluno.gender == 'Male':
            gender += 1
    return gender


@register.filter
def female(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    gender = 0
    for aluno in alunos:
        if aluno.gender == 'Female':
            gender += 1
    return gender

# END GENDER TAGS


@register.filter
def white(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    white = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'White' and aluno.idade() > 17:
            white += 1
    return white


@register.filter
def white_GENERAL(location_instance):
    alunos = Aluno.objects.all()
    white = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'White' and aluno.idade() > 17:
            white += 1
    return white


@register.filter
def white_kids_GENERAL(location_instance):
    alunos = Aluno.objects.all()
    white = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'White' and aluno.idade() <= 17:
            white += 1
    return white


@register.filter
def white_kids(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    white = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'White' and aluno.idade() <= 17:
            white += 1
    return white


@register.filter
def blue(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    blue = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Blue':
            blue += 1
    return blue


@register.filter
def gray(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    gray = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Gray':
            gray += 1
    return gray


@register.filter
def gray_white(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    graywhite = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Gray/White':
            graywhite += 1
    return graywhite


@register.filter
def gray_black(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    grayblack = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Gray/Black':
            grayblack += 1
    return grayblack


@register.filter
def yellow(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    yellow = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Yellow':
            yellow += 1
    return yellow


@register.filter
def yellow_white(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    yellowwhite = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Yellow/White':
            yellowwhite += 1
    return yellowwhite


@register.filter
def yellow_black(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    yellowblack = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Yellow/Black':
            yellowblack += 1
    return yellowblack


@register.filter
def green(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    green = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Green':
            green += 1
    return green


@register.filter
def green_white(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    greenwhite = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Green/White':
            greenwhite += 1
    return greenwhite


@register.filter
def green_black(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    greenblack = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Green/Black':
            greenblack += 1
    return greenblack


@register.filter
def orange(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    orange = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Orange':
            orange += 1
    return orange


@register.filter
def orange_white(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    orangewhite = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Orange/White':
            orangewhite += 1
    return orangewhite


@register.filter
def orange_black(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    orangeblack = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Orange/Black':
            orangeblack += 1
    return orangeblack


@register.filter
def purple(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    purple = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Purple':
            purple += 1
    return purple


@register.filter
def brown(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    brown = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Brown':
            brown += 1
    return brown


@register.filter
def black(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    black = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Black':
            black += 1
    return black


@register.filter
def remove_query_param(url, param):
    """Remove a query parameter from a URL"""
    pattern = re.compile(f'&?{param}=[^&]*')
    url = re.sub(pattern, '', url)
    # Remove any trailing ? or & if it's the last parameter
    url = url.rstrip('?&')
    return url

@register.filter
def add_query_param(url, param_value):
    """Add a query parameter to a URL"""
    param, value = param_value.split('=', 1)
    connector = '&' if '?' in url else '?'
    return f"{url}{connector}{param}={value}"


@register.filter
def classes_to_graduation(total_classes):
    """
    Calculate how many more classes a student needs to attend before they are eligible for graduation.
    Based on the current belt and stripe level of the student.
    """
    if total_classes is None:
        return 0
    
    # Default is 40 classes for adults
    return max(0, 40 - total_classes)


@register.filter
def classes_to_graduation_kids(total_classes):
    """
    Calculate how many more classes a kid student needs to attend before they are eligible for graduation.
    Kids belts require 30 classes per graduation regardless of belt color.
    """
    if total_classes is None:
        return 0
    
    # Kids belts need 30 classes for each graduation
    return max(0, 30 - total_classes)


@register.filter
def classes_needed_for_graduation(aluno_instance):
    """
    Get the number of classes needed for the next graduation based on the GraduationRequirement model.
    """
    # Get current belt and stripe
    belt = aluno_instance.belt
    stripe = aluno_instance.stripe
    
    # Check if there are any Graduation records
    graduations = Graduation.objects.filter(aluno=aluno_instance).order_by('-time_stamp')
    if graduations.exists():
        # Use the most recent graduation record for current belt/stripe
        belt = graduations.first().belt
        stripe = graduations.first().stripe
    
    # Look up the requirement in the GraduationRequirement table
    try:
        requirement = GraduationRequirement.objects.get(belt=belt, stripes=stripe)
        return requirement.required_classes
    except GraduationRequirement.DoesNotExist:
        # Fallback to default values if no matching requirement
        if any(kid_belt in belt for kid_belt in ['Gray', 'Yellow', 'Orange', 'Green']):
            return 30  # Default for kids belts
        elif belt == 'White':
            if stripe == 'IVº Stripe':
                return 40
            else:
                return 25
        elif belt == 'Blue':
            return 50
        elif belt == 'Purple':
            return 60
        elif belt == 'Brown':
            return 65
        else:
            return 30  # Default fallback


@register.filter
def classes_remaining_to_graduation(aluno_instance):
    """
    Calculate how many more classes a student needs before eligible for graduation
    based on their current belt/stripe and the graduation requirements.
    """
    # Get classes required for current belt/stripe
    required_classes = classes_needed_for_graduation(aluno_instance)
    
    # Get classes taken since last graduation
    classes_taken = 0
    last_grad = Graduation.objects.filter(aluno=aluno_instance).order_by('-time_stamp')
    
    if last_grad.exists():
        last_grad_date = last_grad.first().time_stamp
        classes_taken = GetAttendance.objects.filter(
            aluno=aluno_instance, 
            attendance__gt=last_grad_date
        ).count()
    else:
        # If no previous graduation, count all classes
        classes_taken = GetAttendance.objects.filter(aluno=aluno_instance).count()
    
    # Calculate remaining classes needed
    return max(0, required_classes - classes_taken)



