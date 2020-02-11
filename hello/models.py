from django.db import models

# This file serves as a blueprint for the tables in the database.
# Docs: https://docs.djangoproject.com/en/3.0/topics/db/models/

class Users(models.Model):
	user_id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=20)
	password = models.CharField(max_length=50)
	email = models.CharField(max_length=30)
	created_date = models.DateTimeField("date created", auto_now_add=True)

class Jobs(models.Model):
	job_id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey('Users', on_delete=models.CASCADE)
	input_text = models.CharField(max_length=50)
	created_date = models.DateTimeField("date created", auto_now_add=True)
	completed_date = models.DateTimeField("date completed", auto_now_add=False)

class Job_Results(models.Model):
	result_id = models.AutoField(primary_key=True)
	job_id = models.ForeignKey('Jobs', on_delete=models.CASCADE)
	sentiment_score = models.FloatField()
	executed_date = models.DateTimeField("date executed", auto_now_add=False)
