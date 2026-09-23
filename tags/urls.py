from django.urls import path
from . import views

urlpatterns = [
    path('', views.RedTagCreateView.as_view(), name='redtag-create'),
    path('tags/', views.VehicleListView.as_view(), name='redtag-list'),
    path('tags/units/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle-detail'),
    path('tags/export/', views.export_redtags, name='redtag-export'),
    path('tags/<int:pk>/', views.RedTagDetailView.as_view(), name='redtag-detail'),
    path('tags/<int:pk>/edit/', views.RedTagUpdateView.as_view(), name='redtag-update'),
    path('tags/<int:pk>/close/', views.close_redtag, name='redtag-close'),
    path('audit/', views.AuditLogListView.as_view(), name='audit-list'),
    path('audit/<int:pk>/', views.AuditLogDetailView.as_view(), name='audit-detail'),
    path('ajax/load-stations/', views.load_stations, name='ajax-load-stations'),
    path('ajax/load-issue-types/', views.load_issue_types, name='ajax-load-issue-types'),
    path('bootstrap/', views.bootstrap, name='bootstrap'),
]
