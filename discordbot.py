import asyncio
from operator import indexOf
from ssl import RAND_add
import discord
from discord.ext import commands
from os import getenv
import traceback
import random
import database as db

bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())
day=""
name=""
ndm=""

# @bot.event
# async def on_command_error(ctx, error):
#     orig_error = getattr(error, "original", error)
#     error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
#     await ctx.send(error_msg)

# @bot.command()
# async def hoge(ctx,name):
#  conn = db.connect() # このconnを通じて操作する
#  if conn.exists('リスト')==0:#リストがない場合
#   conn.set('リスト', name)
#  else:
#   str=conn.get('リスト')
#   str=str+name
#   conn.set('リスト', str)
#  await ctx.send(name+"を加えました〜")

# @bot.command()
# async def fuga(ctx,name):
#  str=conn.get('リスト')



@bot.command()
async def makefield(ctx,day,name):

       LobbyName = day+" "+name
       Guild = ctx.guild

       # カテゴリを作成する
       Category = await Guild.create_category(LobbyName)

       # チャンネルの作成時にカテゴリを設定する
       await Category.create_text_channel("女神降臨場")
       await Category.create_text_channel("メニュー宣言ゾーン")
       await Category.create_text_channel("フリートーク")
       await ctx.send("カテゴリーを作成しました！")

@bot.command()
async def kungfu(ctx):

       kungfuchr="剣破皇脚翼旋斬弾槍滅追絶覇閃砲極空襲陣舞滅砲衝刃射蹴砕封蒼烈殺襲真絶散斬弓魔旋撃神空陣暴封砕射攻殺牙衝槍羅乱刃連破翼覇銃"#http://tookcg.elgraiv.com/tools/chu2v2.html
       listlen=len(kungfuchr)
       resultstr=""
       conn = db.connect() # このconnを通じて操作する
       for num in range(3):
        result=random.randint(1,listlen)
        resultkanji=kungfuchr[result-1]
        print(str(num+1)+"回目ロール:"+resultkanji)

        if resultstr!="":#2回目いこう
          resultstr=resultstr+","+resultkanji
          dbstr=conn.get(ctx.author.name)
          dbstr=dbstr+resultkanji
          conn.set(ctx.author.name, dbstr)
        else:#初回
          conn.set(ctx.author.name,"")#リセット
          conn.set(ctx.author.name+"ラウンド",0)#リセット
          resultstr=resultkanji
          conn.set(ctx.author.name, resultstr)

       embed = discord.Embed(
       description="お主の漢字はこれだ！"
       )
       embed.add_field(name="漢字一覧",value=resultstr)

       await ctx.send(embed=embed)

@bot.command()
async def mykungfu(ctx):

       conn = db.connect() # このconnを通じて操作する
       dbstr=conn.get(ctx.author.name)

       await ctx.send("お主の今の漢字は「"+dbstr+"」だ！")  
@bot.command()
async def draw2(ctx):
       conn = db.connect() # このconnを通じて操作する
       roundnum=conn.get(ctx.author.name+"ラウンド")
       if int(roundnum)<3:
         kungfuchr="剣破皇脚翼旋斬弾槍滅追絶覇閃砲極空襲陣舞滅砲衝刃射蹴砕封蒼烈殺襲真絶散斬弓魔旋撃神空陣暴封砕射攻殺牙衝槍羅乱刃連破翼覇銃"#http://tookcg.elgraiv.com/tools/chu2v2.html
         listlen=len(kungfuchr)
         resultstr=""
       
         for num in range(2):
           result=random.randint(1,listlen)
           resultkanji=kungfuchr[result-1]
           print(str(num+1)+"回目ロール:"+resultkanji)
           resultstr=resultstr+resultkanji
           
           dbstr=conn.get(ctx.author.name)
           dbstr=dbstr+resultkanji
           conn.set(ctx.author.name, dbstr)
           conn.set(ctx.author.name+"ラウンド", int(roundnum)+1)


         await ctx.send("「"+resultstr+"」が新たな漢字だ。"+"お主の今の漢字は「"+dbstr+"」だ！") 
       else:
          await ctx.send("お主、3ラウンドを経過しているな！最初からやり直せっ！")   

