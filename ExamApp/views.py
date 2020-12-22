from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'regLogPage.html')

def regUser(request):
    errorsFromValidator = User.objects.registerValidator(request.POST)
    if len(errorsFromValidator) > 0:
        for k, v in errorsFromValidator.items():
            messages.error(request, v)
        return redirect('/')
    else:
        reguser = User.objects.create(userName = request.POST['uName'], email = request.POST['email'], password = request.POST['pWord'])

        request.session['loggedInId'] = reguser.id

    return redirect('/success')  

def logIn(request):
    resultsFromValidator = User.objects.loginValidator(request.POST)
    if len(resultsFromValidator) > 0:
        for k, v in resultsFromValidator.items():
            messages.error(request, v)
        return redirect('/')
    else:
        emailMatch = User.objects.filter(email = request.POST['email'])
        request.session['loggedInId'] = emailMatch[0].id 
        return redirect('/success')

def successPage(request):
    if 'loggedInId' not in request.session:
        return redirect('/')

    context = {
        'loggedInUser': User.objects.get(id=request.session['loggedInId'])
    }
    return render(request, 'success.html', context)

def logOut(request):
    request.session.clear()
    return redirect('/')

def QuotesPage(request):
    if 'loggedInId' not in request.session:
        return redirect('/')
    
    context = {
        'loggedInUser': User.objects.get(id=request.session['loggedInId']),
        "allQuotes" : Quote.objects.all(),
        'favoritedQuotes' : Quote.objects.filter(favoritedBy = User.objects.get(id=request.session['loggedInId'])),
        'nonFavoritedQuotes' : Quote.objects.exclude(favoritedBy = User.objects.get(id=request.session['loggedInId']))
    }
    return render(request, 'quotesPage.html', context)

def newQuote(request):
    errorsFromValidator = Quote.objects.quoteValidator(request.POST)
    if len(errorsFromValidator) > 0:
        for k, v in errorsFromValidator.items():
            messages.error(request, v)
        return redirect('/quotes')
    else:
        loggedInUser = User.objects.get(id=request.session['loggedInId'])
        thisQuote = Quote.objects.create(source = request.POST['qSource'], description = request.POST['qDescription'], uploadedBy = loggedInUser)
        loggedInUser.favorited_quotes.add(thisQuote)
    return redirect('/quotes')

def userPage(request, UserId):
    count = 0
    for i in Quote.objects.filter(uploadedBy = User.objects.get(id=UserId)):
        count += 1
    
    context = {
        'profileUser': User.objects.get(id=UserId),
        "quotesPostedBy" : Quote.objects.filter(uploadedBy = User.objects.get(id=UserId)),
        'counter' : count
    }
    return render(request, 'profilePage.html', context)

def delete(request, quoteId):
    thisQuote = Quote.objects.get(id=quoteId)
    thisQuote.delete()
    return redirect('/quotes')

def favorite(request, quoteId):
    loggedInUser = User.objects.get(id=request.session['loggedInId'])
    thisQuote = Quote.objects.get(id=quoteId)
    loggedInUser.favorited_quotes.add(thisQuote)
    return redirect('/quotes')

def unfavorite(request, quoteId):
    loggedInUser = User.objects.get(id=request.session['loggedInId'])
    thisQuote = Quote.objects.get(id=quoteId)
    loggedInUser.favorited_quotes.remove(thisQuote)
    return redirect('/quotes')

def editPage(request, quoteId):
    context = {
        'thisQuote' : Quote.objects.get(id=quoteId)
    }
    return render(request, 'editPage.html', context)

def update(request, quoteId):
    errorsFromValidator = Quote.objects.quoteValidator(request.POST)
    if len(errorsFromValidator) > 0:
        for k, v in errorsFromValidator.items():
            messages.error(request, v)
        return redirect('/quotes/quoteId')
    else:
        thisQuote = Quote.objects.get(id=quoteId)
        thisQuote.source = request.POST['qSource']
        thisQuote.description = request.POST['qDescription']
        thisQuote.save()
        return redirect('/quotes')
