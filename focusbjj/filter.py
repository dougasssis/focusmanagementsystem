import django_filters
from django import forms
from django.forms import TextInput

from .models import Aluno, Graduation, Venda, ProductsList


class AlunoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(field_name="nome", lookup_expr="icontains", label='Nome', widget=TextInput(attrs={
        'placeholder': ' Search'}))

    class Meta:
        model = Aluno
        fields = ['nome', 'location']


class AlunoFilterBranch(django_filters.FilterSet):
    nome = django_filters.CharFilter(field_name="nome", lookup_expr="icontains", label='Nome', widget=TextInput(attrs={
        'placeholder': ' Search'}))

    class Meta:
        model = Aluno
        fields = ['nome']


class SalesFilter(django_filters.FilterSet):

    class Meta:
        model = Venda
        fields = ['aluno', 'time_stamp']


class ProductsFilter(django_filters.FilterSet):
    item = django_filters.CharFilter(field_name="item", lookup_expr="icontains", label='Item', widget=TextInput(attrs={
        'placeholder': ' Search'}))

    class Meta:
        model = ProductsList
        fields = ['item', 'category']