@bot.command()
async def draw3(ctx):
       conn = db.connect() # このconnを通じて操作する
       def check(m):
               # メッセージが `おはよう` かつ メッセージを送信したチャンネルが
               # 欲しいもの「/」[]
               print( m.content[0] in resultstr)
               print( m.content[1]=="/")
               print( m.content[2] in conn.get(ctx.author.name))
               
               return m.content[0] in resultstr and m.content[1]=="/" and m.content[2] in conn.get(ctx.author.name)
       
       roundnum=conn.get(ctx.author.name+"ラウンド")
       if int(roundnum)<3:
         kungfuchr="剣破皇脚翼旋斬弾槍滅追絶覇閃砲極空襲陣舞滅砲衝刃射蹴砕封蒼烈殺襲真絶散斬弓魔旋撃神空陣暴封砕射攻殺牙衝槍羅乱刃連破翼覇銃"#http://tookcg.elgraiv.com/tools/chu2v2.html
         listlen=len(kungfuchr)
         resultstr=""
       
         for num in range(3):
          result=random.randint(1,listlen)
          resultkanji=kungfuchr[result-1]
          print(str(num)+"回目ロール:"+resultkanji)
          resultstr=resultstr+resultkanji
          

          
         

             # 待っているものに該当するかを確認する関数
           
         await ctx.send("新たな漢字は「"+resultstr+"」だ。「欲しい漢字/いらない漢字」の形式で漢字を入力するのだ。")
         try:
             # wait_forを用いて、イベントが発火し指定した条件を満たすまで待機する
             msg = await bot.wait_for('message', check=check)
             # wait_forの1つ目のパラメータは、イベント名の on_がないもの
             # 2つ目は、待っているものに該当するかを確認する関数 (任意)
             # 3つ目は、タイムアウトして asyncio.TimeoutError が発生するまでの秒数
             
         # asyncio.TimeoutError が発生したらここに飛ぶ
         except asyncio.TimeoutError:
             await ctx.send("時間切れじゃ。もう一度抽選するのだ！")
         else:
             dbstr=conn.get(ctx.author.name)
             print(dbstr)
             dbstr=dbstr.replace(msg.content[2],"")
             resultstr=resultstr.replace(msg.content[0],"")
             conn.set("公開カード", resultstr)
             print(msg.content[2]+"と交換")
             dbstr=dbstr+msg.content[0]
             print(dbstr)
             conn.set(ctx.author.name, dbstr)
             conn.set(ctx.author.name+"ラウンド", int(roundnum)+1)
             await ctx.send("交換が終了したぞ。"+"お主の今の漢字は「"+dbstr+"」だ！") 
       else:
          await ctx.send("お主、3ラウンドを経過しているな！最初からやり直せっ！")
       
@bot.command()
async def change(ctx):
       conn = db.connect() # このconnを通じて操作する
       def check(m):

               
               return m.content[0] in koukaistr and m.content[1]=="/" and m.content[2] in conn.get(ctx.author.name)
       
       roundnum=conn.get(ctx.author.name+"ラウンド")
       if int(roundnum)<3:
         conn = db.connect() # このconnを通じて操作する
         koukaistr=conn.get("公開カード")
         if koukaistr is not None:
          await ctx.send("公開中の漢字は「"+koukaistr+"」だ。「欲しい漢字/いらない漢字」の形式で漢字を入力するのだ。")
          try:
              # wait_forを用いて、イベントが発火し指定した条件を満たすまで待機する
              msg = await bot.wait_for('message', check=check)
              # wait_forの1つ目のパラメータは、イベント名の on_がないもの
              # 2つ目は、待っているものに該当するかを確認する関数 (任意)
              # 3つ目は、タイムアウトして asyncio.TimeoutError が発生するまでの秒数
              
          # asyncio.TimeoutError が発生したらここに飛ぶ
          except asyncio.TimeoutError:
              await ctx.send("時間切れじゃ。もう一度抽選するのだ！")
          else:
              dbstr=conn.get(ctx.author.name)
              print(dbstr)
              dbstr=dbstr.replace(msg.content[2],"")
              koukaistr=koukaistr.replace(msg.content[0],"")
              conn.set("公開カード", koukaistr)
              print(msg.content[2]+"と交換")
              dbstr=dbstr+msg.content[0]
              conn.set(ctx.author.name, dbstr)
              conn.set(ctx.author.name+"ラウンド", int(roundnum)+1)
              await ctx.send("交換が終了したぞ。"+"お主の今の漢字は「"+dbstr+"」だ！")
         else:
          await ctx.send("交換可能な公開カードが無いぞ！")
       else:
          await ctx.send("お主、3ラウンドを経過しているな！最初からやり直せっ！")


