import datetime
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import FormView, DetailView, ListView, UpdateView, CreateView, TemplateView, DeleteView, View
from focusbjj.forms import *
from focusbjj.models import *
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .filter import AlunoFilter, AlunoFilterBranch
from .templatetags.attendance_tags import current_belt, current_stripe, last_att_aluno
from .utils import get_students_active, get_students_absent
import xlwt
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
import cloudinary
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from focusbjj.templatetags.dashboard_tags import belt_distribution_average, students_eligible_for_graduation
from datetime import timedelta
from django.contrib.auth.decorators import login_required

cloudinary.config(
    cloud_name="holwfsrwh",
    api_key="751324248687953",
    api_secret="cWnCSmjPRk6p4-2vqX3_0V6957g"
)

# Define the BaseView first
class BaseView(LoginRequiredMixin, TemplateView):
    """Base view for all internal pages"""
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add common context data here
        
        # Add graduation requirements link to sidebar items
        sidebar_items = context.get('sidebar_items', [])
        
        # Add graduation requirements link
        grad_req_link = {
            'url': reverse('focusbjj:graduation_requirements'), 
            'icon': 'fa-trophy', 
            'text': _('Graduation Requirements')
        }
        
        if not any(item.get('url') == grad_req_link['url'] for item in sidebar_items):
            sidebar_items.append(grad_req_link)
        
        context['sidebar_items'] = sidebar_items
        return context

class Attendance(LoginRequiredMixin, FormView):
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


