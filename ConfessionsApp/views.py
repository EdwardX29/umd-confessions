from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Post,  Confession
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

'''
Helper functions
'''

def checkOwnershipConfession(user, confession):
    return confession.owner == user

def checkOwnershipQuestion(user, question):
    return question.owner == user

def checkOwnershipComment(user, comment):
    return comment.owner == user

'''
Generic/Static views
'''

def index(request):
    return render(request, "ConfessionsApp/index.html")

def base(request):
    return render(request, "ConfessionsApp/base.html")

def privacy(request):
    return render(request, "ConfessionsApp/privacy.html")

def about(request):
    return render(request, "ConfessionsApp/about.html")


'''
Question Views
'''

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
        question = Question.objects.create(question_text=request.POST["QuestionInput"], 
                                            body=request.POST["QuestionBodyInput"], 
                                            owner=request.user)
        questions = Question.objects.all()
        context = {
            "questions": questions,
        }
        return redirect('ConfessionsApp:questions')

def deletequestion(request, q_id):

    question = get_object_or_404(Question, id=q_id)
    if not checkOwnershipQuestion(request.user, question):
        return redirect("ConfessionsApp:questions")
    
    if question.owner == request.user:
        question.delete()

    return redirect("ConfessionsApp:questions") 

def editquestion(request, q_id):

    question = get_object_or_404(Question, id=q_id)
    if not checkOwnershipQuestion(request.user, question):
        return redirect("ConfessionsApp:questions")
    
    if request.method != "POST":
        context = {
            "question" : question,
        }
        return render(request, "ConfessionsApp/editQuestion.html", context=context)
    else:

        question.question_text = request.POST["questionText"]
        question.body = request.POST["questionBody"]

        question.edited = True
        question.save()
        return redirect("ConfessionsApp:question", q_id=q_id)


def question(request, q_id):
    if request.method != "POST":
        question = Question.objects.get(id=q_id)
        posts = Post.objects.filter(question=question)
        context = {
            "question": question,
            "posts": posts,
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
        

'''
Confession views
CRUD
'''

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
        confessions = Confession.objects.all().order_by('-date')
        context = {
            "confessions": confessions,
        }
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
        confession.edited = True
        confession.save()
        return redirect('ConfessionsApp:confessions')     


'''
Comment views
'''

@login_required
def deletecomment(request, q_id, cm_id):
    comment = get_object_or_404(Post, id=cm_id)
    if not checkOwnershipComment(request.user, comment):
        return redirect('ConfessionsApp:question', q_id=q_id)
    
    if comment.owner == request.user:
        comment.delete()
    return redirect('ConfessionsApp:question', q_id=q_id)

@login_required
def editcomment(request, q_id, cm_id):
    comment = get_object_or_404(Post, id=cm_id)
    if not checkOwnershipComment(request.user, comment):
        return redirect("ConfessionsApp:question", q_id=q_id)
    if request.method != "POST":
        context = {
            "comment":comment,
        }
        return render(request,"ConfessionsApp/editCommentForm.html", context=context)
    else:
        comment.post_text = request.POST["commentText"]
        comment.edited = True
        comment.save()

        return redirect('ConfessionsApp:question', q_id=q_id)


'''
Views to get User content
'''
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
    questions = Question.objects.filter(owner=user).order_by('-date')
    context = {
        'questions' : questions,
    }
    return render(request, 'ConfessionsApp/userQuestions.html', context=context)

@login_required
def userComments(request):
    user = request.user
    comments = Post.objects.filter(owner=user)
    context = {
        'comments' : comments,
    }
    return render(request, 'ConfessionsApp/userComments.html', context=context)
