from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.utils.translation import gettext as _, get_language, activate
from focusbjj.models import GetAttendance, Aluno, Venda, Graduation, Product, Championship, ProductsList, CustomUser, \
    Posts, GraduationRequirement, StudentFeedback
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


class ProductForm(forms.ModelForm):
    template_name = "add_product"

    class Meta:
        model = ProductsList
        fields = ['image', 'image2', 'image3','item', 'description', 'category', 'price', 'sugg_price']

        labels = {
            'sugg_price': _('Preço de Venda'),
            'description': _('Descrição'),
            'price': _('Preço'),
            'image': _('Imagem Principal'),
            'image2': _('Imagem 2'),
            'image3': _('Imagem 3'),
            'category': _('Categoria'),
        }


class VendaForm(forms.ModelForm):
    template_name = "add_venda__"

    class Meta:
        model = Venda
        fields = ['aluno', 'method', 'price']
        widgets = {
            'aluno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Insira o ID do Aluno')}),
        }
        labels = {
            'aluno': _('Aluno'),
            'method': _('Método de Pagamento'),
            'price': _('Valor Total'),
        }
        help_texts = {
            'aluno': _('Opcional'),
            'price': _('Use " . "(ponto) para separar decimais.'),
        }


ProductFormset = inlineformset_factory(Venda, Product, form=ProductForm, fields=['product', 'qtd'], extra=1,
                                       can_delete=False, )


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


class RegisterChampionship(forms.ModelForm):
    template_name = "campeonatos.html"

    class Meta:
        model = Championship
        fields = "__all__"

        widgets = {
            'athlete': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insert Member ID'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email@focus.com'}),
            'date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

        labels = {
            'athlete': _('Aluno'),
            'date': _('Data'),
            'championship': _('Campeonato'),
            'country': _('País'),
            'city': _('Cidade'),
            'category': _('Categoria'),
            'weight': _('Peso'),
            'ranking': _('Colocação'),
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


class SocialMediaForm(forms.ModelForm):
    template_name = 'add_socialmedia.html'

    class Meta:
        model = Posts
        fields = ['image', 'title']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do Evento'}),
        }

        labels = {
            'image': 'Image',
            'title': 'Título',
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
