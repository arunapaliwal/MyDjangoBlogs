from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,get_object_or_404
from .models import Post
from django.views.generic import ListView,DetailView
from .forms import CommentForm,AddPostForm
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.utils.text import slugify
# Create your views here.

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"
    
    def get_queryset(self):        
        queryset = super().get_queryset()
        data = queryset[:3]
        return data
    
class PostPageView(ListView):
    template_name = "blog/all-post.html"
    model = Post
    ordering = ["-id"]
    context_object_name = "all_posts"
    
    def get_queryset(self):        
        queryset = super().get_queryset()
        data = queryset
        return data    

class SinglePostView(View):
    template_name = "blog/post-detail.html"
    model = Post

    def is_stored_post(self,request,post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            saved_for_later = post_id in stored_posts
        else:
            saved_for_later = False
        
        return saved_for_later

    def get(self,request,slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form" : CommentForm(),
            "comments" : post.comments.all().order_by("-id"),
            "saved_for_later" : self.is_stored_post(request,post.id)
        }
        return render(request,"blog/post-detail.html",context)
    
    def post(self,request,slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse("post-detail-page",args=[slug]))
                
        context = {
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form" : comment_form,
            "comments" : post.comments.all().order_by("-id"),
            "saved_for_later" : self.is_stored_post(request,post.id)
        }
        return render(request,"blog/post-detail.html",context)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_tags"] = self.object.tags.all()
        context["comment_form"] = CommentForm
        return context
    
class ReadLater(View):    
    def get(self,request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None  or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True
        return render(request,"blog/stored-posts.html",context)

    def post(self,request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []
        
        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
            request.session["stored_posts"] = stored_posts
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")
    
class ThankkYouView(TemplateView):   
   template_name = "blog/thank-you.html"

   def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["message"] = "Your post saved successfully."
      return context
    
class AddPostView(CreateView):
    template_name = "blog/add-post.html"
    model = Post
    fields = ("title","excerpt","image","author","content","tags")    
    
    def get(self,request):        
        context = {            
            "post_form" : AddPostForm(),            
        }
        return render(request,"blog/add-post.html",context)
    
    def post(self,request):
        post_form = AddPostForm(request.POST)
        post_form = AddPostForm(request.POST,request.FILES) 

        if post_form.is_valid():            
            tmppost = post_form.save(commit=False)
            tmppost.slug = slugify(tmppost.title)            
            tmppost.save()
            post_form.save_m2m()

            return HttpResponseRedirect(reverse("thank-you"))
                
        context = {            
            "post_form" : post_form,
        }
        return render(request,"blog/add-post.html",context)