class HomeView(LoginRequiredMixin, TemplateView):
    model = Aluno, CustomUser

    def get_template_names(self):
        # Check if superuser is requesting a specific affiliate's dashboard
        affiliate_id = self.request.GET.get('affiliate_id')
        if affiliate_id and self.request.user.is_superuser:
            return ['affiliate_dashboard.html']
        elif self.request.user.is_superuser:
            return ['manager_dashboard.html']
        else:
            return ['affiliate_dashboard.html']

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['alunos'] = Aluno.objects.all()
        context['unidades'] = CustomUser.objects.all()
        
        # Get all users and analyze them
        all_users = CustomUser.objects.all()
        staff_users = all_users.filter(is_staff=True)
        normal_users = all_users.filter(is_staff=False)
        
        # Check if any students are associated with each user
        users_with_students = []
        for u in all_users:
            student_count = Aluno.objects.filter(location=u).count()
            if student_count > 0:
                users_with_students.append(u)
        
        # Use a more reliable count: 
        # 1. Count users that have at least one student, or
        # 2. Count all users minus 1 (for admin)
        # Choose the appropriate method based on your data model
        
        # Method 1: Count users with students
        affiliates_with_students = len(users_with_students)
        
        # Method 2: Count all users minus 1
        total_affiliates = all_users.count()
        affiliates_minus_admin = max(1, total_affiliates - 1)
        
        # Use the appropriate method based on your data
        # For now, we'll use method 1 as it's more accurate
        affiliates_count = max(1, affiliates_with_students)
        
        context['unidades'] = all_users
        context['unidades_count'] = affiliates_count
        context['belts'] = self.get_belts()
        
        # Create a list of all belts in the correct order
        all_belts_ordered = [
            'white', 
            'gray_white', 'gray', 'gray_black',
            'yellow_white', 'yellow', 'yellow_black',
            'orange_white', 'orange', 'orange_black',
            'green_white', 'green', 'green_black',
            'blue', 'purple', 'brown', 'black'
        ]
        context['all_belts_ordered'] = all_belts_ordered
        
        # Create a translation mapping for belt names
        context['belt_display_names'] = {
            'white': 'White',
            'gray_white': 'Gray/White', 
            'gray': 'Gray', 
            'gray_black': 'Gray/Black',
            'yellow_white': 'Yellow/White', 
            'yellow': 'Yellow', 
            'yellow_black': 'Yellow/Black',
            'orange_white': 'Orange/White', 
            'orange': 'Orange', 
            'orange_black': 'Orange/Black',
            'green_white': 'Green/White', 
            'green': 'Green', 
            'green_black': 'Green/Black',
            'blue': 'Blue', 
            'purple': 'Purple', 
            'brown': 'Brown', 
            'black': 'Black'
        }
        
        # Get reverse mapping from belt display name to belt key (with and without 'Belt' suffix)
        belt_mapping = {
            # With 'Belt' suffix
            'White Belt': 'white',
            'Gray/White Belt': 'gray_white',
            'Gray Belt': 'gray',
            'Gray/Black Belt': 'gray_black',
            'Yellow/White Belt': 'yellow_white',
            'Yellow Belt': 'yellow',
            'Yellow/Black Belt': 'yellow_black',
            'Orange/White Belt': 'orange_white',
            'Orange Belt': 'orange',
            'Orange/Black Belt': 'orange_black',
            'Green/White Belt': 'green_white',
            'Green Belt': 'green',
            'Green/Black Belt': 'green_black',
            'Blue Belt': 'blue',
            'Purple Belt': 'purple',
            'Brown Belt': 'brown',
            'Black Belt': 'black',
            
            # Without 'Belt' suffix
            'White': 'white',
            'Gray/White': 'gray_white',
            'Gray': 'gray',
            'Gray/Black': 'gray_black',
            'Yellow/White': 'yellow_white',
            'Yellow': 'yellow',
            'Yellow/Black': 'yellow_black',
            'Orange/White': 'orange_white',
            'Orange': 'orange',
            'Orange/Black': 'orange_black',
            'Green/White': 'green_white',
            'Green': 'green',
            'Green/Black': 'green_black',
            'Blue': 'blue',
            'Purple': 'purple',
            'Brown': 'brown',
            'Black': 'black'
        }
        
        # Initialize system_avg with zeros
        system_avg = {key: 0 for key in all_belts_ordered}
        
        # Count total students per belt across all affiliates
        belt_counts = {}
        for belt_key in all_belts_ordered:
            belt_counts[belt_key] = 0
        
        # Count students by belt
        for student in Aluno.objects.all():
            belt = current_belt(student)
            if belt in belt_mapping:
                belt_key = belt_mapping[belt]
                if belt_key in belt_counts:
                    belt_counts[belt_key] += 1
        
        # Calculate averages by dividing by number of affiliates
        for belt_key, count in belt_counts.items():
            system_avg[belt_key] = round(count / affiliates_count, 1)
        
        context['system_avg'] = system_avg
        
        # If superuser is viewing a specific affiliate's dashboard
        affiliate_id = self.request.GET.get('affiliate_id')
        if affiliate_id and self.request.user.is_superuser:
            try:
                selected_affiliate = CustomUser.objects.get(id=affiliate_id)
                context['selected_affiliate'] = selected_affiliate
                context['view_as_affiliate'] = True
                
                # Calculate affiliate-specific data
                active_students_count = 0
                for student in Aluno.objects.filter(location=selected_affiliate):
                    attendance_records = GetAttendance.objects.filter(aluno=student).order_by('-attendance')
                    if attendance_records.exists():
                        last_attendance = attendance_records.first().attendance
                        days_since_last_attendance = (timezone.now().date() - last_attendance.date()).days
                        if days_since_last_attendance < 30:
                            active_students_count += 1
                context['active_students_count'] = active_students_count
                
                # Calculate busiest times based on check-in data for this affiliate
                all_checkins = GetAttendance.objects.filter(aluno__location=selected_affiliate)
                morning_checkins = all_checkins.filter(attendance__hour__gte=6, attendance__hour__lt=12).count()
                afternoon_checkins = all_checkins.filter(attendance__hour__gte=12, attendance__hour__lt=18).count()
                evening_checkins = all_checkins.filter(attendance__hour__gte=18, attendance__hour__lt=23).count()
                
                context['busiest_times'] = {
                    'morning': morning_checkins,
                    'afternoon': afternoon_checkins,
                    'evening': evening_checkins
                }
                
                # For template filters that use request.user
                context['affiliate_data'] = selected_affiliate
            except CustomUser.DoesNotExist:
                pass
        # Regular affiliate viewing their own dashboard        
        elif not self.request.user.is_superuser:
            # Add active students count (last 30 days)
            active_students_count = 0
            for student in Aluno.objects.filter(location=self.request.user):
                attendance_records = GetAttendance.objects.filter(aluno=student).order_by('-attendance')
                if attendance_records.exists():
                    last_attendance = attendance_records.first().attendance
                    days_since_last_attendance = (timezone.now().date() - last_attendance.date()).days
                    if days_since_last_attendance < 30:
                        active_students_count += 1
            context['active_students_count'] = active_students_count
            
            # Calculate busiest times based on check-in data
            all_checkins = GetAttendance.objects.filter(aluno__location=self.request.user)
            morning_checkins = all_checkins.filter(attendance__hour__gte=6, attendance__hour__lt=12).count()
            afternoon_checkins = all_checkins.filter(attendance__hour__gte=12, attendance__hour__lt=18).count()
            evening_checkins = all_checkins.filter(attendance__hour__gte=18, attendance__hour__lt=23).count()
            
            context['busiest_times'] = {
                'morning': morning_checkins,
                'afternoon': afternoon_checkins,
                'evening': evening_checkins
            }
        
        # Superuser viewing manager dashboard
        else:
            # Calculate busiest times for all affiliates combined
            all_checkins = GetAttendance.objects.all()
            morning_checkins = all_checkins.filter(attendance__hour__gte=6, attendance__hour__lt=12).count()
            afternoon_checkins = all_checkins.filter(attendance__hour__gte=12, attendance__hour__lt=18).count()
            evening_checkins = all_checkins.filter(attendance__hour__gte=18, attendance__hour__lt=23).count()
            
            context['busiest_times'] = {
                'morning': morning_checkins,
                'afternoon': afternoon_checkins,
                'evening': evening_checkins
            }
        
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

    def get_age(self):
        alunos = Aluno.objects.all()
        dict = {'kids': 0, 'adults': 0}
        for aluno in alunos:
            if aluno.idade() <= 17:
                dict['kids'] += 1
            else:
                dict['adults'] += 1

    def get_system_averages(self):
        """Calculate system-wide averages for each belt."""
        affiliates = Affiliate.objects.all()
        total_affiliates = affiliates.count()
        if total_affiliates == 0:
            return {}

        # Get all students across all affiliates
        all_students = Aluno.objects.filter(affiliate__in=affiliates)
        
        # Count students by belt across all affiliates
        belt_counts = {}
        for belt_key in Aluno.BELT_CHOICES:
            belt_counts[belt_key] = all_students.filter(belt=belt_key).count()
        
        # Calculate average by dividing by number of affiliates
        system_avg = {
            belt_key: round(count / total_affiliates, 1)
            for belt_key, count in belt_counts.items()
        }
        
        return system_avg


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
    context_object_name = 'alunos'

    def get_queryset(self):
        # Start with all students if superuser, otherwise filter by location
        if self.request.user.is_superuser:
            # Check if a specific location is selected in the filter
            location_param = self.request.GET.get('location')
            if location_param:
                try:
                    # Get students for the selected location
                    qs = Aluno.objects.filter(location_id=location_param)
                except (ValueError, TypeError):
                    # If location_param is invalid, show all students
                    qs = Aluno.objects.all()
            else:
                # No location selected, show all students
                qs = Aluno.objects.all()
        else:
            # Regular users can only see their students
            qs = Aluno.objects.filter(location=self.request.user)

        # Get the attendance status filter parameter
        attendance_status = self.request.GET.get('attendance_status', 'active')

        # Filter based on attendance status (active/inactive/all)
        if attendance_status == 'active':
            qs = get_students_active(qs)
        elif attendance_status == 'inactive':
            qs = get_students_absent(qs)
        # else 'all': keep qs as is

        # Apply the category filter
        category = self.request.GET.get('category', '')
        if category == 'adults':
            # Filter for students 14 years and older
            adults = []
            for aluno in qs:
                if aluno.idade() >= 14:
                    adults.append(aluno.id)
            qs = qs.filter(id__in=adults)
        elif category == 'kids':
            # Filter for students under 14 years
            kids = []
            for aluno in qs:
                if aluno.idade() < 14:
                    kids.append(aluno.id)
            qs = qs.filter(id__in=kids)

        # Now apply the filter form to the filtered queryset
        self.filterset = AlunoFilter(self.request.GET, queryset=qs)
        filtered_qs = self.filterset.qs

        if not filtered_qs.exists():
            return Aluno.objects.none()
        return filtered_qs

    def get_context_data(self, **kwargs):
        context = super(ManageAlunos, self).get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['attendance_status'] = self.request.GET.get('attendance_status', 'active')
        context['category'] = self.request.GET.get('category', '')
        context['is_superuser'] = self.request.user.is_superuser
        return context


class AlunotDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'deletaraluno.html'
    model = Aluno
    context_object_name = 'aluno'

    def get_success_url(self):
        return reverse('focusbjj:managealunos')


class StudentCheckIn(LoginRequiredMixin, View):
    """View to handle student check-in from the student list pages"""
    
    def post(self, request, *args, **kwargs):
        student_id = kwargs.get('pk')
        next_url = request.POST.get('next', reverse('focusbjj:managealunos'))
        
        try:
            student = Aluno.objects.get(id=student_id)
            
            # Check if student is blocked
            if student.is_blocked:
                messages.error(request, _("Student is inactive. Please contact management."))
                return redirect(next_url)
                
            # Check if already checked in within the last 3 hours
            recent_attendance = GetAttendance.objects.filter(
                aluno=student, 
                attendance__gte=timezone.now() - timedelta(hours=3)
            ).exists()
            
            if recent_attendance:
                messages.warning(request, _("Already checked in. Can check in again for next class or in 3 hours."))
                return redirect(next_url)
                
            # Create new attendance
            GetAttendance.objects.create(aluno=student)
            messages.success(request, f"{student.nome} {student.surname} - {_('Check-in successful')}")
            
        except Aluno.DoesNotExist:
            messages.error(request, _("Student not found."))
        
        return redirect(next_url)


