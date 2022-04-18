from datetime import date, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django_countries.fields import CountryField
from django import template
from shortuuid.django_fields import ShortUUIDField
from django.utils.translation import gettext as _


register = template.Library()

BELT = (
    ('White Belt', 'White Belt'),
    ('Gray/White Belt', 'Gray/White Belt'),
    ('Gray Belt', 'Gray Belt'),
    ('Gray/Black Belt', 'Gray/Black Belt'),
    ('Yellow/White Belt', 'Yellow/White Belt'),
    ('Yellow Belt', 'Yellow Belt'),
    ('Yellow/Black Belt', 'Yellow/Black Belt'),
    ('Orange/White Belt', 'Orange/White Belt'),
    ('Orange Belt', 'Orange Belt'),
    ('Orange/Black Belt', 'Orange/Black Belt'),
    ('Green/White Belt', 'Green/White Belt'),
    ('Green Belt', 'Green Belt'),
    ('Green/Black Belt', 'Green/Black Belt'),
    ('Blue Belt', 'Blue Belt'),
    ('Purple Belt', 'Purple Belt'),
    ('Brown Belt', 'Brown Belt'),
    ('Black Belt', 'Black Belt'),
)

GRAU = (
    ('No Stripes', 'No Stripes'),
    ('Iº Stripe', 'Iº Stripe'),
    ('IIº Stripe', 'IIº Stripe'),
    ('IIIº Stripe', 'IIIº Stripe'),
    ('IVº Stripe', 'IVº Stripe'),
    ('-------------', '-------------'),
    ('Vº Stripe', 'Vº Stripe'),
    ('VIº Stripe', 'VIº Stripe'),
    ('VIIº Stripe', 'VIIº Stripe'),
    ('VIIIº Stripe', 'VIIIº Stripe'),
    ('IXº Stripe', 'IXº Stripe'),
    ('Xº Stripe', 'Xº Stripe'),
    ('XIº Stripe', 'XIº Stripe'),
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
    phone = models.CharField(max_length=15, help_text='Use only numbers')
    join_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True, help_text='Desmarque a caixa para desativar')

    def __str__(self):
        return str(self.country) + " - " + str(self.location)

    class Meta:
        ordering = ["country"]


class Aluno(models.Model):
    DoesNotExist = None
    objects = None
    id = ShortUUIDField(primary_key=True, editable=False, alphabet="0123456789", length=4)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    nome = models.CharField(max_length=12, verbose_name='Name')
    middle_name = models.CharField(max_length=20, verbose_name='Middle Name', blank=True, null=True)
    surname = models.CharField(max_length=15, verbose_name='Last Name', null=True)
    phone = models.CharField(max_length=15, help_text='Use only numbers')
    email = models.EmailField(max_length=128, unique=True)
    location = models.ForeignKey(CustomUser, related_name="alunos", on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    belt = models.CharField(max_length=255, choices=BELT)
    stripe = models.CharField(max_length=255, choices=GRAU)
    join_date = models.DateTimeField(default=timezone.now)
    gender = models.CharField(max_length=255, choices=GENDER)
    dob = models.DateField(verbose_name='Date of Birth')

    USERNAME_FIELD = 'id'

    def __str__(self):
        return self.nome + " - " + str(self.location.location)

    def idade(self):
        today = date.today()
        idade = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return idade

    class Meta:
        ordering = ["nome"]


class GetAttendance(models.Model):
    objects = None
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name='Athlete')
    attendance = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.aluno) + ' - ' + str(self.attendance)


class Venda(models.Model):
    objects = None
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Total', help_text='Use (.) to decimals')
    time_stamp = models.DateField(default=timezone.now)
    unidade = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=METHODS, default='Others')

    def __str__(self):
        return str(self.aluno) + str(self.time_stamp)


class ProductsList(models.Model):
    CATEGORY=(
        ('kimono', _('Gi')),
        ('belt', _('Belt')),
        ('camisetas',_('T-Shirt')),
        ('casaco', _('Hoodie')),
        ('rash', _('Rash Guard')),
        ('short', _('Short')),
        ('others', _('Others')),
    )
    objects = None
    image = models.ImageField(upload_to='produtos/')
    image2 = models.ImageField(upload_to='produtos/', blank=True, null=True, help_text='Opcional')
    image3 = models.ImageField(upload_to='produtos/', blank=True, null=True, help_text='Opcional')
    item = models.CharField(max_length=50)
    description = models.CharField(max_length=70, blank=True, null=True)
    price = models.CharField(max_length=6, null=True)
    category = models.CharField(max_length=10, choices=CATEGORY, null=True)
    sugg_price = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return str(self.item)


class Product(models.Model):
    objects = None
    product = models.ForeignKey(ProductsList, on_delete=models.CASCADE, max_length=50, related_name='produto',
                                verbose_name='Item')
    qtd = models.PositiveIntegerField(verbose_name='Quantidade')
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, null=True, related_name='venda')
    price = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return str(self.product)


class Graduation(models.Model):
    objects = None
    aluno = models.ForeignKey(Aluno, related_name='graduacao', on_delete=models.CASCADE, verbose_name='Athlete')
    master = models.CharField(max_length=15, null=True)
    belt = models.CharField(max_length=255, choices=BELT)
    stripe = models.CharField(max_length=255, choices=GRAU)
    time_stamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.belt)


WEIGHT = (
    ('rooster', 'Rooster'),
    ('light feather', 'Light Feather'),
    ('feather', 'Feather'),
    ('light', 'Light'),
    ('middle', 'Middle'),
    ('middle_heavy', 'Middle Heavy'),
    ('heavy', 'Heavy'),
    ('super_heavy', 'Super Heavy'),
    ('ultra_heavy', 'Ultra Heavy'),
    ('open', 'Open'),
)

CATEGORY = (
    ('juvenile', _('Juvenil')),
    ('adult', _('Adulto/Master')),
)

RANKING = (
    ('first place', _('Primeiro Lugar')),
    ('second place', _('Segundo Lugar')),
    ('third place', _('Teceiro Lugar')),
)


class Championship(models.Model):
    objects = None
    athlete = models.ForeignKey(Aluno, related_name='campeonato', on_delete=models.CASCADE)
    championship = models.CharField(max_length=50)
    date = models.DateField(null=True)
    country = CountryField()
    city = models.CharField(max_length=30)
    category = models.CharField(max_length=20, choices=CATEGORY)
    weight = models.CharField(max_length=20, choices=WEIGHT)
    ranking = models.CharField(max_length=20, choices=RANKING)

    def __str__(self):
        return str(self.athlete) + " - " + str(self.championship)


class Posts(models.Model):
    CATEGORY = (
        ('newyear', _('Ano Novo')),
        ('xmas', _('Natal')),
        ('easter', _('Páscoa')),
        ('father', _('Dia dos Pais')),
        ('mother', _('Dia das Mães')),
        ('kids', _('Dia das Crianças')),
        ('women', _('Dia da Mulher')),
        ('others', _('Outros')),
    )

    objects = None
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=20, default='others', choices=CATEGORY, null=True, blank=True)
    image = models.ImageField(upload_to='socialmedia', )
    timestamp = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    def year(self):
        return self.timestamp.year