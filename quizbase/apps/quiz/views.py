# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from quizbase.apps.quiz.models import *

def index(request):
    collectionList = Collection.objects.all()
    questionList = Question.objects.all()
    return render_to_response("quiz/index.html", 
                              {"collectionList": collectionList,
                               "questionList": questionList},
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
    correctChoiceList = q.correctanswer_set.all()
    corrected = "Nay..."
    for correctChoice in correctChoiceList:
        if selectedChoice == correctChoice.answer:
            corrected = "Yay!"
    
    return render_to_response("quiz/question.html", 
                              {"question": q, "corrected": corrected},
                              context_instance=RequestContext(request))

def previousQuestion(request, question_id):
    currentQuestion = Question.objects.get(pk=question_id)
    questionList = currentQuestion.collection.question_set.all()
    for i, question in enumerate(questionList):
        if question.id == currentQuestion.id:
            questionIndice = i
    questionIndice -= 1
    if questionIndice < 0:
        questionIndice = (len(questionList) - 1)
    question_id = questionList[questionIndice].id
    return HttpResponseRedirect(reverse("quizbase.apps.quiz.views.viewQuestion", args={question_id}))

def nextQuestion(request, question_id):
    currentQuestion = Question.objects.get(pk=question_id)
    questionList = currentQuestion.collection.question_set.all()
    for i, question in enumerate(questionList):
        if question.id == currentQuestion.id:
            questionIndice = i
    questionIndice += 1
    if questionIndice == len(questionList):
        questionIndice = 0
    question_id = questionList[questionIndice].id   
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

def editQuestion(request):
    question_id = request.POST['editQuestionId']
    editQuestionNewQuestion = request.POST['editQuestionNewQuestion']
    editQuestion = Question.objects.get(pk=question_id)
    editQuestion.question = editQuestionNewQuestion
    editQuestion.save()
    #if editQuestion.question == editQuestionNewQuestion:
    #    result = "Success!"
    #else:
    #    result = "Fail..."
    return HttpResponseRedirect(reverse("quizbase.apps.quiz.views.index"))

def deleteQuestion(request):
    question_id = request.POST['deleteQuestionId']
    deleteQuestion = Question.objects.get(pk=question_id)
    deleteQuestion.delete()
    return HttpResponseRedirect(reverse("quizbase.apps.quiz.views.index"))
