import django_filters
from django import forms
from django_filters import FilterSet
from django.forms import TextInput

from .models import Aluno, Graduation, BELT
from focusbjj.templatetags.attendance_tags import current_belt


class AlunoFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(field_name="nome", lookup_expr="icontains", label='Nome', widget=TextInput(attrs={
        'placeholder': ' Search'}))
    belt = django_filters.ChoiceFilter(choices=BELT, label='Belt', method='filter_by_current_belt')

    def filter_by_current_belt(self, queryset, name, value):
        if not value:
            return queryset
            
        # Create a list to hold matching student IDs
        matching_ids = []
        
        # Check each student individually
        for aluno in queryset:
            # Get the current belt for this student
            student_belt = current_belt(aluno)
            
            # Handle different belt format possibilities:
            # 1. Exact match (e.g., "White" == "White")
            # 2. With "Belt" suffix (e.g., "White" matches "White Belt")
            # 3. Case-insensitive comparison
            if (student_belt == value or 
                student_belt == f"{value} Belt" or 
                (value.endswith(" Belt") and student_belt == value[:-5])):
                matching_ids.append(aluno.id)
                
        # Return a queryset filtered by the matching IDs
        return queryset.filter(id__in=matching_ids)

    class Meta:
        model = Aluno
        fields = ['nome', 'location', 'belt']


class AlunoFilterBranch(django_filters.FilterSet):
    nome = django_filters.CharFilter(field_name="nome", lookup_expr="icontains", label='Nome', widget=TextInput(attrs={
        'placeholder': ' Search'}))
    belt = django_filters.ChoiceFilter(choices=BELT, label='Belt', method='filter_by_current_belt')

    def filter_by_current_belt(self, queryset, name, value):
        if not value:
            return queryset
            
        # Create a list to hold matching student IDs
        matching_ids = []
        
        # Check each student individually
        for aluno in queryset:
            # Get the current belt for this student
            student_belt = current_belt(aluno)
            
            # Handle different belt format possibilities
            if (student_belt == value or 
                student_belt == f"{value} Belt" or 
                (value.endswith(" Belt") and student_belt == value[:-5])):
                matching_ids.append(aluno.id)
                
        # Return a queryset filtered by the matching IDs
        return queryset.filter(id__in=matching_ids)

    class Meta:
        model = Aluno
        fields = ['nome', 'belt'] 