import datetime
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.urls import reverse
from django.views.generic import FormView, DetailView, ListView, UpdateView, CreateView, TemplateView, DeleteView
from focusbjj.forms import *
from focusbjj.models import *
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .filter import AlunoFilter, ProductsFilter
from .templatetags.attendance_tags import current_belt, current_stripe
import xlwt
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError


class Attendance(FormView):
    template_name = 'homepage.html'
    model = GetAttendance
    form_class = AttendForm
    success_msg = _("Check in efetuado com sucesso")
    errormsg = _("Aluno está bloqueado. Procure a gerência.")
    errormsg2 = _("Check in já efetuado. Você poderá fazer novo check in na próxima aula ou em 3 horas.")

    def form_valid(self, form):
        form.save(commit=False)
        aluno = form.instance.aluno
        att = GetAttendance.objects.filter(aluno=aluno.id).order_by('-attendance')

        if aluno.is_blocked:
            errormsg = self.error_msg()
            if errormsg:
                messages.error(self.request, errormsg)
                form.save(False)
        elif att:
            last_attendance = att[0].attendance
            if last_attendance + timedelta(hours=3) > timezone.now():
                errormsg2 = self.error_msg2()
                if errormsg2:
                    messages.error(self.request, errormsg2)
                    form.save(False)
            else:
                form.save()
                success_msg = self.get_success_message(form.cleaned_data)
                if success_msg:
                    messages.success(self.request, success_msg)
        else:
            form.save()
            success_msg = self.get_success_message(form.cleaned_data)
            if success_msg:
                messages.success(self.request, success_msg)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        att = GetAttendance.objects.order_by('-attendance')[0]
        aluno = att.aluno.nome
        attendance = att.attendance
        data = attendance.strftime('%d/%m/%Y %H:%M:%S')
        return str(aluno) + " " + str(self.success_msg) + " at " + str(data) % cleaned_data

    def get_success_url(self):
        return reverse('focusbjj:homepage')

    def error_msg(self):
        return self.errormsg

    def error_msg2(self):
        return self.errormsg2


