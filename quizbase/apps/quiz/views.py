# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from quizbase.apps.quiz.models import Question, Choice

def index(request):
    questionList = Question.objects.all()
    return render_to_response("quiz/index.html", {"questionList": questionList})

def question(request, question_id):
    q = Question.objects.get(pk=question_id)
    return render_to_response("quiz/question.html", 
                              {"question": q},
                              context_instance=RequestContext(request))

def correct(request, question_id):
    q = Question.objects.get(pk=question_id)
    selectedChoice = q.choice_set.get(pk=request.POST['choice'])
    correctChoice = q.correctanswer_set.get(pk=question_id)
    
    if selectedChoice == correctChoice.answer:
        corrected = "Yay!"
    else:
        corrected = "Nay..."
    
    return render_to_response("quiz/question.html", 
                              {"question": q, "corrected": corrected},
                              context_instance=RequestContext(request))

def previous(request, question_id):
    question_id = int(question_id) -1
    if question_id < 1:
        question_id = len(Question.objects.all())
    
    return HttpResponseRedirect(reverse("quizbase.apps.quiz.views.question", args={question_id}))

def next(request, question_id):
    question_id = int(question_id) +1
    if question_id > len(Question.objects.all()):
        question_id = 1
    
    return HttpResponseRedirect(reverse("quizbase.apps.quiz.views.question", args={question_id}))
