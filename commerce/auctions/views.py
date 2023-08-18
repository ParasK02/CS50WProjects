from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import User,Auction,Bid, Comment


def index(request):
    auctions = Auction.objects.all()
    return render(request, "auctions/index.html",{
        'auctions':auctions
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
@login_required(login_url='auctions/login.html')
def createListing(request):
    if request.method == 'POST':
        user = request.user  # Use the actual user instance
        title = request.POST['title']
        description = request.POST['description']
        startPrice = Decimal(request.POST['price'])
        price = startPrice
        category = request.POST['category'].lower().capitalize()
        imageURL = request.POST['imageURL']
        createdOn = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        isActive = True
        listing = Auction(
            user=user,  # Assign the user instance
            title=title,
            description=description,
            startPrice=startPrice,
            currentPrice=price,
            imageURL=imageURL,
            createdOn=createdOn,
            isActive=isActive,
            category=category
        )
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        print("Failed to create listing")
        return render(request, "auctions/create.html")
def viewListing(request,listingID):
    listing = get_object_or_404(Auction, id=listingID)
    return render(request, "auctions/listing.html",{
        "listing" : listing,
        "bids": Bid.objects.filter(listing=listingID),
        "comments": Comment.objects.filter(listing=listingID)
    })
@login_required(login_url='auctions/login.html')
def addBid(request, listingID):
    if request.method == 'POST':
        user = request.user
        bidAmount = Decimal(request.POST["bidAmount"])
        bidDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        listing = get_object_or_404(Auction, id=listingID)
        if  user != listing.user and bidAmount > listing.currentPrice:
            placeBid = Bid(user=user, bidAmount=bidAmount, bidDate=bidDate, listing=listing)
            placeBid.save()
            listing.currentPrice = bidAmount
            listing.save()
            return HttpResponseRedirect(reverse('viewListing', args=(listingID,)))
        else:
            return render(request, "auctions/listing.html",{
                "listing": listing,
                "failed": True
            })
    return HttpResponseRedirect(reverse('viewListing', args=(listingID,)))

@login_required(login_url='auctions/login.html')
def watchList(request, listingID):
    listing = get_object_or_404(Auction, id=listingID)
    request.user.watchlist.add(listing)

    return HttpResponseRedirect(reverse('viewListing', args=(listingID,)))
    
@login_required(login_url='auctions/login.html')
def removeWatchList(request,listingID):
    listing = get_object_or_404(Auction, id=listingID)
    request.user.watchlist.remove(listing)
    return HttpResponseRedirect(reverse('viewListing', args=(listingID,)))
    

    
@login_required(login_url='auctions/login.html')
def watchListPage(request):
   return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all()
    })

@login_required(login_url='auctions/login.html')
def closeAuction(request,listingID):
    listing = get_object_or_404(Auction, id=listingID)
    listing.isActive = False
    latestBid = Bid.objects.filter(listing=listing).order_by('-bidDate').first()
    listing.winner = latestBid.user.username
    listing.save()
    
    return HttpResponseRedirect(reverse('viewListing', args=(listingID,)))


@login_required(login_url='auctions/login.html')
def addComment(request,listingID):
    if request.method == 'POST':
        commentText = request.POST['comment']
        user = request.user
        listing = get_object_or_404(Auction, id=listingID)
        commentDate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        comment = Comment(user=user, commentText=commentText,listing=listing, datePosted=commentDate)
        comment.save()
        return HttpResponseRedirect(reverse('viewListing', args=(listingID,)))
    return HttpResponseRedirect(reverse('viewListing', args=(listingID,)))

        
def categories(request):
    if request.method == 'POST':
        category_name = request.POST.get("category").capitalize()
        if category_name:  # Check if a category was selected
            auctions = Auction.objects.filter(category=category_name)
        else:
            auctions = Auction.objects.all()
    else:
        auctions = Auction.objects.all()

    return render(request, "auctions/categories.html", {
        'auctions': auctions
    })
