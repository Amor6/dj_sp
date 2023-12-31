import secrets

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.views.generic import CreateView, UpdateView
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy

from users.models import User
from users.forms import UserRegisterForm, UserProfileForm
from users.services.account_confirmed import account_confirmed

from config import settings


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.is_active = False
            self.object.token = secrets.token_urlsafe(18)[:15]
            account_confirmed(self.object)
            self.object.save()
            self.user_token = self.object.token
            return redirect(self.get_success_url())  # Перенаправление на страницу входа
        return super().form_valid(form)

    def get_success_url(self):
        new_url = super().get_success_url()
        token = self.object.token
        return str(new_url) + str(token)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def verify_email(request, token):
    if request.method == 'POST':
        obj = get_object_or_404(User, token=token)
        obj.is_active = True
        obj.save()
    return render(request, 'users/verify_email.html')


def activate_user(request, token):
    user = User.objects.filter(token=token).first()
    if user:
        user.is_active = True
        user.save()
        return redirect('users:login')
    return render(request, 'users/user_not_found.html')


@login_required
def password_reset_done(request):
    user = request.user
    new_password = User.objects.make_random_password()
    user.set_password(new_password)
    user.save()

    email_subject = 'Восстановление пароля'
    email_body = f'Ваш новый пароль: {new_password}'
    send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, [user.email])

    return redirect(reverse('users:password_reset_done'))


class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        """
        Отправляет сообщение с ссылкой для сброса пароля
        """
        subject = 'Восстановление пароля'
        email = render_to_string(email_template_name, context)
        send_mail(subject, email, from_email, [to_email], html_message=html_email_template_name)

