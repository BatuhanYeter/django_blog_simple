from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to login')
            return redirect('login') # to do this, we need to import redirect
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        # bunlar model formları, spesifik model object üzerinde çalışan
        # bu yüzden instance yollayarak mevcut bilgileri çekebiliriz
        # that way, we fill the blank UserUpdateForm() or the other one with the info of current user
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        # burada pp değişimi için request.FILES da yolluyoruz yeni foto
        # daha sonra valid olup olmadıklarını kontrol edip, save ediyoruz
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            # success mesajını veririz ve profile sayfasına redirect ederiz
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # to do this, we need to import redirect
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)

# messages.debug
# messages.info
# messages.success
# messages.warning