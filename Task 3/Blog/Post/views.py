from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import DetailView, View, CreateView, UpdateView, DeleteView

from .models import UserPost, SimpleUser
from .forms import PostForm, LoginForm, RegistrationForm


class HomeView(View):
    """View for home page with all posts."""
    def get(self, request, *args, **kwargs):
     posts = UserPost.objects.all()
     context = {
         'posts': posts,
     }
     return render(request, 'Post/home.html', context)


class PostView(DetailView):
    """View with post information."""
    model = UserPost
    template_name = 'Post/post.html'
    context_object_name = 'post'


class LoginView(View):
    """Log in user on platform."""
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form}
        return render(request, 'Post/login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
        return render(request, 'Post/login.html', {'form': form})


class RegistrationView(View):
    """Registrate user on platform."""
    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {'form': form}
        return render(request, 'Post/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.email = form.cleaned_data['email']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            SimpleUser.objects.create(
                user=new_user,
                name=form.cleaned_data['name'],
            )
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            login(request, user)  # log in user on platform
            return redirect('home')
        return render(request, 'Post/registration.html', {'form': form})


class CreatePost(CreateView):
    """Create post on platform by user."""
    template_name = 'Post/create_post.html'
    fields = '__all__'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = PostForm(request.POST)
            context = {'form': form}
            return render(request, 'Post/create_post.html', context)
        return redirect('home')

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        author = SimpleUser.objects.get(user=request.user)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.title = form.cleaned_data.get('title')
            new_post.content = form.cleaned_data.get('content')
            new_post.image = form.cleaned_data.get('image')
            new_post.author = author
            new_post.is_published = True
            new_post.save()
            return redirect('home')
        return render(request, 'Post/create_post.html', {'form': form})


class UpdatePost(UpdateView):
    """Update posts on platform by user."""
    template_name = 'Post/update_post.html'
    fields = ('title', 'content', 'image')

    def get(self, request, *args, **kwargs):
        author = SimpleUser.objects.get(user=request.user)
        post = UserPost.objects.get(pk=kwargs['pk'])
        if post.author == author:
            form = PostForm(request.POST, request.FILES, instance=post)
            context = {'form': form}
            return render(request, 'Post/update_post.html', context)
        return redirect('home')

    def post(self, request, *args, **kwargs):
        post = UserPost.objects.get(pk=kwargs['pk'])
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'Post/update_post.html', {'form': form})


class DeletePost(DeleteView):
    """Delete posts on platform by superuser."""
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            post_pk = kwargs.get('pk')
            post = UserPost.objects.get(pk=post_pk)
            post.delete()
        return redirect('home')