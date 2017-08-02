#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from google.appengine.ext import ndb
import jinja2
import os
import webapp2
import urllib2
import json
import urllib
from spotify_data_model import spotifyUserInfo

# import spotipy
# import sys
# import spotipy.util as util
# from spotipy.oauth2 import SpotifyClientCredentials
# import pprint

# sp = spotipy.Spotify()

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# client_credentials_manager = SpotifyClientCredentials()
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # search = self.request.get("search")
        my_template = jinja_environment.get_template("templates/test.html")
        places_data_source = urllib2.urlopen(
            "https://maps.googleapis.com/maps/api/place/textsearch/json?query=subwaysinChicago&key=AIzaSyCCRonxhEphWEum0RufD1kNxAHS1ngWXO0")
        places_json_content = places_data_source.read()
        parsed_places_dictionary = json.loads(places_json_content)
        results = parsed_places_dictionary["results"]

        base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="
        api_key = "AIzaSyCCRonxhEphWEum0RufD1kNxAHS1ngWXO0"
        query = "places in Chicago"
        search_params = {"query": query, "api_key": api_key}
        search_url = base_url + urllib.urlencode(search_params)
        search_url_data_source = urllib2.urlopen(search_url)
        search_url_json_content = search_url_data_source.read()
        parsed_search_url_dictionary = json.loads(search_url_json_content)
        search_url_results = parsed_search_url_dictionary["results"]
        latlngList = []
        # for result in search_url_results:
        for result in results:
            latlngDict = result["geometry"]["location"]
            lat = latlngDict["lat"]
            lng = latlngDict["lng"]
            latlngList.append((lat,lng))
        render_data = { "lat": lat, "lng": lng, "coordinate_list" : latlngList}
        self.response.write(my_template.render(render_data))

class LocationInformationHandler(webapp2.RequestHandler):
    def get(self):
        my_template=jinja_environment.get_template("templates/LocationInformation.html")
        information_data_source = urllib2.urlopen(
        "https://maps.googleapis.com/maps/api/place/textsearch/json?query=subway%20in%20New%20York%20City&key=AIzaSyCCRonxhEphWEum0RufD1kNxAHS1ngWXO0"
        )
        information_json_content = information_data_source.read()
        parsed_information_dictionary = json.loads(information_json_content)
        results = parsed_information_dictionary["results"]
        nameList = []
        # hoursList = []
        for result in results:
            nameDict = result["name"]
            ratingDict = result["rating"]
            nameList.append((nameDict, ratingDict))
        render_data = {"name": nameList}
        self.response.write(my_template.render(render_data))



class LoginHandler(webapp2.RequestHandler):
    def get(self):
        my_template=jinja_environment.get_template("templates/login.html")
        render_data={}
        username=self.request.get("username")
        if username!="":
            spotify_user=spotifyUserInfo(postUserName=username)
            spotify_user.put()
        render_data['name']=username

        self.response.write(my_template.render(render_data))

class ServiceHandler(webapp2.RequestHandler):
    def get(self):
        my_template=jinja_environment.get_template("templates/service.html")
        render_data={}
        query = spotifyUserInfo.query()
        render_data['list_of_users'] = query.fetch()
        self.response.write(my_template.render(render_data))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login',LoginHandler),
    ('/Info', LocationInformationHandler),
    ('/service',ServiceHandler)

], debug=True)
