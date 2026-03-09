from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Blog, CustomUser
from .forms import BlogForm, UserForm




def home(request):
    """Public home page showing all blog posts"""
    blogs = Blog.objects.all()
    return render(request, 'blog/home.html', {'blogs': blogs})


def user_login(request):
    """User login page"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Connexion réussie.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Identifiants invalides.')

    return render(request, 'blog/login.html')


@login_required
def dashboard(request):
    """User dashboard"""
    return render(request, 'blog/dashboard.html')


@login_required
def admin_dashboard(request):
    """User dashboard (alternative route)"""
    return render(request, 'blog/dashboard.html')


def blog_detail(request, pk):
    """View individual blog post"""
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/blog_detail.html', {'blog': blog})


@login_required
def blog_list(request):
    """List all blogs"""
    blogs = Blog.objects.all()
    return render(request, 'blog/admin/blog_list.html', {'blogs': blogs})


@login_required
def blog_create(request):
    """Create new blog post"""
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
    blog = get_object_or_404(Blog, pk=pk)

    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Article supprimé avec succès.')
        return redirect('blog_list')

    return render(request, 'blog/admin/blog_confirm_delete.html', {'blog': blog})


@login_required
def user_list(request):
    """List all users"""
    users = CustomUser.objects.all()
    return render(request, 'blog/admin/user_list.html', {'users': users})


@login_required
def user_create(request):
    """Create new user"""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Utilisateur créé avec succès.')
            return redirect('user_list')
    else:
        form = UserForm()

    return render(request, 'blog/admin/user_form.html', {'form': form, 'title': 'Créer un utilisateur'})


@login_required
def user_delete(request, pk):
    """Delete user"""
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

def contact_view(request):
    """Contact page for non-authenticated users"""
    return render(request, 'blog/contact.html')
