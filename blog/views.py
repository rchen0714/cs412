from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login # NEW
import random

# Create your views here.

class ShowAllView(ListView):
    '''Define a view class to show all blog articles'''

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''
 
 
        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')
 
 
        return super().dispatch(request, *args, **kwargs)

class ArticleView(DetailView):
    '''Display a single article'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article" #singular name

class RandomArticleView(DetailView):
    '''Display a single artice at random '''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article"

    #special method 

    def get_object(self):
        '''return one instance of the Article object selected 
        at random.'''

        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article 

class CreateArticleView(LoginRequiredMixin, CreateView):
    '''Define a view class to create a new blog article'''

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}')
 
        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}")
 
        # attach user to form instance (Article object):
        form.instance.user = user
 
        return super().form_valid(form)
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 


class CreateCommentView(CreateView):
    '''Define a view class to create a new comment on an article'''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse('article', kwargs={'pk': pk})
    
    def get_context_data(self):
        context = super().get_context_data()

        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        context['article'] = article
        return context
    
    def form_valid(self, form):
        '''Called when a valid form is submitted.'''

        print(form.cleaned_data)

        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        form.instance.article = article 

        return super().form_valid(form)
    













    
class UpdateArticleView(UpdateView):
    '''Define a view class to update an existing blog article'''

    model = Article
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'UpdateArticleView: form.cleaned_data={form.cleaned_data}')
 
 
        return super().form_valid(form)

class DeleteCommentView(DeleteView):
    '''Define a view class to delete an existing comment on an article'''

    model = Comment
    template_name = "blog/delete_comment_form.html"

    def get_success_url(self):

        pk = self.kwargs['pk']
        comment = Comment.objects.get(pk=pk)

        article = comment.article
        return reverse('article', kwargs={'pk': article.pk})

class RegistrationView(CreateView):
    '''
    show/process form for account registration
    '''
 
    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User

    def get_success_url(self):
        '''The URL to redirect to after creating a new User.'''
        return reverse('login')
    
    def form_valid(self, form):
        # Save the new user
        user = form.save()

        return super().form_valid(form)