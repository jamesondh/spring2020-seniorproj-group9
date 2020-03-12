from django.db import models

# This file serves as a blueprint for the tables in the database.
# Docs: https://docs.djangoproject.com/en/3.0/topics/db/models/

class Users(models.Model):
	username = models.CharField(max_length=20)
	password = models.CharField(max_length=50)
	email = models.CharField(max_length=30)
	created_date = models.DateTimeField("date created", auto_now_add=True)
	def __str__(self):
		return self.username

class Jobs(models.Model):
	# user_id = models.ForeignKey('Users', on_delete=models.CASCADE)
	input_text = models.CharField(max_length=50)
	created_date = models.DateTimeField("date created", auto_now_add=True)
	completed_date = models.DateTimeField("date completed", auto_now_add=False, null=True, blank=True)
	def __str__(self):
		return self.input_text

class Job_Results(models.Model):
	job_id = models.ForeignKey('Jobs', on_delete=models.CASCADE)
	sentiment_score = models.FloatField()
	executed_date = models.DateTimeField("date executed", auto_now_add=False, null=True, blank=True)
	def __str__(self):
		return str(self.sentiment_score)