class AddProduct(LoginRequiredMixin, CreateView):
    template_name = 'add_product.html'
    model = Product
    form_class = ProductForm
    success_msg = "Product Added Succesfully"

    def form_valid(self, form):
        form.save()
        success_msg = self.get_success_message(form.cleaned_data)
        if success_msg:
            messages.success(self.request, success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('focusbjj:addproduct')

    def get_success_message(self, cleaned_data):
        return self.success_msg % cleaned_data


class AddVenda(LoginRequiredMixin, CreateView):
    template_name = 'add_venda__.html'
    model = Venda
    form_class = VendaForm
    success_msg = "Sale Added Succesfully"

    def get_context_data(self, **kwargs):
        context = super(AddVenda, self).get_context_data()
        context['formset'] = ProductFormset()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = ProductFormset(self.request.POST, instance=form.instance)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        form.instance.unidade = self.request.user
        self.object = form.save(commit=False)
        self.object.save()
        products = formset.save(commit=False)
        for x in products:
            x.venda = self.object
            x.save()
        success_msg = self.get_success_message(form.cleaned_data)
        if success_msg:
            messages.success(self.request, success_msg)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_msg % cleaned_data

    def get_success_url(self):
        return reverse('focusbjj:addvenda')


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'homecontent_.html'
    model = Aluno, CustomUser

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['alunos'] = Aluno.objects.all()
        context['unidades'] = CustomUser.objects.all()
        context['unidades_count'] = CustomUser.objects.all().count() - 2
        context['belts'] = self.get_belts()
        return context

    def get_belts(self):
        alunos = Aluno.objects.all()
        dict_belt = {'white': 0, 'gray_white': 0, 'gray': 0, 'gray_black': 0,
                     'yellow_white': 0, 'yellow': 0, 'yellow_black': 0,
                     'green_white': 0, 'green': 0, 'green_black': 0,
                     'orange_white': 0, 'orange': 0, 'orange_black': 0,
                     'blue': 0, 'purple': 0, 'brown': 0, 'black': 0}
        for aluno in alunos:
            belt = current_belt(aluno)
            if belt == 'White Belt':
                dict_belt['white'] += 1
            elif belt == 'Gray/White Belt':
                dict_belt['gray_white'] += 1
            elif belt == 'Gray Belt':
                dict_belt['gray'] += 1
            elif belt == 'Gray/Black Belt':
                dict_belt['gray_black'] += 1
            elif belt == 'Yellow/White Belt':
                dict_belt['yellow_white'] += 1
            elif belt == 'Yellow Belt':
                dict_belt['yellow'] += 1
            elif belt == 'Yellow/Black Belt':
                dict_belt['yellow_black'] += 1
            elif belt == 'Green/White Belt':
                dict_belt['green_white'] += 1
            elif belt == 'Green Belt':
                dict_belt['green'] += 1
            elif belt == 'Green/Black Belt':
                dict_belt['green_black'] += 1

            elif belt == 'Orange/White Belt':
                dict_belt['orange_white'] += 1
            elif belt == 'Orange Belt':
                dict_belt['orange'] += 1
            elif belt == 'Orange/Black Belt':
                dict_belt['orange_black'] += 1

            elif belt == 'Blue Belt':
                dict_belt['blue'] += 1
            elif belt == 'Purple Belt':
                dict_belt['purple'] += 1
            elif belt == 'Brown Belt':
                dict_belt['brown'] += 1
            elif belt == 'Black Belt':
                dict_belt['black'] += 1
        return dict_belt


class ManageStaff(SuperuserRequiredMixin, TemplateView):
    template_name = 'managestaff.html'
    model = CustomUser, Aluno
    context_object_name = 'afiliado'

    def get_context_data(self, **kwargs):
        context = super(ManageStaff, self).get_context_data(**kwargs)
        context['object_list'] = CustomUser.objects.all()
        context['alunos'] = Aluno.objects.all()
        return context


class ManageAlunos(LoginRequiredMixin, ListView):
    template_name = 'managealunos.html'
    model = Aluno

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = AlunoFilter(self.request.GET, queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super(ManageAlunos, self).get_context_data(**kwargs)
        context['alunos'] = Aluno.objects.all()

        return context


class AlunotDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'deletaraluno.html'
    model = Aluno
    context_object_name = 'aluno'

    def get_success_url(self):
        return reverse('focusbjj:managealunos')


class ManageAlunosKids(LoginRequiredMixin, ListView):
    template_name = 'managealunos_kids.html'
    model = Aluno

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = AlunoFilter(self.request.GET, queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super(ManageAlunosKids, self).get_context_data(**kwargs)
        context['alunos'] = Aluno.objects.all()

        return context


class Agreement(TemplateView):
    template_name = "terms.html"


class ManageAlunosTotal(SuperuserRequiredMixin, ListView):
    template_name = 'managealunostotal.html'
    model = Aluno

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = AlunoFilter(self.request.GET, queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super(ManageAlunosTotal, self).get_context_data(**kwargs)
        context['alunos'] = Aluno.objects.all()
        context['unidades'] = CustomUser.objects.all()
        queryset = self.get_queryset()
        filter = AlunoFilter(self.request.GET, queryset)
        context['filter'] = filter
        return context


class ManageGraduationTotal(LoginRequiredMixin, ListView):
    template_name = 'managegraduationtotal.html'
    model = Aluno

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = AlunoFilter(self.request.GET, queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super(ManageGraduationTotal, self).get_context_data(**kwargs)
        context['alunos'] = Aluno.objects.all()
        context['unidades'] = CustomUser.objects.all()
        queryset = self.get_queryset()
        filter = AlunoFilter(self.request.GET, queryset)
        context['filter'] = filter
        return context


class RegisterStaffView(SuperuserRequiredMixin, FormView):
    form_class = RegisterStaffForm
    template_name = 'add_staff.html'
    success_msg = "Afiliado adicionado com sucesso!"

    def form_valid(self, form):
        form.save()
        afialdos = CustomUser.objects.order_by('-join_date')
        username = afialdos[0].username
        email = afialdos[0].email
        senha = afialdos[0].password
        context = {
            'username': username,
            'senha': senha,
        }
        subject = f'Welcome to Focus Jiu-Jitsu'
        html_message = render_to_string('email_USER.html', {'context': context, 'username': username})
        from_email = settings.EMAIL_HOST_USER
        recipient = [email]
        message = EmailMessage(subject, html_message, from_email, recipient)
        message.content_subtype = 'html'
        message.send(fail_silently=False)
        success_msg = self.get_success_message(form.cleaned_data)
        if success_msg:
            messages.success(self.request, success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('focusbjj:add_staff')

    def get_success_message(self, cleaned_data):
        return self.success_msg % cleaned_data


class RegisterAlunoView(FormView):
    form_class = RegisterAlunoForm
    template_name = 'add_aluno.html'
    success_msg = "Athlete: "
    success_msg2 = " - Member ID  "
    errormsg = "Você precisa concordar com os termos para continuar."

    def form_valid(self, form):
        form.save(commit=False)
        agreement = form.instance.agreement
        if not agreement:
            errormsg = self.error_msg()
            if errormsg:
                form.save(commit=False)
                messages.error(self.request, errormsg)
        else:
            form.save()
            alunos = Aluno.objects.order_by('-time_stamp')
            nome = alunos[0].nome
            surname = alunos[0].surname
            email = alunos[0].email
            copy_to = alunos[0].location.email
            country = alunos[0].location.country
            id = alunos[0].id
            context = {
                'nome': nome,
                'id': id,
                'country': country,
            }
            subject = f' Welcome to Focus JJ, {nome} {surname}'
            html_message = render_to_string('email_template_EN.html', {'context': context, 'nome': nome, 'id': id})
            html_message_pt = render_to_string('email_template_PT.html', {'context': context, 'nome': nome, 'id': id})
            from_email = settings.EMAIL_HOST_USER
            recipient = [email, copy_to]
            if country == 'BR' or country == 'PT' or country == 'AO' or country == 'CV':
                message = EmailMessage(subject, html_message_pt, from_email, recipient)
                message.content_subtype = 'html'
                message.send(fail_silently=False)
            else:
                message = EmailMessage(subject, html_message, from_email, recipient)
                message.content_subtype = 'html'
                message.send(fail_silently=False)
            success_msg = self.get_success_message(form.cleaned_data)
            if success_msg:
                messages.success(self.request, success_msg)
        return super().form_valid(form)

    def error_msg(self):
        return self.errormsg

    def get_success_url(self):
        return reverse('focusbjj:add_aluno')

    def get_success_message(self, cleaned_data):
        aluno = Aluno.objects.order_by('-time_stamp')[0]
        return self.success_msg + aluno.nome + " " + aluno.surname + self.success_msg2 + aluno.id % cleaned_data


class LoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('focusbjj:filiais')


class EditarAluno(LoginRequiredMixin, UpdateView):
    template_name = 'editaralunos.html'
    model = Aluno
    form_class = EditAtlheteForm

    def get_success_url(self):
        return reverse('focusbjj:managealunos')


class EditarBranch(LoginRequiredMixin, UpdateView):
    template_name = 'editarbranch.html'
    model = CustomUser
    form_class = EditBranchForm

    def get_success_url(self):
        return reverse('focusbjj:filiais')


class EditarBranchSuper(LoginRequiredMixin, UpdateView):
    template_name = 'editarbranch.html'
    model = CustomUser
    form_class = EditBranchFormSuper

    def get_success_url(self):
        return reverse('focusbjj:managestaff')


class DetailALunos(LoginRequiredMixin, DetailView):
    template_name = 'details_alunos.html'
    model = Aluno


class DetailBranch(SuperuserRequiredMixin, DetailView):
    template_name = 'branchdetails.html'
    model = CustomUser
    context_object_name = 'afiliado'

    def get_context_data(self, **kwargs):
        context = super(DetailBranch, self).get_context_data(**kwargs)
        context['belts'] = self.get_belts()
        context['alunos'] = Aluno.objects.all()
        return context

    def get_belts(self):
        alunos = Aluno.objects.all()
        dict_belt = {'white': 0, 'whitekids': 0, 'gray_white': 0, 'gray': 0, 'gray_black': 0,
                     'yellow_white': 0, 'yellow': 0, 'yellow_black': 0,
                     'green_white': 0, 'green': 0, 'green_black': 0,
                     'blue': 0, 'purple': 0, 'brown': 0, 'black': 0}
        for aluno in alunos:
            belt = current_belt(aluno)
            if belt == 'White Belt':
                dict_belt['white'] += 1
            elif belt == 'Gray/White Belt':
                dict_belt['gray_white'] += 1
            elif belt == 'Gray Belt':
                dict_belt['gray'] += 1
            elif belt == 'Gray/Black Belt':
                dict_belt['gray_black'] += 1
            elif belt == 'Yellow/White Belt':
                dict_belt['yellow_white'] += 1
            elif belt == 'Yellow Belt':
                dict_belt['yellow'] += 1
            elif belt == 'Yellow/Black Belt':
                dict_belt['yellow_black'] += 1
            elif belt == 'Green/White Belt':
                dict_belt['green_white'] += 1
            elif belt == 'Green Belt':
                dict_belt['green'] += 1
            elif belt == 'Green/Black Belt':
                dict_belt['green_black'] += 1
            elif belt == 'Blue Belt':
                dict_belt['blue'] += 1
            elif belt == 'Purple Belt':
                dict_belt['purple'] += 1
            elif belt == 'Brown Belt':
                dict_belt['brown'] += 1
            elif belt == 'Black Belt':
                dict_belt['black'] += 1
        return dict_belt


class Graduate(LoginRequiredMixin, CreateView):
    template_name = 'graduation.html'
    model = Graduation
    form_class = GraduateForm

    def form_valid(self, form):
        graduate = form.save(commit=False)
        aluno_id = self.kwargs['pk']
        try:
            aluno = Aluno.objects.get(id=aluno_id)
        except Aluno.DoesNotExist:
            raise Http404
        graduate.aluno = aluno
        graduate.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('focusbjj:managealunos')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        aluno_id = self.kwargs['pk']
        try:
            aluno = Aluno.objects.get(id=aluno_id)
        except Aluno.DoesNotExist:
            raise Http404
        data['aluno'] = aluno
        return data


class AddChampionship(LoginRequiredMixin, CreateView):
    template_name = 'campeonatos.html'
    model = Championship
    form_class = RegisterChampionship

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('focusbjj:championship')


class SalesList(LoginRequiredMixin, ListView):
    template_name = 'vendas.html'
    model = Venda


class SaleDetails(LoginRequiredMixin, DetailView):
    template_name = 'saledetails.html'
    model = Venda

    def get_context_data(self, **kwargs):
        context = super(SaleDetails, self).get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


class ProductList(LoginRequiredMixin, ListView):
    template_name = 'products.html'
    model = ProductsList

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = ProductsFilter(self.request.GET, queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['products'] = ProductsList.objects.all()
        queryset = self.get_queryset()
        filter = ProductsFilter(self.request.GET, queryset)
        context['filter'] = filter
        return context


class SocialMedia(LoginRequiredMixin, ListView):
    template_name = 'socialmedia.html'
    model = Posts

    def get_context_data(self, **kwargs):
        context = super(SocialMedia, self).get_context_data(**kwargs)
        context['posts'] = Posts.objects.all()
        return context


class AddSocialMedia(LoginRequiredMixin, CreateView):
    template_name = 'add_socialmedia.html'
    model = Posts
    form_class = SocialMediaForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('focusbjj:socialmedia')


class UpdateSocialMedia(LoginRequiredMixin, UpdateView):
    template_name = 'edit_socialmedia.html'
    model = Posts
    fields = ['title']

    def get_context_data(self, **kwargs):
        context = super(UpdateSocialMedia, self).get_context_data(**kwargs)
        context['posts'] = Posts.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('focusbjj:socialmedia')


class DeleteSocialMedia(LoginRequiredMixin, DeleteView):
    template_name = 'delete_socialmedia.html'
    model = Posts
    context_object_name = 'post'

    def get_success_url(self):
        return reverse('focusbjj:socialmedia')


class EditProduct(LoginRequiredMixin, UpdateView):
    template_name = 'editarprodutos.html'
    model = ProductsList
    form_class = ProductForm

    def get_success_url(self):
        return reverse('focusbjj:products')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'deletarprodutos.html'
    model = ProductsList
    context_object_name = 'products'

    def get_success_url(self):
        return reverse('focusbjj:products')


class ChampionshipDetail(LoginRequiredMixin, ListView):
    template_name = 'championship_history.html'
    model = Championship

    def get_context_data(self, **kwargs):
        context = super(ChampionshipDetail, self).get_context_data(**kwargs)
        context['championships'] = Championship.objects.all()
        return context


def export_xlsx(model, filename, queryset, columns):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(model)

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    default_style = xlwt.XFStyle()

    rows = queryset
    for row, rowdata in enumerate(rows):
        row_num += 1
        for col, val in enumerate(rowdata):
            ws.write(row_num, col, val, default_style)

    wb.save(response)

    return response


def exportar_alunos_xlsx(request):
    mdata = datetime.datetime.now().strftime('%Y-%m-%d')
    model = 'Aluno'
    filename = 'athletes.xls'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{mdata}.{_filename[1]}'

    queryset = Aluno.objects.filter(location=request.user.id).values_list(
        'nome',
        'surname',
        'email',
        'phone',
        'location__location',
        'dob__year',

    ).order_by('nome')
    columns = ('Name', 'Last Name', 'Email', 'Phone', 'Location', 'Year of Birth')
    response = export_xlsx(model, filename_final, queryset, columns,)

    def get_success_url(self):
        return reverse('focusbjj:managealunos')

    return response


def exportar_alunos_total_xlsx(request):
    mdata = datetime.datetime.now().strftime('%Y-%m-%d')
    model = 'Aluno'
    filename = 'alunos.xls'
    _filename = filename.split('.')
    filename_final = f'{_filename[0]}_{mdata}.{_filename[1]}'
    queryset = Aluno.objects.all().values_list(
        'nome',
        'surname',
        'email',
        'phone',
        'location__location',
        'dob__year',
    ).order_by('nome')
    columns = ('Name', 'Last Name', 'Email', 'Phone', 'Location', 'Year of Birth')
    response = export_xlsx(model, filename_final, queryset, columns,)

    def get_success_url(self):
        return reverse('focusbjj:managealunostotal')

    return response
