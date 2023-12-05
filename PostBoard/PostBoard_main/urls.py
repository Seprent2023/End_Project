from django.urls import path
from . import views

from .views import (
	PostsList, PostDetail, SearchResults, PostCreate, PostUpdate, PostDelete, ResponseCreate, ResponseList,
	ResponseDelete
)
urlpatterns = [
	path('', PostsList.as_view(), name='posts'),
	path('<int:pk>', PostDetail.as_view(), name='post_detail'),
	path('search/', SearchResults.as_view(), name='search'),
	path('create/', PostCreate.as_view(), name='post_create'),
	path('<int:pk>/edit', PostUpdate.as_view(), name='post_edit'),
	path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
	# path('response/<int:pk>', views.post_response, name='add_response'),
	# re_path(r'^(?P<res_post>[0-9]+/$)', views.PostDetail.as_view, name='post'),
	# re_path(r'^response/(?P<res_post>[0-9]+/$)', views.post_response, name='add_response'),
	path('<int:pk>/response', ResponseCreate.as_view(), name='add_response'),
	path('responses', ResponseList.as_view(), name='responses'),
	path('responses/<int:pk>/delete', ResponseDelete.as_view(), name='response_delete'),
	# path('responses/<int:pk>', views.to_response_delete, name='response_delete')

]