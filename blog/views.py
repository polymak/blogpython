from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Blog, CustomUser
from .forms import BlogForm, UserForm


def is_admin_user(user):
    """Vérifie si l'utilisateur est un administrateur autorisé"""
    return user.is_authenticated and user.is_active and (
        user.is_staff or user.is_superuser or user.role == 'admin'
    )


def home(request):
    """Public home page showing all blog posts"""
    blogs = Blog.objects.all()
    return render(request, 'blog/home.html', {'blogs': blogs})


def user_login(request):
    """Admin login page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and is_admin_user(user):
            login(request, user)
            messages.success(request, 'Connexion réussie.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Identifiants invalides ou utilisateur non autorisé comme admin.')

    return render(request, 'blog/login.html')


@login_required
def dashboard(request):
    """Admin dashboard"""
    if not is_admin_user(request.user):
        messages.error(request, 'Accès refusé.')
        return redirect('login')

    return render(request, 'blog/dashboard.html')


@login_required
def admin_dashboard(request):
    """Admin dashboard (alternative route)"""
    if not is_admin_user(request.user):
        messages.error(request, 'Accès refusé.')
        return redirect('login')

    return render(request, 'blog/dashboard.html')


def blog_detail(request, pk):
    """View individual blog post"""
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/blog_detail.html', {'blog': blog})


@login_required
def blog_list(request):
    """List all blogs in admin panel"""
    if not is_admin_user(request.user):
        messages.error(request, 'Accès refusé.')
        return redirect('login')

    blogs = Blog.objects.all()
    return render(request, 'blog/admin/blog_list.html', {'blogs': blogs})


@login_required
def blog_create(request):
    """Create new blog post"""
    if not is_admin_user(request.user):
        messages.error(request, 'Accès refusé.')
        return redirect('login')

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article créé avec succès.')
            return redirect('blog_list')
    else:
        form = BlogForm()

    return render(request, 'blog/admin/blog_form.html', {'form': form, 'title': 'Créer un article'})


@login_required
def blog_edit(request, pk):
    """Edit existing blog post"""
    if not is_admin_user(request.user):
        messages.error(request, 'Accès refusé.')
        return redirect('login')

    blog = get_object_or_404(Blog, pk=pk)

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article mis à jour avec succès.')
            return redirect('blog_list')
    else:
        form = BlogForm(instance=blog)

    return render(request, 'blog/admin/blog_form.html', {
        'form': form,
        'title': 'Modifier un article',
        'blog': blog
    })


@login_required
def blog_delete(request, pk):
    """Delete blog post"""
    if not is_admin_user(request.user):
        messages.error(request, 'Accès refusé.')
        return redirect('login')

    blog = get_object_or_404(Blog, pk=pk)

    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Article supprimé avec succès.')
        return redirect('blog_list')

    return render(request, 'blog/admin/blog_confirm_delete.html', {'blog': blog})


@login_required
def user_list(request):
    """List all admin users"""
    if not is_admin_user(request.user):
        messages.error(request, 'Accès refusé.')
        return redirect('login')

    users = CustomUser.objects.all()
    return render(request, 'blog/admin/user_list.html', {'users': users})


@login_required
def user_create(request):
    """Create new admin user"""
    if not is_admin_user(request.user):
        messages.error(request, 'Accès refusé.')
        return redirect('login')

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])

            # Définir automatiquement le nouvel utilisateur comme admin
            if not user.role:
                user.role = 'admin'
            user.is_staff = True
            user.is_active = True

            user.save()
            messages.success(request, 'Utilisateur créé avec succès.')
            return redirect('user_list')
    else:
        form = UserForm()

    return render(request, 'blog/admin/user_form.html', {'form': form, 'title': 'Créer un utilisateur'})


@login_required
def user_delete(request, pk):
    """Delete admin user"""
    if not is_admin_user(request.user):
        messages.error(request, 'Accès refusé.')
        return redirect('login')

    user = get_object_or_404(CustomUser, pk=pk)

    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Utilisateur supprimé avec succès.')
        return redirect('user_list')

    return render(request, 'blog/admin/user_confirm_delete.html', {'user': user})


def user_logout(request):
    """Logout user"""
    logout(request)
    messages.success(request, 'Déconnexion réussie.')
    return redirect('home')