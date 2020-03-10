#!/usr/bin/env python

######################################################################
#                                                                    #
# First project on github, but not the first done.                   #
# You may wonder why im making this and what utility i give to it.   #
# I have too many links saved in notepads, which I can't save in     #
# bookmarks for some reasons and its imposible to open one by one.   #
# This program make my life a little bit easier, and i hope it does  #
# for you.                                                           #
#                                                                    #
#                                                                    #
# Started in: 01/03/2020                                             #
# Finished at: 04/03/2020 at 8:30AM                                  #
# Hours dedicated: About 25HS                                        #
#                                                                    #                              
######################################################################
#                                                                    #
# LICENSE INFO                                                       #
#                                                                    #
# This is free to use.                                               #
#                                                                    #
# You can use, modify, propagate, share and make a better version of #
# this always giving to me all the rights of creator.                #
#                                                                    #
# You cant sell this without my permission.                          #
#                                                                    #
# You cant use this to make money in any way.                        #
#                                                                    #
# I am not responsible for any loss of data or malfunction of the    #
# program.                                                           #
#                                                                    #
######################################################################

# TO-DO LIST
# Improve the code.
# Make the code less ugly (Sorry for that).
# AutoCheck for links.
# Encrypt data.
# Make a gui!

# WHAT YOU CAN DO?
# Add/remove links and open it
# Set password for the program (Soon encrypted config and data files)
# Switch between Firefox and Chrome browser
# Switch between Stealth mode (xxx)

import json
import webbrowser
import os
import configparser
import io
import sys

