from allauth.account.views import LogoutView


from Accounts import views
from .views import (
	PostsList, PostDetail, SearchResults, PostCreate, PostUpdate, PostDelete, ResponseCreate, ResponseList,
	ResponseDelete, ResponseAccept, subscriptions
)
from Accounts.views import SignUp, EmailConfirmedView, EmailConfirmationFailedView, CustomLoginView
from django.urls import path


urlpatterns = [
	path('', PostsList.as_view(), name='posts'),
	path('subscriptions/', subscriptions, name='subscriptions'),
	path('<int:pk>', PostDetail.as_view(), name='post_detail'),
	path('search/', SearchResults.as_view(), name='search'),
	path('accounts/logout', LogoutView.as_view, name='account_logout'),
	path('login/', CustomLoginView.as_view(), name='login'),
	path('create/', PostCreate.as_view(), name='post_create'),
	path('<int:pk>/edit', PostUpdate.as_view(), name='post_edit'),
	path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
	path('<int:pk>/response', ResponseCreate.as_view(), name='add_response'),
	path('responses', ResponseList.as_view(), name='responses'),
	path('responses/<int:pk>/delete', ResponseDelete.as_view(), name='response_delete'),
	path('responses/<int:pk>/accept', ResponseAccept.as_view(), name='response_accept'),
	path('user_register', SignUp.as_view(), name='register'),
	path('accounts/email-confirmation-sent', views.user_confirm_email_view, name='email_confirmation_sent'),
	# path('accounts/confirm-email', views.user_confirm_email_view, name='confirm_email'),
	path('accounts/email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
	path('accounts/confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
]
