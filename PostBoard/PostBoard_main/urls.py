from django.urls import path

from .views import (
	PostsList, PostDetail, SearchResults, PostCreate, PostUpdate, PostDelete,
)

urlpatterns = [
	path('', PostsList.as_view(), name='posts'),
	path('<int:pk>', PostDetail.as_view(), name='post_detail'),
	path('search/', SearchResults.as_view(), name='search'),
	path('create/', PostCreate.as_view(), name='post_create'),
	path('<int:pk>/edit', PostUpdate.as_view(), name='post_edit'),
	path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),

]
