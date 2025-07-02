from django.urls import path
from .views import (
    ProblemListView, 
    ProblemDetailView, 
    create_problem, 
    MyProblemsListView, 
    edit_problem
)

urlpatterns = [
    # List all problems
    path('', ProblemListView.as_view(), name='problem_list'),

    # Create a new problem
    path('create/', create_problem, name='problem_create'),

    # "My Problems" dashboard
    path('my/', MyProblemsListView.as_view(), name='my_problems'),

    # Edit a specific problem (in My Problems)
    path('my/edit/<slug:slug>/', edit_problem, name='problem_edit'),

    # Detail view (must come last, so it doesn't catch 'my/')
    path('<slug:slug>/', ProblemDetailView.as_view(), name='problem_detail'),
]
