from allauth.account.views import LogoutView, LoginView, SignupView
from django.urls import path
from .views import (
	PostsList, PostDetail, SearchResults, PostCreate, PostUpdate, PostDelete, ResponseCreate, ResponseList,
	ResponseDelete, upgrade_user, ResponseAccept, subscriptions
)
from django.urls import path


urlpatterns = [
	path('', PostsList.as_view(), name='posts'),
	path('subscriptions/', subscriptions, name='subscriptions'),
	path('<int:pk>', PostDetail.as_view(), name='post_detail'),
	path('search/', SearchResults.as_view(), name='search'),
	# path('upgrade/', upgrade_user, name='upgrade'),
	path('accounts/logout', LogoutView.as_view, name='account_logout'),
	path('accounts/login', LoginView.as_view, name='account_login'),
	path('accounts/signup', SignupView.as_view, name='account_signup'),
	path('create/', PostCreate.as_view(), name='post_create'),
	path('<int:pk>/edit', PostUpdate.as_view(), name='post_edit'),
	path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
	path('<int:pk>/response', ResponseCreate.as_view(), name='add_response'),
	path('responses', ResponseList.as_view(), name='responses'),
	path('responses/<int:pk>/delete', ResponseDelete.as_view(), name='response_delete'),
	path('responses/<int:pk>/accept', ResponseAccept.as_view(), name='response_accept'),
]
