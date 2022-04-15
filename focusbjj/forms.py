from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.utils.translation import gettext as _, get_language, activate
from focusbjj.models import GetAttendance, Aluno, Venda, Graduation, Product, Championship, ProductsList, CustomUser
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
            'username': "Nome de Utilizador",
            'password': "Password",
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

    class Meta:
        model = Aluno
        fields = ['photo', 'nome', 'surname', 'email', 'address', 'phone', 'gender', 'dob', 'location',
                  'belt', 'stripe']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primeiro Nome'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sobrenome'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'email@focus.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(00)000000000'}),
            'dob': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'address': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control',
                                                                 'placeholder': 'R. da Alegria, 123, Matosinhos, Portugal',
                                                                 }),
        }

        labels = {
            'photo': 'Foto',
            'nome': 'Nome',
            'surname': 'Último Nome',
            'phone': 'Telefone',
            'address': 'Endereço',
            'dob': 'Data de Nascimento',
            'location': 'Unidade',
            'belt': 'Faixa',
            'stripe': 'Grau',
        }


class ProductForm(forms.ModelForm):
    template_name = "add_product"

    class Meta:
        model = ProductsList
        fields = ['image', 'item', 'description', 'price', 'sugg_price']

        labels = {
            'sugg_price': 'Preço de Venda',
            'description': 'Descrição',
            'price': 'Preço',
            'image': 'Imagem',

        }


class VendaForm(forms.ModelForm):
    template_name = "add_venda__"

    class Meta:
        model = Venda
        fields = ['aluno', 'method', 'price']
        widgets = {
            'aluno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insert Member ID'}),
        }
        labels = {
            'aluno': 'Aluno',
            'method': 'Método de Pagamento',
            'price': 'Valor Total',
        }


ProductFormset = inlineformset_factory(Venda, Product, form=ProductForm, fields=['product', 'qtd'], extra=1,
                                       can_delete=False, )


class GraduateForm(forms.ModelForm):
    template_name = "graduation"

    class Meta:
        model = Graduation
        fields = ['belt', 'stripe']

        label = {
            'belt': 'Faixa',
            'stripe': 'Grau'
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
            'athlete': 'Aluno',
            'date': 'Data',
            'championship': 'Campeonato',
            'country': 'País',
            'city': 'Cidade',
            'category': 'Categoria',
            'weight': 'Peso',
            'ranking': 'Colocação,'
        }


class EditBranchForm(forms.ModelForm):
    template_name = "editarbranch.html"

    class Meta:
        model = CustomUser
        fields = ['contact_name', 'email', 'phone']

        labels = {
            'contact_name': 'Nome de Contato',
            'phone': 'Telefone'
        }


class EditAtlheteForm(forms.ModelForm):
    template_name = "editaralunos.html"

    class Meta:
        model = Aluno
        fields = ['nome', 'email', 'phone']

        labels = {
            'nome': 'Nome de Contato',
            'phone': 'Telefone'
        }
