import django_filters
from django import forms
from django.forms import TextInput

from .models import Aluno, Graduation, Venda


class AlunoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(field_name="nome", lookup_expr="contains", label='Nome', widget=TextInput(attrs={
        'placeholder': ' Search'}))

    class Meta:
        model = Aluno
        fields = ['nome', 'location']


class AlunoFilterBranch(django_filters.FilterSet):
    nome = django_filters.CharFilter(field_name="nome", lookup_expr="contains", label='Nome', widget=TextInput(attrs={
        'placeholder': ' Search'}))

    class Meta:
        model = Aluno
        fields = ['nome']


class SalesFilter(django_filters.FilterSet):

    class Meta:
        model = Venda
        fields = ['aluno', 'time_stamp']