class Agreemnet(LoginRequiredMixin, TemplateView):
    template_name = "terms.html"


class ManageAlunosTotal(SuperuserRequiredMixin, ListView):
    template_name = 'managealunostotal.html'
    model = Aluno
    context_object_name = 'alunos'

    def get_queryset(self):
        # Start with all students (for superuser)
        qs = Aluno.objects.all()
        
        # Check if a specific location is selected in the filter
        location_param = self.request.GET.get('location')
        if location_param:
            try:
                # Get students for the selected location
                qs = qs.filter(location_id=location_param)
            except (ValueError, TypeError):
                # If location_param is invalid, show all students
                pass
        
        # Get the attendance status filter parameter
        attendance_status = self.request.GET.get('attendance_status', 'active')

        # Filter based on attendance status (active/inactive/all)
        if attendance_status == 'active':
            qs = get_students_active(qs)
        elif attendance_status == 'inactive':
            qs = get_students_absent(qs)
        # else 'all': keep qs as is

        # Apply the category filter
        category = self.request.GET.get('category', '')
        if category == 'adults':
            # Filter for students 14 years and older
            adults = []
            for aluno in qs:
                if aluno.idade() >= 14:
                    adults.append(aluno.id)
            qs = qs.filter(id__in=adults)
        elif category == 'kids':
            # Filter for students under 14 years
            kids = []
            for aluno in qs:
                if aluno.idade() < 14:
                    kids.append(aluno.id)
            qs = qs.filter(id__in=kids)

        # Now apply the filter form to the filtered queryset
        self.filterset = AlunoFilter(self.request.GET, queryset=qs)
        filtered_qs = self.filterset.qs

        if not filtered_qs.exists():
            return Aluno.objects.none()
        return filtered_qs
        
    def get_context_data(self, **kwargs):
        context = super(ManageAlunosTotal, self).get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['attendance_status'] = self.request.GET.get('attendance_status', 'active')
        context['category'] = self.request.GET.get('category', '')
        context['is_superuser'] = True  # Always true for this view
        context['unidades'] = CustomUser.objects.all()
        return context


class ManageGraduationTotal(LoginRequiredMixin, ListView):
    template_name = 'managegraduationtotal.html'
    model = Aluno

    def get_queryset(self):
        # For superusers, allow filtering by location
        if self.request.user.is_superuser:
            affiliate_id = self.request.GET.get('location')
            if affiliate_id:
                try:
                    affiliate = CustomUser.objects.get(id=affiliate_id)
                    queryset = Aluno.objects.filter(location=affiliate)
                except CustomUser.DoesNotExist:
                    queryset = Aluno.objects.filter(location=self.request.user)
            else:
                # Default to the logged-in user's affiliate
                queryset = Aluno.objects.filter(location=self.request.user)
        else:
            # Regular users can only see their students
            queryset = Aluno.objects.filter(location=self.request.user)
        
        # Return all students, filtering for eligibility will happen in the template
        # using the students_eligible_for_graduation filter
        return queryset.order_by('nome')

    def get_context_data(self, **kwargs):
        context = super(ManageGraduationTotal, self).get_context_data(**kwargs)
        context['alunos'] = self.get_queryset()
        
        # Add students_eligible flag to enable proper template rendering
        context['students_eligible'] = True
        
        if self.request.user.is_superuser:
            context['unidades'] = CustomUser.objects.filter(is_staff=True, is_superuser=False)
            
            # Get the currently selected affiliate for display
            affiliate_id = self.request.GET.get('location')
            if affiliate_id:
                try:
                    context['selected_affiliate'] = CustomUser.objects.get(id=affiliate_id)
                except CustomUser.DoesNotExist:
                    context['selected_affiliate'] = self.request.user
            else:
                context['selected_affiliate'] = self.request.user
        
        return context


