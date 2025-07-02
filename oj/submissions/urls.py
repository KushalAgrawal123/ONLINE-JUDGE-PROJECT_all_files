from django.urls import path
from .views import submit_solution, SubmissionHistoryView
from .views import SubmissionDetailView

urlpatterns=[
    path('submit/<slug:slug>/',submit_solution,name='submit'),
    path('history/',SubmissionHistoryView.as_view(),name='submission_history'),
     path('<int:pk>/', SubmissionDetailView.as_view(), name='submission_detail'),
]