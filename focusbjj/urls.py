from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_view
from django.views.decorators.csrf import csrf_protect
from django.views.generic import RedirectView


app_name = 'focusbjj'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('check-in/', views.Attendance.as_view(), name='homepage'),
    path('home/', views.HomeView.as_view(), name='filiais'),
    path('add_aluno/', views.RegisterAlunoView.as_view(), name='add_aluno'),
    path('managealunos/<int:pk>', views.DetailALunos.as_view(), name='alunos'),
    path('managealunos/', views.ManageAlunos.as_view(), name='managealunos'),
    path('managealunoskids/', RedirectView.as_view(url='/managealunos/?category=kids', permanent=True), name='managealunoskids'),
    path('managealunos/delete/<int:pk>', views.AlunotDeleteView.as_view(), name='deletealunos'),
    path('managealunos/total', views.ManageAlunosTotal.as_view(), name='managealunostotal'),
    path('managealunos/graduation', views.ManageGraduationTotal.as_view(), name='managegraduation'),
    path('student-checkin/<int:pk>/', views.StudentCheckIn.as_view(), name='student_checkin'),
    path('graduation-requirements/', views.GraduationRequirementsView.as_view(), name='graduation_requirements'),
    path('graduation-requirements/update/', views.UpdateGraduationRequirementView.as_view(), name='update_graduation_requirements'),
    path('graduation-eligibility/', views.GraduationEligibilityView.as_view(), name='graduation_eligibility'),
    path('add_branch/', views.RegisterStaffView.as_view(), name='add_staff'),
    path('managebranch/', views.ManageStaff.as_view(), name='managestaff'),
    path('managebranch/<int:pk>', views.DetailBranch.as_view(), name='branchdetails'),
    path('logout/', auth_view.LogoutView.as_view(next_page=reverse_lazy('focusbjj:login')), name='logout'),
    path('editaralunos/<int:pk>', views.EditarAluno.as_view(), name='editaralunos'),
    path('editbranch/<int:pk>', views.EditarBranch.as_view(), name='editarstaff'),
    path('editbranch/super/<int:pk>', views.EditarBranchSuper.as_view(), name='editarstaffsuper'),
    path('editbranch/editpassword/', auth_view.PasswordChangeView.as_view(
        template_name='editarbranch.html', success_url=reverse_lazy('focusbjj:password_done')),
        name='mudarsenha'),
    path('password_change_done/', auth_view.PasswordChangeView.as_view(
        template_name='editarbranch.html', success_url=reverse_lazy('focusbjj:filiais')),
         name='password_done'),
    path('graduation/<int:pk>', views.Graduate.as_view(), name='graduation'),
    path('resetpassword/', auth_view.PasswordResetView.as_view(
        template_name='password_reset.html',
        success_url=reverse_lazy('focusbjj:password_reset_done')), 
        name='password_reset'),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), 
        name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(
        template_name='password_reset_form.html',
        success_url=reverse_lazy('focusbjj:password_reset_complete')),
        name='password_reset_confirm'),
    path('password_reset/complete/', auth_view.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    path('export/xlsx', views.exportar_alunos_xlsx, name='export_xlsx'),
    path('export/total_xlsx', views.exportar_alunos_total_xlsx, name='export_total_xlsx'),
    path('terms/', views.Agreemnet.as_view(), name='terms'),
    path('debug-graduation/<int:pk>', views.GraduationDebugView.as_view(), name='debug_graduation'),
]

