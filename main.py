import urllib2
import json
from datetime import datetime
from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

from OPMLBuilder import OPMLBuilder

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Horse!'

@app.route('/subscriptions.opml')
def get_subscriptions_opml():
    items = []
    body = {'nextPageToken': ''}
    url = 'https://www.googleapis.com/youtube/v3/subscriptions'
    params = { 'part': 'snippet'
             , 'channelId': raise # insert your channel ID here
             , 'maxResults': '50'
             , 'order': 'alphabetical'
             , 'key': raise # insert your YouTube API key here
             }

    while 'nextPageToken' in body:
        params['pageToken'] = body['nextPageToken']
        request_url = url + '?'
        request_url += '&'.join('{}={}'.format(k, v) for k, v in params.iteritems())
        r = urllib2.urlopen(request_url)
        body = json.loads(r.read())
        items += body['items']

    if len(items) != body['pageInfo']['totalResults']:
        return "Something has gone horribly wrong."
    
    opml = OPMLBuilder()
    opml.addFolder('YouTube')
    for i in items:
        name = i['snippet']['title']
        guid = i['snippet']['resourceId']['channelId']
        opml['YouTube'].addSubscription(name, guid)

    return str(opml)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
