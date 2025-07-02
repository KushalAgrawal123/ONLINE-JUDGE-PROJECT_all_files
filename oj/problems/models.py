from django.db import models
from django.conf import settings

class Problem(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    statement = models.TextField()
    time_limit = models.IntegerField(default=2)
    memory_limit = models.IntegerField(default=256)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('problem_detail', args=[self.slug])
class Testcase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='testcases')
    input_data      = models.TextField()
    expected_output = models.TextField()
    is_sample       = models.BooleanField(default=False)
    order           = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'Testcase {self.order} for {self.problem.slug}'