import asyncio
from ssl import RAND_add
import discord
from discord.ext import commands
from os import getenv
import traceback
import random
import database as db

bot = commands.Bot(command_prefix='!')
day=""
name=""
ndm=""

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

         
        
       
       embed.set_author(name=ctx.author.name, # Botのユーザー名
        url="https://repo.exapmle.com/bot", # titleのurlのようにnameをリンクにできる。botのWebサイトとかGithubとか
        icon_url=ctx.author.avatar_url # Botのアイコンを設定してみる
        )
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



token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)

