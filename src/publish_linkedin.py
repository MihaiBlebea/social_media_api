import requests
import argparse

from linkedin_oauth import auth, headers
from variables import get_variable


class LifecycleState():
	DRAFT: str = "DRAFT"
	PUBLISHED: str = "PUBLISHED"

class Publisher():

	profile_url = "https://api.linkedin.com/v2/me"

	post_url = "https://api.linkedin.com/v2/ugcPosts"

	credentials_file = "credentials.json"

	def __init__(self):
		pass

	def __get_user_information(self):
		'''
		Get user information from Linkedin
		'''
		r = requests.get(self.profile_url, headers=self.__get_headers())
		
		if r.status_code != 200:
			return None

		return r.json()

	def __get_headers(self):
		return headers(self.__get_access_token())

	def __get_access_token(self):
		# return auth(self.credentials_file)
		return get_variable("LINKEDIN_ACCESS_TOKEN")

	def post_update(self, message: str):
		# Get user id to make a UGC post
		user_info = self.__get_user_information()
		if user_info is None:
			print("user info is none")
			return None

		urn = user_info['id']

		# UGC will replace shares over time.
		author = f'urn:li:person:{urn}'

		post_data = {
			"author": author,
			"lifecycleState": LifecycleState.PUBLISHED,
			"specificContent": {
				"com.linkedin.ugc.ShareContent": {
					"shareCommentary": {
						"text": message
					},
					"shareMediaCategory": "NONE"
				}
			},
			"visibility": {
				"com.linkedin.ugc.MemberNetworkVisibility": "CONNECTIONS"
			}
		}

		r = requests.post(
			self.post_url, 
			headers=self.__get_headers(), 
			json=post_data
		)

		if r.status_code != 200:
			return None

		return r.json()

# if __name__ == "__main__":
# 	pub = Publisher()
# 	pub.post_update("ceva")
