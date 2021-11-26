import tweepy
from dotenv import dotenv_values


class Publisher():
	
	store_file = "store.db"

	character_limit = 280

	def __init__(self):
		# create the config from env file
		self.config = dotenv_values(".env")

		# create the api client
		auth = tweepy.OAuthHandler(self.config["TWITTER_CONSUMER_KEY"], self.config["TWITTER_CONSUMER_SECRET"])
		auth.set_access_token(self.config["TWITTER_ACCESS_TOKEN"], self.config["TWITTER_ACCESS_TOKEN_SECRET"])

		self.api = tweepy.API(auth)

	def publish(self, message: str, url: str = None):
		if url is not None:
			message = f"{message}\n{url}"

		self.api.update_status(message)
