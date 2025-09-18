from datetime import date, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django_countries.fields import CountryField
from django import template
from shortuuid.django_fields import ShortUUIDField
from django.utils.translation import gettext as _
from cloudinary.models import CloudinaryField


register = template.Library()

BELT = (
    ('White', 'White'),
    ('Gray/White', 'Gray/White'),
    ('Gray', 'Gray'),
    ('Gray/Black', 'Gray/Black'),
    ('Yellow/White', 'Yellow/White'),
    ('Yellow', 'Yellow'),
    ('Yellow/Black', 'Yellow/Black'),
    ('Orange/White', 'Orange/White'),
    ('Orange', 'Orange'),
    ('Orange/Black', 'Orange/Black'),
    ('Green/White', 'Green/White'),
    ('Green', 'Green'),
    ('Green/Black', 'Green/Black'),
    ('Blue', 'Blue'),
    ('Purple', 'Purple'),
    ('Brown', 'Brown'),
    ('Black', 'Black'),
)

GRAU = (
    ('No Stripes', 'No Stripes'),
    ('Iº Stripe', 'Iº Stripe'),
    ('IIº Stripe', 'IIº Stripe'),
    ('IIIº Stripe', 'IIIº Stripe'),
    ('IVº Stripe', 'IVº Stripe')
)

GENDER = (
    ('Female', _('Feminino')),
    ('Male', _('Masculino')),
)

METHODS = (
    ('Credit', _('Cartão de Crédito')),
    ('Debit', _('Cartão de Débito')),
    ('Cash', _('Dinheiro')),
    ('Others', _('Outros'))
)


class CustomUser(AbstractUser):
    id = ShortUUIDField(primary_key=True, editable=False, alphabet="0123456789", length=3)
    email = models.EmailField(max_length=255, unique=True)
    contact_name = models.CharField(max_length=255)
    country = CountryField()
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, help_text=_('Use somente números. Código do País + Telefone'))
    join_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True, help_text='Desmarque a caixa para desativar')

    def __str__(self):
        return str(self.country) + " - " + str(self.location)

    class Meta:
        ordering = ["country", "location"]


class Aluno(models.Model):
    DoesNotExist = None
    objects = None
    id = ShortUUIDField(primary_key=True, editable=False, alphabet="0123456789", length=4)
    photo = CloudinaryField('photo', blank=True, null=True)
    nome = models.CharField(max_length=15, verbose_name='Name')
    middle_name = models.CharField(max_length=20, verbose_name='Middle Name', blank=True, null=True)
    surname = models.CharField(max_length=15, verbose_name='Last Name', null=True)
    phone = models.CharField(max_length=15, help_text='Use only numbers')
    email = models.EmailField(max_length=128)
    location = models.ForeignKey(CustomUser, related_name="alunos", on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    belt = models.CharField(max_length=255, choices=BELT)
    stripe = models.CharField(max_length=255, choices=GRAU, default= 'No Stripes')
    join_date = models.DateTimeField()
    time_stamp = models.DateTimeField(auto_now=True, null=True)
    gender = models.CharField(max_length=255, choices=GENDER)
    dob = models.DateField(verbose_name='Date of Birth',)
    is_blocked = models.BooleanField(default=False)
    agreement = models.BooleanField(default=False)

    USERNAME_FIELD = 'id'

    def __str__(self):
        return self.nome + " - " + str(self.location.location)

    def idade(self): #POR ANO DE NASCIMENTO
        today = date.today()
        idade = today.year - self.dob.year #- ((today.month, today.day) < (self.dob.month, self.dob.day))
        return idade

    @property
    def unidade(self):
        return self.location.country + self.location.location

    class Meta:
        ordering = ["nome"]

class GetAttendance(models.Model):
    objects = None
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name='Athlete')
    attendance = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.aluno) + " - " + str(self.attendance)


class Graduation(models.Model):
    objects = None
    aluno = models.ForeignKey(Aluno, related_name='graduacao', on_delete=models.CASCADE, verbose_name='_(Aluno')
    master = models.CharField(max_length=15, null=True, verbose_name=_('Professor'))
    belt = models.CharField(max_length=255, choices=BELT, verbose_name=_('Faixa'))
    stripe = models.CharField(max_length=255, choices=GRAU, verbose_name=_('Grau'))
    time_stamp = models.DateTimeField(null=True, verbose_name=_('Data'))

    def __str__(self):
        return str(self.belt)


class GraduationRequirement(models.Model):
    """
    Model to define attendance requirements for belt promotions
    """
    BELT_CHOICES = [
        ('White', 'White'),
        ('Gray/White', 'Gray/White'),
        ('Gray', 'Gray'),
        ('Gray/Black', 'Gray/Black'),
        ('Yellow/White', 'Yellow/White'),
        ('Yellow', 'Yellow'),
        ('Yellow/Black', 'Yellow/Black'),
        ('Orange/White', 'Orange/White'),
        ('Orange', 'Orange'),
        ('Orange/Black', 'Orange/Black'),
        ('Green/White', 'Green/White'),
        ('Green', 'Green'),
        ('Green/Black', 'Green/Black'),
        ('Blue', 'Blue'),
        ('Purple', 'Purple'),
        ('Brown', 'Brown'),
        ('Black', 'Black'),
    ]
    
    STRIPE_CHOICES = [
        ('No Stripes', 'No Stripes'),
        ('Iº Stripe', 'Iº Stripe'),
        ('IIº Stripe', 'IIº Stripe'),
        ('IIIº Stripe', 'IIIº Stripe'),
        ('IVº Stripe', 'IVº Stripe'),
    ]
    
    belt = models.CharField(max_length=20, choices=BELT_CHOICES)
    stripes = models.CharField(max_length=15, choices=STRIPE_CHOICES)
    required_classes = models.PositiveIntegerField(help_text="Number of classes required for promotion")
    modified_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['belt', 'stripes']
        ordering = ['belt', 'stripes']
        verbose_name = "Graduation Requirement"
        verbose_name_plural = "Graduation Requirements"
    
    def __str__(self):
        return f"{self.belt} with {self.stripes}: {self.required_classes} classes"


class StudentFeedback(models.Model):
    """
    Model to store feedback for students from instructors
    """
    student = models.ForeignKey(Aluno, related_name='feedback', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    professor_name = models.CharField(max_length=100, blank=True, help_text="Custom name for the professor giving feedback")
    content = models.TextField()
    related_to_graduation = models.BooleanField(default=False, help_text="Is this feedback related to a graduation?")
    related_graduation = models.ForeignKey(Graduation, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Student Feedback"
        verbose_name_plural = "Student Feedback"
        
    def __str__(self):
        return f"Feedback for {self.student.nome} {self.student.surname} by {self.professor_name or self.author.location}"