# @bot.command()
# async def makefield(ctx):
#   await ctx.send("チャンネル名が空ですよ！")

@makefield.error
async def error(ctx,error):
 error = getattr(error, "original", error)

 if isinstance(error, commands.MissingRequiredArgument):
   await ctx.send("チャンネル名が空ですよ！")

@bot.command()
async def roll(ctx,ndm):
    index= ndm.find("d")
    n=int(ndm[:index])#1d
    m=int(ndm[index+1:])#100

    resultstr=""
    sum=0
    for num in range(n):
     result=random.randint(1,m)
     print(str(num)+"回目ロール:"+str(result))
     if resultstr!="":
       resultstr=resultstr+","+str(result)
     else:
       resultstr=str(result)
     sum=sum+result


    embed = discord.Embed(
    description="ロール結果"
    )
    embed.add_field(name="値",value=resultstr)
    if n!=1:
     embed.add_field(name="合計",value=sum)
     
    
   
    embed.set_author(name=ctx.author.name, # Botのユーザー名
     url="https://repo.exapmle.com/bot", # titleのurlのようにnameをリンクにできる。botのWebサイトとかGithubとか
     icon_url=ctx.author.avatar_url # Botのアイコンを設定してみる
     )
    await ctx.send(embed=embed)




# @bot.command()
# async def makefield(ctx):
#   await ctx.send("チャンネル名が空ですよ！")

@makefield.error
async def wo(ctx,error):
 error = getattr(error, "original", error)

 if isinstance(error, commands.MissingRequiredArgument):
   await ctx.send("チャンネル名が空ですよ！")

@bot.command()
async def wordgame(ctx):

       conn = db.connect() # このconnを通じて操作する
       listlen=conn.llen("wordgame_TableA")#長さゲット
       result=random.randint(1,listlen)-1
       wordA = conn.lindex("wordgame_TableA", result)

       listlen=conn.llen("wordgame_TableB")#長さゲット
       result=random.randint(1,listlen)-1
       wordB = conn.lindex("wordgame_TableB", result)

       listlen=conn.llen("wordgame_TableA")#長さゲット
       result=random.randint(1,listlen)-1
       wordC = conn.lindex("wordgame_TableA", result)


       
       await ctx.send("ゲームを始めるよ！\n今回のお題は…こちら！親は見ちゃダメだよ！")
       await ctx.send("||"+wordA+wordB+wordC+"||")

@bot.command()
async def addwordA(ctx,string):
       word=str(string)
       conn = db.connect() # このconnを通じて操作する
       conn.lpush("wordgame_TableA",word)



       
       await ctx.send(string+"を追加したのだ")

@bot.command()
async def addwordB(ctx,string):
       word=str(string)
       conn = db.connect() # このconnを通じて操作する
       conn.lpush("wordgame_TableB",word)#長さゲット



       
       await ctx.send(string+"を追加したのだ")
