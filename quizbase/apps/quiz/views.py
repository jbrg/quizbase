# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from quizbase.apps.quiz.models import *

#def index(request): ## I assume there's no reason to have this
#    questionList = Question.objects.all()
#    return render_to_response("quiz/index.html", {"questionList": questionList})

def listCollections(request):
    collectionList = Collection.objects.all()
    return render_to_response("quiz/collections.html",
                              {"collectionList": collectionList})

def browseCollection(request, collection_id):
    collection = Collection.objects.get(pk=collection_id)
    questionList = collection.question_set.all()
    return render_to_response("quiz/questions.html",
                              {"collection": collection,
                               "questionList": questionList})

def viewQuestion(request, question_id):
    q = Question.objects.get(pk=question_id)
    return render_to_response("quiz/question.html", 
                              {"question": q},
                              context_instance=RequestContext(request))

def correctQuestion(request, question_id):
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

def previousQuestion(request, question_id):
    question_id = int(question_id) -1
    if question_id < 1:
        question_id = len(Question.objects.all())
    
    return HttpResponseRedirect(reverse("quizbase.apps.quiz.views.viewQuestion", args={question_id}))

def nextQuestion(request, question_id):
    question_id = int(question_id) +1
    if question_id > len(Question.objects.all()):
        question_id = 1
    
    return HttpResponseRedirect(reverse("quizbase.apps.quiz.views.viewQuestion", args={question_id}))
