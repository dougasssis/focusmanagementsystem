from django import template
from focusbjj.models import Aluno

register = template.Library()

@register.filter
def under7(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    age = 0
    for aluno in alunos:
        if aluno.idade() <= 6:
            age += 1
    return age

@register.filter
def under10(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    age = 0
    for aluno in alunos:
        if 7 <= aluno.idade() <= 10:
            age += 1
    return age

@register.filter
def under13(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    age = 0
    for aluno in alunos:
        if 11 <= aluno.idade() <= 13:
            age += 1
    return age

@register.filter
def kidsByBranch(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    age = 0
    for aluno in alunos:
        if aluno.idade() <= 13:
            age += 1
    return age


@register.filter
def adulto(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    age = 0
    for aluno in alunos:
        if aluno.idade() >= 14:
            age += 1
    return age


@register.filter
def under7TOTAL(instance):
    # Check if the instance is a QuerySet of Aluno objects
    if hasattr(instance, 'model') and instance.model == Aluno:
        # It's a QuerySet of Aluno objects, just filter it directly
        return sum(1 for aluno in instance if aluno.idade() <= 6)
    
    # Otherwise, assume it's a CustomUser (location) instance
    try:
        alunos = Aluno.objects.filter(location_id=instance.id)
        age = 0
        for aluno in alunos:
            if aluno.idade() <= 6:
                age += 1
        return age
    except AttributeError:
        # Fallback in case of unexpected object type
        return 0


@register.filter
def under10TOTAL(instance):
    # Check if the instance is a QuerySet of Aluno objects
    if hasattr(instance, 'model') and instance.model == Aluno:
        # It's a QuerySet of Aluno objects, just filter it directly
        return sum(1 for aluno in instance if 7 <= aluno.idade() <= 10)
    
    # Otherwise, assume it's a CustomUser (location) instance
    try:
        alunos = Aluno.objects.filter(location_id=instance.id)
        age = 0
        for aluno in alunos:
            if 7 <= aluno.idade() <= 10:
                age += 1
        return age
    except AttributeError:
        # Fallback in case of unexpected object type
        return 0


@register.filter
def under13TOTAL(instance):
    # Check if the instance is a QuerySet of Aluno objects
    if hasattr(instance, 'model') and instance.model == Aluno:
        # It's a QuerySet of Aluno objects, just filter it directly
        return sum(1 for aluno in instance if 11 <= aluno.idade() <= 13)
    
    # Otherwise, assume it's a CustomUser (location) instance
    try:
        alunos = Aluno.objects.filter(location_id=instance.id)
        age = 0
        for aluno in alunos:
            if 11 <= aluno.idade() <= 13:
                age += 1
        return age
    except AttributeError:
        # Fallback in case of unexpected object type
        return 0

@register.filter
def kidsTOTAL(instance):
    # Check if the instance is a QuerySet of Aluno objects
    if hasattr(instance, 'model') and instance.model == Aluno:
        # It's a QuerySet of Aluno objects, just filter it directly
        return sum(1 for aluno in instance if aluno.idade() <= 13)
    
    # Otherwise, assume it's a CustomUser (location) instance
    try:
        alunos = Aluno.objects.filter(location_id=instance.id)
        age = 0
        for aluno in alunos:
            if aluno.idade() <= 13:
                age += 1
        return age
    except AttributeError:
        # Fallback in case of unexpected object type
        return 0


@register.filter
def adultoTOTAL(instance):
    # Check if the instance is a QuerySet of Aluno objects
    if hasattr(instance, 'model') and instance.model == Aluno:
        # It's a QuerySet of Aluno objects, just filter it directly
        return sum(1 for aluno in instance if aluno.idade() >= 14)
    
    # Otherwise, assume it's a CustomUser (location) instance
    try:
        alunos = Aluno.objects.filter(location_id=instance.id)
        age = 0
        for aluno in alunos:
            if aluno.idade() >= 14:
                age += 1
        return age
    except AttributeError:
        # Fallback in case of unexpected object type
        return 0