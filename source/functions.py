import pylast
from pyItunes import *
import tkinter as tk
import time
import datetime
import urllib
import sys
import os
import gui

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def enhanceSimilarity(name):
	name = str(name)
	name = name.lower().replace('+', 'and').replace('&', 'and').replace('-', '').replace(',', '').replace('.', '')
	return name

def buildData(self, username, password, ilib, min):
	def updateStatus(text, self=self):	
		formatTime = time.strptime(time.ctime(), '%a %b %d %H:%M:%S %Y')
		output = self.status_box.insert(tk.INSERT, str(time.strftime("%H:%M:%S", formatTime)) + " " + text + "\n")
		self.queue.put(output)
	##########
	# Settings
	settingsVerbose = False
	settingsMinplays = 10
	##########	
	class Object(object):
			pass
	API_KEY = "abd35684573cd5fb341b366cfe4bed7a" # this is a sample key
	API_SECRET = "4300b0053d0c6078afb72251a4ed61aa"
	password_hash = pylast.md5(password)
	network = pylast.LastFMNetwork(api_key = API_KEY, api_secret =
			API_SECRET, username = username, password_hash = password_hash)
	updateStatus("Checking connection to Last.FM...")
	lastfm_user = network.get_user(username)
	updateStatus("Last.FM connected")
	library = lastfm_user.get_library()
	updateStatus("Last.FM library loaded")
	updateStatus("Loading Last.FM artists...")
	lastfmCount = 0
	lastfmDB = set()
	lastfmdetailsDB = {}
	artists = library.get_artists(limit=0)
	updateStatus("Last.FM artists loaded")
	for artist in artists:
		if artist.playcount >= settingsMinplays: 
			lastfmCount += 1
			if settingsVerbose is True:
				print(artist[0])
			cleanName = enhanceSimilarity(artist[0])
			lastfmDB.add(cleanName)
			lastfmdetailsDB[cleanName] = {}
			lastfmdetailsDB[cleanName]['name'] = artist[0]
			lastfmdetailsDB[cleanName]['playcount'] = artist.playcount
	updateStatus("Last.FM DB built")
	
	updateStatus("Loading iTunes Library file...")
	l = Library(ilib)
	updateStatus("iTunes Library file loaded")
	updateStatus("Building iTunes Library DB")
	printCount = 0
	itunesCount = 0
	itunesDB = set()
	for id, song in l.songs.items():
		itunesCount += 1
		cleanName = song.artist
		if cleanName not in itunesDB:
			itunesDB.add(enhanceSimilarity(cleanName))
			if settingsVerbose is True:
				print(cleanName)
				printCount += 1
	updateStatus("iTunes Library DB built")

	updateStatus("Comparing libraries and processing results")
	
	difference = lastfmDB - itunesDB
	diffCount = len(difference)
	runningCount = 0
	outputDB = {}

	updateStatus('Artists in iTunes library: ' + str(itunesCount))
	updateStatus('Artists scrobbled to LastFM: ' + str(lastfmCount))
	updateStatus('Scrobbled but not on iTunes: ' + str(diffCount))


	updateStatus("Sorting and ordering results")

	for entry in difference:
		if settingsVerbose is True:
			print(str(runningCount) + ' / ' + str(diffCount))
			self.status_box.insert(tk.INSERT, 'Starting ' + str(entry))
		cleanName = str(entry)
		playcount = lastfmdetailsDB[cleanName]['playcount']
		outputDB[playcount] = {}
		outputDB[playcount]['name'] = lastfmdetailsDB[cleanName]['name']
		outputDB[playcount]['playcount'] = playcount
		if settingsVerbose is True:
			self.status_box.insert(tk.INSERT, 'Finished ' + str(entry))
		runningCount += 1
	self.status_box.delete(0.0, 'end')
	self.status_box.insert(tk.INSERT, str(diffCount) + " artists missing from iTunes Library\n\n")

	for key, entry in sorted(outputDB.items(), reverse=True):
		self.status_box.insert(tk.INSERT, str(outputDB[key]['name']) + ' (scrobbled ' + str(outputDB[key]['playcount']) + ' times)\n')
