from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_view


app_name = 'focusbjj'

urlpatterns = [
    path('', views.Attendance.as_view(), name='homepage'),
    path('home/', views.HomeView.as_view(), name='filiais'),
    path('add_aluno/', views.RegisterAlunoView.as_view(), name='add_aluno'),
    path('managealunos/<int:pk>', views.DetailALunos.as_view(), name='alunos'),
    path('managealunos/', views.ManageAlunos.as_view(), name='managealunos'),
    path('managealunos/kids', views.ManageAlunosKids.as_view(), name='managealunoskids'),
    path('managealunos/total', views.ManageAlunosTotal.as_view(), name='managealunostotal'),
    path('managealunos/graduation', views.ManageGraduationTotal.as_view(), name='managegraduation'),
    path('add_branch/', views.RegisterStaffView.as_view(), name='add_staff'),
    path('managebranch/', views.ManageStaff.as_view(), name='managestaff'),
    path('managebranch/<int:pk>', views.DetailBranch.as_view(), name='branchdetails'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('editaralunos/<int:pk>', views.EditarAluno.as_view(), name='editaralunos'),
    path('editbranch/<int:pk>', views.EditarBranch.as_view(), name='editarstaff'),
    path('editbranch//editpassword/', auth_view.PasswordChangeView.as_view(
        template_name='editarbranch.html', success_url=reverse_lazy('attendance:password_done')),
        name='mudarsenha'),
    path('password_change_done/', auth_view.PasswordChangeView.as_view(
        template_name='editarbranch.html', success_url=reverse_lazy('attendance:filiais')),
         name='password_done'),
    path('addproduct/', views.AddProduct.as_view(), name='addproduct'),
    path('addvenda/', views.AddVenda.as_view(), name='addvenda'),
    path('graduation/<int:pk>', views.Graduate.as_view(), name='graduation'),
    path('vendas/<int:pk>', views.SalesList.as_view(), name='vendas'),
    path('saledetails/<int:pk>', views.SaleDetails.as_view(), name='saledetails'),
    path('products/', views.ProductList.as_view(), name='products'),
    path('championship/', views.AddChampionship.as_view(), name='championship'),
    path('championshipdetails/', views.ChampionshipDetail.as_view(), name='championshipdetails'),
    path('editproduct/<int:pk>', views.EditProduct.as_view(), name='editproduct'),
    path('socialmedia/', views.SocialMedia.as_view(), name='socialmedia'),
    path('socialmedia/add', views.AddSocialMedia.as_view(), name='addsocialmedia'),
    path('socialmedia/update/<int:pk>', views.UpdateSocialMedia.as_view(), name='updatesocialmedia'),
    path('socialmedia/delete/<int:pk>', views.DeleteSocialMedia.as_view(), name='deletesocialmedia'),
    path('deleteproduct/<int:pk>', views.ProductDeleteView.as_view(), name='deleteproduct'),
    path('resetpassword/', auth_view.PasswordResetView.as_view(
        template_name='password_reset.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_view.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/set-password/', auth_view.PasswordResetConfirmView.as_view(
        template_name='password_reset_form.html'),name='password_reset_confirm'),
    path('resetpassword_complete/', auth_view.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'), name='password_reset_complete'),

]