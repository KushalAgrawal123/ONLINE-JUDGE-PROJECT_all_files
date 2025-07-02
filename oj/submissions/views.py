import subprocess
import tempfile
import os
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.views.generic import DetailView
from problems.models import Problem
from .models import Submission

@login_required
@login_required
def submit_solution(request, slug):
    problem = get_object_or_404(Problem, slug=slug)
    if request.method == 'POST':
        code = request.POST.get('code', '')
        language = request.POST.get('language')

        # Create submission
        sub = Submission.objects.create(
            user=request.user,
            problem=problem,
            code=code,
            language=language,
            verdict='Running'
        )

        testcases = list(problem.testcases.all())
        if not testcases:
            sub.verdict = 'Pending'
            sub.save()
            return redirect('submission_history')

        overall = 'Accepted'

        for tc in testcases:
            try:
                if language == 'python':
                    # Save to .py and run
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as f:
                        f.write(code.encode())
                        source_file = f.name
                    run_cmd = ['python', source_file]

                elif language == 'cpp':
                    # Save to .cpp
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.cpp') as f:
                        f.write(code.encode())
                        source_file = f.name
                    exec_file = source_file + '.out'

                    # Compile
                    compile_result = subprocess.run(
                        ['g++', source_file, '-o', exec_file],
                        capture_output=True
                    )
                    if compile_result.returncode != 0:
                        overall = 'Compilation Error'
                        break

                    run_cmd = [exec_file]

                else:
                    overall = 'Unsupported Language'
                    break

                # Run program with input
                result = subprocess.run(
                    run_cmd,
                    input=tc.input_data.encode(),
                    capture_output=True,
                    timeout=problem.time_limit
                )
                output = result.stdout.decode().strip()
                expected = tc.expected_output.strip()
                if expected.split() != output.split():
                    overall = 'Wrong Answer'
                    break

            except subprocess.TimeoutExpired:
                overall = 'Time Limit Exceeded'
                break
            except Exception:
                overall = 'Runtime Error'
                break
            finally:
                # Clean up
                if os.path.exists(source_file): os.remove(source_file)
                if language == 'cpp' and os.path.exists(exec_file): os.remove(exec_file)

        sub.verdict = overall
        sub.save()
        return redirect('submission_history')

    return render(request, 'submissions/submit_form.html', {'problem': problem})

class SubmissionHistoryView(ListView):
    model = Submission
    template_name = 'submissions/history.html'
    context_object_name = 'submissions'
    paginate_by = 20

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user).order_by('-submitted_at')
class SubmissionDetailView(DetailView):
    model = Submission
    template_name = 'submissions/submission_detail.html'
    context_object_name = 'submission'
    
    def get_queryset(self):
        # Limit access: only show user's own submissions
        return Submission.objects.filter(user=self.request.user)