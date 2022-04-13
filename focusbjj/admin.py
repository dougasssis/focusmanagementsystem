from django.contrib import admin
from .models import Aluno, CustomUser, GetAttendance, Product, Venda, Graduation, Championship, ProductsList
from django.contrib.auth.admin import UserAdmin

campos = list(UserAdmin.fieldsets)
campos.append(
    ("Dados", {'fields': ('contact_name', 'phone', 'country', 'location',)})
)
UserAdmin.fieldsets = tuple(campos)


class AlunoAdmin(admin.ModelAdmin):
    list_filter = ('location', 'belt', 'gender', 'join_date')
    list_display = ('nome', 'surname', 'location')


class GetAttendanceAdmin(admin.ModelAdmin):
    list_filter = ('aluno',)


class GraduationAdmin(admin.ModelAdmin):
    list_filter = ('aluno',)
    list_display = ('aluno', 'belt', 'stripe')


class ChampionshiopAdmin(admin.ModelAdmin):
    list_filter = ('athlete', 'championship', 'ranking')
    list_display = ('athlete','championship','ranking')


class ProductInline(admin.TabularInline):
    model = Product


class VendaAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline
    ]
    list_display = ('aluno','unidade')


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(GetAttendance, GetAttendanceAdmin)
admin.site.register(Product)
admin.site.register(ProductsList)
admin.site.register(Venda, VendaAdmin)
admin.site.register(Graduation, GraduationAdmin)
admin.site.register(Championship, ChampionshiopAdmin)
