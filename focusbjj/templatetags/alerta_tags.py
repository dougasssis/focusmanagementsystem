from django import template
from focusbjj.templatetags.attendance_tags import new_attendance, current_belt, current_stripe

register = template.Library()


@register.filter
def alert(aluno_instance):
    new_attendance_ = new_attendance(aluno_instance)
    current_belt_ = current_belt(aluno_instance)
    current_stripe_ = current_stripe(aluno_instance)
    if new_attendance_ and current_belt_ and current_stripe_:
        #GRADUAÇÃO WHITE BELT
        if new_attendance_ >= 1 and current_belt_ == 'White Belt' and current_stripe_ == 'No Stripes':
            return 'Graduar Aluno Iº Stripe'
        elif new_attendance_ >= 25 and current_belt_ == 'White Belt' and current_stripe_ == 'Iº Stripe':
            return 'Graduar Aluno IIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'White Belt' and current_stripe_ == 'IIº Stripe':
            return 'Graduar Aluno IIIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'White Belt' and current_stripe_ == 'IIIº Stripe':
            return 'Graduar Aluno IVº Stripe'
        elif new_attendance_ >= 40 and current_belt_ == 'White Belt' and current_stripe_ == 'IVº Stripe':
            return 'Graduar Aluno Faixa Azul'
        #GRADUAÇÃO BLUE BELT
        elif new_attendance_ >= 50 and current_belt_ == 'Blue Belt' and current_stripe_ == 'No Stripes':
            return 'Graduar Aluno Iº Stripe'
        elif new_attendance_ >= 50 and current_belt_ == 'Blue Belt' and current_stripe_ == 'Iº Stripe':
            return 'Graduar Aluno IIº Stripe'
        elif new_attendance_ >= 50 and current_belt_ == 'Blue Belt' and current_stripe_ == 'IIº Stripe':
            return 'Graduar Aluno IIIº Stripe'
        elif new_attendance_ >= 50 and current_belt_ == 'Blue Belt' and current_stripe_ == 'IIIº Stripe':
            return 'Graduar Aluno IVº Stripe'
        elif new_attendance_ >= 50 and current_belt_ == 'Blue Belt' and current_stripe_ == 'IVº Stripe':
            return 'Graduar Aluno Faixa Roxa'
        #GRADUAÇÃO PURPLE BELT
        elif new_attendance_ >= 60 and current_belt_ == 'Purple Belt' and current_stripe_ == 'No Stripes':
            return 'Graduar Aluno Iº Stripe'
        elif new_attendance_ >= 60 and current_belt_ == 'Purple Belt' and current_stripe_ == 'Iº Stripe':
            return 'Graduar Aluno IIº Stripe'
        elif new_attendance_ >= 1 and current_belt_ == 'Purple Belt' and current_stripe_ == 'IIº Stripe':
            return 'Graduar Aluno IIIº Stripe'
        elif new_attendance_ >= 60 and current_belt_ == 'Purple Belt' and current_stripe_ == 'IIIº Stripe':
            return 'Graduar Aluno IVº Stripe'
        elif new_attendance_ >= 60 and current_belt_ == 'Purple Belt' and current_stripe_ == 'IVº Stripe':
            return 'Graduar Aluno Faixa Marrom'
        #GRADUAÇÃO BROWN BELT
        elif new_attendance_ >= 65 and current_belt_ == 'Brown Belt' and current_stripe_ == 'No Stripes':
            return 'Graduar Aluno Iº Stripe'
        elif new_attendance_ >= 65 and current_belt_ == 'Brown Belt' and current_stripe_ == 'Iº Stripe':
            return 'Graduar Aluno IIº Stripe'
        elif new_attendance_ >= 65 and current_belt_ == 'Brown Belt' and current_stripe_ == 'IIº Stripe':
            return 'Graduar Aluno IIIº Stripe'
        elif new_attendance_ >= 65 and current_belt_ == 'Brown Belt' and current_stripe_ == 'IIIº Stripe':
            return 'Graduar Aluno IVº Stripe'
        elif new_attendance_ >= 65 and current_belt_ == 'Brown Belt' and current_stripe_ == 'IVº Stripe':
            return 'Graduar Aluno Faixa Preta'

    else:
        pass
