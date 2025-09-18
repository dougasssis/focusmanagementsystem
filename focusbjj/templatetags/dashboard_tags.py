from django import template
from django.db.models import Count, Q
from focusbjj.models import Aluno, GetAttendance, Graduation, CustomUser, GraduationRequirement
from datetime import datetime, timedelta, date
from django.utils import timezone

from focusbjj.templatetags.attendance_tags import current_belt, current_stripe

register = template.Library()

@register.filter
def birthdays_this_month(location_instance):
    """
    Return all students that have a birthday this month
    """
    today = date.today()
    alunos = Aluno.objects.filter(location=location_instance, date_of_birth__month=today.month)
    return alunos

@register.filter
def birthday_day(student):
    """Returns just the day of the student's birthday"""
    return student.dob.day

@register.filter
def eligible_for_graduation(location_instance):
    """
    Return all students eligible for graduation.
    """
    eligible_students = []
    
    if location_instance.is_superuser:
        alunos = Aluno.objects.all()
    else:
        alunos = Aluno.objects.filter(location=location_instance)
    
    for aluno in alunos:
        belt = current_belt(aluno)
        stripe = current_stripe(aluno)
        attendance_count = GetAttendance.objects.filter(aluno=aluno).count()
        
        # White belt progression
        if belt == 'White Belt':
            if (stripe == 'No Stripes' and attendance_count >= 25) or \
               (stripe == 'Iº Stripe' and attendance_count >= 25) or \
               (stripe == 'IIº Stripe' and attendance_count >= 30) or \
               (stripe == 'IIIº Stripe' and attendance_count >= 30) or \
               (stripe == 'IVº Stripe' and attendance_count >= 40):
                eligible_students.append({'student': aluno, 'attendance_count': attendance_count})
        
        # Blue belt progression
        elif belt == 'Blue Belt':
            if (stripe == 'No Stripes' and attendance_count >= 50) or \
               (stripe == 'Iº Stripe' and attendance_count >= 50) or \
               (stripe == 'IIº Stripe' and attendance_count >= 50) or \
               (stripe == 'IIIº Stripe' and attendance_count >= 50) or \
               (stripe == 'IVº Stripe' and attendance_count >= 50):
                eligible_students.append({'student': aluno, 'attendance_count': attendance_count})
        
        # Purple belt progression
        elif belt == 'Purple Belt':
            if (stripe == 'No Stripes' and attendance_count >= 60) or \
               (stripe == 'Iº Stripe' and attendance_count >= 60) or \
               (stripe == 'IIº Stripe' and attendance_count >= 60) or \
               (stripe == 'IIIº Stripe' and attendance_count >= 60) or \
               (stripe == 'IVº Stripe' and attendance_count >= 60):
                eligible_students.append({'student': aluno, 'attendance_count': attendance_count})
        
        # Brown belt progression
        elif belt == 'Brown Belt':
            if (stripe == 'No Stripes' and attendance_count >= 65) or \
               (stripe == 'Iº Stripe' and attendance_count >= 65) or \
               (stripe == 'IIº Stripe' and attendance_count >= 65) or \
               (stripe == 'IIIº Stripe' and attendance_count >= 65) or \
               (stripe == 'IVº Stripe' and attendance_count >= 65):
                eligible_students.append({'student': aluno, 'attendance_count': attendance_count})
        
        # Kids belt progression (30 classes each)
        elif belt in ['Gray/White Belt', 'Gray Belt', 'Gray/Black Belt', 
                     'Yellow/White Belt', 'Yellow Belt', 'Yellow/Black Belt',
                     'Orange/White Belt', 'Orange Belt', 'Orange/Black Belt',
                     'Green/White Belt', 'Green Belt', 'Green/Black Belt']:
            if attendance_count >= 30:
                eligible_students.append({'student': aluno, 'attendance_count': attendance_count})
    
    return eligible_students

@register.filter
def recent_joiners(location_instance, days=30):
    """
    Return all students who joined in the last X days
    """
    threshold_date = date.today() - timedelta(days=days)
    alunos = Aluno.objects.filter(location=location_instance, join_date__gte=threshold_date)
    return alunos

