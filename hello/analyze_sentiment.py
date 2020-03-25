import GetOldTweets3 as got
import os
from afinn import Afinn
from hello.models import Job_Results
from hello.models import Jobs
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def analyze_sentiment(job):

	correspondingJob = Jobs.objects.get(id = job.id)

	# variables
	records = 5
	afinn = Afinn()

	#load data as objects
	tweetCriteria = got.manager.TweetCriteria() \
					.setQuerySearch(job.input_text) \
					.setSince("2020-01-01") \
					.setUntil("2020-09-30") \
					.setMaxTweets(records)
	index = []
	results =[]
	tweet_text = []

	#data to dataframe
	# loop through the records and create a list of keyword tweets
	for i in range(records):
		tweet = got.manager.TweetManager.getTweets(tweetCriteria)[i]
		#get the tweet text
		txt = tweet.text
		#score the sentiment analyisis
		score = int(afinn.score(txt)) 
		#post resuts to list
		results.append(score)
		#post the tweet text to List
		tweet_text.append(txt)

	final_score = sum(results) / len(results)
	completed = datetime.now

	logger.error("input_text : " + correspondingJob.input_text)
	logger.error("final_score : " + str(final_score))
	logger.error("executed_date : " + str(datetime.now()))

	r = Job_Results(job_id=correspondingJob, sentiment_score=final_score, executed_date=datetime.now())
	r.save()

	return final_score

	#create a dictionary of the results
	# dct = {'results': results, 'tweet_text':tweet_text}  
	# #Send result to dataframe
	# df = pd.DataFrame(dct)
	# #create a csv of the results to local drive
	# df.to_csv('results.csv')
	# print(df)
