from tkinter import *
import tkFileDialog
import tkMessageBox
import datetime
import functions
import sys
import threading

def loadGUI():
	class App:

			def __init__(self, master):
					self.master = master

					#call start to initialize to create the UI elemets
					self.start()

			def start(self):
					self.master.title("Lost artist finder")

					self.now = datetime.datetime.now()

					#CREATE A TEXT/LABEL
					#put "label01" in "self.master" which is the window/frame
					#then, put in the first row (row=0) and in the 2nd column (column=1), align it to "West"/"W"
					Label(self.master, text="Last.FM").grid(row=0, column=0, sticky=W)
					Label(self.master, text="Username").grid(row=1, column=0)
					Label(self.master, text="Password").grid(row=2, column=0)
					Label(self.master, text="Min. scrobbles").grid(row=3, column=0, sticky=W)
					Label(self.master, text="").grid(row=4, column=0, sticky=W)
					Label(self.master, text="iTunes").grid(row=5, column=0, sticky=W)
					Label(self.master, text="Library").grid(row=6, column=0, sticky=W)
					Label(self.master, text="").grid(row=7, column=0, sticky=W)
					Label(self.master, text="Spotify").grid(row=8, column=0, sticky=W)
					Label(self.master, text="Username").grid(row=9, column=0)
					Label(self.master, text="Password").grid(row=10, column=0)
					Label(self.master, text="").grid(row=11, column=0, sticky=W, rowspan=3)
					self.lastfmUser = Entry(self.master)
					self.lastfmUser.insert(END, 'guys_eyes')
					self.lastfmUser["width"] = 20
					self.lastfmUser.focus_set()
					self.lastfmUser.grid(row=1,column=1)
					self.lastfmPass = Entry(self.master, show="*")
					self.lastfmPass.insert(END, 'CA$HM0NEY!')
					self.lastfmPass["width"] = 20
					self.lastfmPass.focus_set()
					self.lastfmPass.grid(row=2,column=1)
					self.optionsMin = Entry(self.master)
					self.optionsMin.insert(END, '10')
					self.optionsMin["width"] = 20
					self.optionsMin.focus_set()
					self.optionsMin.grid(row=3,column=1)

					#CREATE A BUTTON WITH "ASK TO OPEN A FILE"
					self.open_file = Button(self.master, text="Browse for iTunes Library file", command=self.browse_file)
					self.open_file.grid(row=6, column=1,sticky=W) #put it beside the filelocation textbox

					self.spotifyUser = Entry(self.master)
					self.spotifyUser.insert(END, 'holloway')
					self.spotifyUser["width"] = 20
					self.spotifyUser.focus_set()
					self.spotifyUser.grid(row=9,column=1)
					self.spotifyPass = Entry(self.master, show="*")
					self.spotifyPass.insert(END, 'earthb0und')
					self.spotifyPass["width"] = 20
					self.spotifyPass.focus_set()
					self.spotifyPass.grid(row=10,column=1)
		
					#now for a button
					self.submit = Button(self.master, text="Find missing artists", command=self.executeFind, fg="red")
					self.submit.grid(row=14, column=1,sticky=W, columnspan=4)
					
					self.status_box = Text(self.master)
					self.status_box["width"] = 40
					self.status_box.grid(row=15, column=0,sticky=W, columnspan=2)
			def executeFind(self):
					#more code here
					launchBuildData(self)
					t1.start()
			def browse_file(self):
					self.filename = tkFileDialog.askopenfilename(title="Please locate 'iTunes Library.xml'...")
	root = Tk()
	app = App(root)
	root.mainloop()

def launchBuildData(self):
	t1=threading.Thread(target=functions.buildData(self, self.lastfmUser.get(), self.lastfmPass.get(), self.filename, self.optionsMin.get()))