@register.filter
def male_total(alunos):
    """Return the total count of male students"""
    return sum(1 for aluno in alunos if aluno.gender == 'Male')

@register.filter
def female_total(alunos):
    """Return the total count of female students"""
    return sum(1 for aluno in alunos if aluno.gender == 'Female')

@register.filter
def male_percentage(alunos):
    """Return the percentage of male students"""
    total = len(alunos)
    if total == 0:
        return 0
    male_count = sum(1 for aluno in alunos if aluno.gender == 'Male')
    return (male_count / total) * 100

@register.filter
def female_percentage(alunos):
    """Return the percentage of female students"""
    total = len(alunos)
    if total == 0:
        return 0
    female_count = sum(1 for aluno in alunos if aluno.gender == 'Female')
    return (female_count / total) * 100

@register.filter
def male_total_percentage(alunos):
    """Return the percentage of male students"""
    total = len(alunos)
    if total == 0:
        return 0
    male_count = male_total(alunos)
    return (male_count / total) * 100

@register.filter
def female_total_percentage(alunos):
    """Return the percentage of female students"""
    total = len(alunos)
    if total == 0:
        return 0
    female_count = female_total(alunos)
    return (female_count / total) * 100

@register.filter
def morning_checkins_total(input_obj):
    """Return the total number of check-ins during morning hours (6am-12pm) across all locations"""
    # Check if we're dealing with a QuerySet (e.g., alunos)
    if hasattr(input_obj, '__iter__') and not hasattr(input_obj, 'is_superuser'):
        # It's a QuerySet of students or similar collection, get all check-ins
        return GetAttendance.objects.filter(attendance__hour__gte=6, attendance__hour__lt=12).count()
    
    # Original behavior for user objects
    if input_obj.is_superuser:
        return GetAttendance.objects.filter(attendance__hour__gte=6, attendance__hour__lt=12).count()
    else:
        return GetAttendance.objects.filter(aluno__location=input_obj, attendance__hour__gte=6, attendance__hour__lt=12).count()

@register.filter
def afternoon_checkins_total(input_obj):
    """Return the total number of check-ins during afternoon hours (12pm-6pm) across all locations"""
    # Check if we're dealing with a QuerySet (e.g., alunos)
    if hasattr(input_obj, '__iter__') and not hasattr(input_obj, 'is_superuser'):
        # It's a QuerySet of students or similar collection, get all check-ins
        return GetAttendance.objects.filter(attendance__hour__gte=12, attendance__hour__lt=18).count()
    
    # Original behavior for user objects
    if input_obj.is_superuser:
        return GetAttendance.objects.filter(attendance__hour__gte=12, attendance__hour__lt=18).count()
    else:
        return GetAttendance.objects.filter(aluno__location=input_obj, attendance__hour__gte=12, attendance__hour__lt=18).count()

@register.filter
def evening_checkins_total(input_obj):
    """Return the total number of check-ins during evening hours (6pm-11pm) across all locations"""
    # Check if we're dealing with a QuerySet (e.g., alunos)
    if hasattr(input_obj, '__iter__') and not hasattr(input_obj, 'is_superuser'):
        # It's a QuerySet of students or similar collection, get all check-ins
        return GetAttendance.objects.filter(attendance__hour__gte=18, attendance__hour__lt=23).count()
    
    # Original behavior for user objects
    if input_obj.is_superuser:
        return GetAttendance.objects.filter(attendance__hour__gte=18, attendance__hour__lt=23).count()
    else:
        return GetAttendance.objects.filter(aluno__location=input_obj, attendance__hour__gte=18, attendance__hour__lt=23).count()

@register.filter
def male_percentage(user):
    """Return the percentage of male students at this location"""
    if user.is_superuser:
        total = Aluno.objects.count()
        if total == 0:
            return 0
        male_count = Aluno.objects.filter(gender='Male').count()
    else:
        total = Aluno.objects.filter(location=user).count()
        if total == 0:
            return 0
        male_count = Aluno.objects.filter(location=user, gender='Male').count()
    
    return (male_count / total) * 100

