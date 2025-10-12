from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
from django.urls import reverse
import random

# Create your views here.

class ShowAllView(ListView):
    '''Define a view class to show all blog articles'''

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

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

class CreateArticleView(CreateView):
    '''Define a view class to create a new blog article'''

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def form_valid(self, form):

        print(f'CreateArticleView: form_valid(): {form.cleaned_data}')
        return super().form_valid(form)


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
