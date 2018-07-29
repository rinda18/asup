# -*- coding: utf-8 -*-
### IMPORT MODUL ###
from linepy import *
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse
from gtts import gTTS

### LOGIN SETTING DISINI ###
f = open('token.txt','r')
tkn = f.read()

Hans = LINE("{}".format(tkn))##LOGIN LEWAT TOKEN           
f.close()

Hans.log("Auth Token : " + str(Hans.authToken))

### SETTINGAN INFO ###
HansMID = Hans.profile.mid
HansProfile = Hans.getProfile()
lineSettings = Hans.getSettings()
oepoll = OEPoll(Hans)
readOpen = codecs.open("read.json","r","utf-8")
settingsOpen = codecs.open("temp.json","r","utf-8")
read = json.load(readOpen)
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
    print (">Hans SELFBOT TELAH DI RESTART<")
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
        
def sendMention(to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = "@zeroxyuuki "
    if mids == []:
        raise Exception("Invalid mids")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Invalid mids")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
            arr.append(arrData)
            textx += mention
        textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    Hans.sendMessage(to, textx, {'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)
def lineBot(op):
    try:
        if op.type == 0:
            print ("DONE")
            return
        if op.type == 5:
            print ("INFO SELBOT : ADA YANG ADD")
            if settings["autoAdd"] == True:
                Hans.sendMessage(op.param1, "Psdbots v1.55\nThanks for add {} im here".format(str(Hans.getContact(op.param1).displayName)))
        if op.type == 13:
            print ("INFO SELBOT : ADA YANG INVITE GRUP")
            group = Hans.getGroup(op.param1)
            if settings["autoJoin"] == True:
                Hans.acceptGroupInvitation(op.param1)
        if op.type == 24:
            print ("INFO SELBOT : LEAVE ROOM")
            if settings["autoLeave"] == True:
                Hans.leaveRoom(op.param1)
        if op.type == 25:
            print ("INFO SELBOT : MENGIRIM PESAN")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != Hans.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return

                if text.lower() == 'help':
                    Hans.sendMessage(to, "Psdbots v1.55\n1. my help \n2. setting \n3. help self \n4. help group \n5. help media")
                elif text.lower() == 'my help':
                    Hans.sendMessage(to, "Psdbots v1.55\n1. restart \n2. speed \n3. status \n4. about \n5. runtime \n6. errorlog")
                elif text.lower() == 'setting':
                    Hans.sendMessage(to, "Psdbots v1.55\n1. autoadd(on/off) \n2. autoread(on/off) \n3. autojoin(on/off) \n4. autoleave(on/off) \n5. autochecksticker(on/off) \n6. detectmention(on/off)")
                elif text.lower() == 'help self':
                    Hans.sendMessage(to, "Psdbots v1.55\n1. me \n2. mymid \n3. mypicture \n4. myvideo \n5. mycover \n6. stealcontact(mention) \n7. stealmid(mention) \n8. stealbio(mention) \n9. stealpicture(mention) \n10. stealvideoprofile(mention) \n11. stealcover(mention) \n12. cloneprofile(mention) \n13. restoreprofile \n14. mention")
                elif text.lower() == 'help group':
                    Hans.sendMessage(to, "Psdbots v1.55\n1. gcreator \n2. gpicture \n3. glink \n4. qr(on/off) \n5. glist \n6. gmember \n7. ginfo \n8. crash")
                elif text.lower() == 'help media':
                    Hans.sendMessage(to, "Psdbots v1.55\n1. instagraminfo(username) \n2. instagrampost(username) \n3. youtubes(keyword) \n4. image(keyword) \n5. ssweb(link)")

### BOT MENU COMMAND ###

                    
                elif text.lower() == 'speed':
                    start = time.time()
                    Hans.sendMessage(to, "Testing...")
                    elapsed_time = time.time() - start
                    Hans.sendMessage(to,format(str(elapsed_time)))
                elif text.lower() == 'restart':
                    Hans.sendMessage(to, "Brb, going to pee")
                    time.sleep(5)
                    Hans.sendMessage(to, "Psdbots v1.55 done restart")
                    restartBot()
                elif text.lower() == 'errorlog':
                    with open('error.txt', 'r') as er:
                        error = er.read()
                    Hans.sendMessage(to, str(error))          
                elif text.lower() == 'runtime':
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = format_timespan(runtime)
                    Hans.sendMessage(to, "Time it: \n {}".format(str(runtime)))
                elif text.lower() == 'about':
                    try:
                        arr = []
                        saya = "u504305ce649823fa9084b743983b40ac"
                        creator = Hans.getContact(saya)
                        ret_ = "Info Bots"
                        ret_ += "\nPsdbots v1.55"
                        ret_ += "\nBot fun (GRATIS)"
                        ret_ += "\nowner bots : {}".format(creator.displayName)
                        ret_ += "\nId Line : 1. line.me/ti/p/~psd_cihanz\n2. line.me/ti/p/~bangsat-12\n3. line.me/ti/p/~keilanooo\n4. line.me/ti/p/~psd_pps"
                        Hans.sendMessage(to, str(ret_))
                    except Exception as e:
                        Hans.sendMessage(msg.to, str(e))
                elif text.lower() == 'status':
                    try:
                        ret_ = "Status:"
                        if settings["autoAdd"] == True: ret_ += "\nAutoadd:on"
                        else: ret_ += "\nAutoadd:off"
                        if settings["autoJoin"] == True: ret_ += "\nAutojoin:on"
                        else: ret_ += "\nAutojoin:off"
                        if settings["autoLeave"] == True: ret_ += "\nAutoleave:on"
                        else: ret_ += "\nAutoleave:off"
                        if settings["autoRead"] == True: ret_ += "\nAutoread:on"
                        else: ret_ += "\nAutoread:off"
                        if settings["checkSticker"] == True: ret_ += "\nStickerDetect:on"
                        else: ret_ += "\nStickerDetect:off"
                        if settings["detectMention"] == True: ret_ += "\nMentionDetect:on"
                        else: ret_ += "\nMentionDetect:off"
                        ret_ += " "
                        Hans.sendMessage(to, str(ret_))
                    except Exception as e:
                        Hans.sendMessage(msg.to, str(e))
                elif text.lower() == 'autoadd on':
                    settings["autoAdd"] = True
                    Hans.sendMessage(to, "<on>")
                elif text.lower() == 'autoadd off':
                    settings["autoAdd"] = False
                    Hans.sendMessage(to, "<off>")
                elif text.lower() == 'autojoin on':
                    settings["autoJoin"] = True
                    Hans.sendMessage(to, "<on>")
                elif text.lower() == 'autojoin off':
                    settings["autoJoin"] = False
                    Hans.sendMessage(to, "<off>")
                elif text.lower() == 'autoleave on':
                    settings["autoLeave"] = True
                    Hans.sendMessage(to, "<on>")
                elif text.lower() == 'autojoin off':
                    settings["autoLeave"] = False
                    Hans.sendMessage(to, "<off>")
                elif text.lower() == 'autoread on':
                    settings["autoRead"] = True
                    Hans.sendMessage(to, "<on>")
                elif text.lower() == 'autoread off':
                    settings["autoRead"] = False
                    Hans.sendMessage(to, "<off>")
                elif text.lower() == 'autochecksticker on':
                    settings["checkSticker"] = True
                    Hans.sendMessage(to, "<on>")
                elif text.lower() == 'autochecksticker off':
                    settings["checkSticker"] = False
                    Hans.sendMessage(to, "<off>")
                elif text.lower() == 'detectmention on':
                    settings["datectMention"] = True
                    Hans.sendMessage(to, "<on>")
                elif text.lower() == 'detectmention off':
                    settings["datectMention"] = False
                    Hans.sendMessage(to, "<off>")
                elif text.lower() == 'clonecontact':
                    settings["copy"] = True
                    Hans.sendMessage(to, "Send contact please")
                    
### SELFBOT COMMAND ###
                    
                elif text.lower() == 'me':
                    sendMessageWithMention(to, HansMID)
                    Hans.sendContact(to, HansMID)
                elif text.lower() == 'mymid':
                    Hans.sendMessage(msg.to,"Mid: " +  HansMID)
                elif text.lower() == 'mypicture':
                    me = Hans.getContact(HansMID)
                    Hans.sendImageWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus)
                elif text.lower() == 'myvideo':
                    me = Hans.getContact(HansMID)
                    Hans.sendVideoWithURL(msg.to,"http://dl.profile.line-cdn.net/" + me.pictureStatus + "/vp")
                elif text.lower() == 'mycover':
                    me = Hans.getContact(HansMID)
                    cover = Hans.getProfileCoverURL(HansMID)    
                    Hans.sendImageWithURL(msg.to, cover)
                elif msg.text.lower().startswith("stealcontact "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = Hans.getContact(ls)
                            mi_d = contact.mid
                            Hans.sendContact(msg.to, mi_d)
                elif msg.text.lower().startswith("stealmid "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = "MID : "
                        for ls in lists:
                            ret_ += "\n{}" + ls
                        Hans.sendMessage(msg.to, str(ret_))
                elif msg.text.lower().startswith("stealname "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = Hans.getContact(ls)
                            Hans.sendMessage(msg.to, "NAME : \n" + contact.displayName)
                elif msg.text.lower().startswith("stealbio "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            contact = Hans.getContact(ls)
                            Hans.sendMessage(msg.to, "INFO BIO : \n{}" + contact.statusMessage)
                elif msg.text.lower().startswith("stealpicture "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line.naver.jp/" + Hans.getContact(ls).pictureStatus
                            Hans.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("stealvideoprofile "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        for ls in lists:
                            path = "http://dl.profile.line.naver.jp/" + Hans.getContact(ls).pictureStatus + "/vp"
                            Hans.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("stealcover "):
                    if line != None:
                        if 'MENTION' in msg.contentMetadata.keys()!= None:
                            names = re.findall(r'@(\w+)', text)
                            mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                            mentionees = mention['MENTIONEES']
                            lists = []
                            for mention in mentionees:
                                if mention["M"] not in lists:
                                    lists.append(mention["M"])
                            for ls in lists:
                                path = Hans.getProfileCoverURL(ls)
                                Hans.sendImageWithURL(msg.to, str(path))
                elif msg.text.lower().startswith("cloneprofile "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        for mention in mentionees:
                            contact = mention["M"]
                            break
                        try:
                            Hans.cloneContactProfile(contact)
                            Hans.sendMessage(msg.to, "Done clone contact")
                        except:
                            Hans.sendMessage(msg.to, "Failed")
                            
                elif text.lower() == 'restoreprofile':
                    try:
                        HansProfile.displayName = str(myProfile["displayName"])
                        HansProfile.statusMessage = str(myProfile["statusMessage"])
                        HansProfile.pictureStatus = str(myProfile["pictureStatus"])
                        Hans.updateProfileAttribute(8, HansProfile.pictureStatus)
                        Hans.updateProfile(HansProfile)
                        Hans.sendMessage(msg.to, "Profile backsr")
                    except:
                        Hans.sendMessage(msg.to, "Failed")
                        
#=======### COMMAND GRUP ###

                elif text.lower() == 'crash':
                    Hans.sendContact(to, "ub621484bd88d2486744123db00551d5e',")
                elif text.lower() == 'gcreator':
                    group = Hans.getGroup(to)
                    GS = group.creator.mid
                    Hans.sendContact(to, GS)
                elif text.lower() == 'gpicture':
                    group = Hans.getGroup(to)
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    Hans.sendImageWithURL(to, path)
                elif text.lower() == 'glink':
                    if msg.toType == 2:
                        group = Hans.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            link = Hans.reissueGroupTicket(to)
                            Hans.sendMessage(to, "Link:\nhttps://line.me/R/ti/g/{}".format(str(link)))
                        else:
                            Hans.sendMessage(to, "Please qr open in groups")
                elif text.lower() == 'qr on':
                    if msg.toType == 2:
                        group = Hans.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            Hans.sendMessage(to, "Link open")
                        else:
                            group.preventedJoinByTicket = False
                            Hans.updateGroup(group)
                            Hans.sendMessage(to, "Group qr open")
                elif text.lower() == 'qr off':
                    if msg.toType == 2:
                        group = Hans.getGroup(to)
                        if group.preventedJoinByTicket == True:
                            Hans.sendMessage(to, "Link close")
                        else:
                            group.preventedJoinByTicket = True
                            Hans.updateGroup(group)
                            Hans.sendMessage(to, "Group qr close")
                elif text.lower() == 'ginfo':
                    group = Hans.getGroup(to)
                    try:
                        gCreator = group.creator.displayName
                    except:
                        gCreator = "No makers"
                    if group.preventedJoinByTicket == True:
                        gQr = "Close"
                        gTicket = "Tidak ada"
                    else:
                        gQr = "Open"
                        gTicket = "https://line.me/R/ti/g/{}".format(str(Hans.reissueglink(group.id)))
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    ret_ = "Info Group: "
                    ret_ += "\n1. NAMA GRUP : {}".format(str(group.name))
                    ret_ += "\n2. CREATOR GRUP : {}".format(str(gCreator))
                    ret_ += "\n3. JUMBLAH MEMBER : {}".format(str(len(group.members)))
                    ret_ += "\n4. GRUP QR : {}".format(gQr)
                    ret_ += "\n5. LINK JOIN : {}".format(gTicket)
                    Hans.sendMessage(to, str(ret_))
                    Hans.sendImageWithURL(to, path)
                elif text.lower() == 'gmember':
                    if msg.toType == 2:
                        group = Hans.getGroup(to)
                        ret_ = "List anggota"
                        no = 0 + 1
                        for mem in group.members:
                            ret_ += "\n{}. {}".format(str(no), str(mem.displayName))
                            no += 1
                        ret_ += "\nTotal:\n{}".format(str(len(group.members)))
                        Hans.sendMessage(to, str(ret_))
                elif text.lower() == 'glist':
                        groups = Hans.groups
                        ret_ = "List Group"
                        no = 0 + 1
                        for gid in groups:
                            group = Hans.getGroup(gid)
                            ret_ += "\n{}. {} | {}".format(str(no), str(group.name), str(len(group.members)))
                            no += 1
                        ret_ += "\nTotal: \n{}".format(str(len(groups)))
                        Hans.sendMessage(to, str(ret_))
                        
                elif text.lower() == 'mention':
                    group = Hans.getGroup(msg.to)
                    nama = [contact.mid for contact in group.members]
                    k = len(nama)//100
                    for a in range(k+1):
                        txt = u''
                        s=0
                        b=[]
                        for i in group.members[a*100 : (a+1)*100]:
                            b.append({"S":str(s), "E" :str(s+6), "M":i.mid})
                            s += 7
                            txt += u'@Alin \n'
                        Hans.sendMessage(to, text=txt, contentMetadata={u'MENTION': json.dumps({'MENTIONEES':b})}, contentType=0)
                        Hans.sendMessage(to, "Total {} Mention".format(str(len(nama))))          

###ELIF COMMAND###
                        
                elif text.lower() == 'kalender':
                    tz = pytz.timezone("Asia/Jakarta")
                    timeNow = datetime.now(tz=tz)
                    day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                    hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                    bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                    hr = timeNow.strftime("%A")
                    bln = timeNow.strftime("%m")
                    for i in range(len(day)):
                        if hr == day[i]: hasil = hari[i]
                    for k in range(0, len(bulan)):
                        if bln == str(k): bln = bulan[k-1]
                    readTime = hasil + ", " + timeNow.strftime('%d') + " - " + bln + " - " + timeNow.strftime('%Y') + "\nJam : [ " + timeNow.strftime('%H:%M:%S') + " ]"
                    Hans.sendMessage(msg.to, readTime)                 
                elif "ssweb" in msg.text.lower():
                    sep = text.split(" ")
                    query = text.replace(sep[0] + " ","")
                    with requests.session() as web:
                        r = web.get("http://rahandiapi.herokuapp.com/sswebAPI?key=betakey&link={}".format(urllib.parse.quote(query)))
                        data = r.text
                        data = json.loads(data)
                        Hans.sendImageWithURL(to, data["result"])
                elif "instagraminfo" in msg.text.lower():
                    sep = text.split(" ")
                    search = text.replace(sep[0] + " ","")
                    with requests.session() as web:
                        web.headers["User-Agent"] = random.choice(settings["userAgent"])
                        r = web.get("https://www.instagram.com/{}/?__a=1".format(search))
                        try:
                            data = json.loads(r.text)
                            ret_ = ("Instagram Info <{}> ".format(search))
                            ret_ += "\n1. PROFIL : {}".format(str(data["user"]["full_name"]))
                            ret_ += "\n2. USERNAME : {}".format(str(data["user"]["username"]))
                            ret_ += "\n3. STATUS BIO : {}".format(str(data["user"]["biography"]))
                            ret_ += "\n4. FOLLOWERS : {}".format(format_number(data["user"]["followed_by"]["count"]))
                            ret_ += "\n5. FOLLOWING : {}".format(format_number(data["user"]["follows"]["count"]))
                            if data["user"]["is_verified"] == True:
                                ret_ += "\nSTATUS VERIFIED : VERIFIED"
                            else:
                                ret_ += "\nSTATUS VERIFIED : NOT VERIFIED"
                            if data["user"]["is_private"] == True:
                                ret_ += "\nSTATUS PRIVATE : PRIVATE"
                            else:
                                ret_ += "\nSTATUS PRIVATE : NOT PRIVATE"
                            ret_ += "\nTOTAL POST : {}".format(format_number(data["user"]["media"]["count"]))
                            ret_ += "\nLINK : https://www.instagram.com/{} ]".format(search)
                            path = data["user"]["profile_pic_url_hd"]
                            Hans.sendImageWithURL(to, str(path))
                            Hans.sendMessage(to, str(ret_))
                        except:
                            Hans.sendMessage(to, "INSTAGRAM TIDAK DI TEMUKAN")
                elif "instagrampost" in msg.text.lower():
                    separate = msg.text.split(" ")
                    user = msg.text.replace(separate[0] + " ","")
                    profile = "https://www.instagram.com/" + user
                    with requests.session() as x:
                        x.headers['user-agent'] = 'Mozilla/5.0'
                        end_cursor = ''
                        for count in range(1, 999):
                            print('PAGE: ', count)
                            r = x.get(profile, params={'max_id': end_cursor})
                        
                            data = re.search(r'window._sharedData = (\{.+?});</script>', r.text).group(1)
                            j    = json.loads(data)
                        
                            for node in j['entry_data']['ProfilePage'][0]['user']['media']['nodes']: 
                                if node['is_video']:
                                    page = 'https://www.instagram.com/p/' + node['code']
                                    r = x.get(page)
                                    url = re.search(r'"video_url": "([^"]+)"', r.text).group(1)
                                    print(url)
                                    Hans.sendVideoWithURL(msg.to,url)
                                else:
                                    print (node['display_src'])
                                    Hans.sendImageWithURL(msg.to,node['display_src'])
                            end_cursor = re.search(r'"end_cursor": "([^"]+)"', r.text).group(1)
                elif "image" in msg.text.lower():
                    separate = msg.text.split(" ")
                    search = msg.text.replace(separate[0] + " ","")
                    with requests.session() as web:
                        web.headers["User-Agent"] = random.choice(settings["userAgent"])
                        r = web.get("http://rahandiapi.herokuapp.com/imageapi?key=betakey&q={}".format(urllib.parse.quote(search)))
                        data = r.text
                        data = json.loads(data)
                        if data["result"] != []:
                            items = data["result"]
                            path = random.choice(items)
                            a = items.index(path)
                            b = len(items)
                            Hans.sendImageWithURL(to, str(path))
                elif "youtubes" in msg.text.lower():
                    sep = text.split(" ")
                    search = text.replace(sep[0] + " ","")
                    params = {"search_query": search}
                    with requests.session() as web:
                        web.headers["User-Agent"] = random.choice(settings["userAgent"])
                        r = web.get("https://www.youtube.com/results", params = params)
                        soup = BeautifulSoup(r.content, "html5lib")
                        ret_ = "List Youtube"
                        datas = []
                        for data in soup.select(".yt-lockup-title > a[title]"):
                            if "&lists" not in data["href"]:
                                datas.append(data)
                        for data in datas:
                            ret_ += "\nJUDUL : {} ".format(str(data["title"]))
                            ret_ += "\nLINK : https://www.youtube.com{}".format(str(data["href"]))
                        Hans.sendMessage(to, str(ret_))
            elif msg.contentType == 7:
                if settings["autochecksticker"] == True:
                    stk_id = msg.contentMetadata['STKID']
                    stk_ver = msg.contentMetadata['STKVER']
                    pkg_id = msg.contentMetadata['STKPKGID']
                    ret_ = "Info sticker: "
                    ret_ += "\nID STICKER : {}".format(stk_id)
                    ret_ += "\nLINK STICKER : line://shop/detail/{}".format(pkg_id)
                    ret_ += "\nPsdbots v1.55"
                    Hans.sendMessage(to, str(ret_))
                    
            elif msg.contentType == 13:
                if settings["copy"] == True:
                    _name = msg.contentMetadata["displayName"]
                    copy = msg.contentMetadata["mid"]
                    groups = Hans.getGroup(msg.to)
                    targets = []
                    for s in groups.members:
                        if _name in s.displayName:
                            print ("[Target] Copy")
                            break                             
                        else:
                            targets.append(copy)
                    if targets == []:
                        Hans.sendText(msg.to, "Target, not found")
                        pass
                    else:
                        for target in targets:
                            try:
                                Hans.cloneContactProfile(target)
                                Hans.sendMessage(msg.to, "Done copy contact")
                                settings['copy'] = False
                                break
                            except:
                                     msg.contentMetadata = {'mid': target}
                                     settings["copy"] = False
                                     break                     
                    
                    


        if op.type == 26:
            print ("PENSAN TELAH DI TERIMA!!!")
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != Hans.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
                if settings["autoRead"] == True:
                    Hans.sendChatChecked(to, msg_id)
                if to in read["readPoint"]:
                    if sender not in read["ROM"][to]:
                        read["ROM"][to][sender] = True
                if sender in settings["mimic"]["target"] and settings["mimic"]["status"] == True and settings["mimic"]["target"][sender] == True:
                    text = msg.text
                    if text is not None:
                        Hans.sendMessage(msg.to,text)
                if msg.contentType == 0 and sender not in HansMID and msg.toType == 2:
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if HansMID in mention["M"]:
                                if settings["detectMention"] == True:
                                    contact = Hans.getContact(sender)
                                    Hans.sendMessage(to, "sundala nu")
                                    sendMessageWithMention(to, contact.mid)
                                break

                            
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
