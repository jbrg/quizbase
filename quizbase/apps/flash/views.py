## Django stuff
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

## App stuff
from models import *

## Python stuff
import re

#### Stuff for viewing stuff ####

def index(request):
    collections = Collection.objects.all()
    cards = Card.objects.all()
    return render_to_response('flash/index.html',
                              {'collections': collections,
                               'cards': cards},
                              context_instance=RequestContext(request))

def listCollections(request):
    collections = Collection.objects.all()
    return render_to_response('flash/collections.html',
                              {'collections': collections})

def viewCollection(request, collectionId):
    collection = Collection.objects.get(pk=collectionId)
    cards = collection.card_set.all()
    return render_to_response('flash/view/collection.html',
                              {'collection': collection,
                               'cards': cards})

def viewCard(request, cardId):
    card = Card.objects.get(pk=cardId)
    if request.path == '/flash/view/card/'+cardId+'/question/':
        return render_to_response('flash/view/card.html',
                                  {'cardText': card.question,
                                   'card': card})
    elif request.path == '/flash/view/card/'+cardId+'/answer/':
        return render_to_response('flash/view/card.html',
                                  {'cardText': card.answer,
                                   'card': card})
    else:
        return render_to_response('flash/view/card.html',
                                  {'cardText': card.answer,
                                   'card': card})

def cycleCard(request, cardId):
    currentCard = Card.objects.get(pk=cardId)
    cards = currentCard.collection.card_sed.all()

    for i, card in enumerate(cards):
        if card.id == currentCard.id:
            cardId = i
        else:
            pass

    if re.match('\W+/previous/', request.path):
        cardIndex -= 1
        if cardIndex < 0:
            cardIndex = (len(cards) - 1)
    elif re.match('\W+/next/', request.path):
        cardIndex += 1
        if cardIndex == len(cards):
            cardIndex = 0
    cardId = cards[cardIndex].id
    return HttpResponseRedirect(reverse('quizbase.apps.flash.views.viewCard', args={cardId}))