@register.filter
def female_percentage(user):
    """Return the percentage of female students at this location"""
    if user.is_superuser:
        total = Aluno.objects.count()
        if total == 0:
            return 0
        female_count = Aluno.objects.filter(gender='Female').count()
    else:
        total = Aluno.objects.filter(location=user).count()
        if total == 0:
            return 0
        female_count = Aluno.objects.filter(location=user, gender='Female').count()
    
    return (female_count / total) * 100

@register.filter
def inactive_students(location_instance):
    """
    Return all students who haven't attended classes in the last 30 days
    """
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    if hasattr(location_instance, 'is_superuser') and location_instance.is_superuser:
        # For superusers, get all students
        students = Aluno.objects.all()
    else:
        # For affiliates, only get their students
        students = Aluno.objects.filter(location=location_instance)
    
    inactive_students = []
    for student in students:
        # Get latest attendance record
        latest_attendance = GetAttendance.objects.filter(aluno=student).order_by('-attendance').first()
        
        # If no attendance record or last attendance was more than 30 days ago
        if not latest_attendance or latest_attendance.attendance < thirty_days_ago:
            inactive_students.append(student)
    
    return inactive_students

@register.filter
def inactive_students_count(location_instance):
    """
    Return the count of students who haven't attended classes in the last 30 days
    """
    return len(inactive_students(location_instance))

@register.filter
def birthdays_this_week(location_instance):
    """
    Return students who have a birthday in the current week (Mon-Sun)
    """
    today = date.today()
    
    # Get the start of the week (Monday)
    start_of_week = today - timedelta(days=today.weekday())
    
    # Get the end of the week (Sunday)
    end_of_week = start_of_week + timedelta(days=6)
    
    if hasattr(location_instance, 'is_superuser') and location_instance.is_superuser:
        # For superusers, check all students
        students = Aluno.objects.all()
    else:
        # For affiliates, only check their students
        students = Aluno.objects.filter(location=location_instance)
    
    birthday_students = []
    for student in students:
        # Get the student's birthday this year
        birthday_this_year = date(today.year, student.dob.month, student.dob.day)
        
        # Check if the birthday falls within the current week
        if start_of_week <= birthday_this_year <= end_of_week:
            birthday_students.append(student)
    
    return birthday_students

@register.filter
def busiest_days_of_week(location_instance):
    """
    Return attendance counts grouped by day of the week
    """
    if hasattr(location_instance, 'is_superuser') and location_instance.is_superuser:
        # For superusers, get all attendance records
        attendances = GetAttendance.objects.all()
    else:
        # For affiliates, only get their students' attendance
        attendances = GetAttendance.objects.filter(aluno__location=location_instance)
    
    # Initialize counters for each day - return as a list, not a dictionary
    days = [
        {'name': 'Monday', 'count': 0},
        {'name': 'Tuesday', 'count': 0},
        {'name': 'Wednesday', 'count': 0},
        {'name': 'Thursday', 'count': 0},
        {'name': 'Friday', 'count': 0},
        {'name': 'Saturday', 'count': 0},
        {'name': 'Sunday', 'count': 0}
    ]
    
    # Count attendance for each day
    for attendance in attendances:
        weekday = attendance.attendance.weekday()
        days[weekday]['count'] += 1
    
    return days

