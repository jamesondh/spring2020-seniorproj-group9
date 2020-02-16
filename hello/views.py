from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from hello.models import Jobs, Job_Results
from hello.analyze_sentiment import analyze_sentiment

# temporary submit job view (will be moved to dashboard later)
def index(request):
    return render(request, "index.html")

# for submitting jobs
def submit_job(request):
	if request.method == 'POST':
		hashtag = request.POST.get('inputTwitterHashtag')
		print(hashtag)
		j = Jobs(input_text=hashtag)
		j.save()
		analyze_sentiment(j)
		return HttpResponseRedirect('/dashboard/')

# for viewing jobs
def dashboard(request):
    j = Job_Results.objects.all()
    return HttpResponse(j)

# for viewing details of each job
# def detail(request, job_id)
