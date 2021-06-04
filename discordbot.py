from discord.ext import commands
import os
import traceback
import datetime
import locale
import time
import threading
import gspread
import re

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 

#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('clanbattle-315409-50ad6095d3dd.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '1_eL4J3wk3ZBa7A48dkC4eP_s9eyncJe388iNDaG-u7I'

#共有設定したスプレッドシートのシート1を開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
#worksheet2 = gc.open_by_key(SPREADSHEET_KEY).sheet2



botname = "希留耶#" + str(2087)

kakikomi_ID = 846292473973309470
totusinkou_ID = 846292541015851038
shukei_ID = 846292511873171486
owari_ID = 846292621167951892
kibou_ID = 846292619683561493
totuchu_ID = 848836850726207488
guild_ID = 736128219501166594

channel_kakikomi = 0
channel_sinkou = 0
channel_shukei = 0
channel_owari = 0
channel_kibou = 0
channel_totuchu = 0

totulist = {}   #メンバーリスト　discordID:残り凸数
membername = {}
toturesultmsg = {}  #凸中の状況保存（ダメージなど）
shukei = 0
owari = 0
totuchu = 0

guild = 0
chosamsg = 0

bossname = {1:"ワイバーン", 2:"ランドスロース", 3:"オークチーフ", 4:"スピリットホーン", 5:"ツインピッグス"}
bosshp = { 11:6000000, 12:8000000, 13:10000000, 14:12000000, 15:15000000, 21:6000000, 22:8000000, 23:10000000, 24:12000000, 25:15000000, 31:10000000, 32:11000000, 33:16000000, 34:18000000, 35:22000000, 41:18000000, 42:19000000, 43:22000000, 44:23000000, 45:26000000, 51:85000000, 52:90000000, 53:95000000, 54:100000000, 55:110000000}
boss = 10
boss1 = [1]     #1：ボス番号、2：周目、3：残りhp
boss2 = [2]
boss3 = [3]
boss4 = [4]
boss5 = [5]


clanrole = '<Role id=846560521767223306 name=\'クラバト\'>'
sinkorole = '<Role id=850032890259177545 name=\'進行\'>'
tasukiruid = 850044161565655090
clanroleid = 846560521767223306

totu0 = ['\n\n---完凸---\n'] #数字は残り凸数
totu1 = ['\n\n---1凸残り---\n']
totu2 = ['\n---2凸残り---\n']
totu3 = ['\n---3凸残り---\n']

genzai = '現在の状況'
kakoi = '```'
totuing = '現在の各ボスへの凸状況\n'
chu1 = ['\n\n--- 1boss  ']
chu2 = ['\n\n--- 2boss  ']
chu3 = ['\n\n--- 3boss  ']
chu4 = ['\n\n--- 4boss  ']
chu5 = ['\n\n--- 5boss  ']

kibo1 = ['\n--- 1boss---\n']
kibo2 = ['\n--- 2boss---\n']
kibo3 = ['\n--- 3boss---\n']
kibo4 = ['\n--- 4boss---\n']
kibo5 = ['\n--- 5boss---\n']

emoji1 = '1⃣'
emoji2 = '2⃣'
emoji3 = '3⃣'
emoji4 = '4⃣'
emoji5 = '5⃣'


dataframe = {1:"a",2:"b",3:"c",4:"d",5:"e",6:"f",7:"",8:"h",9:"i",10:"j",11:"k",12:"l",13:"m",14:"n",15:"o",16:"p",17:"q",18:"r",19:"s",20:"t"}


#@bot.command()




async def start():
    global channel_kakikomi
    global channel_sinkou
    global channel_shukei
    global channel_owari
    global channel_kibou
    global channel_totuchu
    global guild
    channel_kakikomi = client.get_channel(kakikomi_ID)
    channel_sinkou = client.get_channel(totusinkou_ID)
    channel_shukei = client.get_channel(shukei_ID)
    channel_owari = client.get_channel(owari_ID)
    channel_kibou = client.get_channel(kibou_ID)
    channel_totuchu = client.get_channel(totuchu_ID)
    guild = client.get_guild(guild_ID)
    global shukei
    shukei = await channel_shukei.send(genzai)
    global totuchu
    totuchu = await channel_totuchu.send(totuing)
    await owajokyo(0)
    await bossreset()
    await gssload()
    return

