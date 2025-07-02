from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Problem
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from .models import Problem, Testcase
from .forms import ProblemForm, TestcaseForm
from django.shortcuts import get_object_or_404


class ProblemListView(ListView):
    model = Problem
    template_name = 'problems/problem_list.html'
    context_object_name = 'problems'  # now matches your template
    paginate_by = 20

class ProblemDetailView(DetailView):
    model=Problem; template_name='problems/problem_detail.html'

# class ProblemCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
#     model=Problem; fields=['title','slug','statement','time_limit','memory_limit']
#     template_name='problems/problem_form.html'; success_url='/problems/'
#     def form_valid(self,form):
#         form.instance.created_by=self.request.user
#         return super().form_valid(form)
#     def test_func(self):
#         return self.request.user.is_author or self.request.user.is_superuser
@login_required
def create_problem(request):
    # create a formset of TestcaseForm tied to Problem
    TCFormSet = inlineformset_factory(
        Problem, Testcase, form=TestcaseForm,
        extra=1,     # number of blank testcases shown
        can_delete=True
    )

    if request.method == 'POST':
        p_form  = ProblemForm(request.POST)
        fset    = TCFormSet(request.POST)
        if p_form.is_valid() and fset.is_valid():
            # 1) save the problem
            problem = p_form.save(commit=False)
            problem.created_by = request.user
            problem.save()
            # 2) save its testcases
            fset.instance = problem
            fset.save()
            return redirect(problem.get_absolute_url())
    else:
        p_form = ProblemForm()
        fset   = TCFormSet()

    return render(request, 'problems/problem_form.html', {
        'form': p_form,
        'formset': fset
    })
class MyProblemsListView(LoginRequiredMixin, ListView):
    model = Problem
    template_name = 'problems/my_problems.html'
    context_object_name = 'problems'
    paginate_by = 20

    def get_queryset(self):
        return Problem.objects.filter(created_by=self.request.user).order_by('-created_at')
@login_required
def edit_problem(request, slug):
    problem = get_object_or_404(Problem, slug=slug, created_by=request.user)

    TestcaseFormSet = inlineformset_factory(
        Problem, Testcase, form=TestcaseForm, extra=0, can_delete=True
    )

    if request.method == 'POST':
        p_form = ProblemForm(request.POST, instance=problem)
        fset   = TestcaseFormSet(request.POST, instance=problem)
        if p_form.is_valid() and fset.is_valid():
            p_form.save()
            fset.save()
            return redirect('problem_detail', slug=problem.slug)
    else:
        p_form = ProblemForm(instance=problem)
        fset   = TestcaseFormSet(instance=problem)

    return render(request, 'problems/problem_form.html', {
        'form': p_form,
        'formset': fset,
    })