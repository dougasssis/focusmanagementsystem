from django import template
from focusbjj.templatetags.attendance_tags import new_attendance, current_belt, current_stripe
from datetime import date
from focusbjj.models import GetAttendance, Graduation
from django.utils import timezone

register = template.Library()


@register.filter
def alert(aluno_instance):
    new_attendance_ = new_attendance(aluno_instance)
    current_belt_ = current_belt(aluno_instance)
    current_stripe_ = current_stripe(aluno_instance)
    if new_attendance_ and current_belt_ and current_stripe_:
        #GRADUAÇÃO WHITE BELT
        if new_attendance_ >= 25 and current_belt_ == 'White Belt' and current_stripe_ == 'No Stripes':
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
        elif new_attendance_ >= 60 and current_belt_ == 'Purple Belt' and current_stripe_ == 'IIº Stripe':
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

        # GRADUAÇÃO KIDS BELTS - 30 classes for each progression
        # Gray/White Belt
        elif new_attendance_ >= 30 and current_belt_ == 'Gray/White Belt' and current_stripe_ == 'No Stripes':
            return 'Graduar Aluno Iº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Gray/White Belt' and current_stripe_ == 'Iº Stripe':
            return 'Graduar Aluno IIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Gray/White Belt' and current_stripe_ == 'IIº Stripe':
            return 'Graduar Aluno IIIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Gray/White Belt' and current_stripe_ == 'IIIº Stripe':
            return 'Graduar Aluno IVº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Gray/White Belt' and current_stripe_ == 'IVº Stripe':
            return 'Graduar Aluno Faixa Cinza'
            
        # Gray Belt
        elif new_attendance_ >= 30 and current_belt_ == 'Gray Belt' and current_stripe_ == 'No Stripes':
            return 'Graduar Aluno Iº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Gray Belt' and current_stripe_ == 'Iº Stripe':
            return 'Graduar Aluno IIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Gray Belt' and current_stripe_ == 'IIº Stripe':
            return 'Graduar Aluno IIIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Gray Belt' and current_stripe_ == 'IIIº Stripe':
            return 'Graduar Aluno IVº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Gray Belt' and current_stripe_ == 'IVº Stripe':
            return 'Graduar Aluno Faixa Cinza/Preta'
            
        # Gray/Black Belt
        elif new_attendance_ >= 30 and current_belt_ == 'Gray/Black Belt' and current_stripe_ == 'No Stripes':
            return 'Graduar Aluno Iº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Gray/Black Belt' and current_stripe_ == 'Iº Stripe':
            return 'Graduar Aluno IIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Gray/Black Belt' and current_stripe_ == 'IIº Stripe':
            return 'Graduar Aluno IIIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Gray/Black Belt' and current_stripe_ == 'IIIº Stripe':
            return 'Graduar Aluno IVº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Gray/Black Belt' and current_stripe_ == 'IVº Stripe':
            return 'Graduar Aluno Faixa Amarela/Branca'
            
        # Yellow/White Belt
        elif new_attendance_ >= 30 and current_belt_ == 'Yellow/White Belt' and current_stripe_ == 'No Stripes':
            return 'Graduar Aluno Iº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Yellow/White Belt' and current_stripe_ == 'Iº Stripe':
            return 'Graduar Aluno IIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Yellow/White Belt' and current_stripe_ == 'IIº Stripe':
            return 'Graduar Aluno IIIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Yellow/White Belt' and current_stripe_ == 'IIIº Stripe':
            return 'Graduar Aluno IVº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Yellow/White Belt' and current_stripe_ == 'IVº Stripe':
            return 'Graduar Aluno Faixa Amarela'
            
        # Yellow Belt
        elif new_attendance_ >= 30 and current_belt_ == 'Yellow Belt' and current_stripe_ == 'No Stripes':
            return 'Graduar Aluno Iº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Yellow Belt' and current_stripe_ == 'Iº Stripe':
            return 'Graduar Aluno IIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Yellow Belt' and current_stripe_ == 'IIº Stripe':
            return 'Graduar Aluno IIIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Yellow Belt' and current_stripe_ == 'IIIº Stripe':
            return 'Graduar Aluno IVº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Yellow Belt' and current_stripe_ == 'IVº Stripe':
            return 'Graduar Aluno Faixa Amarela/Preta'
            
        # Yellow/Black Belt
        elif new_attendance_ >= 30 and current_belt_ == 'Yellow/Black Belt' and current_stripe_ == 'No Stripes':
            return 'Graduar Aluno Iº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Yellow/Black Belt' and current_stripe_ == 'Iº Stripe':
            return 'Graduar Aluno IIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Yellow/Black Belt' and current_stripe_ == 'IIº Stripe':
            return 'Graduar Aluno IIIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Yellow/Black Belt' and current_stripe_ == 'IIIº Stripe':
            return 'Graduar Aluno IVº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Yellow/Black Belt' and current_stripe_ == 'IVº Stripe':
            return 'Graduar Aluno Faixa Laranja/Branca'
            
        # Orange/White Belt
        elif new_attendance_ >= 30 and current_belt_ == 'Orange/White Belt' and current_stripe_ == 'No Stripes':
            return 'Graduar Aluno Iº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Orange/White Belt' and current_stripe_ == 'Iº Stripe':
            return 'Graduar Aluno IIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Orange/White Belt' and current_stripe_ == 'IIº Stripe':
            return 'Graduar Aluno IIIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Orange/White Belt' and current_stripe_ == 'IIIº Stripe':
            return 'Graduar Aluno IVº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Orange/White Belt' and current_stripe_ == 'IVº Stripe':
            return 'Graduar Aluno Faixa Laranja'
            
        # Orange Belt
        elif new_attendance_ >= 30 and current_belt_ == 'Orange Belt' and current_stripe_ == 'No Stripes':
            return 'Graduar Aluno Iº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Orange Belt' and current_stripe_ == 'Iº Stripe':
            return 'Graduar Aluno IIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Orange Belt' and current_stripe_ == 'IIº Stripe':
            return 'Graduar Aluno IIIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Orange Belt' and current_stripe_ == 'IIIº Stripe':
            return 'Graduar Aluno IVº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Orange Belt' and current_stripe_ == 'IVº Stripe':
            return 'Graduar Aluno Faixa Laranja/Preta'
            
        # Orange/Black Belt
        elif new_attendance_ >= 30 and current_belt_ == 'Orange/Black Belt' and current_stripe_ == 'No Stripes':
            return 'Graduar Aluno Iº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Orange/Black Belt' and current_stripe_ == 'Iº Stripe':
            return 'Graduar Aluno IIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Orange/Black Belt' and current_stripe_ == 'IIº Stripe':
            return 'Graduar Aluno IIIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Orange/Black Belt' and current_stripe_ == 'IIIº Stripe':
            return 'Graduar Aluno IVº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Orange/Black Belt' and current_stripe_ == 'IVº Stripe':
            return 'Graduar Aluno Faixa Verde/Branca'
            
        # Green/White Belt
        elif new_attendance_ >= 30 and current_belt_ == 'Green/White Belt' and current_stripe_ == 'No Stripes':
            return 'Graduar Aluno Iº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Green/White Belt' and current_stripe_ == 'Iº Stripe':
            return 'Graduar Aluno IIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Green/White Belt' and current_stripe_ == 'IIº Stripe':
            return 'Graduar Aluno IIIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Green/White Belt' and current_stripe_ == 'IIIº Stripe':
            return 'Graduar Aluno IVº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Green/White Belt' and current_stripe_ == 'IVº Stripe':
            return 'Graduar Aluno Faixa Verde'
            
        # Green Belt
        elif new_attendance_ >= 30 and current_belt_ == 'Green Belt' and current_stripe_ == 'No Stripes':
            return 'Graduar Aluno Iº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Green Belt' and current_stripe_ == 'Iº Stripe':
            return 'Graduar Aluno IIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Green Belt' and current_stripe_ == 'IIº Stripe':
            return 'Graduar Aluno IIIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Green Belt' and current_stripe_ == 'IIIº Stripe':
            return 'Graduar Aluno IVº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Green Belt' and current_stripe_ == 'IVº Stripe':
            return 'Graduar Aluno Faixa Verde/Preta'
            
        # Green/Black Belt
        elif new_attendance_ >= 30 and current_belt_ == 'Green/Black Belt' and current_stripe_ == 'No Stripes':
            return 'Graduar Aluno Iº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Green/Black Belt' and current_stripe_ == 'Iº Stripe':
            return 'Graduar Aluno IIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Green/Black Belt' and current_stripe_ == 'IIº Stripe':
            return 'Graduar Aluno IIIº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Green/Black Belt' and current_stripe_ == 'IIIº Stripe':
            return 'Graduar Aluno IVº Stripe'
        elif new_attendance_ >= 30 and current_belt_ == 'Green/Black Belt' and current_stripe_ == 'IVº Stripe':
            return 'Graduar Aluno Faixa Azul'

    return None
