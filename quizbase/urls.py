from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'quizbase.views.home', name='home'),
    # url(r'^quizbase/', include('quizbase.foo.urls')),
    #url(r'^quiz/$', 'quizbase.apps.quiz.views.index'),
    #url(r'^question/(?P<question_id>\d+)/$', 'quizbase.apps.quiz.views.question'),
    #url(r'^question/(?P<question_id>\d+)/correct/$', 'quizbase.apps.quiz.views.correct'),
    #url(r'^question/(?P<question_id>\d+)/previous/$', 'quizbase.apps.quiz.views.previous'),
    #url(r'^question/(?P<question_id>\d+)/next/$', 'quizbase.apps.quiz.views.next'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('quizbase.apps.quiz.views',
                        url(r'^quiz/$', 'index'),
                        url(r'^quiz/collection/(?P<collection_id>\d+)/$', 'browseCollection'),
                        url(r'^quiz/collection/question/(?P<question_id>\d+)/$', 'viewQuestion'),
                        url(r'^quiz/collection/question/(?P<question_id>\d+)/correct/$', 'correctQuestion'),
                        url(r'^quiz/collection/question/(?P<question_id>\d+)/next/$', 'nextQuestion'),
                        url(r'^quiz/collection/question/(?P<question_id>\d+)/previous/$', 'previousQuestion'),
                        url(r'^quiz/add/collection/$', 'addCollection'),
                        url(r'^quiz/add/question/$', 'addQuestion'),
                        url(r'^quiz/new/choice/(?P<question_id>\d+)/$', 'newChoice'),
                        url(r'^quiz/add/choice/(?P<question_id>\d+)/$', 'newChoice'),
                        url(r'^quiz/edit/question/$', 'editQuestion'),
                        url(r'^quiz/edit/question/(?P<question_id>\d+)/$', 'editQuestion'),
                        url(r'^quiz/save/question/(?P<question_id>\d+)/$', 'saveQuestion'),
                        url(r'^quiz/save/choice/(?P<question_id>\d+)/$', 'saveChoice'),
                        url(r'^quiz/delete/question/$', 'deleteQuestion'),
                        url(r'^quiz/delete/collection/$', 'deleteCollection'),
)

urlpatterns += patterns('quizbase.apps.flash.views',
                        url(r'^flash/$', 'index'),
                        url(r'^flash/view/collection/(?P<collectionId>\d+)/$', 'viewCollection'),
                        url(r'^flash/view/card/(?P<cardId>\d+)/\w*/*$', 'viewCard'),
                        url(r'^flash/view/card/(?P<cardId>\d+)/\w*/\w+/$', 'cycleCard'),
)
