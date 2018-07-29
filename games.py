# -*- coding: utf-8 -*-
from linepy import *
from datetime import datetime
#from kbbi import KBBI
#from Aditya.thrift.protocol import TCompactProtocol
#from Aditya.thrift.transport import THttpClient
#from Aditya.ttypes import LoginRequest
import json, requests, LineService,os,sys,subprocess,traceback,os.path,time,humanize

with open('user.json', 'r') as fp:
    wait = json.load(fp)
ditdit = LineClient(authToken='Ev7NsZpbtAStY3iwZXT3.m7QAK9mmg/fv3Yt11op1GW.ndlfVGqRprpqG64XDjtVS8Go/7Xa+eWUzobUAWvthyk=')
poll = LinePoll(ditdit)

datagame = {
    'P':{},
    'W': {},
    'R': {},
    'RR': 0
}
def headers():
    Headers = {
    'User-Agent': "Line/2.1.5",
    'X-Line-Application': "DESKTOPWIN\t2.1.5\tPUY\tPUY\10.13.2",
    "x-lal": "ja-US_US",
    }
    return Headers
def waktu(secs):
    mins, secs = divmod(secs,60)
    hours, mins = divmod(mins,60)
    days, hours = divmod(hours, 24)
    return '%02d Hari %02d Jam %02d Menit %02d Detik' % (days, hours, mins, secs)
