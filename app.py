# -*- coding: utf-8 -*-
import os

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

import flask
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api, Namespace, Resource, fields
from flask_marshmallow import Marshmallow

#Google API
################################################################################
# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_id.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
################################################################################


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Note: A secret key is included in the sample so that it works, but if you
# use this code in your application please replace this with a truly secret
# key. See http://flask.pocoo.org/docs/0.12/quickstart/#sessions.
app.secret_key = 'Super Secret Key'

# Extensions initialization
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app, version='1.0', title='YouTube Music Videos API',
          description='An API for your YouTube Music Videos')

# Database table definition (SQLAlchemy)
class Vid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    code = db.Column(db.String())
    def link(self):
        return f'https://www.youtube.com/watch?v={self.code}'

# Serialization/Deserialization schema definition
class VidSchema(ma.ModelSchema):
    class Meta:
        strict = True
        model = Vid()
        fields = ['id', 'title', 'link', 'code']

# Variables to facilitate calling
vid_schema = VidSchema()
vids_schema = VidSchema(many=True)

#API model
video_model = api.model('videos', {
    'title': fields.String('Title of the video.'),
    'code': fields.String('Code of the video.')
})

# "Videos" resource RESTful API definitions
videos_api = Namespace('videos')
api.add_namespace(videos_api)

# If video doesn't exist then abort
def check_if_video_exists(code):
    video_exists = db.session.query(Vid).filter_by(code=code).first()
    if video_exists:
        return video_exists
    else:
        api.abort(404, f"Video code {code} doesn't exist")
        return

#Parser for the new title
parser = api.parser()
parser.add_argument('title', type=str, required=True, help='The New Title')

#API Routes
#MAIN route
@videos_api.route('/')
class Videos(Resource):
    @api.doc(responses={404: 'Error', 200: 'Success'})
    def get(self):
        '''Get all the music videos stored in the database'''
        videos_all = Vid.query.all()
        output = vids_schema.dump(videos_all).data
        return {'videos':output}, 200

    @api.doc(responses={404: 'Video Already on the Database', 200: 'Success'})
    @videos_api.expect(video_model)
    def post(self):
        '''Add new video to the list'''
        title = videos_api.payload['title']
        code = videos_api.payload['code']

        # Check if the video is already on the database
        video_exists = db.session.query(Vid).filter_by(code=code).first()
        #If video are not on the database, then add them
        if not video_exists:
            new_video = Vid(title=title, code=code)
            db.session.add(new_video)
            db.session.commit()
            return {'result': 'video added'}, 200
        return {'result': 'video already on db'}, 404

#YouTube routes
@videos_api.route('/youtube')
@api.doc(responses={404: 'Not able to fetch the YouTube API', 200: 'Success'})
class YoutubeLikedVideos(Resource):
    def get(self):
        '''
        Get the last 50 YouTube liked music videos
        Note: The session must be authorized for retrieving the list
        To launch OAuth2 please visit http://localhost:8090/videos/youtube in your browser once.
        '''
        if 'credentials' not in flask.session:
            flask.redirect('authorize')
        # Load the credentials from the session.
        credentials = google.oauth2.credentials.Credentials(**flask.session['credentials'])
        client = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

        response =  playlist_items_list_by_playlist_id(client,part='snippet', maxResults=50, playlistId='LM')

        return response, 200

@videos_api.route('/youtube/add_all')
@api.doc(responses={404: 'Not able to fetch the YouTube API', 200:'Success'})
class AddAllTheLikedVideos(Resource):
    def get(self):
        '''Add the 50 of your liked music videos to the database'''

        if 'credentials' not in flask.session:
            flask.redirect('authorize')
        # Load the credentials from the session.
        credentials = google.oauth2.credentials.Credentials(**flask.session['credentials'])
        client = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

        response =  playlist_items_list_by_playlist_id(client,part='snippet', maxResults=50, playlistId='LM')

        for video in response:
            # Check if the video is already on the database
            video_exists = db.session.query(Vid).filter_by(code=video['code']).first()
            #If video are not on the database, then add them
            if not video_exists:
                new_video = Vid(title=video['title'], code=video['code'])
                db.session.add(new_video)

        db.session.commit()
        return {'result': 'videos added'}, 200