@bot.command()
async def wordgame2(ctx):
       conn = db.connect() # このconnを通じて操作する

       listA=conn.lrange("wordgame_Things", 0, conn.llen("wordgame_Things"))
       listB=conn.lrange("wordgame_Object", 0, conn.llen("wordgame_Object"))
       listC=conn.lrange("wordgame_Name", 0, conn.llen("wordgame_Name"))


       listlen=conn.llen("wordgame_TableA")#長さゲット
       result=random.randint(1,listlen)
       wordA = conn.lindex("wordgame_TableA", result)
       if wordA in listC :#人の名前
        wordBlist = ["が霞むほどの","だけじゃない","に騙されそうな","故の","かもしれない","にありがちな","をモチーフとした","が好きな","がどうしても勝てない","の","が嫌いな","が作った","と一緒にいる","による","だけの","だらけの","っぽい"]
        listlen=len(wordBlist)-1
        result=random.randint(1,listlen)
        wordB = wordBlist[result]
       elif wordA in listB :#物の名前
        wordBlist = ["の上の","に入っている","but","故の","かもしれない","にありがちな","で遊ぶ","をモチーフとした","だけの","だらけの","っぽい"]
        listlen=len(wordBlist)-1
        result=random.randint(1,listlen)
        wordB = wordBlist[result]
       elif wordA in listA :#概念の名前
         wordBlist = ["but","故の","にありがちな","をモチーフとした","にありがちな","の","による","だらけの","っぽい"]
         listlen=len(wordBlist)-1
         result=random.randint(1,listlen)
         wordB = wordBlist[result]
       if(wordB=="で遊ぶ"):
        listlen=conn.llen("wordgame_Name")#長さゲット
       else:
        listlen=conn.llen("wordgame_TableA")#長さゲット
        result=random.randint(1,listlen)
        wordC = conn.lindex("wordgame_TableA", result)


       
       await ctx.send("改善版ゲームを始めるよ！\n今回のお題は…こちら！親は見ちゃダメだよ！")
       await ctx.send("||"+wordA+wordB+wordC+"||")




       


@bot.command()
async def addwordPerson(ctx,string):
       word=str(string)
       conn = db.connect() # このconnを通じて操作する
       conn.lpush("wordgame_Name",word)
       conn.lpush("wordgame_TableA",word)#長さゲット
       
       await ctx.send(string+"を追加したのだ")

@bot.command()
async def addwordObject(ctx,string):
       word=str(string)
       conn = db.connect() # このconnを通じて操作する
       conn.lpush("wordgame_Object",word)#長さゲット
       conn.lpush("wordgame_TableA",word)#長さゲット

       await ctx.send(string+"を追加したのだ")

@bot.command()
async def addwordThings(ctx,string):
       word=str(string)
       conn = db.connect() # このconnを通じて操作する
       conn.lpush("wordgame_Things",word)#長さゲット
       conn.lpush("wordgame_TableA",word)#長さゲット

       await ctx.send(string+"を追加したのだ")

@bot.command()
async def showwordtable(ctx):
      conn = db.connect() # このconnを通じて操作する
      listA=conn.lrange("wordgame_TableA", 0, conn.llen("wordgame_TableA"))
      listB=conn.lrange("wordgame_TableB", 0, conn.llen("wordgame_TableB"))


      embed = discord.Embed(
      description="表データ一覧"
      )
      embed.add_field(name="A",value=listA)
      embed.add_field(name="B",value=listB)
      embed.add_field(name="Aの個数",value=len(listA))
      embed.add_field(name="Bの個数",value=len(listB))
       
      
     
      embed.set_author(name=ctx.author.name, # Botのユーザー名
       url="https://repo.exapmle.com/bot", # titleのurlのようにnameをリンクにできる。botのWebサイトとかGithubとか
       icon_url=ctx.author.avatar_url )# Botのアイコンを設定してみる

       
      await ctx.send(embed=embed)

@bot.command()
async def showwordtable2(ctx):
      conn = db.connect() # このconnを通じて操作する
      listA=conn.lrange("wordgame_Things", 0, conn.llen("wordgame_Things"))
      listB=conn.lrange("wordgame_Object", 0, conn.llen("wordgame_Object"))
      listC=conn.lrange("wordgame_Name", 0, conn.llen("wordgame_Name"))


      embed = discord.Embed(
      description="表データ一覧"
      )
      embed.add_field(name="概念",value=listA)
      embed.add_field(name="物",value=listB)
      embed.add_field(name="名前",value=listC)

       
      
     
      embed.set_author(name=ctx.author.name, # Botのユーザー名
       url="https://repo.exapmle.com/bot", # titleのurlのようにnameをリンクにできる。botのWebサイトとかGithubとか
       icon_url=ctx.author.avatar_url )# Botのアイコンを設定してみる

       
      await ctx.send(embed=embed)
         