@register.simple_tag
def belt_distribution_average():
    """
    Calculate the system-wide average of students per belt type per affiliate
    Returns a dictionary with belt types as keys and average counts as values
    """
    # Get the actual count of affiliates (only staff users that aren't superusers)
    total_affiliates = CustomUser.objects.filter(is_staff=True, is_superuser=False).count()
    
    # Ensure at least 1 to avoid division by zero
    if total_affiliates <= 0:
        total_affiliates = 1
    
    # Define all belt keys
    belt_keys = [
        'white', 
        'gray_white', 'gray', 'gray_black',
        'yellow_white', 'yellow', 'yellow_black',
        'orange_white', 'orange', 'orange_black',
        'green_white', 'green', 'green_black',
        'blue', 'purple', 'brown', 'black'
    ]
    
    # Initialize counts
    belt_counts = {belt_key: 0 for belt_key in belt_keys}
    
    # Get reverse mapping from belt display name to belt key
    belt_mapping = {
        # With 'Belt' suffix
        'White Belt': 'white',
        'Gray/White Belt': 'gray_white',
        'Gray Belt': 'gray',
        'Gray/Black Belt': 'gray_black',
        'Yellow/White Belt': 'yellow_white',
        'Yellow Belt': 'yellow',
        'Yellow/Black Belt': 'yellow_black',
        'Orange/White Belt': 'orange_white',
        'Orange Belt': 'orange',
        'Orange/Black Belt': 'orange_black',
        'Green/White Belt': 'green_white',
        'Green Belt': 'green',
        'Green/Black Belt': 'green_black',
        'Blue Belt': 'blue',
        'Purple Belt': 'purple',
        'Brown Belt': 'brown',
        'Black Belt': 'black',
        
        # Without 'Belt' suffix
        'White': 'white',
        'Gray/White': 'gray_white',
        'Gray': 'gray',
        'Gray/Black': 'gray_black',
        'Yellow/White': 'yellow_white',
        'Yellow': 'yellow',
        'Yellow/Black': 'yellow_black',
        'Orange/White': 'orange_white',
        'Orange': 'orange',
        'Orange/Black': 'orange_black',
        'Green/White': 'green_white',
        'Green': 'green',
        'Green/Black': 'green_black',
        'Blue': 'blue',
        'Purple': 'purple',
        'Brown': 'brown',
        'Black': 'black'
    }
    
    # Count students by belt across all affiliates
    for student in Aluno.objects.all():
        belt = current_belt(student)
        if belt in belt_mapping:
            belt_key = belt_mapping[belt]
            if belt_key in belt_counts:
                belt_counts[belt_key] += 1
    
    # Calculate average per affiliate
    average_belts = {}
    for belt_key, count in belt_counts.items():
        average_belts[belt_key] = round(count / total_affiliates, 1)
    
    return average_belts

