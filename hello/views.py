from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import Jobs
from .models import Job_Results
from .tables import Job_ResultsTable
from hello.analyze_sentiment import analyze_sentiment
from django_tables2 import SingleTableView
from django.utils import timezone
import logging
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


# home page
def index(request):
	return render(request, "index.html")

# log-in
def login_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect('/dashboard/')
		else:
			messages.error(request, 'Invalid login credentials. Please try again.')
			return HttpResponseRedirect('/login/')
	else:
		if request.user.is_authenticated:
			messages.error(request, 'You are already logged in.')
			return HttpResponseRedirect('/dashboard/')
		else:
			return render(request, "login.html")

# register
def register_view(request):
	if request.method == 'POST':
		email = request.POST['email']
		username = request.POST['username']
		password = request.POST['password']
		user = User.objects.create_user(username, email, password)
		user.save()
		login(request, user)
		messages.info(request, "User successfully created!")
		return HttpResponseRedirect('/dashboard/')
	else:
		if request.user.is_authenticated:
			messages.error(request, 'You must log out to register a new account.')
			return HttpResponseRedirect('/dashboard/')
		else:
			return render(request, "register.html")

# for submitting jobs
def submit_job(request):
	# verify if user is signed in
	if request.user.is_authenticated == False:
		# redirect to log-in page
		messages.error(request, 'You must be signed in to submit a job.')
		return HttpResponseRedirect('/login/')

	# verify a POST request has been recieved
	if request.method == 'POST':
		# get hashtag and create job record
		hashtag = request.POST.get('inputTwitterHashtag')
		notes = request.POST.get('notesText')
		j = Jobs(input_text=hashtag,
				 user=request.user,
				 notes=notes,
				 created_date=timezone.now())
		j.save()

		# analyze sentiment and update completion time of job
		analyze_sentiment(j)
		j.completed_date = timezone.now()
		j.save()

		# output success message and redirect to dashboard
		success_message = ('Your keyword \"' + j.input_text + '\" has been sent for scraping. Please check back in 5~10 minutes to see the results.')
		messages.info(request, success_message)
		return HttpResponseRedirect('/dashboard/')

# for viewing jobs
# class dashboard(SingleTableView):
# 	# queryset = Job_Results.objects.all()
# 	model = Job_Results
# 	table_class = Job_ResultsTable
# 	template_name = "dashboard.html"
def dashboard(request):
	current_user = request.user
	table = Job_ResultsTable(
		Job_Results.objects.filter(job__user__exact = current_user).order_by('-executed_date')
	)

	return render(request, "dashboard.html", {
		"table": table
	})

# for viewing details of each job
def detail(request, job_id):

	# fetch job_result
	try:
		j_res = Job_Results.objects.get(id=job_id)
	except Job_Results.DoesNotExist:
		raise Http404("Job result does not exist.")

	# fetch corresponding job
	try:
		j = Jobs.objects.get(id=j_res.job.id)
	except Jobs.DoesNotExist:
		raise Http404("Corresponding job does not exist.")

	# verify user has correct permissions to view job
	if request.user != j.user:
		# redirect to log-in page
		messages.error(request, 'You do not have the correct permissions to view this job.')
		return HttpResponseRedirect('/dashboard/')

	return render(request, "detail.html", {
		'job_result': j_res,
		'job': j
	})

from django.contrib.auth import logout

def logout_view(request):
	logout(request)
	# Redirect to a success page.
	messages.info(request, 'You have successfully logged out.')
	return HttpResponseRedirect('/')