@bot.command()
async def rollm3(ctx):
   island=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T",\
           "あ","い","う","え","お","カ","キ","ク","ケ","コ","サ"]
       #島内の最大ブース番号。アルファベットひらがなカタカナの順。
   booth=[18,24,24,24,24,\
          24,24,24,24,24,\
          24,24,18,24,24,\
          24,6,20,9,37,\
          16,32,40,40,36,20,\
          13,36,40,40,40\
         ]
   #ab合体ブースの番号です。
   ab=[[2,3,5,7,9,12,15,16],[2,10,15,16,17,20,21,22],[1,9,10,16,21],[],[7,8,16,17,18,19,21,22,23,24],\
       [8,14,16,18],[9,11,14,16,19],[10],[1,2,3,4,5,6,7,8,9,10,11,12,17,18,23,24],[4,9,10,11,17],\
       [6],[4,6,14,17,19],[4,14,17,18],[9,10,11,15,21,24],[2,4,8,10,11,14,21,22],\
       [6,8,16,17,18,19],[1,2],[1,3,4,5,6,8,9,10,13,14,15,16,17,18],[6,7,8,9],[2,6,10,11,13,14,15,16,17,18,19,20,21,27,28,31,34,37],\
       [1,2,5,6,7,10,11,14],[1,3,5,8,15,20],[9,12,17,21,22,27,28,35],[1,2,3,4,5,6,7,8,11,12,13,16,19,21,22,26,33,37,39,40],[2,5,7,10,14,17,18,23,30],[1,4,5,6,8,15,16,19,20],
       [1,2,3,4,5,9,13],[5,23,24,36],[6,15,16,26,35],[6,7,8,9,11,17,18,19,20,22,26,28,29,30,32,34,36,37,39],[2,6,12,13,16,21,22,25,28,39,40],[1,3,4,5,9,10,12,13,16,18,19,20,21,22]]
   islandsize=len(island)
   islandpos=random.randint(1,islandsize)#島決定
   boothsize=booth[islandpos-1]
   boothnum=random.randint(1,boothsize)#番号決定
   if boothnum<10:
       boothstr="0"+str(boothnum)
   else:
       boothstr=str(boothnum)
   
   
   if boothnum in ab[islandpos-1]:
       String=island[islandpos-1]+"-"+boothstr+"ab"
   else:
       abdice=random.randint(1,2)
       if abdice==1:
          String=island[islandpos-1]+"-"+boothstr+"a"
       else:
          String=island[islandpos-1]+"-"+boothstr+"b"

          
   await ctx.send("2023年秋M3ダイス：結果は…\n"+String) 
          

@bot.command()
async def Play(ctx):
   URLCommonStr="https://gdbg.tv/release/"
   year=random.randint(2009,2021)#2009~2021
   albumnum=year-2009
   albumlist=[[7,7,6,6,6],[17,17,5],[12,12,11],[12,12,13],[12,12,12],[10,9,9,10],[10,10,10,11],[10,10,10,10],[20,20],[6,5,5,6,5,5,5,5],[10,9,10,10,10],[12,12,12,12],[12,12,12,12]]
   thisalbum=albumlist[albumnum]
   albumsize=len(thisalbum)
   discpos=random.randint(1,albumsize)
   disc=thisalbum[discpos-1]
   track=random.randint(1,disc)

   String=URLCommonStr+str(year)+"-"+str(discpos)+"-"+str(track)


   await ctx.send("今回のおすすめはこちら\n"+String)

@bot.command()
async def nabe(ctx,n):
       guzailist=[]
       conn = db.connect() # このconnを通じて操作する
       listlen=conn.llen("nabelist")#長さゲット
       result=random.randint(1,listlen)-1
       for x in range(int(n)):
        guzai = conn.lindex("nabelist", result)
        guzailist.append(guzai)


       
       embed = discord.Embed(
       description="今回のお鍋("+n+"種入り)"
       )
       embed.add_field(name="具材",value=guzailist)

       await ctx.send(embed=embed)










token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
