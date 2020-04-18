from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import Jobs
from .tables import JobsTable
from .models import Job_Results
from .tables import Job_ResultsTable
from hello.analyze_sentiment import analyze_sentiment
from django_tables2 import SingleTableView
from django.utils import timezone
import logging
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from background_task import background

logger = logging.getLogger(__name__)

# helper function
def is_not_blank(s):
    return bool(s and s.strip())

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

# account settings
def accountsettings_view(request):
	if request.user.is_authenticated:
		current_user = request.user
		if request.method == 'POST':
			# get post data load
			email = request.POST['email']
			username = request.POST['username']
			password = request.POST['password']

			# change field values if post data differs from database record
			if (current_user.email != email) & is_not_blank(email):
				current_user.email = email
				# logger.error("Email changed")
			if (current_user.username != username) & is_not_blank(username):
				current_user.username = username
				# logger.error("Username changed")
			if (current_user.password != password) & is_not_blank(password):
				current_user.password = password
				# logger.error("Password changed")

			# save user and relog
			current_user.save()
			logout(request)
			login(request, current_user)
			
			messages.info(request, "Account settings successfully updated!")
			return HttpResponseRedirect('/dashboard/')
		else:
			return render(request, "accountsettings.html", {
				"username" : current_user.username,
				"email" : current_user.email})
	else:
		messages.error(request, 'You must log in to change account settings.')
		return HttpResponseRedirect('/')

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

		queue_job(j.id)

		# output success message and redirect to dashboard
		success_message = ('Your keyword \"' + j.input_text + '\" has been sent for scraping. Please check back in 5~10 minutes to see the results.')
		messages.info(request, success_message)
		return HttpResponseRedirect('/dashboard/')

@background(schedule=60)
def queue_job(job_id):
	# retrieve job
	job = Jobs.objects.get(id__exact=job_id)

	# analyze sentiment and update completion time of job
	analyze_sentiment(job)
	job.completed_date = timezone.now()
	job.save()

# for viewing job results
def dashboard(request):
	current_user = request.user
	table = Job_ResultsTable(
		Job_Results.objects.filter(job__user__exact = current_user).order_by('-executed_date')
	)

	return render(request, "dashboard.html", {
		"table": table
	})

# for viewing jobs
def jobs(request):
	current_user = request.user
	table = JobsTable(
		Jobs.objects.filter(user__exact = current_user).order_by('-completed_date')
	)

	return render(request, "jobs.html", {
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
