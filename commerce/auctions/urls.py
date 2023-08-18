from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.createListing,name="create"),
    path("<int:listingID>", views.viewListing, name="viewListing"),
    path("<int:listingID>/bid",views.addBid, name="addBid"),
    path("<int:listingID>/addWatchList", views.watchList, name="watchList"),
    path("<int:listingID>/removeWatchList", views.removeWatchList, name="removeWatchList"),
    path("watchlist",views.watchListPage, name="watchlistPage"),
    path("<int:listingID>/closeAuction", views.closeAuction, name="closeAuction"),
    path("<int:listingID>/comment",views.addComment,name="addComment"),
    path("category",views.categories, name="categories")
]