async def bossreset():
    boss1.append(1)
    boss1.append(bosshp[11])
    boss2.append(1)
    boss2.append(bosshp[12])
    boss3.append(1)
    boss3.append(bosshp[13])
    boss4.append(1)
    boss4.append(bosshp[14])
    boss5.append(1)
    boss5.append(bosshp[15])


async def allreset():
    users = [member for member in client.get_all_members()]
    cellnum = 2
    for user in users:
        userrole = str(user.roles)
        if clanrole in userrole:
            global totulist
            totulist[str(user)] = 3
            worksheet.update_cell(cellnum,1, str(user))
            worksheet.update_cell(cellnum,2, str(user.display_name))
            worksheet.update_cell(cellnum,3, 3)
            cellnum += 1

    await start()
    await jokyo()
    return

async def gssload():
    global totulist
    allmemberlist = worksheet.get_all_records(empty2zero=False, head=1, default_blank="")
    namelist = [d.get("id") for d in allmemberlist]
    jokyolist = ([d.get("残り凸数") for d in allmemberlist])
    dnamelist = [d.get("名前") for d in allmemberlist]
    for n in range(30):
        totulist[str(namelist[n])] = float(jokyolist[n])
        membername[str(namelist[n])] = str(dnamelist[n])

    dt_now=datetime.datetime.now()
                
    for k, v in totulist.items():
        if v == 0:
            global totu0
            totu0.append((dt_now.strftime('%H:%M ')) + membername[k])
        elif v == 1.0:
            totu1.append (k)
        elif v == 2.0:
            totu2.append (k)
        elif v == 3.0:
            totu3.append (k)
        elif v == 0.5:
            totu1.append (k +"（持ち越し中）")
        elif v == 1.5:
            totu2.append (k +"（持ち越し中）")
        elif v == 2.5:
            totu3.append (k +"（持ち越し中）")
        else:
            print("ダメ：" + k)
    await jokyo()
    await channel_kakikomi.send("読み込みました")


