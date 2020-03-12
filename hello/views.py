from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import Jobs
from .models import Job_Results
from .tables import JobsTable
from hello.analyze_sentiment import analyze_sentiment
from django_tables2 import SingleTableView
import datetime
import logging

logger = logging.getLogger(__name__)


# temporary submit job view (will be moved to dashboard later)
def index(request):
	return render(request, "index.html")

# for submitting jobs
def submit_job(request):
	if request.method == 'POST':
		# HttpResponseRedirect('/dashboard/')
		hashtag = request.POST.get('inputTwitterHashtag')
		j = Jobs(input_text=hashtag, created_date=datetime.datetime.now())
		j.save()
		score = analyze_sentiment(j)
		j.completed_date = datetime.datetime.now()
		j.save()
		success_message = ('The Twitter sentiment score of \"' + j.input_text + \
			'\" as of ' + str(j.created_date) + ' is ' + str(score))
		logger.error("score : " + str(score))
		logger.error("success_message : " + success_message)
		messages.info(request, success_message)
		return HttpResponseRedirect('/dashboard/')

# for viewing jobs
class dashboard(SingleTableView):
    table_class = JobsTable
    queryset = Jobs.objects.all()
    template_name = "dashboard.html"

# for viewing details of each job
# def detail(request, job_id)
# 	return render(request, "detail.html", {
# 		j: Job_Results(id=job_id)
# 	})
