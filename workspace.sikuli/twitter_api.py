from __future__ import with_statement
from java.awt import Toolkit, Dimension
from java.io import File
from twitter4j import *
from sikuliwrapper import *
import os
import time
from twitter_config import *


class TwitterApi(BaseLogger):
	ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

	@staticmethod
	def create_twitter_api():
		customer_builder = conf.ConfigurationBuilder()
		customer_builder.setOAuthConsumerKey(consumer_key);
		customer_builder.setOAuthConsumerSecret(consumer_secret);
		customer_configuration = customer_builder.build();
		customer_factory = TwitterFactory(customer_configuration);
		customer_twitter = customer_factory.getInstance()
		customer_accessToken = auth.AccessToken(access_token, access_token_secret)
		customer_twitter.setOAuthAccessToken(customer_accessToken)
		return customer_twitter

	@staticmethod
	def agent_create_twitter_api():
		agent_builder = conf.ConfigurationBuilder()
		agent_builder.setOAuthConsumerKey(agent_consumer_key);
		agent_builder.setOAuthConsumerSecret(agent_consumer_secret);
		agent_configuration = agent_builder.build();
		agent_factory = TwitterFactory(agent_configuration);
		agent_twitter = agent_factory.getInstance()
		agent_accessToken = auth.AccessToken(agent_access_token, agent_access_token_secret)
		agent_twitter.setOAuthAccessToken(agent_accessToken)
		return agent_twitter

	def set_twitter_accounts(self):
		global customer_api
		customer_api = self.create_twitter_api()
		global agent_api
		agent_api = self.agent_create_twitter_api()


	def customer_post_tweet(self, keyword):
		global subject
		subject = keyword
		global status_update
		status_update = customer_api.updateStatus(subject)
		print "Customer tweet: " + subject

	def customer_reply_to_last_status(self, keyword):
		reply_tweet = StatusUpdate(keyword)
		reply_tweet.setInReplyToStatusId(status_update.getId())
		global reply
		reply = customer_api.updateStatus(reply_tweet)
		print "Customer reply: " + keyword

	def customer_retweet_last_status(self, keyword):
		retweet_status = keyword + " https://twitter.com/" + tw_agent_screen_name +"/status/" + str(status_update.getId())
		customer_api.updateStatus(retweet_status)
		print "Customer reply: " + retweet_status

	def customer_post_tweet_with_image(self, keyword, image):
		global subject
		subject = keyword
		global update
		global status_update_image
		image_file = File(os.getcwd() + "\images\\" + image)
		update = StatusUpdate(keyword)
		update.setMedia(image_file)
		status_update_image = customer_api.updateStatus(update)
		print "Customer tweet: " + subject

	def customer_reply_to_last_status_with_image(self, keyword, image):
		image_file = File(os.getcwd() + "\images\\" + image)
		reply_tweet = StatusUpdate(keyword)
		reply_tweet.setMedia(image_file)
		reply_tweet.setInReplyToStatusId(status_update_image.getId())
		global reply
		reply =	customer_api.updateStatus(reply_tweet)
		print "Customer reply: " + keyword

	def customer_retweet_last_status_with_image(self, keyword, image):
		image_file = File(os.getcwd() + "\images\\" + image)
		retweet_status = keyword + " https://twitter.com/" + tw_agent_screen_name +"/status/" + str(status_update_image.getId())
		update = StatusUpdate(retweet_status)
		update.setMedia(image_file)
		customer_api.updateStatus(update)
		print "Customer retweet: " + update.getStatus()

	def verify_last_status_agent(self, posted_status):
		time.sleep(25)
		page = Paging(1, 1)
		last_status = agent_api.getUserTimeline(page)
		status_text = last_status[0].getText()
		status_id = last_status[0].getId()
		if posted_status in status_text:
			self.log.passed("Last status update by agent found")
		else:
			self.log.failed("Last status update by agent not found. Instead found : " + status_text + ". // And expected : " + posted_status)

	def verify_last_reply_agent(self, posted_status, option):
		time.sleep(5)
		page = Paging(1, 1)
		last_reply = agent_api.getUserTimeline(page)
		reply_text = last_reply[0].getText()
		reply_id = last_reply[0].getInReplyToStatusId()
		if option == "with image":
			if (posted_status in reply_text) & (status_update_image.getId() == reply_id):
				self.log.passed("Last status update by agent found")
			else:
				self.log.failed("Last status update by agent not found. Instead found : " + reply_text + ". // And expected : " + posted_status + ". Status ID : "+ str(status_update_image.getId()) + " and Reply ID : " + str(reply_id))
		else:
			if (posted_status in reply_text) & (status_update.getId() == reply_id):
				self.log.passed("Last status update by agent found")
			else:
				self.log.failed("Last status update by agent not found. Instead found : " + reply_text + ". // And expected : " + posted_status + ". Status ID : "+ str(status_update.getId()) + " and Reply ID : " + str(reply_id))

	def verify_last_favorite_agent(self, posted_status):
		time.sleep(5)
		page = Paging(1, 1)
		last_favorite = agent_api.getFavorites(page)
		status_text = last_favorite[0].getText()
		if posted_status in status_text:
			self.log.passed("Last favorite tweet of agent found")
		else:
			self.log.failed("Last favorite tweet of agent not found. Instead found : "+status_text+". // And expected : "+posted_status)

	def verify_last_DM_customer(self, posted_dm):
		time.sleep(5)
		page = Paging(1, 1)
		last_status = customer_api.getDirectMessages(page)
		dm_text = last_status[0].getText()
		if posted_dm in dm_text:
			self.log.passed("Last DM by agent found")
		else:
			self.log.failed("Last DM by agent not found. Instead found : "+dm_text+". // And expected : "+posted_dm)

	def customer_send_DM(self, keyword):
		global subject
		subject = keyword
		global sent_dm
		sent_dm = customer_api.sendDirectMessage(tw_agent_screen_name, subject)
		print "Sent DM: " + sent_dm.getText()