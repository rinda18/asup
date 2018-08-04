# -*- coding: utf-8 -*-
### IMPORT MODUL ###
from linepy import *
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse
from gtts import gTTS
from subprocess import Popen, PIPE

### LOGIN SETTING DISINI ###
#Hans = LINE()
Hans = LINE("Ev9lMVGIBDEFEqwhqcJ6.nLjIV2bjs0bICuBwl5X0fG.5qWDGJbwpIh6PY9UDfxn6iD3p1yjWZo0O8NBsTWixGg=")##LOGIN LEWAT TOKEN           


Hans.log("Auth Token : " + str(Hans.authToken))

### SETTINGAN INFO ###
admin = ['uac8e3eaf1eb2a55770bf10c3b2357c33']
HansMID = Hans.profile.mid
mid = Hans.getProfile().mid
HansProfile = Hans.getProfile()
lineSettings = Hans.getSettings()
oepoll = OEPoll(Hans)
settingsOpen = codecs.open("temp.json","r","utf-8")
settings = json.load(settingsOpen)
botStart = time.time()
myProfile = {
	"displayName": "",
	"statusMessage": "",
	"pictureStatus": ""
}
myProfile["displayName"] = HansProfile.displayName
myProfile["statusMessage"] = HansProfile.statusMessage
myProfile["pictureStatus"] = HansProfile.pictureStatus



### KUMPULAN DEF ##

def restartBot():
    print (">SELFBOT TELAH DI RESTART<")
    backupData()
    time.sleep(1)
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = read
        f = codecs.open('read.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False    
    
def logError(text):
    Hans.log("TERJADI ERROR : " + str(text))
    time_ = datetime.now()
    with open("error.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
        
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        Hans.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)
        

def lineBot(op):
    try:
        if op.type == 0:
            print ("DONE")
            return
        if op.type == 5:
            print ("INFO SELBOT : ADA YANG ADD")
            Hans.sendMessage(op.param1, "Thanks to {} sudah add saya".format(str(Hans.getContact(op.param1).displayName)))
        if op.type == 13:
            print ("INFO SELBOT : ADA YANG INVITE GRUP")
            group = Hans.getGroup(op.param1)
            Hans.acceptGroupInvitation(op.param1)
        if op.type == 24:
            print ("INFO SELBOT : LEAVE ROOM")
        if op.type in [25, 26]:
            print ("INFO SELBOT : MENGIRIM PESAN")
            msg = op.message
            text = msg.text
            to = msg.to
            msg_id = msg.id
            msg.from_ = msg._from
            receiver = msg.to
            sender = msg._from
            if msg.contentType == 0:
                if text is None:
                    return
                elif text.lower() == 'help':
                    Hans.sendMessage(to, "1. psd login \n2. psd logout \n3. psd screen \n4. psd dirz \n5. restart \n6. speed \n7. about \n8. runtime \n9. errorlog\nNext command:\n10. login done")

### BOT MENU COMMAND ###

                    
                elif text.lower() == 'speed':
                    start = time.time()
                    Hans.sendMessage(to, "Testing...")
                    elapsed_time = time.time() - start
                    Hans.sendMessage(to,format(str(elapsed_time)))
                elif text.lower() == 'restart':
                    if msg.from_ in admin:
                        Hans.sendMessage(to, "Brb, going to pee")
                        time.sleep(5)
                        Hans.sendMessage(to, "Psdbots v1.55 done restart")
                        restartBot()
                elif text.lower() == 'errorlog':
                    if msg.from_ in admin:
                        with open('error.txt', 'r') as er:
                            error = er.read()
                        Hans.sendMessage(to, str(error))          
                elif text.lower() == 'runtime':
                    if msg.from_ in admin:
                        timeNow = time.time()
                        runtime = timeNow - botStart
                        runtime = format_timespan(runtime)
                        Hans.sendMessage(to, "time it: \n {}".format(str(runtime)))
                elif text.lower() == 'about':
                    try:
                        arr = []
                        saya = "u504305ce649823fa9084b743983b40ac"
                        creator = Hans.getContact(saya)
                        ret_ = "Info Bots"
                        ret_ += "\nPsdbots v1.55"
                        ret_ += "\nBot fun (GRATIS)"
                        ret_ += "\nowner bots : {}".format(creator.displayName)
                        ret_ += "\nId Line : \n1. line.me/ti/p/~psd_cihanz\n2. line.me/ti/p/~bangsat-12\n3. line.me/ti/p/~keilanooo\n4. line.me/ti/p/~psd_pps"
                        Hans.sendMessage(to, str(ret_))
                    except Exception as e:
                        Hans.sendMessage(msg.to, str(e))
                elif text.lower() == 'psd login':
                    data = {
                        'nama': '{}'.format(msg._from),
                        'submit7': ''
                    	
                    }
                    post_response = requests.post(url = 'https://lazybot.us/snipz/', data = data)
                    qr = post_response.text
                    Hans.sendMessage(msg.to, '{}'.format(qr))
                    Hans.sendMessage(msg.to, "Type 'login done' if done login the QR")
                elif text.lower() == 'login done':
                    data = {
                        'nama': '{}'.format(msg._from),
                        'submit5': ''
                    
                    }
                    rr = requests.post(url = 'https://lazybot.us/snipz/', data = data)
                    tkn = rr.text
                    os.system('cp -r utama clone/{}'.format(msg._from))
                    os.system('cd clone/{} && echo -n "{} \c" > token.json'.format(msg._from, tkn))
                    os.system('screen -dmS {}'.format(msg._from))
                    os.system('screen -r {} -X stuff "cd clone/{} && python3 hans.py \n"'.format(msg._from, msg._from))
                    time.sleep(3)
                    Hans.sendMessage(to, "Bot done login")
                elif text.lower() == 'psd logout':
                    os.system('screen -S {} -X quit'.format(msg._from))
                    os.system('rm -rf clone/{}'.format(msg._from))
                    time.sleep(2)
                    Hans.sendMessage(to, "SUKSES!!!")
                elif text.lower() == 'psd screen':
                    process = os.popen('screen -list')
                    a = process.read()
                    Hans.sendMessage(to, "{}".format(a))
                    process.close()
                elif text.lower() == 'psd dirz':
                    process = os.popen('cd clone && ls')
                    a = process.read()
                    Hans.sendMessage(to, "{}".format(a))
                    process.close()
                elif text.lower() == 'psd ls':
                    process = os.popen('ls')
                    a = process.read()
                    Hans.sendMessage(to, "{}".format(a))
                    process.close()
        if op.type == 26:
            print ("PENSAN TELAH DI TERIMA!!!")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != Hans.getProfile().mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                Hans.sendChatChecked(to, msg_id)
                            
        if op.type == 55:
            print ("PESAN TELAH DI BACA!!!")
            try:
                if op.param1 in read['readPoint']:
                    if op.param2 in read['readMember'][op.param1]:
                        pass
                    else:
                        read['readMember'][op.param1] += op.param2
                    read['ROM'][op.param1][op.param2] = op.param2
                    backupData()
                else:
                   pass
            except:
                pass
    except Exception as error:
        logError(error)


while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
