from django import template
from django.db.models import Sum, Q, Count
from focusbjj.models import GetAttendance, Venda, Graduation, Aluno, Championship, Product
from datetime import timedelta
from django.utils import timezone

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
    if att[0].attendance + timedelta(days=15) < timezone.now():
        tempo = timezone.now() - att[0].attendance
        return tempo
    else:
        return ''


@register.filter
def campeonatos(athlete_instance):
    return Championship.objects.filter(athlete_id=athlete_instance.id)


@register.filter
def vendas(aluno_instance):
    return Venda.objects.filter(aluno_id=aluno_instance.id)


@register.filter
def produto(venda_instance):
    return Product.objects.filter(venda=venda_instance.id)


@register.filter
def somavendas(aluno_instance):
    soma = Venda.objects.filter(aluno_id=aluno_instance.id).aggregate(Sum('price'))
    somafinal = soma['price__sum']
    return somafinal


@register.filter
def campeonatos_branch(unidade):
    return Championship.objects.filter(unidade=unidade.id).order_by('-time_stamp')


@register.filter
def vendas_branch(unidade_instance):
    return Venda.objects.filter(unidade_id=unidade_instance.id).order_by('-time_stamp')[:4]


@register.filter
def vendas_branch_detalhes(unidade_instance):
    return Venda.objects.filter(unidade_id=unidade_instance.id).order_by('-time_stamp')


@register.filter
def somavendas_branch(unidade_instance):
    soma = Venda.objects.filter(unidade_id=unidade_instance.id).aggregate(Sum('price'))
    somafinal = soma['price__sum']
    return somafinal


@register.filter
def graduacoes(aluno_instance):
    return Graduation.objects.filter(aluno_id=aluno_instance.id).order_by('-time_stamp')


@register.filter
def current_belt(aluno_instance):
    belt = Graduation.objects.filter(aluno_id=aluno_instance.id).order_by('-time_stamp')
    if belt:
        current = belt[0].belt
    else:
        current = aluno_instance.belt
    return current


@register.filter
def current_stripe(aluno_instance):
    belt = Graduation.objects.filter(aluno_id=aluno_instance.id).order_by('-time_stamp')
    if belt:
        current = belt[0].stripe
    else:
        current = aluno_instance.stripe
    return current


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
    last_grad = Graduation.objects.filter(aluno_id=aluno_instance.id).order_by('-time_stamp')
    if last_grad:
        date = last_grad[0].time_stamp
        enddate = timezone.now()
        attendance = len(GetAttendance.objects.filter(aluno_id=aluno_instance.id).filter(attendance__range=[date, enddate]))
        return attendance


'''@register.filter 
def male(gender_instance):
    men = Aluno.objects.filter(gender='Male').annotate(male=Count('pk', filter=Q(gender='Male')))
    return len(men)

@register.filter
def female(aluno_instance):
    girls = Aluno.objects.filter(gender='Female').annotate(female=Count('pk', filter=Q(gender='Female')))
    return len(girls)'''


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


@register.filter
def white(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    white = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'White Belt' and aluno.idade() > 13:
            white += 1
    return white


@register.filter
def white_kids(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    white = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'White Belt' and aluno.idade() <= 13:
            white += 1
    return white


@register.filter
def blue(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    blue = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Blue Belt':
            blue += 1
    return blue


@register.filter
def gray(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    gray = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Gray Belt':
            gray += 1
    return gray


@register.filter
def gray_white(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    graywhite = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Gray/White Belt':
            graywhite += 1
    return graywhite


@register.filter
def gray_black(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    grayblack = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Gray/Black Belt':
            grayblack += 1
    return grayblack


@register.filter
def yellow(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    yellow = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Yellow Belt':
            yellow += 1
    return yellow


@register.filter
def yellow_white(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    yellowwhite = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Yellow/White Belt':
            yellowwhite += 1
    return yellowwhite


@register.filter
def yellow_black(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    yellowblack = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Yellow/Black Belt':
            yellowblack += 1
    return yellowblack


@register.filter
def green(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    green = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Green Belt':
            green += 1
    return green


@register.filter
def green_white(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    greenwhite = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Green/White Belt':
            greenwhite += 1
    return greenwhite


@register.filter
def green_black(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    greenblack = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Green/Black Belt':
            greenblack += 1
    return greenblack


@register.filter
def orange(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    orange = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Orange Belt':
            orange += 1
    return orange


@register.filter
def orange_white(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    orangewhite = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Orange/White Belt':
            orangewhite += 1
    return orangewhite


@register.filter
def orange_black(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    orangeblack = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Orange/Black Belt':
            orangeblack += 1
    return orangeblack


@register.filter
def purple(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    purple = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Purple Belt':
            purple += 1
    return purple


@register.filter
def brown(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    brown = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Brown Belt':
            brown += 1
    return brown


@register.filter
def black(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    black = 0
    for aluno in alunos:
        belt = current_belt(aluno)
        if belt == 'Black Belt':
            black += 1
    return black


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
def adulto(location_instance):
    alunos = Aluno.objects.filter(location_id=location_instance.id)
    age = 0
    for aluno in alunos:
        if aluno.idade() > 13:
            age += 1
    return age
