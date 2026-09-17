from django.urls import path
from . import views

urlpatterns = [
    path('', views.RedTagCreateView.as_view(), name='redtag-create'),
    path('tags/', views.RedTagListView.as_view(), name='redtag-list'),
    path('tags/export/', views.export_redtags, name='redtag-export'),
    path('tags/<int:pk>/', views.RedTagDetailView.as_view(), name='redtag-detail'),
    path('tags/<int:pk>/edit/', views.RedTagUpdateView.as_view(), name='redtag-update'),
    path('tags/<int:pk>/close/', views.close_redtag, name='redtag-close'),
    path('ajax/load-stations/', views.load_stations, name='ajax-load-stations'),
    path('ajax/load-issue-types/', views.load_issue_types, name='ajax-load-issue-types'),
]
