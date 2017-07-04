from __future__ import with_statement
from java.nio.file import Files
from java.nio.file import Paths
from java.lang import String
from com.restfb import *
from com.restfb.types import Message, GraphResponse, Post, FacebookType, Comment
from com.restfb.types.send import IdMessageRecipient
from com.restfb.types.send import SendResponse
from facebook.facebook_sender import SeleniumSender
from sikuliwrapper import *
import os
from facebook_config import *



class FacebookHelper(BaseLogger):
	ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

	def makeFacebookPost(self, text):
		fb_client = DefaultFacebookClient(customer_page_token, Version.LATEST)
		publishMessageResponse = fb_client.publish(page_id+"/feed", GraphResponse, Parameter.with("message", text))
		msg_id = publishMessageResponse.getId()
		return msg_id

	def makeEventPost(self, text):
		fb_client = DefaultFacebookClient(customer_page_token, Version.LATEST)
		publishMessageResponse = fb_client.publish(event_id+"/feed", GraphResponse, Parameter.with("message", text))
		msg_id = publishMessageResponse.getId()
		return msg_id

	def SendCommentOnNote(self, text, attachment=None):
		fb_client = DefaultFacebookClient(customer_page_token, Version.LATEST)
		if attachment == None:
			comment = fb_client.publish(note_id + "/comments", GraphResponse, Parameter.with("message", text))
		else:
			comment = fb_client.publish(note_id + "/comments", GraphResponse, BinaryAttachment.with(attachment, self.streamPhoto(attachment)), Parameter.with("message", text))
		comment_id = comment.getId()
		return comment_id

	def isCommentExist(self, post_id, comment_text):
		fb_client = DefaultFacebookClient(customer_page_token, Version.LATEST)
		all_comments = fb_client.fetchConnection(post_id+"/comments", Comment)
		for post_comments in all_comments:
			for comment in post_comments:
				if comment_text in comment.getMessage():
					self.log.passed("Comment by agent found")
					return True
		self.log.failed("Comment by agent not found")
		return False

	def isCommentLevel2Exist(self, comment_id, comment_text):
		fb_client = DefaultFacebookClient(customer_page_token, Version.LATEST)
		all_comments = fb_client.fetchConnection(comment_id+"/comments", Comment)
		for post_comments in all_comments:
			for comment in post_comments:
				if comment_text in comment.getMessage():
					self.log.passed("Comment by agent found")
					return True
				else:
					self.log.info(comment.getMessage())
		self.log.failed("Comment by agent not found")
		return False

	def getAdminCommentId(self, post_id, comment_text):
		fb_client = DefaultFacebookClient(customer_page_token, Version.LATEST)
		all_comments = fb_client.fetchConnection(post_id + "/comments?filter=stream", Comment)
		for post_comments in all_comments:
			for comment in post_comments:
				if comment_text in comment.getMessage():
					self.log.passed("Comment by admin found")
					return comment.getId()
		self.log.failed("Comment by admin not found")

	def getPostLikesCount(self, post_id):
		fb_client = DefaultFacebookClient(customer_page_token, Version.LATEST)
		post_likes_data = fb_client.fetchConnection(post_id+"/likes", Post.Likes,
			Parameter.with("summary", 1), Parameter.with("limit", 0))
		likes_count = post_likes_data.getTotalCount()
		return likes_count

	def isPostExistOnPage(self, post_text, page):
		fb_client = DefaultFacebookClient(customer_page_token, Version.LATEST)
		page_feed = fb_client.fetchConnection(page+"/feed", Post)
		for posts in page_feed:
			for post in posts:
				if post.getMessage() == post_text:
					return True
		return False

	def getAgentPostId(self, post_text, page):
		fb_client = DefaultFacebookClient(customer_page_token, Version.LATEST)
		page_feed = fb_client.fetchConnection(page+"/posts", Post)
		for posts in page_feed:
			for post in posts:
				if post.getMessage() == post_text:
					self.log.passed("Post by admin found")
					return post.getId()
		self.log.failed("Post by admin not found while retreiving Post ID")

	def SendCommentOnOldPostByAdmin(self, comment_text, attachment=None):
		fb_client = DefaultFacebookClient(customer_page_token, Version.LATEST)
		if attachment == None:
			comment = fb_client.publish(oldPostByAdmin+"/comments",GraphResponse, Parameter.with("message", comment_text))
		else:
			comment = fb_client.publish(oldPostByAdmin + "/comments", GraphResponse, BinaryAttachment.with(attachment, self.streamPhoto(attachment)), Parameter.with("message", comment_text))
		comment_id = comment.getId()
		return comment_id

	def SendCommentOnOldPostByCustomer(self, comment_text, attachment=None):
		fb_client = DefaultFacebookClient(customer_page_token, Version.LATEST)
		if attachment == None:
			comment = fb_client.publish(oldPostByCustomer+"/comments",GraphResponse, Parameter.with("message", comment_text))
		else:
			comment = fb_client.publish(oldPostByCustomer + "/comments", GraphResponse, BinaryAttachment.with(attachment, self.streamPhoto(attachment)), Parameter.with("message", comment_text))
		comment_id = comment.getId()
		return comment_id

	def commentPostAsCustomer(self, post, comment_text, attachment=None):
		fb_client = DefaultFacebookClient(customer_page_token, Version.LATEST)
		comment = fb_client.publish(post+"/comments",GraphResponse, Parameter.with("message", comment_text))
		return comment.getId()

	def postLevel2CommentAsCustomer(self, post, comment1, comment_text, attachment=None):
		fb_client = DefaultFacebookClient(customer_page_token, Version.LATEST)
		all_comments = fb_client.fetchConnection(post + "/comments", Comment)
		for post_comments in all_comments:
			for comment in post_comments:
				if comment1 in comment.getMessage():
					comment = fb_client.publish(comment.getId() + "/comments", GraphResponse, Parameter.with("message", comment_text))
					return comment.getId()
				else:
					self.log.failed("Comment by agent not found while replying.")

	def streamPhoto(self, photo):
		full_path = os.getcwd() + "\images\\" + photo
		path = Paths.get(full_path)
		stream = Files.readAllBytes(path)
		return stream

	def publishPhotoAsCustomer(self, page, text, photo):
		response_id = 0
		fb_client = DefaultFacebookClient(customer_page_token, Version.LATEST)
		full_path = os.getcwd() + "\images\\" + photo
		path = Paths.get(full_path)
		stream = Files.readAllBytes(path)
		response = fb_client.publish(page+"/photos", FacebookType, BinaryAttachment.with(photo, stream), Parameter.with("message", text))
		response_id = response.getId()
		return response_id

	def sendPrivateMessageToPage(self, page, message):
		customer = SeleniumSender(customer_fb_login, customer_fb_password, 'firefox')
		customer.send_private_message(page, message)
		customer.teardown()

	def sendImagePrivateMessage(self, page, img_name):
		customer = SeleniumSender(customer_fb_login, customer_fb_password, 'firefox')
		customer.attach_image_private_message(page, img_name)
		customer.teardown()













