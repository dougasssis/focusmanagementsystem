from django.contrib import admin
from .models import Aluno, CustomUser, GetAttendance, Graduation, GraduationRequirement, StudentFeedback
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


@admin.register(GraduationRequirement)
class GraduationRequirementAdmin(admin.ModelAdmin):
    list_display = ('belt', 'stripes', 'required_classes', 'last_modified')
    list_filter = ('belt',)
    search_fields = ('belt',)
    ordering = ('belt', 'stripes')
    fieldsets = (
        (None, {
            'fields': ('belt', 'stripes', 'required_classes')
        }),
        ('Additional Information', {
            'fields': ('modified_by',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Set the modified_by field to the current user
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)


class StudentFeedbackAdmin(admin.ModelAdmin):
    list_display = ('student', 'professor_name', 'related_to_graduation', 'created_at')
    list_filter = ('related_to_graduation', 'created_at')
    search_fields = ('student__nome', 'professor_name', 'content')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('student', 'author', 'professor_name', 'content')
        }),
        ('Graduation Related', {
            'fields': ('related_to_graduation', 'related_graduation')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(GetAttendance, GetAttendanceAdmin)
admin.site.register(Graduation, GraduationAdmin)
admin.site.register(StudentFeedback, StudentFeedbackAdmin)