# Single videos route
@videos_api.route('/<string:code>')
@api.doc(responses={404: 'Code Not Found', 200:'Success'},
         params={'code': 'The Video Code'})
class Video(Resource):

    '''Show a single item and lets you delete it'''
    def get(self, code):
        '''Fetch a single video.'''
        video = check_if_video_exists(code)
        output = vid_schema.dump(video).data
        return {'video':output}, 200

    def delete(self, code):
        '''Delete a single video'''
        video = check_if_video_exists(code)
        db.session.delete(video)
        db.session.commit()
        return {'result':'deleted'}, 200

    @api.doc(parser=parser)
    def put(self, code):
        '''Update the title of a single video'''
        args = parser.parse_args()
        new_details = {'title':args['title'], 'code':code}
        video = check_if_video_exists(code)

        video.title = new_details['title']
        db.session.commit()

        return {'result':'updated'}, 200


################################################################################
################################################################################
#Google API BEGIN
################################################################################
@app.route('/authorize')
def authorize():
  # Create a flow instance to manage the OAuth 2.0 Authorization Grant Flow
  # steps.
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES)
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

  authorization_url, state = flow.authorization_url(
      # This parameter enables offline access which gives your application
      # both an access and refresh token.
      access_type='offline',
      # This parameter enables incremental auth.
      include_granted_scopes='true')

  # Store the state in the session so that the callback can verify that
  # the authorization server response.
  flask.session['state'] = state

  return flask.redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
  # Specify the state when creating the flow in the callback so that it can
  # verify the authorization server response.
  state = flask.session['state']
  flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
      CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
  flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

  # Use the authorization server's response to fetch the OAuth 2.0 tokens.
  authorization_response = flask.request.url
  flow.fetch_token(authorization_response=authorization_response)

  # Store the credentials in the session.
  # ACTION ITEM for developers:
  #     Store user's access and refresh tokens in your data store if
  #     incorporating this code into your real app.
  credentials = flow.credentials
  flask.session['credentials'] = {
      'token': credentials.token,
      'refresh_token': credentials.refresh_token,
      'token_uri': credentials.token_uri,
      'client_id': credentials.client_id,
      'client_secret': credentials.client_secret,
      'scopes': credentials.scopes
  }

  return flask.redirect('videos/youtube')

#YouTube API response functions
# This function extracts the desired values from the YouTube API response
def parse_response(response):
    if response:
        videos = []
        for video in response['items']:
            title = video['snippet']['title']
            code = video['snippet']['resourceId']['videoId']
            link = f'https://www.youtube.com/watch?v={code}'
            videos.append({'title': title, 'code': code, 'link':link})

        return videos
    else:
      return ('This request does not return a response. For these samples, ' +
              'this is generally true for requests that delete resources, ' +
              'such as <code>playlists.delete()</code>, but it is also ' +
              'true for some other methods, such as <code>videos.rate()</code>.')

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
  good_kwargs = {}
  if kwargs is not None:
    for key, value in kwargs.items():
      if value:
        good_kwargs[key] = value
  return good_kwargs

def playlist_items_list_by_playlist_id(client, **kwargs):
  kwargs = remove_empty_kwargs(**kwargs)
  response = client.playlistItems().list(**kwargs).execute()
  return parse_response(response)

################################################################################
#Google API END
################################################################################
################################################################################


if __name__ == '__main__':
  # When running locally, disable OAuthlib's HTTPs verification. When
  # running in production *do not* leave this option enabled.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

  #Create all the tables of the database
  db.create_all()

  # Check if the videos codes are already on the database
  dummy1 = db.session.query(Vid).filter_by(code='XA4vo1kef6g').first()
  dummy2 = db.session.query(Vid).filter_by(code='DU64jmOPL5k').first()

  #If videos are not on the database, then add them
  if not dummy1 or not dummy2:
      with db.session.begin(nested=True):
          db.session.add(Vid(title = 'Boris Brejcha - I Take It Smart', code='XA4vo1kef6g'))
          db.session.add(Vid(title = 'Noku Mana - Curawaka', code='DU64jmOPL5k'))


  app.run('localhost', 8090, debug=True,) #use_reloader=False)
