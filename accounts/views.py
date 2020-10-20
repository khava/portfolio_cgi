import os

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import View
from django.shortcuts import get_object_or_404

from accounts.forms import ProfileForm, SignupForm
from accounts.models import User
from accounts.tokens import account_activation_token
from discussion.models import Room, Theme


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Активируйте свой аккаунт.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()

            message_email_confirm = 'Чтобы завершить регистрацию подтвердите свой адрес электронной почты'
            return render(request, 'registration/email_confirmation_page.html', {'message': message_email_confirm})
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        
        message = 'Ваша учетная запись подтверждена. Теперь вы можете войти в свой аккаунт'
        return render(request, 'registration/email_confirmation_page.html', {'message': message})
    else:
        message = 'Ссылка на активацию аккаунта недействительна'
        return render(request, 'registration/email_confirmation_page.html', {'message': message})  


class ProfileView(View):

    @method_decorator(login_required)
    def get(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        themes = Theme.objects.filter(author=user)
        context = {
            'form': ProfileForm(),
            'themes': themes,
        }
        return render(request, 'registration/profile_page.html', context=context)


    @method_decorator(login_required)
    def post(self, request): 
        request.FILES['avatar'].name = request.user.email + '.jpg'
        form = ProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            user = User.objects.get(pk=request.user.pk)
            if user.avatar.name != 'avatars/default_avatar.jpg':
                os.remove(user.avatar.path)
            user.avatar = form.cleaned_data['avatar']
            user.save()

        return redirect(reverse('profile'))


class UserCommentsView(View):

    @method_decorator(login_required)
    def get(self, request, discussion_id):
        room = get_object_or_404(Room, id=discussion_id)
        
        context = {
            'room': room,
            'red': room.comments.filter(color='red'),
            'blue': room.comments.filter(color='blue'),
            'yellow': room.comments.filter(color='yellow'),
            'green': room.comments.filter(color='green'),
            'white': room.comments.filter(color='white'),
            'black': room.comments.filter(color='black'),
        }
        return render(request, 'registration/user_comments_page.html', context=context)


class UserAccountDetailView(View):

    @method_decorator(login_required)
    def get(self, request, username):

        if username == request.user.username:
            return redirect(reverse('profile'))
        
        user = get_object_or_404(User, username=username)
        themes = Theme.objects.filter(author=user)
        context = {
            'user': user,
            'themes': themes,
        }

        return render(request, 'registration/user_account_page.html', context=context)
