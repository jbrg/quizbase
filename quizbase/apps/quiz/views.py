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

#### Stuff for browsing through collections, questions and stuff ####

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
    ## Get questions in collection using current question id
    currentQuestion = Question.objects.get(pk=question_id)
    questionList = currentQuestion.collection.question_set.all()
    
    ## We need to find out where in the list the question is, this is done by:
    ## Iterate over the questions and check for an id matching current question id
    ## if match, remember where in the list that object is 
    for i, question in enumerate(questionList):
        if question.id == currentQuestion.id:
            questionIndex = i
        else:
            pass
    
    ## Then we take that index and decrease it by one
    ## And if necessary, wrap it to avoid index out of range error
    questionIndex -= 1
    if questionIndex < 0:
        questionIndex = (len(questionList) - 1)
    else:
        pass
    question_id = questionList[questionIndex].id
    return HttpResponseRedirect(reverse("quizbase.apps.quiz.views.viewQuestion", args={question_id}))

def nextQuestion(request, question_id):
    ## Get questions in collection using current question id
    currentQuestion = Question.objects.get(pk=question_id)
    questionList = currentQuestion.collection.question_set.all()
    
    ## We need to find out where in the list the question is, this is done by:
    ## Iterate over the questions and check for an id matching current question id
    ## if match, remember where in the list that object is 
    for i, question in enumerate(questionList):
        if question.id == currentQuestion.id:
            questionIndex = i
        else:
            pass

    ## Then we take that index and increase it by on
    ## and if necessary, wrap it to avoid index out of range error
    questionIndex += 1
    if questionIndex == len(questionList):
        questionIndex = 0
    else:
        pass
    question_id = questionList[questionIndex].id   
    return HttpResponseRedirect(reverse("quizbase.apps.quiz.views.viewQuestion", args={question_id}))

#### Stuff for adding new collections, questions, choices and stuff ####
#### this functions is basically divided into two groups, new and add
#### new* will retreive data from forms on index and render specific forms
#### add* will retrieve data from the specific forms and save it to the database

def addCollection(request):
    newCollectionName = request.POST['newCollectionName']
    if Collection.objects.filter(name__exact=newCollectionName):
        #return error stuff here
        pass
    newCollection = Collection()
    newCollection.name = newCollectionName
    newCollection.save()
    return HttpResponseRedirect(reverse("quizbase.apps.quiz.views.index"))

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

# def newChoice(request, question_id):
#     return render_to_response("quiz/new/choice.html",
#                               {"question_id": question_id},
#                               context_instance=RequestContext(request))

def newChoice(request, question_id):
    if request.method == 'POST':
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
    else:
        return render_to_response("quiz/new/choice.html",
                                  {"question_id": question_id},
                                  context_instance=RequestContext(request))
  

#### Stuff for editing collections, question, choices and stuff ####
#### comments from the previous section more or less applies here, except here we have edit/save

def editQuestion(request, question_id=0):
    if request.path == '/quiz/edit/question/':
        question_id = request.POST['editQuestionId']
        return HttpResponseRedirect(reverse("quizbase.apps.quiz.views.editQuestion", args={question_id}))
    elif request.path == '/quiz/edit/question/'+question_id+'/':
        question = Question.objects.get(pk=question_id)
        choiceList = question.choice_set.all()
        return render_to_response("quiz/edit/question.html",
                                  {"question_id": question_id,
                                   "question": question,
                                   "choiceList": choiceList},
                                  context_instance=RequestContext(request))

def saveQuestion(request, question_id):
    editQuestionNewQuestion = request.POST['editQuestionNewQuestion']
    editQuestion = Question.objects.get(pk=question_id)
    editQuestion.question = editQuestionNewQuestion
    editQuestion.save()
    return HttpResponseRedirect(reverse("quizbase.apps.quiz.views.editQuestion", args={question_id}))

def saveChoice(request, question_id):
    ## retrieve data
    editChoiceId = request.POST['editChoiceId']
    editChoiceNewChoice = request.POST['editChoiceNewChoice']
    correctAnswer = int(request.POST['correctAnswer'])
    editChoice = Choice.objects.get(pk=editChoiceId)

    ## save new choice 
    if editChoiceNewChoice:
        editChoice.choice = editChoiceNewChoice
        editChoice.save()
    else:
        pass

    ## create or remove CorrectAnswer entry
    if correctAnswer == 1:
        newCorrectAnswer = CorrectAnswer()
        newCorrectAnswer.question = Question.objects.get(pk=question_id)
        newCorrectAnswer.answer = editChoice
        newCorrectAnswer.save()
    elif correctAnswer == 0:
        if editChoice.correctanswer_set.all():
            editChoice.correctanswer_set.all().delete()
        else:
            pass
    else:
        pass
    return HttpResponseRedirect(reverse("quizbase.apps.quiz.views.editQuestion", args={question_id}))

#### Stuff for deleting collections, questions, choices and junk ####

def deleteQuestion(request):
    question_id = request.POST['deleteQuestionId']
    deleteQuestion = Question.objects.get(pk=question_id)
    deleteQuestion.delete()
    return HttpResponseRedirect(reverse("quizbase.apps.quiz.views.index"))

def deleteCollection(request):
    collection_id = request.POST['deleteCollectionId']
    deleteCollection = Collection.objects.get(pk=collection_id)
    deleteCollection.delete()
    return HttpResponseRedirect(reverse("quizbase.apps.quiz.views.index"))