def RECEIVE_MESSAGE(op):
    msg = op.message
    text1 = msg.text
    dits = text1
    if msg.contentType == 0:
        if dits is None:
            return
        else:
            if dits.lower() == 'respon':
                if msg._from in wait['info'] or msg._from in ['u8cae982abc647f463d9d1baae6138d57','u911a53f18a83a7efed7f96474a0d1c75']:
                    ditdit.sendMessage(msg.to,'Hi!')
            if dits.lower() == 'anbot help':ditdit.sendMessage(msg.to,' 「 ANBOT 」\n | Owner |\naddsb name @\ndelsb name @\n\n | Serivce |\nanbot login\n\n | GAME |\nanbot start\nanbot join\nanbot score')
            if dits.lower() == 'anbot reset':
                if msg.to not in datagame['P']:
                    return
                datagame['P'][msg.to] = {}
                ditdit.sendMention(msg.to,' 「 ANBOT 」\n@!Telah mereset room {} di grup ini'.format(datagame['R'][msg.to]['N']),'',[msg._from])
                datagame['R'][msg.to] = {}
            if dits.lower() == 'anbot join':
                if datagame['R'][msg.to]['S'] == False:
                    return ditdit.sendMention(msg.to,' 「 ANBOT 」\nHy @!Room {} Telah berlangsung pada digrup ini silahkan tunggu game selesai'.format(datagame['R'][msg.to]['N']),'',[msg._from])
                if msg._from not in datagame['P'][msg.to]:
                    datagame['P'][msg.to][msg._from] = {'H':10,'S':0}
                    ditdit.sendMention(msg.to,' 「 ANBOT 」\n@!Berhasil join di room {}'.format(datagame['R'][msg.to]['N']),'',[msg._from])
                else:ditdit.sendMention(msg.to,' 「 ANBOT 」\n@!Anda telah join di room {}'.format(datagame['R'][msg.to]['N']),'',[msg._from])
            if dits.lower() == 'anbot start':
                if msg.to in datagame['P']:
                    return
                datagame['P'][msg.to] = {}
                datagame['W'][msg.to] = time.time()
                datagame['R'][msg.to] = {'N':datagame['RR']+1,'S':True}
                datagame['RR']+= 1
                if msg._from not in datagame['P'][msg.to]:
                    datagame['P'][msg.to][msg._from] = {'H':10,'S':0}
                    ditdit.sendMention(msg.to,' 「 ANBOT 」\nRoom {} Telah dibuat oleh @!Silahkan ketik anbot login untuk join game akan dimulai setelah 60 detik kedepan'.format(datagame['R'][msg.to]['N']),'',[msg._from])
            if dits.lower().startswith('addme ') or dits.lower() == 'addme':
                if msg._from in ['u8cae982abc647f463d9d1baae6138d57','u911a53f18a83a7efed7f96474a0d1c75']:
                    if msg._from not in wait['info']:
                        pay = time.time()
                        nama = str(dits.split(' ')[1])
                        wait['name'][nama] =  {"mid":key1,"pay":pay+60*60*24*30,"runtime":pay,"token":{}}
                        wait['info'][key1] =  '%s' % nama
                        ditdit.sendMention(msg.to, ' 「 Serivce 」\n@! Add to Service','', [msg._from])
                    else:
                        if dits.lower() == 'addme':
                            wait['name'][wait['info'][msg._from]]['pay'] = wait['name'][wait['info'][msg._from]]['pay']+60*60*24*30;time.sleep(4)
                            os.system('screen -S %s -X kill'%wait['info'][msg._from])
                            os.system('screen -S %s -dm python3 %s.py kill'%(wait['info'][msg._from],wait['info'][msg._from]))
                            ditdit.sendMention(msg.to, ' 「 Serivce 」\nHey @! your expired selfbot now {}'.format(humanize.naturaltime(datetime.fromtimestamp(wait['name'][wait['info'][msg._from]]["pay"]))),'', [msg._from])
            if dits.lower().startswith('addsb ') and msg._from in ['u8cae982abc647f463d9d1baae6138d57','u911a53f18a83a7efed7f96474a0d1c75']:        
                if 'MENTION' in msg.contentMetadata.keys()!= None:
                    key = eval(msg.contentMetadata["MENTION"])
                    key1 = key["MENTIONEES"][0]["M"]
                    if key1 not in wait['info']:
                        pay = time.time()
                        nama = str(dits.split(' ')[1])
                        wait['name'][nama] =  {"mid":key1,"pay":pay+60*60*24*30,"runtime":pay,"token":{}}
                        wait['info'][key1] =  '%s' % nama
                        ditdit.sendMention(msg.to, ' 「 Serivce 」\n@! Add to Service','', [key1])
                    else:ditdit.sendMention(msg.to, ' 「 Serivce 」\n@! Already in Service','', [key1])
            if dits.lower().startswith('delsb ') and msg._from in ['u8cae982abc647f463d9d1baae6138d57','u911a53f18a83a7efed7f96474a0d1c75']:        
                if 'MENTION' in msg.contentMetadata.keys()!= None:
                    key = eval(msg.contentMetadata["MENTION"])
                    key1 = key["MENTIONEES"][0]["M"]
                    if key1 in wait['info']:
                        b = wait['info'][key1]
                        os.system('screen -S %s -X kill'%b)
                        h =  wait['name'][b]
                        try:subprocess.getoutput('rm {}.py protect/{}.json'.format(b,b))
                        except:pass
                        del wait['info'][key1]
                        del wait['name'][b]
                        ditdit.sendMention(msg.to, ' 「 Serivce 」\n@! Del from Service','', [key1])
                    else:
                        ditdit.sendMention(msg.to, ' 「 Serivce 」\n@! not in Service','', [key1])
            if dits.lower().startswith("bot name1") and msg._from in ['u8cae982abc647f463d9d1baae6138d57','u911a53f18a83a7efed7f96474a0d1c75']:ditdit.setname(msg.to,msg)
            if dits.lower() == 'list1':
                if msg._from in ['u8cae982abc647f463d9d1baae6138d57','u911a53f18a83a7efed7f96474a0d1c75']:
                    h = [a for a in wait['info']]
                    k = len(h)//100
                    for aa in range(k+1):
                        msgas = '╭「 List Login 」─'
                        no=0
                        for a in h:
                            no+=1
                            if wait['name'][wait['info'][a]]["pay"] <= time.time():sd = 'Expired'
                            else:sd = humanize.naturaltime(datetime.fromtimestamp(wait['name'][wait['info'][a]]["pay"]))
                            if no == len(h):msgas+='\n╰{}. @! {}'.format(no,sd)
                            else:msgas += '\n│{}. @! {}'.format(no,sd)
                        ditdit.sendMention(msg.to, msgas,'', h)
            if dits.lower() == 'runall':
                if msg._from in ['u8cae982abc647f463d9d1baae6138d57','u911a53f18a83a7efed7f96474a0d1c75']:
                    h = ''
                    no=0
                    for a in wait['info']:
                        us = wait["info"][a]
                        if wait['name'][us]["token"] != '':
                            try:
                                os.system('screen -S %s -X kill'%us)
                                os.system('screen -S %s -dm python3 %s.py kill'%(us,us))
                            except:pass
                    ditdit.sendMessage(msg.to,'Done Run All Customer')
            if dits.lower() == 'killall':
                if msg._from in ['u8cae982abc647f463d9d1baae6138d57','u911a53f18a83a7efed7f96474a0d1c75']:
                    h = ''
                    no=0
                    for a in wait['info']:
                        us = wait["info"][a]
                        if wait['name'][us]["token"] != '':
                            try:
                                os.system('screen -S %s -X kill'%us)
                            except:pass
                    ditdit.sendMessage(msg.to,'Done Kill All Customer')
            if dits.lower() == "restart" and msg._from in ['u8cae982abc647f463d9d1baae6138d57','u911a53f18a83a7efed7f96474a0d1c75']:ditdit.sendMessage(msg.to, " 「 Restarting 」\nType: Restart Program\nRestarting...");ditdit.restart_program()
            if dits.lower() == 'anbot login':
                if msg._from in wait['info'] or msg._from in ['u8cae982abc647f463d9d1baae6138d57','u911a53f18a83a7efed7f96474a0d1c75']:
                    try:del wait["limit"][msg._from]
                    except:pass
                    if msg._from not in wait["limit"]:
                        us = wait["info"][msg._from]
                        ti = wait['name'][us]["pay"]-time.time()
                        sec = int(ti %60)
                        minu = int(ti/60%60)
                        hours = int(ti/60/60 %24)
                        days = int(ti/60/60/24)
                        wait['name'][us]["pay"] = wait['name'][us]["pay"]
                        hasil = " 「 Login 」\nUser: @!\nFile: {}\nExpired: {} Hari {} Jam {} Menit\n\nANBOT SELFBOT EDITION~".format(us,days,hours,minu)
                        if wait["name"][us]["pay"] <= time.time():
                            ditdit.sendMention(msg._from, ' 「 Expired 」\n Sorry @! Aditya Ur Account Hasbeen Expired','', [msg._from])
                        else:
                                us = wait["info"][msg._from]
                                wait["limit"][msg._from] =  '%s' % us
                                wait['name'][us]["tempat"] = msg.to
                                try:
                                    a = headers()
                                    a.update({'x-lpqs' : '/api/v4/TalkService.do'})
                                    transport = THttpClient.THttpClient('https://gd2.line.naver.jp/api/v4/TalkService.do')
                                    transport.setCustomHeaders(a)
                                    protocol = TCompactProtocol.TCompactProtocol(transport)
                                    client = LineService.Client(protocol)
                                    qr = client.getAuthQrcode(keepLoggedIn=1, systemName='ANBOT SelfBot')
                                    link = "line://au/q/" + qr.verifier
                                    if msg.toType == 2:ditdit.sendMention(msg.to, ' 「 Login 」\nCek Your PM @!','', [msg._from])
                                    else:pass
                                    ditdit.sendMention(msg._from, ' 「 Login 」\n@! Click Only 2 Minute\n{}'.format(link),'', [msg._from])
                                    a.update({"x-lpqs" : '/api/v4/TalkService.do', 'X-Line-Access': qr.verifier})
                                    json.loads(requests.session().get('https://gd2.line.naver.jp/Q', headers=a).text)
                                    a.update({'x-lpqs' : '/api/v4p/rs'})
                                    transport = THttpClient.THttpClient('https://gd2.line.naver.jp/api/v4p/rs')
                                    transport.setCustomHeaders(a)
                                    protocol = TCompactProtocol.TCompactProtocol(transport)
                                    client = LineService.Client(protocol)
                                    req = LoginRequest()
                                    req.type = 1
                                    req.verifier = qr.verifier
                                    req.e2eeVersion = 1
                                    res = client.loginZ(req)
                                    try:
                                        wait['name'][us]["token"] = res.authToken
                                        cpfile(us,wait['name'][us]["token"])
                                        if msg.toType == 2:ditdit.sendMention(msg.to, hasil,'', [msg._from])
                                        else:ditdit.sendMention(msg._from, hasil,'', [msg._from])
                                        os.system('screen -S %s -X kill'%us)
                                        os.system('screen -S %s -dm python3 %s.py kill'%(us,us))
                                    except:
                                        if msg.toType == 2:ditdit.sendMention(msg.to, ' 「 Error 」\nSilahkan cek perangkat and @!,\nJika tidak ditemukan silahkan login ulang setelah 24 jam \n Atau hubungi admin kami','', [msg._from])
                                        else:ditdit.sendMention(msg._from, ' 「 Error 」\nSilahkan cek perangkat and @!,\nJika tidak ditemukan silahkan login ulang setelah 24 jam \n Atau hubungi admin kami','', [msg._from])
                                    del wait["limit"][msg._from]
                                except:
                                    del wait["limit"][msg._from]
                                    try:to = msg.to
                                    except:to=msg._from
                                    ditdit.sendMessage(to, ' 「 Login 」\nStatus: Expired')
                    else:ditdit.sendMention(msg.to," 「 404 」\nuser @! dalam sesi login\nJika ditemukan trouble silahkan kontak admin kami.",'', [msg._from])
poll.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE
})
def NOTIFIED_INVITE_INTO_GROUP(op):
    if ditdit.getProfile().mid in op.param3:ditdit.acceptGroupInvitation(op.param1)
poll.addOpInterruptWithDict({
    OpType.NOTIFIED_INVITE_INTO_GROUP: NOTIFIED_INVITE_INTO_GROUP
})
def cpfile(t,tt):
    a = open('text.txt','r').read()
    b = open('{}.py'.format(t),'w').write('{}'.format(a.replace('sasuke','"{}"'.format(tt)).replace('sarada',t)))
    return b
def start():
    while True:
        poll.trace()
        ditdit.backupjson_1('user.json',wait)
if __name__ == '__main__':
    start()
