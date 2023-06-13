from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import ListingForm, BidForm
from django.db.models import Max


from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.all() # Fetch all listing objects from the database
    return render(request, "auctions/index.html", {"listings": listings})


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

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        print(request.POST)  # debug print to see the POST data
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            messages.success(request, "Listing created successfully!")
            return HttpResponseRedirect(reverse("index"))
        else:
            print(form.errors)
    else:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        form = ListingForm()
    return render(request, "auctions/create_listing.html", {
        "form": form
    })

def listing_detail(request, listing_id):
    # Fetch the listing data. Raise a 404 error if the object doesn't exist.
    listing = get_object_or_404(Listing, pk=listing_id)
    
    # Create a new instance of BidForm
    bid_form = BidForm(request.POST or None)

    if request.method == 'POST':
        # Check if 'add_to_watchlist' is a key in request.POST. If it is, add the listing to the watchlist.
        if 'add_to_watchlist' in request.POST:
            request.user.watchlist.add(listing)
            messages.success(request, "Added to watchlist!")
        # Check if 'remove_from_watchlist' is a key in request.POST. If it is, remove the listing from the watchlist.
        elif 'remove_from_watchlist' in request.POST:
            request.user.watchlist.remove(listing)
            messages.success(request, "Removed from watchlist!")
        # Check if 'place_bid' is a key in request.POST. If it is, validate and place a bid.
        elif 'place_bid' in request.POST and bid_form.is_valid():
            bid = bid_form.save(commit=False)
            bid.user = request.user  # assign the current user to the bid
            bid.listing = listing
            highest_bid = listing.bids.aggregate(Max('amount'))['amount__max'] or 0
            if bid.amount > highest_bid or (not listing.bids.exists() and bid.amount >= listing.start_bid):
                bid.save()
                messages.success(request, "Bid placed successfully!")
            else:
                messages.warning(request, "Bid should be higher than the current highest bid or starting bid.")

    is_in_watchlist = request.user.watchlist.filter(pk=listing_id).exists() if request.user.is_authenticated else False
    current_bid = listing.highest_bid() if listing.bids.exists() else listing.start_bid
    
    # Fetch all comments associated with the listing
    comments = listing.comments.all()
    
    return render(request, "auctions/listing_detail.html", {
        "listing": listing,
        "is_in_watchlist": is_in_watchlist,
        "bid_form": bid_form,
        "current_bid": current_bid,
        "comments": comments,
    })
    
@login_required
def toggle_watchlist(request, listing_id):
    # Get the listing.
    listing = get_object_or_404(Listing, id=listing_id)
    
    # Check if the listing is in the user's watchlist.
    if listing.watched_by.filter(id=request.user.id).exists():
        # If it is, remove it.
        listing.watched_by.remove(request.user)
    else:
        # If it's not, add it.
        listing.watched_by.add(request.user)
    
    # Redirect back to the listing detail page.
    return HttpResponseRedirect(reverse('listing_detail', args=[listing_id]))

@login_required
def close_listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)

    if request.method == "POST":
        if request.user == listing.owner:
            # Close the listing
            listing.is_active = False

            # If the listing has bids, set the winner to the user who placed the highest bid
            if listing.bids.exists():
                highest_bid = listing.bids.order_by('-amount').first()
                listing.winner = highest_bid.user

            # Save the changes
            listing.save()

            # Display a success message
            messages.success(request, "Listing closed successfully!")
        
    return redirect('listing_detail', listing_id=listing_id)

@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.method == "POST":
        text = request.POST['text']
        Comment.objects.create(user=request.user, listing=listing, text=text)
        messages.success(request, "Comment added successfully!")
    return redirect('listing_detail', listing_id=listing.id)