__author__ = "Matias Fanger"
__copyright__ = "Copyright 2020"
__credits__ = ["Google.com", "geeksforgeeks.org", "stackoverflow.com"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Matias Fanger"
__email__ = "matifanger@outlook.com"
__status__ = "Completed at 95%"



def menu():
    print("\n\n\n1. Add/Remove links")
    print("2. List links")
    print("3. List links and open")
    print("4. Settings")
    print("5. Exit")
    number = int(input("Pick: "))
    pick(number)

def pick(number):
    if number == 1:
        print("\n\n\n\n\n\n1. Add links\n2. Remove links\n3. Go back")
        addremove = int(input("Choice: "))
        if addremove == 1:
            cv.addvideos()
        elif addremove == 2:
            cv.removevideos()
        elif number != 1 or  number != 2:
            menu()
    elif number == 2:
        cv.listvideos(True)
    elif number == 3:
        cv.listvideosandopen()
    elif number == 4:
        settingsmenu()
    elif number == 5:
        print("Closing...")
        sys.exit()
    else: menu()

class controlvideos:
    def loadvideos(self,dataremoved=False):
        if os.path.isfile('data.json'):
            with open('data.json') as json_file:
                global data
                try:
                    data = json.load(json_file)
                    print('\n\nDictionary updated!')
                except:
                    data = {}
                    print('\n\nDictionary empty!')

        else:        
            cfgfile = open("data.json",'w')
            cfgfile.close()
            print('[!] Json file created.')

        if dataremoved == True:
            print('[!] All data removed')

    def listvideos(self,comefromain=False):
            print('\n\n\n\n\n\n\n\n---------- VIDEO LIST ------------')
            keys = tuple(data.keys())
            lkeys = len(keys)
            if lkeys != 0:
                try:
                    for k in keys:
                        value = data.get(k)
                        print(keys[k] , '. | Title: ' + value['title'] + ' | Link: ' + value['link'] + ' | Stars: ' + value['stars']+'/10')
                    if comefromain == True:
                        menu()
                except:
                    print('\n\n[!] FATAL ERROR TRYING TO LIST VIDEOS!')
                    menu()
            else: 
                print('[!] No videos added!')
                menu()


    def addvideos(self):
        global nid
        nid = input("\n\n\nID: ")
        title = input("Title: ")
        link = input("Link: ")
        stars = input("Stars (1/10): ")

        try:
            data[nid] = {'ID':nid, 'title':title, 'link':link, 'stars':stars}
            print(data)
        except:
            data[nid] = {}
            data[nid] = {'ID':nid,'title':title, 'link':link, 'stars':stars}
            print(data)

        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
        
        
    
        proceed = int(input("\nVideo added succesfully. Continue? 1:Yes 2:No: "))
        if proceed == 1:
            self.addvideos()
        elif proceed != 1:
            cv.loadvideos()
            cv.changekeysname()
                
    
    def removevideos(self):
        cv.listvideos()
        removeid = int(input('\nWhat video you want to remove?: '))
        del data[removeid]

        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
    
        proceed = int(input("\nVideo removed succesfully. Continue? 1:Yes 2:No: "))
        if proceed == 1:
            self.removevideos()
        elif proceed != 1:
            cv.loadvideos()
            cv.changekeysname()
    
    def listvideosandopen(self):
        cv.listvideos(False)
        videopick = 0
        

        defaultbrowser = Config.getboolean('MOZILLA', 'DEFAULT_BROWSER')
        if defaultbrowser == True:
            path = 'C:/Program Files/Mozilla Firefox/firefox.exe %s --incognito'
        elif defaultbrowser == False:
            path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s --incognito'

        while videopick != -1:
            videopick = int(input("Pick a video to open! (Type -1 to cancel): "))
            if videopick != -1:
                webbrowser.get(path).open_new(data[videopick]['link'])
            else:
                print('\n\n\nReturning to main menu...')
                menu()

            
    def changekeysname(self):
        keys = list(data.keys())
        n = 0
        for q in keys:
            data[n] = data[keys[n]]
            data.pop(keys[n])
            n = n + 1
        cv.updatedict()

    
    def updatedict(self):
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
    
        print('[!] Dictionary IDS updateds!')
        menu()

class controlconfig:
    def loadconfig(self,allowPrint=True):
        global Config
        Config = configparser.ConfigParser()
        # Check if there is already a configurtion file
        if os.path.isfile("config.ini"):
            Config.read("config.ini")
            if allowPrint == True:
                print('[!] Config loaded.')
        else:
            cc.createconfig()
            print('[!] Config created.')

    def createconfig(self):
        
        Config = configparser.ConfigParser()
        # lets create that config file for next time...
        cfgfile = open("config.ini",'w')
        # add the settings to the structure of the file, and lets write it out...
        Config.add_section('SETINFO')
        Config.add_section('MOZILLA')
        Config.add_section('CHROME')
        Config.add_section('OTHER')
        Config.set('SETINFO','PASSWORD','')
        Config.set('SETINFO','KEY','')
        Config.set('MOZILLA','EXECUTABLE_LINK', 'C:/Program Files/Mozilla Firefox/firefox.exe')
        Config.set('CHROME','EXECUTABLE_LINK', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe')
        Config.set('MOZILLA','DEFAULT_BROWSER', 'True')
        Config.set('CHROME','DEFAULT_BROWSER', 'False')
        Config.set('OTHER','PRIVATE_BROWSER_MODE', 'True')

        Config.write(cfgfile)
        cfgfile.close()


def settingsmenu():
    cc.loadconfig(allowPrint=False)
    print("\n\n\n1. Change password")
    print("2. Browser settings")
    print("3. Remove all the links")
    print("4. Return to main menu")
    settingsnumber = int(input("Pick: "))
    settingsmenulogic(settingsnumber)

def settingsmenulogic(settingsnumber):
    if settingsnumber == 1:
        cs.changepassword()
    elif settingsnumber == 2:
        browseroptions()
    elif settingsnumber == 3:
        cs.removeallthelinks()
    elif settingsnumber == 4:
        menu()
    else:
        settingsmenu()

def browseroptions():
        #returns True or false
        status = cs.browsermode()

        print('\n\n\n\n\n\n\n\n\n\n\n1. Change default browser | Currently: Chrome' if status[1] else '1. Change default browser | Currently: Firefox')
        print('2. Change private mode | Currently: active' if status[0] else '2. Change private mode | Currently: inactive')
        print('3. Go back')
        Pick = int(input('Choice: ' ))
        if Pick == 1:
            cs.browsermode(browserdefaultchange=True)
        elif Pick == 2:
            cs.browsermode(privatemodechange=True)
        elif pick != 1 or pick != 2:
            settingsmenu()

class controlsettings:
    def createpassword(self):

        try:
            haspassword = Config.get('SETINFO','PASSWORD')
            if haspassword == '':
                password = input('\n\n\n\n\n\n\nCreate password: ')
                repeatpassword = input('Repeat password: ')
                if password == repeatpassword:
                    cfgfile = open("config.ini",'w')

                    Config.set('SETINFO', 'PASSWORD', str(password))

                    Config.write(cfgfile)
                    cfgfile.close()
                    menu()
        
            else:
                thepassword = Config.get('SETINFO','PASSWORD')
                print('\n\n\n\n')
                for p in range(3):
                    inserted = input('[!] Put your password ('+str(p)+'/3): ')
                    if inserted == thepassword:
                        print('\nSESSION STARTED!')
                        print('SESSION STARTED!')
                        menu()
                    else: continue
                print('\n\n\n\nPROGRAM TERMINATED!')
                print('PROGRAM TERMINATED!\n\n\n')
        except:
            print('Reload is required!')
            sys.exit()

    def changepassword(self):
        realactualpassword = Config.get('SETINFO','PASSWORD')
        askactualpassword = input('\n\n\n\n\n\n\nActual password: ')
        if realactualpassword == askactualpassword:
            newpassword = input('Create new password: ')
            repeatnewpassword = input('Repeat new password: ')
            if newpassword == repeatnewpassword:
                cfgfile = open("config.ini",'w')

                Config.set('SETINFO', 'PASSWORD', str(newpassword))

                Config.write(cfgfile)
                cfgfile.close()
                cs.createpassword()
        else:
            print('\n\n\n\nThats not the actual password!')
            print('PROGRAM TERMINATED!\n\n\n')
            sys.exit()

    def browsermode(self,privatemodechange=False,browserdefaultchange=False):
        print('\n\n\n\n\n\n\n\n\n\n\n\n')
        privatemode = Config.getboolean('OTHER', 'PRIVATE_BROWSER_MODE')
        browserdefault = Config.getboolean('CHROME', 'DEFAULT_BROWSER')

        if privatemodechange == False and browserdefaultchange == False:
            return [privatemode, browserdefault]
            
        elif privatemodechange == True:
            cfgfile = open("config.ini",'w')
            if privatemode == True:
                Config.set('OTHER', 'PRIVATE_BROWSER_MODE', 'False')
            elif privatemode == False:
                Config.set('OTHER', 'PRIVATE_BROWSER_MODE', 'True')
            Config.write(cfgfile)
            cfgfile.close()
            print('\n\n\n\n\n\n\n\n')
            browseroptions()
        elif browserdefaultchange == True:
            cfgfile = open("config.ini",'w')

            if browserdefault == True:
                Config.set('MOZILLA','DEFAULT_BROWSER', 'True')
                Config.set('CHROME','DEFAULT_BROWSER', 'False')
                print('[!] Mozilla is your new default browser.')

            elif browserdefault == False:
                Config.set('MOZILLA','DEFAULT_BROWSER', 'False')
                Config.set('CHROME','DEFAULT_BROWSER', 'True')
                print('[!] Chrome is your new default browser.')
            
            Config.write(cfgfile)
            cfgfile.close()
            browseroptions()

    def removeallthelinks(self):
        proceed = str(input("\n\n\n[!] Are you sure? You can not go back. (Type YES or NO): "))

        if proceed in ['yes', 'YES', 'Y', 'y']:
            data = {}
            with open('data.json', 'w') as outfile:
                json.dump(data, outfile)

            cv.loadvideos(dataremoved=True)
            cv.changekeysname()


        if proceed in ['no', 'NO', 'n', 'N']:
            print('[!] You conserved your data')
            menu()

        



cc = controlconfig()
cs = controlsettings()
cv = controlvideos()
cv.loadvideos()
cc.loadconfig()


#cv.changekeysname()

cs.createpassword()
