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
def under7TOTAL(location_instance):
    alunos = Aluno.objects.all()
    age = 0
    for aluno in alunos:
        if aluno.idade() <= 6:
            age += 1
    return age


@register.filter
def under10TOTAL(location_instance):
    alunos = Aluno.objects.all()
    age = 0
    for aluno in alunos:
        if 7 <= aluno.idade() <= 10:
            age += 1
    return age


@register.filter
def under13TOTAL(location_instance):
    alunos = Aluno.objects.all()
    age = 0
    for aluno in alunos:
        if 11 <= aluno.idade() <= 13:
            age += 1
    return age

@register.filter
def kidsTOTAL(location_instance):
    alunos = Aluno.objects.all()
    age = 0
    for aluno in alunos:
        if aluno.idade() <= 13:
            age += 1
    return age


@register.filter
def adultoTOTAL(location_instance):
    alunos = Aluno.objects.all()
    age = 0
    for aluno in alunos:
        if aluno.idade() >= 14:
            age += 1
    return age