async def admin(message):
    target1 = ">"
    target2 = "."
    idx1 = message.content.find(target1)
    msg = message.content[idx1+1:] 
    if msg.startswith("boss"):
        info = msg[6:]
        idx2 = info.find(target2)
        lap = info[:idx2]
        hp = info[idx2+1:]
        if msg[4] == "1":
            boss1[1] = int(lap)
            boss1[2] = int(hp) * 10000
            await channel_kakikomi.send("1ボスを" + str(lap) + "周目 残りHP" + str(hp) + "万に更新しました")
        elif msg[4] == "2":
            boss2[1] = int(lap)
            boss2[2] = int(hp) * 10000
            await channel_kakikomi.send("2ボスを" + str(lap) + "周目 残りHP" + str(hp) + "万に更新しました")
        elif msg[4] == "3":
            boss3[1] = int(lap)
            boss3[2] = int(hp) * 10000
            await channel_kakikomi.send("3ボスを" + str(lap) + "周目 残りHP" + str(hp) + "万に更新しました")
        elif msg[4] == "4":
            boss4[1] = int(lap)
            boss4[2] = int(hp) * 10000
            await channel_kakikomi.send("4ボスを" + str(lap) + "周目 残りHP" + str(hp) + "万に更新しました")
        elif msg[4] == "5":
            boss5[1] = int(lap)
            boss5[2] = int(hp) * 10000
            await channel_kakikomi.send("5ボスを" + str(lap) + "周目 残りHP" + str(hp) + "万に更新しました")
        elif msg[4] == ".":
            if msg[5:-1] == "phase":
                global boss
                boss = int(msg[10:]) * 10
                boss1[2] = bosshp[(boss//10)*10+1]
                boss2[2] = bosshp[(boss//10)*10+2]
                boss3[2] = bosshp[(boss//10)*10+3]
                boss4[2] = bosshp[(boss//10)*10+4]
                boss5[2] = bosshp[(boss//10)*10+5]
                await channel_kakikomi.send(str(boss//10) + "段階目に変更しました")
            else:
                await channel_sinkou.send(message.author.mention + "段階を変更する場合は[boss.phasex],xに現在の段階を入力する")
                return
        else:
            await channel_sinkou.send(message.author.mention + "ボス情報を変更する際は[boss(変更したいボス番号).周回数.残りHP]で入力してください\n(例:1ボスを23周目残りHP600万にしたい場合→boss1.23.600)")
            return
        await totuchuu()

   
async def tasukiru(message):
    msg = message.content[1:]
    if msg == "タスキル":
        await channel_kakikomi.send(message.author.mention + "タスキルしたってまじぃ！？！？ｗｗｗあり得ないんですけどぉｗｗｗｗｗｗｗｗｗｗ")
        role = guild.get_role(tasukiruid)
        await message.author.add_roles(role)
    else:
        return


async def cancel(message):
    msg = message.content
    name = message.author.name
    disc = message.author.discriminator
    msguserid = name + "#" + disc
    listname = msguserid
    if totulist[msguserid] % 1 == 0.5:
        listname += "（持ち越し中）"
    if(msg == "cl"):
        if listname in chu1:               #凸中リストから名前を削除
            chu1.remove(listname)
        elif listname in chu2:
            chu2.remove(listname)
        elif listname in chu3:
            chu3.remove(listname)
        elif listname in chu4:
            chu4.remove(listname)
        elif listname in chu5:
            chu5.remove(listname)
        else:
            await channel_sinkou.send("<@" + str(message.author.id) + "> あんたは凸ってないわよ！")
        await totuchuu()



  
async def jokyo():
    dt_now=datetime.datetime.now()
    #print(dt_now.strftime('%Y年%m月%d日 %H:%M'))
    start = kakoi + (dt_now.strftime('%Y年%m月%d日 %H:%M'))
    #end = '\n残りn人 n凸 (持ち越し中n人)```'
            
    target1 = "#"
    target2 = "（"
    totujokyo = genzai + start + totu1[0]
    motikosi = 0
    for ttjk in totu1[1:]:
        idx1 = ttjk.find(target1)
        totujokyo += membername[ttjk[:idx1+5]]
        if ttjk.find("（") > 0:
            totujokyo += "（持ち越し中）"
            motikosi += 1
        totujokyo += "\n"
    totujokyo += totu2[0]
    for ttjk in totu2[1:]:
        idx1 = ttjk.find(target1)
        totujokyo += membername[ttjk[:idx1+5]]
        if ttjk.find("（") > 0:
            totujokyo += "（持ち越し中）"
            motikosi += 1
        totujokyo += "\n"
    totujokyo += totu3[0]
    for ttjk in totu3[1:]:
        idx1 = ttjk.find(target1)
        totujokyo += membername[ttjk[:idx1+5]]
        if ttjk.find("（") > 0:
            totujokyo += "（持ち越し中）"
            motikosi += 1
        totujokyo += "\n"
    nokori = len(totu1) + len(totu2) + len(totu3) - 3
    nokoritotu = len(totu1) + len(totu2)*2 + len(totu3)*3 - 6
    totujokyo += "\n残り "+ str(nokori) + "人　" + str(nokoritotu) + "凸（持ち越し中" + str(motikosi) + "人）```"
    

    """users = [member for member in client.get_all_members()]
    for user in users:
        await channel_shukei.send('```' + str(user.name) + '```')"""
    
    await totuchuu()

    await shukei.edit(content = totujokyo)

    return

async def owajokyo(msgid):
    global owari
    dt_now=datetime.datetime.now()
    kantotu = kakoi + (dt_now.strftime('%Y年%m月%d日 %H:%M')) + totu0[0]
    target1 = "（"
    for ttjk in totu0[1:]:
        if ttjk.find(target1) > 0:
            kantotu += str(ttjk[:6]) + str(membername[ttjk[6:ttjk.find(target1)]])
        elif ttjk.find(target1) == -1:
            kantotu += str(ttjk[:6]) + str(membername[ttjk[6:]])
    kantotu += kakoi
    if msgid != 0:
        await channel_owari.send("<@" + str(msgid) + ">の3凸は終了よ！お疲れ様.凸完了" + str(len(totu0) - 1) + "人目.")
    owari = await channel_owari.send(kantotu)


async def totu(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    
    msg = message.content
    print(msg)
    if (any(map(str.isdigit, msg))):    #文字に数字が含まれているか
        name = message.author.name
        disc = message.author.discriminator
        msguserid = name + "#" + disc
        bossnum = int(re.sub(r"\D","",msg))     #数字のみを取り出す
        alltotuing = chu1 + chu2 + chu3 + chu4 + chu5
        for listmsg in alltotuing:
            if listmsg.startswith(msguserid):
                username = "<@" + str(message.author.id) + "> あんたは今凸中よ！"
                await channel_kakikomi.send(username)
                return
        
        global totulist
        n = totulist[msguserid]
        if 0 < n < 4:
            username = message.author.mention + "の" + str(int(await henkan(n))) + "凸目よ"
            if totulist[msguserid] % 1 == 0.5:
                msguserid += "（持ち越し中）"
            if bossnum in [1,2,3,4,5]:
                if bossnum == 1:
                    chu1.append(msguserid)
                elif bossnum == 2:
                    chu2.append(msguserid)
                elif bossnum == 3:
                    chu3.append(msguserid)
                elif bossnum == 4:
                    chu4.append(msguserid)
                elif bossnum == 5:
                    chu5.append(msguserid)
                toturesultmsg[msguserid] = ""
            else:
                await channel_sinkou.send(message.author.mention + " 1~5までの数字を入力してください")
                return
            await channel_kakikomi.send(username)
            await totuchuu()
        else:
            await channel_sinkou.send(message.author.mention + " あんたはもう完凸してるはずよ！")
    elif msg[1:] == "希望":
        await kiboudisplay(message)
    elif msg[1:] == "調査" and sinkorole in str(message.author.roles):
        await totuchosa(message)
    else:
        await channel_sinkou.send(message.author.mention + " 凸先のボス番号を入力してください")
        return


async def totuchuu():
    global boss
    totuchujokyo = totuing + "**現在 " + str(boss//10) + "段階目**\n" + kakoi
    target1 = "#"
    totuchujokyo += chu1[0] +  str(boss1[1]) + "周目 " + bossname[boss1[0]] + " 残りHP：" + '{:,}'.format(boss1[2]) + " ---\n"
    for ttjk in chu1[1:]:
        idx1 = ttjk.find(target1)
        ttjkin = membername[ttjk[:idx1+5]]
        if ttjk.find("（") > 0:
            ttjkin += "（持ち越し中）"
        ttjkin += " " + toturesultmsg.get(ttjk[:idx1+5], "")
        ttjkin += "\n"
        totuchujokyo += str(ttjkin)
    totuchujokyo += chu2[0] + str(boss2[1]) + "周目 " + bossname[boss2[0]] + " 残りHP：" + '{:,}'.format(boss2[2]) + " ---\n"
    for ttjk in chu2[1:]:
        idx1 = ttjk.find(target1)
        ttjkin = membername[ttjk[:idx1+5]]
        if ttjk.find("（") > 0:
            ttjkin += "（持ち越し中）"
        ttjkin += " " + toturesultmsg.get(ttjk[:idx1+5], "")
        ttjkin += "\n"
        totuchujokyo += str(ttjkin)
    totuchujokyo += chu3[0] + str(boss3[1]) + "周目 " + bossname[boss3[0]] + " 残りHP：" + '{:,}'.format(boss3[2]) + " ---\n"
    for ttjk in chu3[1:]:
        idx1 = ttjk.find(target1)
        ttjkin = membername[ttjk[:idx1+5]]
        if ttjk.find("（") > 0:
            ttjkin += "（持ち越し中）"
        ttjkin += " " + toturesultmsg.get(ttjk[:idx1+5], "")
        ttjkin += "\n"
        totuchujokyo += str(ttjkin)
    totuchujokyo += chu4[0] + str(boss4[1]) + "周目 " + bossname[boss4[0]] + " 残りHP：" + '{:,}'.format(boss4[2]) + " ---\n"
    for ttjk in chu4[1:]:
        idx1 = ttjk.find(target1)
        ttjkin = membername[ttjk[:idx1+5]]
        if ttjk.find("（") > 0:
            ttjkin += "（持ち越し中）"
        ttjkin += " " + toturesultmsg.get(ttjk[:idx1+5], "")
        ttjkin += "\n"
        totuchujokyo += str(ttjkin)
    totuchujokyo += chu5[0] + str(boss5[1]) + "周目 " + bossname[boss5[0]] + " 残りHP：" + '{:,}'.format(boss5[2]) + " ---\n"
    for ttjk in chu5[1:]:
        idx1 = ttjk.find(target1)
        ttjkin = membername[ttjk[:idx1+5]]
        if ttjk.find("（") > 0:
            ttjkin += "（持ち越し中）"
        ttjkin += " " + toturesultmsg.get(ttjk[:idx1+5], "")
        ttjkin += "\n"
        totuchujokyo += str(ttjkin)

    totuchujokyo += "\n\n n人凸中 " + kakoi
    
    
    await totuchu.edit(content = totuchujokyo)

    return

async def toturesult(message):
    name = message.author.name
    disc = message.author.discriminator
    msguserid = name + "#" + disc
    target = " "
    msg = message.content
    if message.content[1] in [" ", "　"]:
        message.content = "凸" + str(message.content[0])
        await totu(message)
        msg = msg[2:]
    toturesultmsg[msguserid] = msg

    await totuchuu()



async def totutta(message):
    if message.content.startswith('凸った@') and (message.channel.id == totusinkou_ID):
        global totulist
        global totu0
        name = message.author.name
        disc = message.author.discriminator
        msguserid = name + "#" + disc
        alltotu = chu1 + chu2 + chu3 + chu4 + chu5
        listname = msguserid
        if totulist[msguserid] % 1 == 0.5:
            listname += "（持ち越し中）"
        if listname not in alltotu:
            await channel_sinkou.send(message.author.mention + " あんたはまだ凸ってないわよ！")
            return
        username = "<@" + str(message.author.id) + ">の"  
        target = "@"
        msg = message.content
        idx = msg.find(target)
        dmgmsg = msg[idx + 1:] 
        n = 1
        
        if dmgmsg == "LA" and (totulist[msguserid] in [1,2,3]): #新品凸で〆たとき（持ち越し発生）
            listname = msguserid
            username += str(await henkan(totulist[msguserid])-0.5) + "凸目完了.持ち越しが発生したわよ."
        elif dmgmsg == "LA" and (totulist[msguserid] in [1.5,2.5,0.5]):   #持ち越し凸で〆たとき（持ち越し発生なし）
            listname = msguserid + "（持ち越し中）"
            username +=  "持ち越し凸終了." + str(int(await henkan(totulist[msguserid]))) +  "凸目完了."
        elif dmgmsg.isdecimal()  and (totulist[msguserid] in [1,2,3]):  #新品凸で凸った時（持ち越し発生なし）
            listname = msguserid
            n = 2
            username += str(int(await henkan(totulist[msguserid]))) + "凸目完了"
        elif dmgmsg.isdecimal()  and (totulist[msguserid] in [1.5,2.5,0.5]):  #持ち越し凸で凸った時（持ち越し発生なし）
            listname = msguserid + "（持ち越し中）"
            username += "持ち越し凸終了." + str(int(await henkan(totulist[msguserid]))) + "凸目完了."
        else:
            await channel_sinkou.send("あたしねこだからりかいできないにゃ٩( ᐛ )و")
            return
        await channel_kakikomi.send(username)

        if totulist[msguserid] % 1 == 0.5 or n == 2:  #残り凸数が減った場合（持ち越しを持たない状態）集計から1凸減らした場所に表記する為の処理↓
            if totulist[msguserid] in [0.5, 1.0]:  #凸が減ったら名前を削除
                totu1.remove(listname)
                dt_now=datetime.datetime.now()
                totu0.append((dt_now.strftime('%H:%M ')) + listname)
                await owari.delete()
                await owajokyo(message.author.id)
            elif totulist[msguserid] in [1.5, 2.0]:
                totu2.remove(listname)
                totu1.append(msguserid)
            elif totulist[msguserid] in [2.5, 3.0]:
                totu3.remove(listname)
                totu2.append(msguserid)
        elif  totulist[msguserid] % 1 == 0:
            if totulist[msguserid] == 1:
                i = totu1.index(msguserid)
                totu1[i] = totu1[i] + "（持ち越し中）"
            elif totulist[msguserid] == 2:
                i = totu2.index(msguserid)
                totu2[i] = totu2[i] + "（持ち越し中）"
            elif totulist[msguserid] == 3:
                i = totu3.index(msguserid)
                totu3[i] = totu3[i] + "（持ち越し中）"

        if listname in chu1:               #凸中リストから名前を削除
            await bossinfoupdate(dmgmsg,1)
            chu1.remove(listname)
            if dmgmsg == "LA":
                del chu1[1:]
        elif listname in chu2:
            await bossinfoupdate(dmgmsg,2)
            chu2.remove(listname)
            if dmgmsg == "LA":
                del chu2[1:]
        elif listname in chu3:
            await bossinfoupdate(dmgmsg,3)
            chu3.remove(listname)
            if dmgmsg == "LA":
                del chu3[1:]
        elif listname in chu4:
            await bossinfoupdate(dmgmsg,4)
            chu4.remove(listname)
            if dmgmsg == "LA":
                del chu4[1:]
        elif listname in chu5:
            await bossinfoupdate(dmgmsg,5)
            chu5.remove(listname)
            if dmgmsg == "LA":
                del chu5[1:]
        totulist[msguserid] -= 0.5*n        #消化した凸を削除
        
        await jokyo()
    
    return


async def bossinfoupdate(msg,n):
    global boss
    if msg == "LA":
        if n == 1:
            boss1[1] += 1
            num = (boss // 10) * 10 + n
            if 0 < boss1[1] < 4:
                boss1[2] = bosshp[num]
            elif boss1[1] == 4:
                boss += 2       
                boss1[2] = 0
            elif 4 < boss1[1] < 11:
                boss1[2] = bosshp[num]
            elif boss1[1] == 11:
                boss += 2
                boss1[2] = 0
            elif 11 < boss1[1] < 31:
                boss1[2] = bosshp[num]
            elif boss1[1] == 31:
                boss += 2
                boss1[2] = 0
            elif 31 < boss1[1] < 41:
                boss1[2] = bosshp[num]
            elif boss1[1] == 41:
                boss += 2
                boss1[2] = 0
            elif 41 < boss1[1]:
                boss1[2] = bosshp[num]
        elif n == 2:
            boss2[1] += 1
            num = (boss // 10) * 10 + n
            if 0 < boss2[1] < 4:
                boss2[2] = bosshp[num]
            elif boss2[1] == 4:
                boss += 2
                boss2[2] = 0
            elif 4 < boss2[1] < 11:
                boss2[2] = bosshp[num]
            elif boss2[1] == 11:
                boss += 2
                boss2[2] = 0
            elif 11 < boss2[1] < 31:
                boss2[2] = bosshp[num]
            elif boss2[1] == 31:
                boss += 2
                boss2[2] = 0
            elif 31 < boss2[1] < 41:
                boss2[2] = bosshp[num]
            elif boss2[1] == 41:
                boss += 2
                boss2[2] = 0
            elif 41 < boss2[1]:
                boss2[2] = bosshp[num]
        elif n == 3:
            boss3[1] += 1
            num = (boss // 10) * 10 + n
            if 0 < boss3[1] < 4:
                boss3[2] = bosshp[num]
            elif boss3[1] == 4:
                boss += 2
                boss3[2] = 0
            elif 4 < boss3[1] < 11:
                boss3[2] = bosshp[num]
            elif boss3[1] == 11:
                boss += 2
                boss3[2] = 0
            elif 11 < boss3[1] < 31:
                boss3[2] = bosshp[num]
            elif boss3[1] == 31:
                boss += 2
                boss3[2] = 0
            elif 31 < boss3[1] < 41:
                boss3[2] = bosshp[num]
            elif boss3[1] == 41:
                boss += 2
                boss3[2] = 0
            elif 41 < boss3[1]:
                boss3[2] = bosshp[num]
        elif n == 4:
            boss4[1] += 1
            num = (boss // 10) * 10 + n
            if 0 < boss4[1] < 4:
                boss4[2] = bosshp[num]
            elif boss4[1] == 4:
                boss += 2
                boss4[2] = 0
            elif 4 < boss4[1] < 11:
                boss4[2] = bosshp[num]
            elif boss4[1] == 11:
                boss += 2
                boss4[2] = 0
            elif 11 < boss4[1] < 31:
                boss4[2] = bosshp[num]
            elif boss4[1] == 31:
                boss += 2
                boss4[2] = 0
            elif 31 < boss4[1] < 41:
                boss4[2] = bosshp[num]
            elif boss4[1] == 41:
                boss += 2
                boss4[2] = 0
            elif 41 < boss4[1]:
                boss4[2] = bosshp[num]
        elif n == 5:
            boss5[1] += 1
            num = (boss // 10) * 10 + n
            if 0 < boss1[1] < 4:
                boss1[2] = bosshp[num]
            elif boss1[1] == 4:
                boss += 2 
                boss5[2] = 0
            elif 4 < boss1[1] < 11:
                boss1[2] = bosshp[num]
            elif boss1[1] == 11:
                boss += 2
                boss5[2] = 0
            elif 11 < boss1[1] < 31:
                boss1[2] = bosshp[num]
            elif boss1[1] == 31:
                boss += 2
                boss5[2] = 0
            elif 31 < boss1[1] < 41:
                boss1[2] = bosshp[num]
            elif boss1[1] == 41:
                boss += 2
                boss5[2] = 0
            elif 41 < boss1[1]:
                boss1[2] = bosshp[num]
        if boss in [20, 30, 40, 50]:
            boss1[2] = bosshp[(num // 10) * 10 + 1]
            boss2[2] = bosshp[(num // 10) * 10 + 2]
            boss3[2] = bosshp[(num // 10) * 10 + 3]
            boss4[2] = bosshp[(num // 10) * 10 + 4]
            boss5[2] = bosshp[(num // 10) * 10 + 5]
            await channel_kakikomi.send("<@&" + str(clanroleid) + ">" + str(boss//10) + "段階目に入りました")
    else:
        if n == 1:
            boss1[2] -= int(msg) * 10000
        elif n == 2:
            boss2[2] -= int(msg) * 10000
        elif n == 3:
            boss3[2] -= int(msg) * 10000
        elif n == 4:
            boss4[2] -= int(msg) * 10000
        elif n == 5:
            boss5[2] -= int(msg) * 10000


async def kibou(message):
    name = message.author.name
    disc = message.author.discriminator
    msguserid = name + "#" + disc
    msg = int(message.content[2])
    if msg == 1:
        if msguserid in kibo1:
            kibo1.remove(msguserid)
        kibo1.append(msguserid)
    elif msg == 2:
        if msguserid in kibo2:
            kibo2.remove(msguserid)
        kibo2.append(msguserid)
    elif msg == 3:
        if msguserid in kibo3:
            kibo3.remove(msguserid)
        kibo3.append(msguserid)
    elif msg == 4:
        if msguserid in kibo4:
            kibo4.remove(msguserid)
        kibo4.append(msguserid)
    elif msg == 5:
        if msguserid in kibo5:
            kibo5.remove(msguserid)
        kibo5.append(msguserid)
    else:
        await channel_kibou.send(message.author.mention + "1-5の数字を入力してください")
    await channel_kibou.send(message.author.mention + "さんの" + bossname[msg] + "の予約を受け付けました")

async def kiboudisplay(message):
    dt_now=datetime.datetime.now()
    start = (dt_now.strftime('%Y年%m月%d日 %H:%M'))
    target1 = "#"
    kibojokyo = kakoi + "現在の希望状況 " + start
    for kbjk in kibo1[0:]:
        idx1 = kbjk.find(target1)
        kbjkin = kbjk[:idx1]
        kbjkin += "\n"
        kibojokyo += str(kbjkin)
    for kbjk in kibo2[0:]:
        idx1 = kbjk.find(target1)
        kbjkin = kbjk[:idx1]
        kbjkin += "\n"
        kibojokyo += str(kbjkin)
    for kbjk in kibo3[0:]:
        idx1 = kbjk.find(target1)
        kbjkin = kbjk[:idx1]
        kbjkin += "\n"
        kibojokyo += str(kbjkin)
    for kbjk in kibo4[0:]:
        idx1 = kbjk.find(target1)
        kbjkin = kbjk[:idx1]
        kbjkin += "\n"
        kibojokyo += str(kbjkin)
    for kbjk in kibo5[0:]:
        idx1 = kbjk.find(target1)
        kbjkin = kbjk[:idx1]
        kbjkin += "\n"
        kibojokyo += str(kbjkin)
    kibojokyo += kakoi
    ch = message.channel
    await ch.send(kibojokyo)

async def totuchosa(message):
    global chosamsg
    ch = message.channel
    chosamsg = await ch.send('行けるボスにリアクションするのよ！')
    await chosamsg.add_reaction(emoji1)
    await chosamsg.add_reaction(emoji2)
    await chosamsg.add_reaction(emoji3)
    await chosamsg.add_reaction(emoji4)
    await chosamsg.add_reaction(emoji5)

    #aaa = message.reactions
    #print(aaa)

async def kibogo(message):
    print("ok")

async def henkan(n):
    if n == 3:
        m = 1
        return(m)
    elif n == 2:
        return(n)
    elif n == 1:
        m = 3
        return(m)
    elif n == 2.5:
        m = 1
        return(m)
    elif n == 1.5:
        m = 2
        return(m)
    elif n == 0.5:
        m = 3
        return(m)



# 接続に必要なオブジェクトを生成
Intents = discord.Intents.all()
client = discord.Client(intents = Intents)


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    dt_now=datetime.datetime.now()
    print(dt_now)
    
    await start()
    



# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    msg = message.content
    if message.content.startswith('凸った@') and (message.channel.id == totusinkou_ID):
        await totutta(message)
    elif (msg.startswith('凸') or msg.startswith('totu') or msg.startswith('tomu') or msg.startswith('とつ') or msg.startswith('とむ')) and (message.channel.id == totusinkou_ID):
        await totu(message)
    elif msg[0].isdecimal():
        await toturesult(message)
    elif (msg == '集計'):
        await gssload()
    elif (msg == "cl") and (message.channel.id == totusinkou_ID):
        await cancel(message)
    elif client.user in message.mentions and sinkorole in str(message.author.roles):
        await admin(message)
    elif msg == "凸調査" and sinkorole in str(message.author.roles):
        await totuchosa(message)
    elif msg.startswith("希望") and (message.channel.id == kibou_ID):
        await kibou(message)
    elif msg == "凸希望" and (message.channel.id == kibou_ID):
        await kiboudisplay(message)
    elif msg.startswith('!'):
        await tasukiru(message)
    elif msg == "reset" and sinkorole in str(message.author.roles):
        await allreset()

bot.run(token)
