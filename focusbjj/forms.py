from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.utils.translation import gettext as _, get_language, activate
from focusbjj.models import GetAttendance, Aluno, Graduation, CustomUser, \
    GraduationRequirement, StudentFeedback
from django.contrib.auth import get_user_model

User = get_user_model()


class AttendForm(forms.ModelForm):
    template_name = 'homepage.html'

    class Meta:
        model = GetAttendance
        fields = ['aluno']
        widgets = {
            'aluno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insert Member ID'})
        }
        labels = {
            'aluno':  _("INSIRA O SEU ID" )
        }


class LoginForm(forms.Form):
    class Meta:
        fields = ['username', 'password']
        labels = {
            'username': _("Usuário"),
            'password': _("Password"),
        }


class RegisterStaffForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'contact_name', 'email', 'phone', 'country', 'location', 'password1', 'password2']
        widgets = {
            'contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name and Last Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email@focus.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country Code + Phone Number'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City', 'label': 'City'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'focus+city Ex: focusporto'}),
        }
        labels = {
            "contact_name": "Nome de Contato",
            'location': 'Cidade',
            'phone': 'Telefone',
            'username': 'Nome de Usuário',
            'country': 'País',
        }


class RegisterAlunoForm(forms.ModelForm):
    template_name = "add_aluno"
    agreement = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label=_('I have read and accept the Privacy Policy and Personal Data Protection Policy'),
        help_text=_('You must accept the terms to register a student')
    )

    class Meta:
        model = Aluno
        fields = ['photo', 'nome', 'middle_name', 'surname', 'email', 'address', 'phone', 'gender', 'dob',
                  'belt', 'stripe', 'join_date', 'agreement']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Primeiro Nome')}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Nome do Meio')}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Sobrenome')}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email@focus.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00)000000000'}),
            'dob': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'join_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'address': forms.TextInput(attrs={'class': 'form-control',
                                           'placeholder': 'R. da Alegria, 123, Matosinhos, Portugal',
                                           }),
        }

        labels = {
            'photo': _('Foto'),
            'nome': _('Nome'),
            'middle_name': _('Nome do Meio'),
            'surname': _('Último Nome'),
            'phone': _('Telefone'),
            'address': _('Endereço'),
            'dob': _('Data de Nascimento'),
            'belt': _('Faixa'),
            'stripe': _('Grau'),
            'join_date': _('Data de Início'),
        }

        help_texts = {
            'email': _('Digite o endereço corretamente.'),
        }

    def clean_agreement(self):
        agreement = self.cleaned_data.get('agreement')
        if not agreement:
            raise forms.ValidationError(_('You must accept the terms and conditions to register a student.'))
        return agreement


class GraduateForm(forms.ModelForm):
    template_name = "graduation"

    class Meta:
        model = Graduation
        fields = ['belt', 'stripe', 'master', 'time_stamp']

        widgets = {
            'belt': forms.Select(attrs={'class': 'form-control'}),
            'stripe': forms.Select(attrs={'class': 'form-control'}),
            'master': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Professor')}),
            'time_stamp': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'belt': _('New Belt'),
            'stripe': _('New Stripe'),
            'master': _('Graduating Professor'),
            'time_stamp': _('Graduation Date'),
        }


class EditBranchFormSuper(forms.ModelForm):
    template_name = "editarbranch.html"

    class Meta:
        model = CustomUser
        fields = ['contact_name', 'email', 'phone', 'is_active']

        labels = {
            'contact_name': _('Nome de Contato'),
            'phone': _('Telefone'),
            'is_active': _('Usuário Ativo')
        }


class EditBranchForm(forms.ModelForm):
    template_name = "editarbranch.html"

    class Meta:
        model = CustomUser
        fields = ['contact_name', 'email', 'phone']

        labels = {
            'contact_name': _('Nome de Contato'),
            'phone': _('Telefone'),
        }


class EditAtlheteForm(forms.ModelForm):
    template_name = "editaralunos.html"

    class Meta:
        model = Aluno
        fields = ['photo', 'nome', 'middle_name', 'surname', 'dob', 'email', 'phone', 'address']
        widgets = {
            'join_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
          }


        labels = {
            'photo': _('Foto'),
            'nome': _('Nome de Contato'),
            'middle_name': _('Nome do Meio'),
            'surname': _('Último Nome'),
            'phone': _('Telefone'),
            'email': _('E-Mail'),
            'address': _('Endereço'),
            'dob': _('Data de Nascimento'),
          
        }


# Add new form for graduation requirements
class GraduationRequirementForm(forms.ModelForm):
    class Meta:
        model = GraduationRequirement
        fields = ['belt', 'stripes', 'required_classes']
        widgets = {
            'required_classes': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '999'})
        }


class StudentFeedbackForm(forms.ModelForm):
    """Form for creating and editing student feedback"""
    
    class Meta:
        model = StudentFeedback
        fields = ['professor_name', 'content', 'related_to_graduation']
        widgets = {
            'professor_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Enter your name as professor/instructor')}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': _('Enter feedback for the student')}),
            'related_to_graduation': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'professor_name': _('Professor Name'),
            'content': _('Feedback'),
            'related_to_graduation': _('Related to Graduation')
        }
        help_texts = {
            'professor_name': _('Your name as the professor giving feedback'),
            'content': _('Provide constructive feedback for the student'),
            'related_to_graduation': _('Check if this feedback is related to a graduation')
        }
