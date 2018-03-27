from flask import Flask, render_template, request
from authlib.client import OAuth2Session
import requests
import json

#for forms?
from flask_wtf import FlaskForm
from wtforms import TextField, StringField, PasswordField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)

@app.route("/slug/change", methods=['GET', 'POST'])
def slugchangeform():	
	return render_template('form_slug_change.html')
	
@app.route("/slug", methods=['GET', 'POST'])
def slugchange():
	global client_id
	global client_secret
	global redirect_uri
	global session
	#for any nation to be compat
	global nation_slug
	
	#store OAuth 2.0 values for Blake's Test People App as session information
	client_id = r'002ab1e9470339222ee3a65220dfbe0ee77c82d8122805c0502227b5c72c9a10'
	client_secret = r'a6bb5365453640bbdf64be0912d0f8726da622739bfea05d91cc2a526c896883'
	redirect_uri = 'https://0523d76e.ngrok.io/authenticate'
	session = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri)
	
	nation_slug = request.form['form_nation_slug']
	
	authorize_url = 'https://' + nation_slug + '.nationbuilder.com/oauth/authorize'
	uri, state = session.authorization_url(authorize_url)
	
	return render_template('slug_change_block.html', uri=uri, nation_slug=nation_slug)

@app.route("/", methods=['GET', 'POST'])
def index():
	global client_id
	global client_secret
	global redirect_uri
	global session
	global nation_slug
	
	try:
		nation_slug
	except NameError:
		nation_slug = 'blakemizelledev'
	
	#this workflow is from here: https://docs.authlib.org/en/latest/client/oauth2.html#oauth-2-session
	#store OAuth 2.0 values for Blake's Test People App as session information
	client_id = r'002ab1e9470339222ee3a65220dfbe0ee77c82d8122805c0502227b5c72c9a10'
	client_secret = r'a6bb5365453640bbdf64be0912d0f8726da622739bfea05d91cc2a526c896883'
	redirect_uri = 'https://0523d76e.ngrok.io/authenticate'
	session = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri)

	authorize_url = 'https://' + nation_slug + '.nationbuilder.com/oauth/authorize'
	uri, state = session.authorization_url(authorize_url)
	
	return render_template('index.html', uri=uri)
	
@app.route("/authenticate")
def authenticate():
	global raw_access_token
	
	#gets ?code param from URL returned by Nationbuilder
	full_response_url = request.url
	code = request.args.get('code')
	
	#begin getting access token
	authorization_response = full_response_url
	access_token_url = 'https://' + nation_slug + '.nationbuilder.com/oauth/token'
	kwargs = {'grant_type':'authorization_code'}
	token = session.fetch_access_token(access_token_url, authorization_response=authorization_response)

	raw_access_token = session.token['access_token']

	return render_template('authenticate.html', code=code, access_token=raw_access_token, nation_slug=nation_slug)

@app.route("/people/count")
def peoplecount():
	api_url = 'https://' + nation_slug + '.nationbuilder.com/api/v1/people/count' + '?access_token=' + raw_access_token
	
	r = requests.get(api_url)
	results = r.json()

	return render_template('people_count_block.html', results=results)
	
@app.route("/people/list")
def peoplelist():
	api_url = 'https://' + nation_slug + '.nationbuilder.com/api/v1/people' + '?access_token=' + raw_access_token + '&limit=10000'
	
	r = requests.get(api_url)
	raw_data = r.json()
	data = raw_data.get('results')
	
	return render_template('people_list_block.html', data=data)

@app.route("/people/create/form")
def peoplecreateform():
	
	return render_template('form_people_create.html')
	
@app.route("/people/create", methods=['POST', 'GET'])
def peoplecreate():
	api_url = 'https://' + nation_slug + '.nationbuilder.com/api/v1/people' + '?access_token=' + raw_access_token
	
	form_first_name = request.form['person_first_name']
	form_last_name = request.form['person_last_name']
	form_email = request.form['person_email']
	
	data = {"person": {"email": form_email, "last_name": form_last_name, "first_name": form_first_name, "sex": "", "signup_type": 0, "employer": "", "party": "","registered_address": {"state": "", "country_code": ""}}}
	
	r = requests.post(api_url, json=data)
	response = r.text
	
	return render_template('people_create_block.html', r=r, response=response)

@app.route("/people/update/form")
def peopleupdateform():
	api_url = 'https://' + nation_slug + '.nationbuilder.com/api/v1/people' + '?access_token=' + raw_access_token + '&limit=10000'
	
	r = requests.get(api_url)
	raw_data = r.json()
	data = raw_data.get('results')
	
	return render_template('form_people_update.html', data=data)
	
@app.route("/people/update", methods=['POST', 'GET'])
def peopleupdate():
	form_id = request.form['person_id']
	api_url = 'https://' + nation_slug + '.nationbuilder.com/api/v1/people/' + form_id + '?access_token=' + raw_access_token
	
	form_first_name = request.form['person_first_name']
	form_last_name = request.form['person_last_name']
	form_email = request.form['person_email']
	
	data = {"person": {"email": form_email, "last_name": form_last_name, "first_name": form_first_name, "sex": "", "signup_type": 0, "employer": "", "party": "","registered_address": {"state": "", "country_code": ""}}}
	
	r = requests.put(api_url, json=data)
	response = r.text
	
	return render_template('people_create_block.html', r=r, response=response)

@app.route("/people/delete/form")
def peopledeleteform():
	api_url = 'https://' + nation_slug + '.nationbuilder.com/api/v1/people' + '?access_token=' + raw_access_token + '&limit=10000'
	
	r = requests.get(api_url)
	raw_data = r.json()
	data = raw_data.get('results')
	
	return render_template('form_people_delete.html', data=data)
	
@app.route("/people/delete", methods=['POST', 'GET', 'DELETE'])
def peopledelete():
	form_id = request.form['person_id']
	api_url = 'https://' + nation_slug + '.nationbuilder.com/api/v1/people/' + form_id + '?access_token=' + raw_access_token
	
	#data = {"person": {"email": form_email, "last_name": form_last_name, "first_name": form_first_name, "sex": "", "signup_type": 0, "employer": "", "party": "","registered_address": {"state": "", "country_code": ""}}}
	
	r = requests.delete(api_url)
	response = r.text
	
	return render_template('people_create_block.html', r=r, response=response)	

if __name__ == "__main__":
   app.run()