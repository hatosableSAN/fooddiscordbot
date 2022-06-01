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
async def error(ctx,error):
 error = getattr(error, "original", error)

 if isinstance(error, commands.MissingRequiredArgument):
   await ctx.send("チャンネル名が空ですよ！")


token = getenv('DISCORD_BOT_TOKEN')
bot.run(token)












