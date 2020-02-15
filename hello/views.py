from django.shortcuts import render
from django.http import HttpResponse

from hello.models import Jobs
# from .forms import JobForm

# temporary submit job view (will be moved to dashboard later)
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")

# for submitting jobs
def submit_job(request):
	if request.method == 'POST':
		j = Jobs(input_text=request.POST.get('inputTwitterHashtag'))
		j.save()
		return HttpResponseRedirect('/dashboard/')
		# form = JobForm(request.POST)
		# if form.is_valid():
		# 	j = Jobs(input_text=form.cleaned_data['input_text'])
		# 	j.save()
		# 	return HttpResponseRedirect('/dashboard/')
		# else:
		# 	return HttpResponse('Error: Form is invalid.')

# for viewing jobs
def dashboard(request):
    j = Jobs.objects.all()
    return HttpResponse(j)

# for viewing details of each job
# def detail(request, job_id)
