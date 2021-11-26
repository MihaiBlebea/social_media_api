from flask import Flask, jsonify, request, abort

from variables import get_variable
from publish_twitter import Publisher as TwitterPublisher
from publish_linkedin import Publisher as LinkedinPublisher
app = Flask(__name__)

# @app.before_request
# def before_request_func():
# 	proxy_secret = request.headers.get("X-RapidAPI-Proxy-Secret")

# 	if proxy_secret is None:
# 		return abort(401)

# 	if proxy_secret != get_variable("RAPIDAPI_PROXY_SECRET"):
# 		return abort(401)

@app.route("/health", methods=["GET"])
def health():
	return jsonify({
		"status": "OK"
	})

@app.route("/post/twitter", methods=["POST"])
def post_twitter():
	body = request.json
	if "message" not in body:
		abort(500)
	
	if "url" not in body:
		abort(500)

	publisher = TwitterPublisher()
	publisher.publish(body["message"], body["url"])

	return jsonify({
		"status": "OK"
	})

@app.route("/post/linkedin", methods=["POST"])
def post_linkedin():
	body = request.json
	if "message" not in body:
		abort(500)

	publisher = LinkedinPublisher()
	publisher.post_update(body["message"])

	return jsonify({
		"status": "OK"
	})

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)