from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from models import *

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
                                  {'cardText': card.question})
    elif request.path == '/flash/view/card/'+cardId+'/answer/':
        return render_to_response('flash/view/card.html',
                                  {'cardText': card.answer})
    else:
        return render_to_response('flash/view/card.html')
