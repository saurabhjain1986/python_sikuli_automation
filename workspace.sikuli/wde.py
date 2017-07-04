# -*- coding: utf-8 -*-
from __future__ import with_statement
from java.awt import Toolkit, Dimension
from twitter4j import *
from sikuliwrapper import *
import os

# add custom image library
addImagePath(common.cfgImageLibrary)

s = Screen()


class WDE(BaseLogger):
	ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

	def __init__(self):
		screen_size = Toolkit.getDefaultToolkit().getScreenSize()
		self.width = screen_size.getWidth()
		self.height = screen_size.getHeight()
		self.appCoordinates = (0, 0, self.width, self.height)

	# def startApp(self):
	# 	wdeApp = App("Workspace - Log In")
	# 	if not wdeApp.window():
	# 		App.open("run_wde.bat")
	# 		s.wait(45)
	# 	wdeApp.focus()
	# 	self.verifyElement("WDE.StartScreen.buttons.png", 60)
	# 	self.verifyApp()

	def startApp(self):
		# wdeApp = App("Workspace - Log In")
		App.open("run_wde.bat")
		# self.verifyElement("WDE.StartScreen.buttons.png", 90)

		if exists(Pattern("WDE.StartScreen.buttons.png").similar(0.95), 90):
			self.log.passed("WDE Window Appeared.")
		else:
			self.log.failed("WDE Window did not appear.")

	# def verifyApp(self):
	# 	# check application
	# 	if exists("WDE.StartScreen.buttons.png"):
	# 		self.log.passed("WDE window appeared")
	# 	else:
	# 		self.log.screenshot()
	# 		self.log.failed("No wde login window")

	def verifyElement(self, filename, timeout=60):
		screen_size = Toolkit.getDefaultToolkit().getScreenSize()
		self.width = screen_size.getWidth()
		self.height = screen_size.getHeight()
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		if exists(filename, timeout):
			return True
			self.log.passed("Element Appeared.")
		else:
			error_msg = "Element is not visible after {seconds} seconds : {element}".format(seconds=timeout,
																							element=filename)
			return False
			# self.log.screenshot()
			self.log.failed(error_msg)

	def doLogin(self):
		if exists("recent_place_unchecked.png"):
			self.log.passed("Use recent workspace checkbox is unchecked")
			s.find("recent_place_unchecked.png").click()
		self.verifyElement("WDE.StartScreen.buttons.png", 60)
		s.find("WDE.StartScreen.buttons.png")
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		self.verifyElement("WDE.StartScreen.login.png", 10)
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.StartScreen.login.png")

	def setAgentStatusReady(self):
		self.verifyElement("WDE.MainWindow.agentStatusButton.png", 60)
		s.find("WDE.MainWindow.agentStatusButton.png")
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		# self.verifyElement("WDE.MainWindow.agentStatusButton.png")
		appRegion.click("WDE.MainWindow.agentStatusButton.png")
		self.verifyElement("WDE.MainWindow.agentStatusMenu.png", 10)
		s.find("WDE.MainWindow.agentStatusMenu.png")
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		self.verifyElement("WDE.MainWindow.agentStatusReady.png", 15)
		appRegion.click("WDE.MainWindow.agentStatusReadyHover.png", "WDE.MainWindow.agentStatusReady.png")

	def openMainMenu(self):
		self.verifyElement("WDE.MainWindow.mainMenuButton.png", 30)
		s.find("WDE.MainWindow.mainMenuButton.png")
		# self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		# self.verifyElement("WDE.MainWindow.mainMenuButton.png")
		appRegion.click("WDE.MainWindow.mainMenuButton.png")

	def openPostUpdateDropdown(self):
		self.verifyElement("WDE.MainWindow.mainMenu.png", 30)
		s.find("WDE.MainWindow.mainMenu.png")
		self.verifyElement("WDE.MainWindow.mainMenu.postUpdateDropdown.png", 25)
		appRegion = Region(*self.appCoordinates)
		# self.verifyElement("WDE.MainWindow.mainMenu.postUpdateDropdown.png")
		appRegion.hover("WDE.MainWindow.mainMenu.postUpdateDropdown.png")

	def openTwitterOutboundInteraction(self):
		s.find("PostUpdateOptions.png")
		appRegion = Region(*self.appCoordinates)
		self.verifyElement("PostUpdateOptions.Twitter.png")
		appRegion.click("PostUpdateOptions.Twitter.Hover.png", "PostUpdateOptions.Twitter.png")
		s.wait("WDE.Interactions.Outbound.Twitter.png", 25)

	def typeTweet(self, tweet_text):
		s.wait(5)
		reply_window = Pattern("ReplyWindow.png").similar(0.98)
		self.verifyElement(reply_window, 30)
		text_field = s.find(reply_window).above(200)
		text_field.click()
		text_field.type(tweet_text)
		s.wait(2)

	def typePost(self, text):
		self.verifyElement("ReplyWindow.SendButtonActive.png", 15)
		text_field = s.find("ReplyWindow.SendButtonActive.png").above(300)
		text_field.click()
		text_field.type(text)

	def sendPost(self):
		self.scrollReplyWindowVertical()
		self.scrollReplyWindowHorizontol()
		if exists(Pattern("ReplyWindow.SendButtonActive.png").similar(0.97), 2):
			send_button = Pattern("ReplyWindow.SendButtonActive.png").similar(0.97)
		elif exists(Pattern("ReplyWindow.DirectMessage.SendButtonActive.png").similar(0.97), 2):
			send_button = Pattern("ReplyWindow.DirectMessage.SendButtonActive.png").similar(0.97)
		else:
			self.log.failed("Send button not found.")
		self.verifyElement(send_button, 15)
		s.find(send_button)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click(send_button)
		s.waitVanish("ReplyWindow.png", 25)

	def sendPostMyHistory(self):
		self.scrollReplyWindowMyHistoryVerticalFacebook()
		if exists(Pattern("ReplyWindow.SendButtonActive.png").similar(0.97), 5):
			send_button = Pattern("ReplyWindow.SendButtonActive.png").similar(0.97)
		elif exists(Pattern("ReplyWindow.DirectMessage.SendButtonActive.png").similar(0.90), 5):
			send_button = Pattern("ReplyWindow.DirectMessage.SendButtonActive.png").similar(0.90)
		elif exists(Pattern("MyHistory.SendReplyButton.png").similar(0.90), 5):
			send_button = Pattern("MyHistory.SendReplyButton.png").similar(0.90)
		else:
			self.log.failed("Send button not found.")
		self.verifyElement(send_button, 15)
		s.find(send_button)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click(send_button)
		s.waitVanish("ReplyWindow.png", 25)

	def openFacebookOutboundInteraction(self):
		s.find("PostUpdateOptions.png")
		appRegion = Region(*self.appCoordinates)
		self.verifyElement("PostUpdateOptions.Facebook.png")
		appRegion.click("PostUpdateOptions.FacebookHover.png", "PostUpdateOptions.Facebook.png")
		s.wait("WDE.Interactions.Outbound.Facebook.Actions.png", 25)

	def selectFacebookAccount(self, account):
		try:
			if exists("WDE.Interactions.SelectAccountButton.png"):
				s.waitVanish("WDE.Interactions.SelectAccountButton.png", 25)
		except FindFailed as e:
			self.log.screenshot()
			raise e

		appRegion = Region(*self.appCoordinates)
		alt_btn = "Facebook.SelectAccount.Alternative.png"
		btn = "Facebook.SelectAccount.png"
		if exists(btn):
			appRegion.click(btn)
		else:
			appRegion.click(alt_btn)

		self.verifyElement("Facebook.AccountsDropdown.png")
		accounts = {'application page': "Facebook.AccountsDropdown.ApplicationPage.png",
					'event page': "Facebook.AccountsDropdown.EventPage.png"}
		accounts_hover = {'application page': "Facebook.AccountsDropdown.ApplicationPageHover.png",
					'event page': "Facebook.AccountsDropdown.EventPageHover.png"}

		try:
			self.verifyElement(accounts[account])
			appRegion.click(accounts_hover[account], accounts[account])
			self.verifyElement("WDE.Interactions.AgentDetails.png")
		except KeyError as e:
			raise e

	def openUploadDialog(self):
		self.verifyElement("AddPicture.png", 30)
		s.find("AddPicture.png")
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		# self.verifyElement("AddPicture.png")
		appRegion.click("AddPictureHover.png", "AddPicture.png")

	def enterFileName(self, filename):
		self.verifyElement("UploadDialog.AddressField.png", 25)
		# self.verifyElement("UploadDialog.AddressField.png")
		file_path_field = s.find("UploadDialog.AddressField.png").right(100)
		file_path_field.click()
		full_path = os.getcwd() + "\images\\" + filename
		file_path_field.type(full_path)
		file_path_field.type(Key.ENTER)

	def attachImage(self, filename):
		self.openUploadDialog()
		self.enterFileName(filename)

	def changeAgentStatusToReady(self):
		try:
			if exists("WDE.MainWindow.StatusMenuButton.png"):
				s.find("WDE.MainWindow.StatusMenuButton.png").click()
				self.verifyElement("WDE.MainWindow.StatusMenu.png")
				s.find("WDE.MainWindow.StatusMenu.Ready.png").click()
				self.verifyElement("WDE.MainWindow.StatusMenuButton.Ready.png")

		except Exception as e:
			raise e

	def acceptPendingInteractions(self):
		moreInteractions = 1
		while (moreInteractions != 0):
			if exists(Pattern("WDE.IncomingInteractionReject.png").similar(0.90), 90):
				self.log.passed("Incoming Interaction Appeared.")
				if exists("WDE.IncomingInteractionOptions.png"):
					s.find("WDE.IncomingInteractionOptions.png")
					self.appCoordinates = (0, 0, int(self.width), int(self.height))
					appRegion = Region(*self.appCoordinates)
					self.verifyElement("WDE.IncomingInteractionAccept.png", 10)
					appRegion.click("WDE.IncomingInteractionAccept.png")
					s.wait(5)
					self.markInteractionDone()
				else:
					s.find("WDE.IncomingInteractionOptions2.png")
					self.appCoordinates = (0, 0, int(self.width), int(self.height))
					appRegion = Region(*self.appCoordinates)
					self.verifyElement("WDE.IncomingInteractionAccept2.png", 10)
					appRegion.click("WDE.IncomingInteractionAccept2hover.png", "WDE.IncomingInteractionAccept2.png")
					s.wait(5)
					self.markInteractionDone()
			else:
				moreInteractions = 0

	def acceptInteraction(self):
		self.acceptIncomingInteraction()

	def verifyNoInteractionReceived(self, fail_msg="Incoming Interaction Appeared."):
		if exists(Pattern("WDE.IncomingInteractionReject.png").similar(0.90), 180):
			if exists("WDE.IncomingInteractionOptions.png"):
				s.find("WDE.IncomingInteractionOptions.png")
				self.appCoordinates = (0, 0, int(self.width), int(self.height))
				appRegion = Region(*self.appCoordinates)
				self.verifyElement("WDE.IncomingInteractionAccept.png", 10)
				appRegion.click("WDE.IncomingInteractionAccept.png")
			else:
				s.find("WDE.IncomingInteractionOptions2.png")
				self.appCoordinates = (0, 0, int(self.width), int(self.height))
				appRegion = Region(*self.appCoordinates)
				self.verifyElement("WDE.IncomingInteractionAccept2.png", 10)
				appRegion.click("WDE.IncomingInteractionAccept2hover.png", "WDE.IncomingInteractionAccept2.png")
			self.markInteractionDone()
			s.wait(3)
			self.log.failed(fail_msg)

	def acceptIncomingInteraction(self):
		if exists(Pattern("WDE.IncomingInteractionReject.png").similar(0.90), 600):
			self.log.passed("Incoming Interaction Appeared.")
		else:
			self.log.failed("Incoming Interaction did not appear in 10 minutes.")
		if exists("WDE.IncomingInteractionOptions.png"):
			s.find("WDE.IncomingInteractionOptions.png")
			self.appCoordinates = (0, 0, int(self.width), int(self.height))
			appRegion = Region(*self.appCoordinates)
			self.verifyElement("WDE.IncomingInteractionAccept.png", 2)
			appRegion.click("WDE.IncomingInteractionAccept.png")
		else:
			s.find("WDE.IncomingInteractionOptions2.png")
			self.appCoordinates = (0, 0, int(self.width), int(self.height))
			appRegion = Region(*self.appCoordinates)
			self.verifyElement("WDE.IncomingInteractionAccept2.png", 2)
			appRegion.click("WDE.IncomingInteractionAccept2hover.png", "WDE.IncomingInteractionAccept2.png")

	def acceptIncomingInteractionFromEvent(self):
		if exists(Pattern("WDE.IncomingInteractionReject.png").similar(0.90), 600):
			self.log.passed("Incoming Interaction Appeared.")
		else:
			self.log.failed("Incoming Interaction did not appear in 3 minutes.")
		if exists("WDE.IncomingInteractionOptions.png"):
			s.find("WDE.IncomingInteractionOptions.png")
			self.appCoordinates = (0, 0, int(self.width), int(self.height))
			appRegion = Region(*self.appCoordinates)
			self.verifyElement("WDE.IncomingInteractionAccept.png", 10)
			appRegion.click("WDE.IncomingInteractionAccept.png")
		else:
			s.find("WDE.IncomingInteractionOptions2.png")
			self.appCoordinates = (0, 0, int(self.width), int(self.height))
			appRegion = Region(*self.appCoordinates)
			self.verifyElement("WDE.IncomingInteractionAccept2.png", 10)
			appRegion.click("WDE.IncomingInteractionAccept2hover.png", "WDE.IncomingInteractionAccept2.png")

	def clickCommentButton(self):
		self.verifyElement("WDE.Interactions.Inbound.Facebook.Actions.Comment.png")
		s.find("WDE.Interactions.Inbound.Facebook.Actions.Comment.png")
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.Interactions.Inbound.Facebook.Actions.CommentHover.png", "WDE.Interactions.Inbound.Facebook.Actions.Comment.png")
		self.scrollReplyWindowVertical()
		self.scrollReplyWindowHorizontol()
		self.verifyElement("WDE.Interactions.Inbound.Facebook.CommentArea.png")

	def clickLastCommentButton(self):
		self.scrollReplyWindowVertical()
		self.scrollReplyWindowHorizontol()
		self.verifyElement("WDE.Interactions.Inbound.Facebook.Actions.Comment.png")
		comment_buttons = s.findAll("WDE.Interactions.Inbound.Facebook.Actions.Comment.png")
		sorted_comment_buttons = sorted(comment_buttons, key=lambda m: m.y)
		comment_buttons_count = len(sorted_comment_buttons)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.Interactions.Inbound.Facebook.Actions.CommentHover.png", sorted_comment_buttons[comment_buttons_count-1])
		self.scrollReplyWindowVertical()
		self.scrollReplyWindowHorizontol()
		self.verifyElement("WDE.Interactions.Inbound.Facebook.CommentArea.png")

	def enterCommentText(self, comment):
		self.verifyElement("WDE.Interactions.Inbound.Facebook.CommentArea.png")
		s.find("WDE.Interactions.Inbound.Facebook.CommentArea.png").click()
		s.find("WDE.Interactions.Inbound.Facebook.CommentArea.png").type(comment)

	def enterPrivateMessageText(self, text):
		s.wait(5)
		self.verifyElement("Facebook.PrivateMessage.ReplyWindowArea.png", 15)
		s.find("Facebook.PrivateMessage.ReplyWindowArea.png")
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		self.verifyElement("Facebook.PrivateMessage.ReplyWindow.png", 15)
		appRegion.click("Facebook.PrivateMessage.ReplyWindow.png")
		appRegion.type(text)

	def waitForInboundInteraction(self):
		self.verifyElement(Pattern("WDE.IncomingInteractionReject.png").similar(0.90), 180)

	# To check that interaction is not empty
	def verifyTwitterInteractionText(self):
		self.verifyElement("Twitter.TextValidator.png", 30)
		s.find("Twitter.TextValidator.png")
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		if exists("Twitter.TextValidator.png"):
			self.log.passed("Twitter interaction text appeared")
		else:
			self.log.screenshot()
			self.log.failed("No twitter interaction text found")

	def verifyGroupTweetsCount(self, count):
		self.verifyElement("Twitter.TextValidator.png", 30)
		tweets = s.findAll("Twitter.TextValidator.png")
		sorted_tweets = sorted(tweets, key=lambda m: m.y)
		tweets_count = len(sorted_tweets)
		if int(tweets_count) == int(count):
			self.log.passed("Found a group of " + str(count) + " interactions.")
		else:
			self.log.screenshot()
			self.log.failed("Found " + str(tweets_count) + " interactions. And expected " + str(count) + " interactions.")

	def verifyFacebookInteractionText(self):
		self.verifyElement("Facebook.TextValidator.png", 30)
		s.find("Facebook.TextValidator.png")
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		if exists("Facebook.TextValidator.png"):
			self.log.passed("Facebook interaction text appeared")
		else:
			self.log.screenshot()
			self.log.failed("No Facebook interaction text found")

	def verifyCustomElement(self, pattern_img, timeout=60):
		result = self.verifyElement(pattern_img, timeout)
		return result

	def verifyFacebookPostCount(self, count):
		self.verifyElement("Facebook.TextValidator.png", 30)
		posts = s.findAll("Facebook.TextValidator.png")
		sorted_posts = sorted(posts, key=lambda m: m.y)
		posts_count = len(sorted_posts)
		if int(posts_count) == int(count):
			self.log.passed("Found a group of " + str(count) + " interactions.")
		else:
			self.log.screenshot()
			self.log.failed("Found " + str(posts_count) + " interactions. And expected " + str(count) + " interactions.")

	def markInteractionAsDone(self):
		self.verifyElement("WDE.Interactions.Inbound.Facebook.Done.png")
		s.find("WDE.Interactions.Inbound.Facebook.Done.png").click()
		s.waitVanish("WDE.Interactions.Inbound.Facebook.Done.png", 5)

	def markInteractionDone(self):
		self.verifyElement("WDE.MarkDoneButton.png", 30)
		s.find("WDE.MarkDoneButton.png")
		s.wait(5)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		# self.verifyElement("WDE.MarkDoneButton.png")
		appRegion.click("WDE.MarkDoneButton.png")

	def verifyStaticText(self):
		self.verifyElement("WDE.Interactions.Inbound.Facebook.StaticText.png")

	def verifyStaticHyperlink(self):
		self.verifyElement("WDE.Interactions.Inbound.Facebook.StaticHyperlink.png")

	def verifyStaticEmojis(self):
		self.verifyElement("WDE.Interactions.Inbound.Facebook.StaticEmojis.png")

	def verifyStaticImage(self):
		sleep(15)
		self.scrollReplyWindowVertical()
		self.scrollReplyWindowHorizontol()
		self.verifyElement("WDE.Interactions.Inbound.Facebook.StaticImage.png")

	def deleteFacebookInboundInteraction(self):
		self.verifyElement("WDE.Interactions.Inbound.Facebook.Actions.Delete.png")
		s.find("WDE.Interactions.Inbound.Facebook.Actions.Delete.png")
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.Interactions.Inbound.Facebook.Actions.DeleteHover.png", "WDE.Interactions.Inbound.Facebook.Actions.Delete.png")
		s.wait(5)
		self.verifyElement("WDE.Interactions.Inbound.Facebook.DeleteDialog.png")
		s.find("WDE.Interactions.Inbound.Facebook.DeleteDialog.YesButton.png").click()

	def commentFacebookInboundInteractionAsAgent(self, comment):
		self.verifyElement("WDE.Interactions.Inbound.Facebook.Actions.Comment.png")
		s.find("WDE.Interactions.Inbound.Facebook.Actions.Comment.png")
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.Interactions.Inbound.Facebook.Actions.CommentHover.png", "WDE.Interactions.Inbound.Facebook.Actions.Comment.png")

	def likeFacebookInboundInteractionAsAgent(self):
		self.verifyElement("WDE.Interactions.Inbound.Facebook.Actions.Like.png")
		s.find("WDE.Interactions.Inbound.Facebook.Actions.Like.png")
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.Interactions.Inbound.Facebook.Actions.LikeHover.png", "WDE.Interactions.Inbound.Facebook.Actions.Like.png")

	def agentClickMoveToWorkbin(self):
		self.verifyElement("WDE.MoveToWorkbinButton.png", 15)
		s.find("WDE.MoveToWorkbinButton.png")
		s.wait(5)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		# self.verifyElement("WDE.MarkDoneButton.png")
		appRegion.click("WDE.MoveToWorkbinButton.png")
		s.wait(5)

	def agentClickMoveToWorkbinDraftTwitter(self):
		self.verifyElement("WDE.MoveToWorkbinDraftButtonTwitter.png", 15)
		s.find("WDE.MoveToWorkbinDraftButtonTwitter.png")
		s.wait(5)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		# self.verifyElement("WDE.MarkDoneButton.png")
		appRegion.click("WDE.MoveToWorkbinDraftButtonTwitter.png")
		s.wait(5)

	def agentClickMoveToWorkbinFacebook(self):
		self.verifyElement("WDE.MoveToWorkbinButtonFacebook.png", 15)
		s.find("WDE.MoveToWorkbinButtonFacebook.png")
		s.wait(5)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		# self.verifyElement("WDE.MarkDoneButton.png")
		appRegion.click("WDE.MoveToWorkbinButtonFacebook.png")
		s.wait(5)

	def agentNavigateToTwitterWorkbinInprogress(self):
		self.verifyElement("WDE.ExtraMenuButton.png", 15)
		s.find("WDE.ExtraMenuButton.png")
		s.wait(2)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.ExtraMenuButton.png")
		self.verifyElement("WDE.ExtraMenu.MyWorkbins.png", 15)
		s.find("WDE.ExtraMenu.MyWorkbins.png")
		s.wait(2)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.ExtraMenu.MyWorkbinsHover.png", "WDE.ExtraMenu.MyWorkbins.png")
		self.verifyElement("WDE.Workbins.TwitterWorkbinInprogress.png", 15)
		s.find("WDE.Workbins.TwitterWorkbinInprogress.png")
		s.wait(2)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.Workbins.TwitterWorkbinInprogress.png")

	def agentNavigateToTwitterWorkbinDraft(self):
		self.verifyElement("WDE.ExtraMenuButton.png", 15)
		s.find("WDE.ExtraMenuButton.png")
		s.wait(2)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.ExtraMenuButton.png")
		self.verifyElement("WDE.ExtraMenu.MyWorkbins.png", 15)
		s.find("WDE.ExtraMenu.MyWorkbins.png")
		s.wait(2)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.ExtraMenu.MyWorkbinsHover.png", "WDE.ExtraMenu.MyWorkbins.png")
		self.verifyElement("WDE.Workbins.TwitterWorkbinDraft.png", 15)
		s.find("WDE.Workbins.TwitterWorkbinDraft.png")
		s.wait(2)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.Workbins.TwitterWorkbinDraft.png")

	def agentNavigateToFacebookWorkbinInprogress(self):
		self.verifyElement("WDE.ExtraMenuButton.png", 15)
		s.find("WDE.ExtraMenuButton.png")
		s.wait(2)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.ExtraMenuButton.png")
		self.verifyElement("WDE.ExtraMenu.MyWorkbins.png", 15)
		s.find("WDE.ExtraMenu.MyWorkbins.png")
		s.wait(2)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.ExtraMenu.MyWorkbinsHover.png", "WDE.ExtraMenu.MyWorkbins.png")
		self.verifyElement("WDE.Workbins.FacebookWorkbinInprogress.png", 15)
		s.find("WDE.Workbins.FacebookWorkbinInprogress.png")
		s.wait(2)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.Workbins.FacebookWorkbinInprogress.png")

	def agentCloseWorkbin(self):
		s.wait(5)
		self.verifyElement("WDE.CloseWorkbinArea.png", 15)
		s.find("WDE.CloseWorkbinArea.png")
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		self.verifyElement("WDE.CloseWorkbinButton.png", 15)
		appRegion.click("WDE.CloseWorkbinButtonHover.png", "WDE.CloseWorkbinButton.png")
		s.waitVanish("WDE.CloseWorkbinButtonHover.png", 5)

	def agentOpenLastInteractionFromWorkbin(self):
		self.verifyElement("WDE.Workbins.ReceivedColumn.png", 15)
		s.find("WDE.Workbins.ReceivedColumn.png")
		s.wait(1)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.hover("WDE.Workbins.ReceivedColumn.png")
		click_count = 0
		while not exists(Pattern("WDE.Workbins.ReceivedColumnSorted.png").similar(0.90), 3):
			appRegion.click("WDE.Workbins.ReceivedColumn.png")
			click_count += 1
			if click_count == 3:
				self.agentCloseWorkbin()
				self.log.failed("Unable to sort the interactions in workbin.")
		self.verifyElement("WDE.Workbins.LastInteractionArea.png", 15)
		s.find("WDE.Workbins.LastInteractionArea.png")
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		self.verifyElement("WDE.Workbins.LastInteraction.png", 15)
		appRegion.hover("WDE.Workbins.LastInteraction.png")
		sleep(1)
		appRegion.doubleClick("WDE.Workbins.LastInteraction.png")
		self.verifyElement("WDE.Interactions.AgentDetails.png", 60)

	def agentSelectLastInteractionFromWorkbin(self):
		self.verifyElement("WDE.Workbins.ReceivedColumn.png", 15)
		s.find("WDE.Workbins.ReceivedColumn.png")
		s.wait(1)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.hover("WDE.Workbins.ReceivedColumn.png")
		click_count = 0
		while not exists(Pattern("WDE.Workbins.ReceivedColumnSorted.png").similar(0.90), 3):
			appRegion.click("WDE.Workbins.ReceivedColumn.png")
			click_count += 1
			if click_count == 3:
				self.agentCloseWorkbin()
				self.log.failed("Unable to sort the interactions in workbin.")
		self.verifyElement("WDE.Workbins.LastInteractionArea.png", 15)
		s.find("WDE.Workbins.LastInteractionArea.png")
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		self.verifyElement("WDE.Workbins.LastInteraction.png", 15)
		appRegion.hover("WDE.Workbins.LastInteraction.png")
		sleep(1)
		appRegion.click("WDE.Workbins.LastInteraction.png")

	def deleteInteractionFromWorkbin(self):
		self.verifyElement("WDE.Workbins.TwitterWorkbinDraft.DeleteButton.png", 15)
		s.find("WDE.Workbins.TwitterWorkbinDraft.DeleteButton.png")
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.Workbins.TwitterWorkbinDraft.DeleteButtonHover.png", "WDE.Workbins.TwitterWorkbinDraft.DeleteButton.png")
		self.verifyElement("WDE.Workbins.TwitterWorkbinDraft.DeleteButton.Yes.png", 15)
		s.find("WDE.Workbins.TwitterWorkbinDraft.DeleteButton.Yes.png")
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.Workbins.TwitterWorkbinDraft.DeleteButton.Yes.png")
		self.verifyElement("WDE.Workbins.TwitterWorkbinDraft.DeleteConfirmation.png", 15)

	def agentOpenLastInteractionFromWorkbinFacebook(self):
		self.verifyElement("WDE.Workbins.ReceivedColumn.png", 15)
		s.find("WDE.Workbins.ReceivedColumn.png")
		s.wait(1)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.hover("WDE.Workbins.ReceivedColumn.png")
		click_count = 0
		while not exists(Pattern("WDE.Workbins.ReceivedColumnSorted.png").similar(0.90), 3):
			appRegion.click("WDE.Workbins.ReceivedColumn.png")
			click_count += 1
			if click_count == 3:
				self.agentCloseWorkbin()
				self.log.failed("Unable to sort the interactions in workbin.")
		self.verifyElement("WDE.Workbins.LastInteractionAreaFacebook.png", 15)
		s.find("WDE.Workbins.LastInteractionAreaFacebook.png")
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		self.verifyElement("WDE.Workbins.LastInteractionFacebook.png", 15)
		appRegion.hover("WDE.Workbins.LastInteractionFacebook.png")
		sleep(1)
		appRegion.doubleClick("WDE.Workbins.LastInteractionFacebook.png")

	def agentNavigateToMyHistory(self):
		if exists("WDE.MyHistory.LastInteractionArea.png", 5):
			self.agentCloseWorkbin()
		self.verifyElement("WDE.ExtraMenuButton.png", 15)
		s.find("WDE.ExtraMenuButton.png")
		s.wait(2)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.ExtraMenuButton.png")
		self.verifyElement("WDE.ExtraMenu.MyHistory.png", 15)
		s.find("WDE.ExtraMenu.MyHistory.png")
		s.wait(2)
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.ExtraMenu.MyHistoryHover.png", "WDE.ExtraMenu.MyHistory.png")

	def agentOpenLastInteractionFromHistory(self):
		self.verifyElement("WDE.MyHistory.LastInteractionArea.png", 15)
		s.find("WDE.MyHistory.LastInteractionArea.png")
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		self.verifyElement("WDE.MyHistory.LastInteraction.png", 15)
		appRegion.click("WDE.MyHistory.LastInteraction.png")
		s.wait(3)

	def agentClickReplyTweet(self):
		ReplyTweetButtonArea = Pattern("Twitter.ReplyTweetButtonArea.png").similar(0.85)
		self.verifyElement(ReplyTweetButtonArea, 60)
		s.find(ReplyTweetButtonArea)
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		self.verifyElement("Twitter.ReplyTweetButton.png", 15)
		appRegion.click("Twitter.ReplyTweetButtonHover.png", "Twitter.ReplyTweetButton.png")
		self.scrollReplyWindowVertical()
		self.scrollReplyWindowHorizontol()

	def agentClickReplyAllTweet(self):
		ReplyTweetButtonArea = Pattern("Twitter.ReplyAllTweetButton.png").similar(0.85)
		self.verifyElement(ReplyTweetButtonArea, 60)
		s.find(ReplyTweetButtonArea)
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		self.verifyElement("Twitter.ReplyAllTweetButton.png", 15)
		appRegion.click("Twitter.ReplyAllTweetButtonHover.png", "Twitter.ReplyAllTweetButton.png")
		self.scrollReplyWindowVertical()
		self.scrollReplyWindowHorizontol()

	def agentClickRetweet(self):
		RetweetButtonArea = Pattern("Twitter.RetweetButtonArea.png").similar(0.85)
		self.verifyElement(RetweetButtonArea, 60)
		s.find(RetweetButtonArea)
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		self.verifyElement("Twitter.RetweetButton.png", 15)
		appRegion.click("Twitter.RetweetButtonHover.png", "Twitter.RetweetButton.png")
		self.scrollReplyWindowVertical()
		self.scrollReplyWindowHorizontol()
		RetweetButtonArea = Pattern("Twitter.RetweetButton2.png").similar(0.85)
		self.verifyElement(RetweetButtonArea, 60)
		s.find(RetweetButtonArea)
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		self.verifyElement("Twitter.RetweetButton2.png", 15)
		appRegion.click("Twitter.RetweetButton2.png")
		self.scrollReplyWindowVertical()
		self.scrollReplyWindowHorizontol()

	def agentClickReplyTweetMyHistory(self):
		self.scrollReplyWindowMyHistoryVertical()
		ReplyTweetButtonArea = Pattern("Twitter.ReplyTweetButtonArea.png").similar(0.85)
		self.verifyElement(ReplyTweetButtonArea, 60)
		s.find(ReplyTweetButtonArea)
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		self.verifyElement("Twitter.ReplyTweetButton.png", 15)
		appRegion.click("Twitter.ReplyTweetButtonHover.png", "Twitter.ReplyTweetButton.png")
		self.scrollReplyWindowMyHistoryVertical()

	def clickCommentButtonMyHistory(self):
		self.scrollReplyWindowMyHistoryVerticalFacebook()
		self.verifyElement("WDE.Interactions.Inbound.Facebook.Actions.Comment.png")
		s.find("WDE.Interactions.Inbound.Facebook.Actions.Comment.png")
		self.appCoordinates = (0, 0, int(self.width), int(self.height))
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.Interactions.Inbound.Facebook.Actions.CommentHover.png", "WDE.Interactions.Inbound.Facebook.Actions.Comment.png")
		self.scrollReplyWindowMyHistoryVerticalFacebook()
		self.verifyElement("WDE.Interactions.Inbound.Facebook.CommentArea.png")

	def scrollReplyWindowVertical(self):
		if exists("Twitter.ReplyWindowVerticalScrollBar.png", 2):
			regionScrollbar = s.find("Twitter.ReplyWindowVerticalScrollBar.png")
			# dragDrop(regionScrollbar, Location(regionScrollbar.getX(), regionScrollbar.getY() + 200))
			wheel(regionScrollbar, WHEEL_DOWN, 10)

	def scrollReplyWindowHorizontol(self):
		if exists("Twitter.ReplyWindowHorizontolScrollBar.png", 2):
			regionScrollbar = s.find("Twitter.ReplyWindowHorizontolScrollBar.png")
			dragDrop(regionScrollbar, Location(regionScrollbar.getX() + 150, regionScrollbar.getY()))

	def scrollReplyWindowMyHistoryVertical(self):
		if exists("WDE.MyHistory.InteractionWindow.ScrollVerticalArea2.png", 2):
			s.find("WDE.MyHistory.InteractionWindow.ScrollVerticalArea2.png")
			match = s.getLastMatch()
			self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
			appRegion = Region(*self.appCoordinates)
			self.verifyElement("WDE.MyHistory.InteractionWindow.ScrollVertical.png", 5)
			regionScrollbar = appRegion.find("WDE.MyHistory.InteractionWindow.ScrollVertical.png")
			wheel(regionScrollbar, WHEEL_DOWN, 10)

	def scrollReplyWindowMyHistoryVerticalFacebook(self):
		if exists("WDE.MyHistory.InteractionWindow.ScrollVerticalArea2.png", 2):
			s.find("WDE.MyHistory.InteractionWindow.ScrollVerticalArea2.png")
			match = s.getLastMatch()
			self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
			appRegion = Region(*self.appCoordinates)
			self.verifyElement("WDE.MyHistory.InteractionWindow.ScrollVertical.png", 5)
			if appRegion.exists("WDE.MyHistory.InteractionWindow.ScrollVertical.png", 2):
				regionScrollbar = appRegion.find("WDE.MyHistory.InteractionWindow.ScrollVertical.png")
			else:
				regionScrollbar = appRegion.find("WDE.MyHistory.InteractionWindow.ScrollVertical2.png")
			wheel(regionScrollbar, WHEEL_DOWN, 10)

	def agentClickRetweetWithComments(self):
		self.verifyElement("Twitter.RetweetWithCommentsButton.png", 15)
		s.find("Twitter.RetweetWithCommentsButton.png")
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		self.verifyElement("Twitter.RetweetWithCommentsButton.png", 15)
		appRegion.click("Twitter.RetweetWithCommentsButtonHover.png", "Twitter.RetweetWithCommentsButton.png")
		self.scrollReplyWindowVertical()
		self.scrollReplyWindowHorizontol()

	def agentClickDirectMessage(self):
		self.verifyElement("Twitter.DirectMessageButton.png", 15)
		s.find("Twitter.DirectMessageButton.png")
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		# self.verifyElement("Twitter.ReplyTweetButton.png", 15)
		appRegion.click("Twitter.DirectMessageButton.png")
		self.scrollReplyWindowVertical()
		self.scrollReplyWindowHorizontol()

	def agentClickDirectMessageMyHistory(self):
		self.scrollReplyWindowMyHistoryVertical()
		self.verifyElement("Twitter.DirectMessageButton.png", 15)
		s.find("Twitter.DirectMessageButton.png")
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		# self.verifyElement("Twitter.ReplyTweetButton.png", 15)
		appRegion.click("Twitter.DirectMessageButton.png")
		self.scrollReplyWindowMyHistoryVertical()

	def agentClickFavorite(self):
		self.verifyElement("Twitter.ReplyTweetButton.png", 15)
		self.scrollReplyWindowVertical()
		self.scrollReplyWindowHorizontol()
		self.verifyElement("Twitter.FavoriteButton.png", 15)
		s.find("Twitter.FavoriteButton.png")
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		# self.verifyElement("Twitter.ReplyTweetButton.png", 15)
		appRegion.click("Twitter.FavoriteButtonHover.png", "Twitter.FavoriteButton.png")

	def clickAttachmentLinkFacebook(self):
		self.verifyElement("Facebook.PrivateMessage.AttachmentLink.png", 15)
		s.find("Facebook.PrivateMessage.AttachmentLink.png")
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		appRegion.click("Facebook.PrivateMessage.AttachmentLink.png")

	def verifyActionabilityActionable(self):
		self.verifyElement("WDE.Interactions.ActionabilityIcon.png", 15)
		s.find("WDE.Interactions.ActionabilityIcon.png")
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		appRegion.hover("WDE.Interactions.ActionabilityIcon.png")
		result = self.verifyElement("WDE.Interactions.Actionability.Label.Actionable.png", 15)
		return result

	def verifyActionabilityNotActionable(self):
		self.verifyElement("WDE.Interactions.NotActionableIcon.png", 15)
		s.find("WDE.Interactions.NotActionableIcon.png")
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		appRegion.hover("WDE.Interactions.NotActionableIcon.png")
		result = self.verifyElement("WDE.Interactions.Actionability.Label.NotActionable.png", 15)
		return result

	def changeActionabilityToNotActionable(self):
		self.verifyElement("WDE.Interactions.ActionabilityIcon.png", 15)
		s.find("WDE.Interactions.ActionabilityIcon.png")
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.Interactions.ActionabilityIconHover.png", "WDE.Interactions.ActionabilityIcon.png")
		self.verifyElement("WDE.Interactions.Actionability.Options.NotActionable.png", 15)
		s.find("WDE.Interactions.Actionability.Options.NotActionable.png")
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		appRegion.click("WDE.Interactions.Actionability.Options.NotActionableHover.png", "WDE.Interactions.Actionability.Options.NotActionable.png")
		self.verifyElement("WDE.Interactions.NotActionableIcon.png", 5)


	def agentEnterTweetText(self, keyword):
		self.verifyElement("Twitter.ReplyTweetWindowArea.png", 15)
		s.find("Twitter.ReplyTweetWindowArea.png")
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		self.verifyElement("Twitter.ReplyTweetWindow.png", 15)
		appRegion.click("Twitter.ReplyTweetWindow.png")
		appRegion.type(keyword)

	def agentEnterRetweetText(self, keyword):
		self.verifyElement("Twitter.RetweetWindowArea.png", 15)
		s.find("Twitter.RetweetWindowArea.png")
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		self.verifyElement("Twitter.RetweetWindow.png", 15)
		appRegion.click("Twitter.RetweetWindow.png")
		appRegion.type(keyword)

	def agentEnterDmText(self, keyword):
		self.verifyElement("Twitter.DirectMsgWindowArea.png", 15)
		s.find("Twitter.DirectMsgWindowArea.png")
		match = s.getLastMatch()
		self.appCoordinates = (match.getX(), match.getY(), match.getW(), match.getH())
		appRegion = Region(*self.appCoordinates)
		self.verifyElement("Twitter.DirectMsgWindow.png", 15)
		appRegion.click("Twitter.DirectMsgWindow.png")
		appRegion.type(keyword)

	def verifyResult(self, *args):
		expected_result = str(eval(''.join(args)))
		actual_result = self.getResultFromClipboard()

		# verification
		if actual_result == expected_result:
			self.log.passed("Action performed correctly and result equals %s" % expected_result)
		else:
			self.log.failed(
				"Actual result '%s' is not equal to expected result '%s'" % (actual_result, expected_result))