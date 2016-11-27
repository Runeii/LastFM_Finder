from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox
import datetime
import functions
import sys
import threading
import queue as Queue

def loadGUI():
	class App:
			
			def __init__(self, master):
					self.master = master
					
					#call start to initialize to create the UI elemets
					self.start()

			def start(self):
					self.running = False
					self.filename = False
					self.master.title("Lost artist finder")
					self.now = datetime.datetime.now()
					def styledLabel(inputText):
						return Label(self.master, text=inputText, font="14")
					#CREATE A TEXT/LABEL
					#put "label01" in "self.master" which is the window/frame
					#then, put in the first row (row=0) and in the 2nd column (column=1), align it to "West"/"W"
					styledLabel("Last.FM").grid(row=0, column=0, sticky=W)
					styledLabel("Username").grid(row=1, column=0)
					styledLabel("Password").grid(row=2, column=0)
					styledLabel("Min. scrobbles").grid(row=3, column=0)
					styledLabel("").grid(row=4, column=0, sticky=W)
					styledLabel("iTunes").grid(row=5, column=0, sticky=W)
					styledLabel("Library").grid(row=6, column=0)
					styledLabel("").grid(row=7, column=0, sticky=W)
					#styledLabel("Spotify").grid(row=8, column=0, sticky=W)
					#styledLabel("Username").grid(row=9, column=0)
					#styledLabel("Password").grid(row=10, column=0)
					
					self.lastfmUser = Entry(self.master)
					self.lastfmUser["width"] = 20
					self.lastfmUser.focus_set()
					self.lastfmUser.grid(row=1,column=1)
					self.lastfmPass = Entry(self.master, show="*")
					self.lastfmPass["width"] = 20
					self.lastfmPass.focus_set()
					self.lastfmPass.grid(row=2,column=1)
					self.optionsMin = Entry(self.master)
					self.optionsMin.insert(END, '10')
					self.optionsMin["width"] = 20
					self.optionsMin.focus_set()
					self.optionsMin.grid(row=3,column=1)
					
					#CREATE A BUTTON WITH "ASK TO OPEN A FILE"
					self.open_file = Button(self.master, text="Browse for Library file", command=self.browse_file)
					self.open_file.grid(row=6, column=1)
					
					#self.spotifyUser = Entry(self.master)
					#self.spotifyUser.insert(END, 'holloway')
					#self.spotifyUser["width"] = 20
					#self.spotifyUser.focus_set()
					#self.spotifyUser.grid(row=9,column=1)
					#self.spotifyPass = Entry(self.master, show="*")
					#self.spotifyPass.insert(END, 'earthb0und')
					#self.spotifyPass["width"] = 20
					#self.spotifyPass.focus_set()
					#self.spotifyPass.grid(row=10,column=1)
					
					#now for a button
					self.submit = Button(self.master, text="Find missing artists", command=self.executeFind, fg="red")
					self.submit.grid(row=14, column=1,sticky=W, columnspan=4)
					
					self.status_box = Text(self.master)
					self.status_box["width"] = 50
					self.status_box.grid(row=15, column=0,columnspan=4)
					self.queue = Queue.Queue()
					
			def periodicCall(self):
					"""
					Check every 200 ms if there is something new in the queue.
					"""
					self.gui.processIncoming()
					if self.running is False:
							# This is the brutal stop of the system. You may want to do
							# some cleanup before actually shutting it down.
							import sys
							sys.exit(1)
					self.master.after(200, self.periodicCall)					
			def executeFind(self):
					#more code here
					if self.filename is not False:
						if self.running is False:
							self.running = True
							self.submit.config(state="disabled")
							newthread = threading.Thread(target=functions.buildData, args=(self, self.lastfmUser.get(), self.lastfmPass.get(), self.filename, self.optionsMin.get()))
							newthread.start()
					else:
						self.status_box.insert(tk.INSERT, str(time.strftime("%H:%M:%S", formatTime)) + " No iTunes library specified\n")
			def browse_file(self):
					self.filename = filedialog.askopenfilename(title="Please locate 'iTunes Library.xml'...",initialdir="~/Music/iTunes")
			def endApplication(self):
					self.running = False
	root = Tk()
	app = App(root)
	root.mainloop()