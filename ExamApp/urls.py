from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration', views.regUser),
    path('logIn', views.logIn),
    path('success', views.successPage),
    path('logOut', views.logOut),
    path('quotes', views.QuotesPage),
    path('newQuote', views.newQuote),
    path('users/<int:UserId>', views.userPage),
    path('delete/<int:quoteId>', views.delete),
    path('Fav/<int:quoteId>', views.favorite),
    path('unFav/<int:quoteId>', views.unfavorite),
    path('edit/<int:quoteId>', views.editPage),
    path('updateQuote/<int:quoteId>', views.update)
]