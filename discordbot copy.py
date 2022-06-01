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
async def wordgame(ctx):

       conn = db.connect() # このconnを通じて操作する
       listlen=conn.llen("wordgame_TableA")#長さゲット
       result=random.randint(1,listlen)
       wordA = conn.lindex("wordgame_TableA", result)

       listlen=conn.llen("wordgame_TableB")#長さゲット
       result=random.randint(1,listlen)
       wordB = conn.lindex("wordgame_TableB", result)

       listlen=conn.llen("wordgame_TableA")#長さゲット
       result=random.randint(1,listlen)
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
         


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)