class RegisterStaffView(SuperuserRequiredMixin, FormView):
    form_class = RegisterStaffForm
    template_name = 'add_staff.html'
    success_msg = "Afiliado adicionado com sucesso!"

    def form_valid(self, form):
        form.save()
        # Get the newly created affiliate
        new_affiliate = CustomUser.objects.order_by('-join_date').first()
        self.new_affiliate_id = new_affiliate.id
        
        username = new_affiliate.username
        email = new_affiliate.email
        
        # Skip sending email if in development environment
        if not settings.DEBUG:
            try:
                subject = 'Welcome to Focus Jiu-Jitsu'
                # Use our new dedicated template for affiliate welcome emails
                html_message = render_to_string('affiliate_welcome_email.html', {
                    'username': username
                })
                from_email = settings.EMAIL_HOST_USER
                recipient = [email]
                message = EmailMessage(subject, html_message, from_email, recipient)
                message.content_subtype = 'html'
                message.send(fail_silently=True)
            except Exception as e:
                pass
        
        success_msg = self.get_success_message(form.cleaned_data)
        if success_msg:
            messages.success(self.request, success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the affiliate's dashboard
        if hasattr(self, 'new_affiliate_id'):
            return f"{reverse('focusbjj:filiais')}?affiliate_id={self.new_affiliate_id}"
        return reverse('focusbjj:add_staff')

    def get_success_message(self, cleaned_data):
        return self.success_msg % cleaned_data


class RegisterAlunoView(LoginRequiredMixin, FormView):
    form_class = RegisterAlunoForm
    template_name = 'add_aluno.html'
    success_msg = "Athlete: "
    success_msg2 = " - Member ID  "
    errormsg = "Você precisa concordar com os termos para continuar."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Remove location field from the form as it will be set automatically
        if 'location' in form.fields:
            form.fields.pop('location')
        return form

    def form_valid(self, form):
        form.instance = form.save(commit=False)
        # Set the location to the logged-in user's affiliate
        form.instance.location = self.request.user
        
        agreement = form.instance.agreement
        if not agreement:
            errormsg = self.error_msg()
            if errormsg:
                messages.error(self.request, errormsg)
        else:
            form.instance.save()
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

    def form_valid(self, form):
        # Preserve the original location and join_date values
        instance = self.get_object()
        form.instance.location = instance.location
        form.instance.join_date = instance.join_date
        
        # Handle photo upload if provided
        if self.request.FILES.get('photo'):
            image = self.request.FILES['photo']
            upload_result = cloudinary.uploader.upload(image)
            form.instance.photo = upload_result['url']  # Save Cloudinary URL
        
        return super().form_valid(form)

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all feedback for this student
        context['feedback_list'] = StudentFeedback.objects.filter(student=self.object).order_by('-created_at')
        # Add feedback form
        context['feedback_form'] = StudentFeedbackForm(initial={'professor_name': self.request.user.contact_name})
        
        # Add belt info directly to context
        from focusbjj.templatetags.attendance_tags import current_belt
        context['belt_name'] = current_belt(self.object)
        
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = StudentFeedbackForm(request.POST)
        
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.student = self.object
            feedback.author = request.user
            feedback.save()
            messages.success(request, _("Feedback added successfully"))
        else:
            messages.error(request, _("There was an error adding your feedback"))
            
        return redirect('focusbjj:alunos', pk=self.object.pk)


class DetailBranch(SuperuserRequiredMixin, DetailView):
    template_name = 'branchdetails.html'
    model = CustomUser
    context_object_name = 'afiliado'

    def get(self, request, *args, **kwargs):
        """
        Redirect to the HomeView with the affiliate_id parameter 
        to show the new affiliate dashboard for this branch.
        """
        affiliate_id = self.kwargs.get('pk')
        if affiliate_id:
            return redirect(f"{reverse('focusbjj:filiais')}?affiliate_id={affiliate_id}")
        return super().get(request, *args, **kwargs)

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


class Graduate(LoginRequiredMixin, FormView):
    template_name = 'graduation_form.html'
    form_class = GraduateForm
    
    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        return reverse('focusbjj:alunos', kwargs={'pk': self.aluno.id})
    
    def get_object(self):
        """Get the student object based on URL parameters"""
        aluno_id = self.kwargs['pk']
        try:
            return Aluno.objects.get(id=aluno_id)
        except Aluno.DoesNotExist:
            raise Http404(_("Student not found"))
    
    def get(self, request, *args, **kwargs):
        """Handle GET requests: retrieve and display a form."""
        self.aluno = self.get_object()
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        """Handle POST requests: process form data."""
        self.aluno = self.get_object()
        
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        # Add initial data for the form based on the student's current belt and stripe
        if hasattr(self, 'aluno'):
            initial = kwargs.get('initial', {})
            
            # Set up belt and stripe values
            current_belt = self.aluno.belt
            if " Belt" in current_belt:
                # Remove "Belt" suffix for form field
                current_belt = current_belt.replace(" Belt", "")
            
            initial['belt'] = current_belt
            initial['stripe'] = self.aluno.stripe
            initial['master'] = self.request.user.contact_name
            
            # Set today's date as the default graduation date
            from django.utils import timezone
            initial['time_stamp'] = timezone.now().date()
            
            kwargs['initial'] = initial
        return kwargs

    def form_valid(self, form):
        """Process a valid form."""
        # Get the student
        aluno = self.aluno
        aluno_id = aluno.id
        
        # Create and save graduation record - always use current timestamp for proper attendance tracking
        from django.utils import timezone
        now = timezone.now()
        
        graduate = Graduation.objects.create(
            aluno=aluno,
            belt=form.cleaned_data['belt'], 
            stripe=form.cleaned_data['stripe'],
            master=form.cleaned_data['master'],
            time_stamp=now  # Always use current time for consistency
        )
        
        # Normalize belt format - ensure consistency
        new_belt = graduate.belt
        if " Belt" not in new_belt and new_belt in ["White", "Blue", "Purple", "Brown", "Black"]:
            new_belt = f"{new_belt} Belt"
        
        # Force update the student model directly using raw SQL
        # This bypasses any caching issues with the ORM
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE focusbjj_aluno SET belt = %s, stripe = %s WHERE id = %s",
                [new_belt, graduate.stripe, aluno_id]
            )
        
        # Reload the student from database to verify update
        updated_student = Aluno.objects.get(id=aluno_id)
        
        # Check if the update was successful
        if updated_student.belt != new_belt or updated_student.stripe != graduate.stripe:
            # Try one more direct update on the object and save
            updated_student.belt = new_belt
            updated_student.stripe = graduate.stripe
            updated_student.save(update_fields=['belt', 'stripe'])
        
        # Add feedback if provided
        feedback_content = self.request.POST.get('feedback_content')
        professor_name = self.request.POST.get('professor_name', '')
        
        if feedback_content:
            feedback = StudentFeedback(
                student=aluno,
                author=self.request.user,
                professor_name=professor_name,
                content=feedback_content,
                related_to_graduation=True,
                related_graduation=graduate
            )
            feedback.save()
            messages.success(self.request, _("Graduation and feedback recorded successfully"))
        else:
            messages.success(self.request, _("Graduation recorded successfully"))
        
        # Use the get_success_url method for redirection
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle an invalid form submission."""
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        """Get context data for rendering the template."""
        context = super().get_context_data(**kwargs)
        
        # Ensure we have the student object
        if hasattr(self, 'aluno'):
            aluno = self.aluno
        else:
            aluno = self.get_object()
            self.aluno = aluno
            
        context['aluno'] = aluno
        
        # Check if student is eligible for graduation (for information only)
        from focusbjj.templatetags.dashboard_tags import is_eligible_for_graduation
        eligibility = is_eligible_for_graduation(aluno)
        context['eligibility'] = eligibility
        
        # Add feedback form field with initial data
        context['feedback_form'] = StudentFeedbackForm(initial={'professor_name': self.request.user.contact_name})
        
        return context


class GraduationRequirementsView(BaseView):
    """
    View to display graduation requirements - accessible by all users
    """
    template_name = 'graduation_requirements.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Define the belt order for sorting
        belt_order = [
            'White', 
            'Gray/White', 
            'Gray', 
            'Gray/Black',
            'Yellow/White', 
            'Yellow', 
            'Yellow/Black',
            'Orange/White', 
            'Orange', 
            'Orange/Black',
            'Green/White', 
            'Green', 
            'Green/Black',
            'Blue', 
            'Purple', 
            'Brown', 
            'Black'
        ]
        
        # Get all requirements and sort them by belt and stripe
        requirements = GraduationRequirement.objects.all()
        
        # Define a custom sorting function
        def sort_by_belt_and_stripe(req):
            # First sort by belt order
            belt_idx = belt_order.index(req.belt) if req.belt in belt_order else 999
            
            # Then by stripe
            stripe_order = {
                'No Stripes': 0,
                'Iº Stripe': 1,
                'IIº Stripe': 2,
                'IIIº Stripe': 3,
                'IVº Stripe': 4
            }
            stripe_idx = stripe_order.get(req.stripes, 999)
            
            return (belt_idx, stripe_idx)
        
        # Sort the requirements using the custom sorting function
        sorted_requirements = sorted(requirements, key=sort_by_belt_and_stripe)
        
        context['requirements'] = sorted_requirements
        
        return context


class UpdateGraduationRequirementView(UserPassesTestMixin, BaseView):
    """
    View to update graduation requirements - only accessible by superusers
    """
    template_name = 'update_graduation_requirements.html'
    
    def test_func(self):
        # Only allow superusers to access this view
        return self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Define the belt order for sorting
        belt_order = [
            'White', 
            'Gray/White', 
            'Gray', 
            'Gray/Black',
            'Yellow/White', 
            'Yellow', 
            'Yellow/Black',
            'Orange/White', 
            'Orange', 
            'Orange/Black',
            'Green/White', 
            'Green', 
            'Green/Black',
            'Blue', 
            'Purple', 
            'Brown', 
            'Black'
        ]
        
        # Get all requirements
        requirements = GraduationRequirement.objects.all()
        
        # Define a custom sorting function
        def sort_by_belt_and_stripe(req):
            # First sort by belt order
            belt_idx = belt_order.index(req.belt) if req.belt in belt_order else 999
            
            # Then by stripe
            stripe_order = {
                'No Stripes': 0,
                'Iº Stripe': 1,
                'IIº Stripe': 2,
                'IIIº Stripe': 3,
                'IVº Stripe': 4
            }
            stripe_idx = stripe_order.get(req.stripes, 999)
            
            return (belt_idx, stripe_idx)
        
        # Sort the requirements using the custom sorting function
        sorted_requirements = sorted(requirements, key=sort_by_belt_and_stripe)
        
        # Create forms for all requirements
        context['requirement_forms'] = [GraduationRequirementForm(instance=req) for req in sorted_requirements]
        
        return context
    
    def post(self, request, *args, **kwargs):
        # Process all forms
        updated_count = 0
        
        # Get all requirements
        requirements = GraduationRequirement.objects.all()
        
        # Process requirements
        for req in requirements:
            form_data = request.POST.get(f'required_classes_{req.id}', None)
            if form_data and form_data.isdigit():
                req.required_classes = int(form_data)
                req.modified_by = request.user
                req.save()
                updated_count += 1
        
        # Store the success message with a specific tag that identifies this view
        messages.success(request, f'Successfully updated {updated_count} graduation requirements.', extra_tags='graduation_req_update')
        return redirect('focusbjj:graduation_requirements')


class GraduationEligibilityView(LoginRequiredMixin, TemplateView):
    template_name = 'graduation.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all affiliates (for superuser filter dropdown)
        if self.request.user.is_superuser:
            context['affiliates'] = CustomUser.objects.filter(is_staff=True, is_superuser=False)
        
        # Get filter parameters
        affiliate_id = self.request.GET.get('affiliate')
        
        # Set selected affiliate
        if affiliate_id and self.request.user.is_superuser:
            try:
                selected_affiliate = CustomUser.objects.get(id=affiliate_id)
                context['selected_affiliate'] = selected_affiliate
            except CustomUser.DoesNotExist:
                context['selected_affiliate'] = self.request.user
        else:
            # For non-superusers or superusers without a filter, use their own affiliate
            context['selected_affiliate'] = self.request.user
            
        return context


class GraduationDebugView(LoginRequiredMixin, View):
    """A debugging view to test the graduation form submission process via the web interface"""
    
    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('pk')
        
        try:
            student = Aluno.objects.get(id=student_id)
        except Aluno.DoesNotExist:
            messages.error(request, f"Student with ID {student_id} not found")
            return redirect('focusbjj:managealunos')
        
        # Create and validate a test form
        from django.utils import timezone
        
        form_data = {
            'belt': 'Purple',
            'stripe': 'IIº Stripe', 
            'master': request.user.contact_name,
            'time_stamp': timezone.now().date()
        }
        
        form = GraduateForm(data=form_data)
        
        debug_info = {
            'student': {
                'id': student.id,
                'nome': student.nome,
                'surname': student.surname,
                'current_belt': student.belt,
                'current_stripe': student.stripe
            },
            'form_data': form_data,
            'form_is_valid': form.is_valid(),
            'form_errors': dict(form.errors.items()) if not form.is_valid() else None
        }
        
        if form.is_valid():
            # Create graduation record
            try:
                from django.utils import timezone
                now = timezone.now()
                
                graduate = Graduation.objects.create(
                    aluno=student,
                    belt=form.cleaned_data['belt'], 
                    stripe=form.cleaned_data['stripe'],
                    master=form.cleaned_data['master'],
                    time_stamp=now  # Always use current time for consistency
                )
                
                # Normalize belt name
                new_belt = form.cleaned_data['belt']
                if " Belt" not in new_belt and new_belt in ["White", "Blue", "Purple", "Brown", "Black"]:
                    new_belt = f"{new_belt} Belt"
                
                # Update student using direct SQL
                from django.db import connection
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE focusbjj_aluno SET belt = %s, stripe = %s WHERE id = %s",
                        [new_belt, form.cleaned_data['stripe'], student.id]
                    )
                
                # Verify update
                student.refresh_from_db()
                update_success = (student.belt == new_belt and student.stripe == form.cleaned_data['stripe'])
                
                debug_info['update_result'] = {
                    'success': update_success,
                    'graduation_id': graduate.id,
                    'new_belt': new_belt,
                    'new_stripe': form.cleaned_data['stripe'],
                    'actual_belt': student.belt,
                    'actual_stripe': student.stripe
                }
                
                if update_success:
                    messages.success(request, f"Debug graduation successful for {student.nome} {student.surname}")
                else:
                    messages.error(request, "Update verification failed. See debug information.")
                    
            except Exception as e:
                debug_info['error'] = str(e)
                messages.error(request, f"Error during graduation: {str(e)}")
        
        # Convert debug info to text output
        debug_text = []
        debug_text.append(f"STUDENT: {debug_info['student']['nome']} {debug_info['student']['surname']} (ID: {debug_info['student']['id']})")
        debug_text.append(f"CURRENT: Belt={debug_info['student']['current_belt']}, Stripe={debug_info['student']['current_stripe']}")
        debug_text.append("\nFORM DATA:")
        for key, value in debug_info['form_data'].items():
            debug_text.append(f"  {key}: {value}")
        
        debug_text.append(f"\nFORM VALID: {debug_info['form_is_valid']}")
        
        if not debug_info['form_is_valid']:
            debug_text.append("FORM ERRORS:")
            for field, errors in debug_info['form_errors'].items():
                debug_text.append(f"  {field}: {', '.join(errors)}")
        
        if 'update_result' in debug_info:
            debug_text.append("\nUPDATE RESULT:")
            debug_text.append(f"  Success: {debug_info['update_result']['success']}")
            debug_text.append(f"  Graduation ID: {debug_info['update_result']['graduation_id']}")
            debug_text.append(f"  Expected Belt: {debug_info['update_result']['new_belt']}")
            debug_text.append(f"  Expected Stripe: {debug_info['update_result']['new_stripe']}")
            debug_text.append(f"  Actual Belt: {debug_info['update_result']['actual_belt']}")
            debug_text.append(f"  Actual Stripe: {debug_info['update_result']['actual_stripe']}")
        
        if 'error' in debug_info:
            debug_text.append("\nERROR:")
            debug_text.append(f"  {debug_info['error']}")
        
        # Output debug info
        from django.http import HttpResponse
        response = HttpResponse("<pre>" + "\n".join(debug_text) + "</pre>")
        return response


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


@login_required
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


@login_required
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
