# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from quizbase.apps.quiz.models import *

def index(request):
    collectionList = Collection.objects.all()
    return render_to_response("quiz/index.html", 
                              {"collectionList": collectionList},
                              context_instance=RequestContext(request))

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


def addCollection(request):
    newCollectionName = request.POST['newCollectionName']
    if Collection.objects.filter(name__exact=newCollectionName):
        #return error stuff here
        pass
    newCollection = Collection()
    newCollection.name = newCollectionName
    newCollection.save()
    return HttpResponseRedirect(reverse("quizbase.apps.quiz.views.index"))

def newQuestion(request):
    collection_id = request.POST['collection_id']
    return render_to_response("quiz/newQuestion.html",
                              {"collectionList": collectionList},
                              context_instance=RequestContext(request))

def addQuestion(request):
    newQuestionQuestion = request.POST['newQuestionQuestion']
    collection_id = request.POST['newQuestionCollection']
    if Question.objects.filter(question__exact=newQuestionQuestion):
        #return error stuff here
        #Also, we probably want to be able to have the same question in different objects in different collections
        pass
    newQuestion = Question()
    newQuestion.question = newQuestionQuestion
    newQuestion.collection = Collection.objects.get(pk=collection_id)
    newQuestion.save()
    return HttpResponseRedirect(reverse("quizbase.apps.quiz.views.newChoice", args={newQuestion.id}))

def newChoice(request, question_id):
    return render_to_response("quiz/new/choice.html",
                              {"question_id": question_id},
                              context_instance=RequestContext(request))

def addChoice(request, question_id):
    newChoiceChoice = request.POST['newChoiceChoice']
    correctAnswer = int(request.POST['correctAnswer'])
    if Choice.objects.filter(choice__exact=newChoiceChoice):
        #return error stuff
        #We don't want duplicate choices to the same question
        pass
    newChoice = Choice()
    newChoice.choice = newChoiceChoice
    newChoice.question = Question.objects.get(pk=question_id)
    newChoice.save()
    if correctAnswer == 1:
        newCorrectAnswer = CorrectAnswer()
        newCorrectAnswer.question = Question.objects.get(pk=question_id)
        newCorrectAnswer.answer = newChoice
        newCorrectAnswer.save()
    else:
        pass
    return HttpResponseRedirect(reverse("quizbase.apps.quiz.views.newChoice", args={question_id}))

# def addQuestion(request):
#     newQuestionEntry = Question()
#     collectionToAddTo = Collection.objects.get(pk=request.POST['newQuestionCollection'])
#     newQuestionEntry.collection = collectionToAddTo
#     newQuestionEntry.question = request.POST['newQuestion']
#     newQuestionEntry.save()
    
#     choice1 = Choice()
#     choice1.question = newQuestionEntry
#     choice1.choice = request.POST['newQuestionChoice1']
#     choice1.save()
    
#     choice2 = Choice()
#     choice2.question = newQuestionEntry
#     choice2.choice = request.POST['newQuestionChoice2']
#     choice2.save()
    
#     choice3 = Choice()
#     choice3.question = newQuestionEntry
#     choice3.choice = request.POST['newQuestionChoice3']
#     choice3.save()
    
#     choice4 = Choice()
#     choice4.question = newQuestionEntry
#     choice4.choice = request.POST['newQuestionChoice4']
#     choice4.save()
    
#     correctAnswer = CorrectAnswer()
#     correctAnswer.question = newQuestionEntry
#     correctAnswer.answer = choice1
#     correctAnswer.save()
    
#     return HttpResponseRedirect(reverse("quizbase.apps.quiz.views.newQuestion", args={}))
