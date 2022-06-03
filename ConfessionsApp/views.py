from contextlib import ContextDecorator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Post, PostComment, Like, Confession
from django.db.models import Count
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def checkOwnershipConfession(user, confession):
    return confession.owner == user

# def checkOwnershipQuestion(user, confession):
#     return confession.owner == user

def index(request):
    return render(request, "ConfessionsApp/index.html")

def base(request):
    return render(request, "ConfessionsApp/base.html")

def questions(request):
    if request.method != "POST":

        SortBy = request.GET.get("SortBy")
        if SortBy == "Oldest":
            Questions = Question.objects.all().order_by("date")
        elif SortBy == "Newest":
            Questions = Question.objects.all().order_by("-date")
        else:
            Questions = Question.objects.all().order_by("-date")
        
        paginator = Paginator(Questions, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "ConfessionsApp/questions.html", {
            "page_obj" : page_obj,
        })
    else:
        question = Question.objects.create(question_text=request.POST["QuestionInput"], owner=request.user)
        Questions = Question.objects.all()
        context = {
            "Questions": Questions,
        }
        return redirect('ConfessionsApp:questions')

def question(request, q_id):
    if request.method != "POST":
        question = Question.objects.get(id=q_id)
        Posts = Post.objects.filter(question=question)
        context = {
            "Question": question,
            "Posts": Posts,
        }
        return render(request, "ConfessionsApp/question.html", context)
    else:
        question = Question.objects.get(id=q_id)
        post_data = request.POST["post-input"]
        post = Post.objects.create(
            owner=request.user,
            question=question,
            post_text=post_data,
        )
        return redirect("ConfessionsApp:question", q_id=q_id)
        

def confessions(request):
    if request.method != "POST":

        SortBy = request.GET.get('SortBy') 
        if SortBy == "Newest":
            Confessions = Confession.objects.all().order_by('-date')
        elif SortBy == "Oldest":
            Confessions = Confession.objects.all().order_by('date')
        else:
            Confessions = Confession.objects.all().order_by('-date')
        
        paginator = Paginator(Confessions, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'ConfessionsApp/confessions.html', 
                    {'page_obj': page_obj,
                    'SortBy' : SortBy,})

    else:
        confession = Confession.objects.create(body=request.POST["ConfessionInput"], owner=request.user)
        Confessions = Confession.objects.all().order_by('-date')
        context = {
            "Confessions": Confessions,
        }
        return redirect('ConfessionsApp:confessions')

@login_required
def likeconfession(request, c_id):

    confession = get_object_or_404(Confession, id=c_id)
    if not checkOwnershipConfession(request.user, confession):
        return redirect('ConfessionsApp:confessions')


    if confession.like_set.filter(owner=request.user, confession=confession).exists():
        user_like = Like.objects.filter(owner=request.user, confession=confession)[0]
        confession.like_set.remove(user_like)
    else:
        Like.objects.create(owner=request.user, confession=confession)
    
    return redirect('ConfessionsApp:confessions')

@login_required
def deleteconfession(request, c_id):
    confession = get_object_or_404(Confession, id=c_id)

    if not checkOwnershipConfession(request.user, confession):
        return redirect('ConfessionsApp:confessions')

    if confession.owner == request.user:
        confession.delete()
    
    return redirect('ConfessionsApp:confessions')

@login_required
def editconfession(request, c_id):
    confession = get_object_or_404(Confession, id=c_id)
    if not checkOwnershipConfession(request.user, confession):
        return redirect('ConfessionsApp:confessions')
    
    if request.method != "POST":
        
        context = {
            "confession" : confession
        }
        return render(request, 'ConfessionsApp/editconfessionForm.html', context=context)
    else:
        confession.body = request.POST["confessionText"]
        confession.save()
        return redirect('ConfessionsApp:confessions')     

@login_required
def userConfessions(request):
    user = request.user
    confessions = Confession.objects.filter(owner=user).order_by("-date")
    context = {
        'confessions' : confessions
    }
    return render(request, 'ConfessionsApp/userConfessions.html', context=context)

@login_required
def userQuestions(request):
    user = request.user
    Questions = Question.objects.filter(owner=user).order_by('-date')
    context = {
        'questions' : Questions,
    }
    return render(request, 'ConfessionsApp/userQuestions.html', context=context)

@login_required
def userComments(request):
    user = request.user
    Comments = Post.objects.filter(owner=user)
    context = {
        'comments' : Comments,
    }
    return render(request, 'ConfessionsApp/userComments.html', context=context)

def privacy(request):
    return render(request, "ConfessionsApp/privacy.html")

def about(request):
    return render(request, "ConfessionsApp/about.html")