@register.filter
def mul(value, arg):
    """Multiply the value by the argument"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
    
@register.filter
def div(value, arg):
    """
    Divide the value by the argument
    """
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError, TypeError):
        return 0
        
@register.filter
def get_item(dictionary, key):
    """
    Get an item from a dictionary
    """
    return dictionary.get(key, 0)
        
@register.filter
def belt_count(affiliate, belt_key):
    """
    Count the number of students with a specific belt type for an affiliate
    """
    count = 0
    # Define mappings for both with and without 'Belt' suffix
    belt_mapping = {
        # With 'Belt' suffix
        'White Belt': 'white',
        'Gray/White Belt': 'gray_white',
        'Gray Belt': 'gray',
        'Gray/Black Belt': 'gray_black',
        'Yellow/White Belt': 'yellow_white',
        'Yellow Belt': 'yellow',
        'Yellow/Black Belt': 'yellow_black',
        'Orange/White Belt': 'orange_white',
        'Orange Belt': 'orange',
        'Orange/Black Belt': 'orange_black',
        'Green/White Belt': 'green_white',
        'Green Belt': 'green',
        'Green/Black Belt': 'green_black',
        'Blue Belt': 'blue',
        'Purple Belt': 'purple',
        'Brown Belt': 'brown',
        'Black Belt': 'black',
        
        # Without 'Belt' suffix
        'White': 'white',
        'Gray/White': 'gray_white',
        'Gray': 'gray',
        'Gray/Black': 'gray_black',
        'Yellow/White': 'yellow_white',
        'Yellow': 'yellow',
        'Yellow/Black': 'yellow_black',
        'Orange/White': 'orange_white',
        'Orange': 'orange',
        'Orange/Black': 'orange_black',
        'Green/White': 'green_white',
        'Green': 'green',
        'Green/Black': 'green_black',
        'Blue': 'blue',
        'Purple': 'purple',
        'Brown': 'brown',
        'Black': 'black'
    }
    
    # Get all students for this affiliate
    students = Aluno.objects.filter(location=affiliate)
    
    # Count students by their current belt
    for student in students:
        belt = current_belt(student)
        if belt in belt_mapping and belt_mapping[belt] == belt_key:
            count += 1
            
    return count

@register.filter
def belt_distribution_average(belt_key, total_affiliates):
    """
    Calculate the average number of students with a specific belt type across all affiliates
    """
    count = 0
    # Define mappings for both with and without 'Belt' suffix
    belt_mapping = {
        # With 'Belt' suffix
        'White Belt': 'white',
        'Gray/White Belt': 'gray_white',
        'Gray Belt': 'gray',
        'Gray/Black Belt': 'gray_black',
        'Yellow/White Belt': 'yellow_white',
        'Yellow Belt': 'yellow',
        'Yellow/Black Belt': 'yellow_black',
        'Orange/White Belt': 'orange_white',
        'Orange Belt': 'orange',
        'Orange/Black Belt': 'orange_black',
        'Green/White Belt': 'green_white',
        'Green Belt': 'green',
        'Green/Black Belt': 'green_black',
        'Blue Belt': 'blue',
        'Purple Belt': 'purple',
        'Brown Belt': 'brown',
        'Black Belt': 'black',
        
        # Without 'Belt' suffix
        'White': 'white',
        'Gray/White': 'gray_white',
        'Gray': 'gray',
        'Gray/Black': 'gray_black',
        'Yellow/White': 'yellow_white',
        'Yellow': 'yellow',
        'Yellow/Black': 'yellow_black',
        'Orange/White': 'orange_white',
        'Orange': 'orange',
        'Orange/Black': 'orange_black',
        'Green/White': 'green_white',
        'Green': 'green',
        'Green/Black': 'green_black',
        'Blue': 'blue',
        'Purple': 'purple',
        'Brown': 'brown',
        'Black': 'black'
    }
    
    # Ensure total_affiliates is a number
    try:
        total_affiliates = int(total_affiliates)
    except (ValueError, TypeError):
        # If not explicitly provided, calculate it ourselves
        total_affiliates = CustomUser.objects.filter(is_staff=True, is_superuser=False).count()
    
    if total_affiliates <= 0:
        total_affiliates = 1
    
    # Get all students with this belt
    for student in Aluno.objects.all():
        belt = current_belt(student)
        if belt in belt_mapping and belt_mapping[belt] == belt_key:
            count += 1
    
    # Return the average (rounded to 1 decimal place)
    return round(count / total_affiliates, 1)

@register.filter
def students_eligible_for_graduation(location_instance, limit=None):
    """
    Return all students eligible for graduation with details on next belt/stripe and classes attended.
    
    Args:
        location_instance: CustomUser instance of the affiliate or superuser
        limit: Optional limit on number of students to return
        
    Returns:
        List of dicts with student info, next belt/stripe, classes attended, and classes required
    """
    eligible_students = []
    
    # Get students based on location or all if superuser
    if hasattr(location_instance, 'is_superuser') and location_instance.is_superuser:
        # For superuser, if a specific affiliate is selected, use that
        affiliate_id = getattr(location_instance, 'selected_affiliate_id', None)
        if affiliate_id:
            try:
                affiliate = CustomUser.objects.get(id=affiliate_id)
                students = Aluno.objects.filter(location=affiliate)
            except CustomUser.DoesNotExist:
                students = Aluno.objects.all()
        else:
            students = Aluno.objects.all()
    else:
        # Regular user only sees their students
        students = Aluno.objects.filter(location=location_instance)
    
    # Check eligibility for each student
    for student in students:
        eligibility = is_eligible_for_graduation(student)
        if eligibility['eligible']:
            student_info = {
                'student': student,
                'next_belt': eligibility['next_belt'],
                'next_stripe': eligibility['next_stripe'],
                'classes_attended': eligibility['classes_attended'],
                'classes_required': eligibility['classes_required'],
                'classes_over': eligibility['classes_over_requirement']
            }
            eligible_students.append(student_info)
    
    # Sort by classes over requirement (most first)
    eligible_students.sort(key=lambda x: x['classes_over'], reverse=True)
    
    # Apply limit if provided
    if limit and isinstance(limit, int):
        eligible_students = eligible_students[:limit]
    
    return eligible_students

@register.filter
def is_eligible_for_graduation(student):
    """
    Determine if a specific student is eligible for graduation
    
    Args:
        student: Aluno instance
        
    Returns:
        Dict with eligibility info including:
        - eligible (boolean)
        - next_belt (string)
        - next_stripe (string)
        - classes_attended (int)
        - classes_required (int)
        - classes_over_requirement or classes_remaining (int)
    """
    # Use the current belt and stripe from attendance_tags
    from focusbjj.templatetags.attendance_tags import current_belt, current_stripe
    
    # Get current belt and stripe
    belt = current_belt(student).replace(' Belt', '')
    stripe = current_stripe(student)
    
    # Get the last graduation timestamp
    last_grad = Graduation.objects.filter(aluno=student).order_by('-time_stamp').first()
    last_grad_date = last_grad.time_stamp if last_grad else student.join_date
    
    # Count classes since last graduation
    classes_attended = GetAttendance.objects.filter(
        aluno=student, 
        attendance__gt=last_grad_date
    ).count()
    
    # Get the graduation requirement for current belt/stripe
    try:
        requirement = GraduationRequirement.objects.get(belt=belt, stripes=stripe)
        classes_required = requirement.required_classes
    except GraduationRequirement.DoesNotExist:
        # Default requirements if not found in database
        if any(kid_belt in belt for kid_belt in ['Gray', 'Yellow', 'Orange', 'Green']):
            # Kids program requirements
            classes_required = 30
        elif belt == 'White':
            if stripe == 'IVº Stripe':
                classes_required = 40
            else:
                classes_required = 25
        elif belt == 'Blue':
            classes_required = 50
        elif belt == 'Purple':
            classes_required = 60
        elif belt == 'Brown':
            classes_required = 65
        else:
            classes_required = 30
    
    # Determine if student is eligible based on classes attended
    eligible = classes_attended >= classes_required
    
    # Determine next belt and stripe
    next_belt, next_stripe = get_next_belt_stripe(belt, stripe)
    
    # Calculate classes over requirement or remaining
    if eligible:
        classes_over = classes_attended - classes_required
        result = {
            'eligible': True,
            'next_belt': next_belt,
            'next_stripe': next_stripe,
            'classes_attended': classes_attended,
            'classes_required': classes_required,
            'classes_over_requirement': classes_over
        }
    else:
        classes_remaining = classes_required - classes_attended
        result = {
            'eligible': False,
            'next_belt': next_belt,
            'next_stripe': next_stripe,
            'classes_attended': classes_attended,
            'classes_required': classes_required,
            'classes_remaining': classes_remaining
        }
    
    return result

def get_next_belt_stripe(belt, stripe):
    """Helper function to determine the next belt and stripe based on the BJJ progression."""
    
    # Handle special case of White Belt with 4 stripes - goes to Blue Belt
    if belt == 'White' and stripe == 'IVº Stripe':
        return 'Blue', 'No Stripes'
    
    # Handle Blue Belt with 4 stripes - goes to Purple Belt
    if belt == 'Blue' and stripe == 'IVº Stripe':
        return 'Purple', 'No Stripes'
    
    # Handle Purple Belt with 4 stripes - goes to Brown Belt
    if belt == 'Purple' and stripe == 'IVº Stripe':
        return 'Brown', 'No Stripes'
    
    # Handle Brown Belt with 4 stripes - goes to Black Belt
    if belt == 'Brown' and stripe == 'IVº Stripe':
        return 'Black', 'No Stripes'
    
    # Kids belts progression
    if belt == 'White' and stripe != 'IVº Stripe':
        # Kids start with white belt and progress through the stripes
        stripe_mapping = {
            'No Stripes': 'Iº Stripe',
            'Iº Stripe': 'IIº Stripe',
            'IIº Stripe': 'IIIº Stripe',
            'IIIº Stripe': 'IVº Stripe'
        }
        return belt, stripe_mapping.get(stripe, 'Iº Stripe')
    
    # Kids specific belts
    if belt in ['Gray/White', 'Gray', 'Gray/Black', 
                'Yellow/White', 'Yellow', 'Yellow/Black',
                'Orange/White', 'Orange', 'Orange/Black',
                'Green/White', 'Green', 'Green/Black']:
        
        # Within same belt color, progress through stripes
        if stripe != 'IVº Stripe':
            stripe_mapping = {
                'No Stripes': 'Iº Stripe',
                'Iº Stripe': 'IIº Stripe',
                'IIº Stripe': 'IIIº Stripe',
                'IIIº Stripe': 'IVº Stripe'
            }
            return belt, stripe_mapping.get(stripe, 'Iº Stripe')
        
        # At 4 stripes, progress to next belt
        kid_belt_progression = [
            'White', 
            'Gray/White', 'Gray', 'Gray/Black',
            'Yellow/White', 'Yellow', 'Yellow/Black',
            'Orange/White', 'Orange', 'Orange/Black',
            'Green/White', 'Green', 'Green/Black',
            'Blue'  # They move to adult system
        ]
        
        try:
            current_index = kid_belt_progression.index(belt)
            if current_index < len(kid_belt_progression) - 1:
                return kid_belt_progression[current_index + 1], 'No Stripes'
        except ValueError:
            # If belt not found in progression, default to next stripe
            return belt, 'Iº Stripe'
    
    # Adult belts (Blue, Purple, Brown, Black) - progress through stripes
    stripe_mapping = {
        'No Stripes': 'Iº Stripe',
        'Iº Stripe': 'IIº Stripe',
        'IIº Stripe': 'IIIº Stripe',
        'IIIº Stripe': 'IVº Stripe'
    }
    return belt, stripe_mapping.get(stripe, 'Iº Stripe')

@register.filter
def total_checkins(affiliate):
    """
    Count the total number of check-ins for an affiliate in the last 30 days
    """
    # Get all students for this affiliate
    students = Aluno.objects.filter(location=affiliate)
    
    # Count check-ins from the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    total_count = GetAttendance.objects.filter(
        aluno__in=students,
        attendance__gte=thirty_days_ago
    ).count()
    
    return total_count

@register.filter
def checkin_percentage(affiliate):
    """
    Calculate the percentage of check-ins for this affiliate compared to the total system
    Returns a number between 0-100
    """
    # Get all check-ins for this affiliate in the last 30 days
    students = Aluno.objects.filter(location=affiliate)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    affiliate_checkins = GetAttendance.objects.filter(
        aluno__in=students,
        attendance__gte=thirty_days_ago
    ).count()
    
    # Get total check-ins across all academies
    total_checkins = GetAttendance.objects.filter(
        attendance__gte=thirty_days_ago
    ).count()
    
    if total_checkins == 0:
        return 0
    
    return (affiliate_checkins / total_checkins) * 100

@register.filter
def retention_rate(alunos, months_ago=0):
    """Calculate retention rate based on active students vs total students for a given month"""
    if not alunos:
        return 0
    
    # Calculate the date range for the specified month
    end_date = timezone.now() - timedelta(days=30 * months_ago)
    start_date = end_date - timedelta(days=30)
    
    # Get total students who were active in that month
    total_students = sum(1 for aluno in alunos if GetAttendance.objects.filter(
        aluno=aluno,
        attendance__lte=end_date
    ).exists())
    
    if total_students == 0:
        return 0
    
    # Get students who attended at least one class in that month
    active_students = sum(1 for aluno in alunos if GetAttendance.objects.filter(
        aluno=aluno,
        attendance__range=(start_date, end_date)
    ).exists())
    
    return (active_students / total_students * 100) if total_students > 0 else 0

@register.filter
def graduation_ready_count(alunos):
    """Calculate number of students ready for graduation based on attendance and time in current belt"""
    ready_count = 0
    for aluno in alunos:
        # Get the student's last graduation date
        last_graduation = Graduation.objects.filter(aluno=aluno).order_by('-time_stamp').first()
        if last_graduation:
            time_in_current_belt = timezone.now() - last_graduation.time_stamp
            # Get attendance count since last graduation
            attendance_count = GetAttendance.objects.filter(
                aluno=aluno,
                attendance__gte=last_graduation.time_stamp
            ).count()
            
            # Define minimum requirements based on belt
            min_days = 180  # 6 months minimum
            min_classes = 50  # minimum classes
            
            if aluno.belt == 'White':
                min_days = 180  # 6 months
                min_classes = 60
            elif aluno.belt == 'Blue':
                min_days = 365  # 1 year
                min_classes = 100
            elif aluno.belt == 'Purple':
                min_days = 545  # 18 months
                min_classes = 150
            elif aluno.belt == 'Brown':
                min_days = 730  # 2 years
                min_classes = 200
            
            # Check if student meets both time and attendance requirements
            if time_in_current_belt.days >= min_days and attendance_count >= min_classes:
                ready_count += 1
                
    return ready_count

@register.filter
def avg_time_to_blue(alunos):
    """Calculate average time (in months) for students to reach blue belt"""
    blue_belt_times = []
    
    for aluno in alunos:
        graduations = Graduation.objects.filter(aluno=aluno).order_by('time_stamp')
        white_start = None
        blue_achieved = None
        
        for grad in graduations:
            if grad.belt == 'White' and not white_start:
                white_start = grad.time_stamp
            elif grad.belt == 'Blue':
                blue_achieved = grad.time_stamp
                break
        
        if white_start and blue_achieved:
            months = (blue_achieved - white_start).days / 30
            blue_belt_times.append(months)
    
    return round(sum(blue_belt_times) / len(blue_belt_times)) if blue_belt_times else 0

@register.filter
def avg_time_to_graduate(alunos):
    """Calculate average time (in months) for students to graduate to any belt"""
    graduation_times = []
    
    for aluno in alunos:
        graduations = Graduation.objects.filter(aluno=aluno).order_by('time_stamp')
        
        if graduations.exists():
            # Get the first graduation (from join date to first belt)
            first_graduation = graduations.first()
            join_date = aluno.join_date
            first_grad_date = first_graduation.time_stamp
            
            # Calculate time from join to first graduation
            months = (first_grad_date - join_date).days / 30
            graduation_times.append(months)
            
            # Also calculate time between graduations
            for i in range(1, len(graduations)):
                prev_grad = graduations[i-1]
                curr_grad = graduations[i]
                months_between = (curr_grad.time_stamp - prev_grad.time_stamp).days / 30
                graduation_times.append(months_between)
    
    return round(sum(graduation_times) / len(graduation_times)) if graduation_times else 0

@register.filter
def morning_checkins_total(alunos):
    """Calculate total morning check-ins in the last 30 days"""
    thirty_days_ago = timezone.now() - timedelta(days=30)
    morning_start = 6  # 6 AM
    morning_end = 12   # 12 PM
    
    return GetAttendance.objects.filter(
        aluno__in=alunos,
        attendance__gte=thirty_days_ago,
        attendance__hour__gte=morning_start,
        attendance__hour__lt=morning_end
    ).count()

@register.filter
def afternoon_checkins_total(alunos):
    """Calculate total afternoon check-ins in the last 30 days"""
    thirty_days_ago = timezone.now() - timedelta(days=30)
    afternoon_start = 12  # 12 PM
    afternoon_end = 18    # 6 PM
    
    return GetAttendance.objects.filter(
        aluno__in=alunos,
        attendance__gte=thirty_days_ago,
        attendance__hour__gte=afternoon_start,
        attendance__hour__lt=afternoon_end
    ).count()

@register.filter
def evening_checkins_total(alunos):
    """Calculate total evening check-ins in the last 30 days"""
    thirty_days_ago = timezone.now() - timedelta(days=30)
    evening_start = 18  # 6 PM
    evening_end = 23    # 11 PM
    
    return GetAttendance.objects.filter(
        aluno__in=alunos,
        attendance__gte=thirty_days_ago,
        attendance__hour__gte=evening_start,
        attendance__hour__lt=evening_end
    ).count()

@register.filter
def checkin_percentage(affiliate):
    """Calculate check-in percentage for an affiliate based on active students"""
    total_students = affiliate.alunos.count()
    if total_students == 0:
        return 0
        
    thirty_days_ago = timezone.now() - timedelta(days=30)
    active_students = affiliate.alunos.filter(
        getattendance__attendance__gte=thirty_days_ago
    ).distinct().count()
    
    return (active_students / total_students) * 100 