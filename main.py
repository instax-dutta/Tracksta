import discord
from discord.ext import commands, tasks
from motor.motor_asyncio import AsyncIOMotorClient
import datetime
import schedule
import asyncio

# Bot setup
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(command_prefix="...", intents=intents)

# MongoDB setup
MONGO_URI = "mongo_uri"
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client['discord_activity']
activity_collection = db['user_activity']
reports_collection = db['weekly_reports']

# Bot events
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    generate_weekly_reports.start()

@bot.event
async def on_presence_update(before, after):
    if before.status != after.status:
        now = datetime.datetime.utcnow()
        user_data = await activity_collection.find_one({"user_id": after.id})
        if not user_data:
            user_data = {
                "user_id": after.id,
                "sessions": [],
                "total_online_time": 0
            }
        
        # Handling online/offline updates
        if after.status == discord.Status.online:
            user_data["sessions"].append({
                "start_time": now,
                "game": after.activity.name if after.activity else "None"
            })
        elif after.status == discord.Status.offline:
            if user_data["sessions"] and "end_time" not in user_data["sessions"][-1]:
                user_data["sessions"][-1]["end_time"] = now
                session_time = (now - user_data["sessions"][-1]["start_time"]).total_seconds()
                user_data["total_online_time"] += session_time

        await activity_collection.replace_one({"user_id": after.id}, user_data, upsert=True)

@bot.event
async def on_member_update(before, after):
    if before.activities != after.activities:
        now = datetime.datetime.utcnow()
        game_activities = [activity for activity in after.activities if isinstance(activity, discord.Game)]
        for game in game_activities:
            user_data = await activity_collection.find_one({"user_id": after.id})
            if not user_data:
                user_data = {
                    "user_id": after.id,
                    "sessions": [],
                    "total_online_time": 0
                }
            if user_data["sessions"] and "game" not in user_data["sessions"][-1]:
                user_data["sessions"][-1]["game"] = game.name
                await activity_collection.replace_one({"user_id": after.id}, user_data, upsert=True)

# Break reminders
@tasks.loop(minutes=1)
async def check_for_breaks():
    now = datetime.datetime.utcnow()
    general_channel_id = 123456789012345678  # Replace with your general chat channel ID
    general_channel = bot.get_channel(general_channel_id)

    async for user_data in activity_collection.find():
        for session in user_data["sessions"]:
            if "end_time" not in session and not session.get("reminded", False):
                session_time = (now - session["start_time"]).total_seconds()
                if session_time > 2 * 60 * 60:  # 2 hours
                    user = bot.get_user(user_data["user_id"])
                    if general_channel and user:
                        reminder_message = await general_channel.send(
                            f"{user.mention}, you've been playing for more than 2 hours. Please take a break!"
                        )
                        session["reminded"] = True
                        await activity_collection.replace_one({"user_id": user_data["user_id"]}, user_data)
                        
                        # Delete the message after 5 minutes
                        await asyncio.sleep(300)  # 5 minutes in seconds
                        await reminder_message.delete()
# Weekly reports
@tasks.loop(hours=24 * 7)
async def generate_weekly_reports():
    now = datetime.datetime.utcnow()
    start_of_week = now - datetime.timedelta(days=7)
    reports = {}

    async for user_data in activity_collection.find():
        total_time = 0
        games_played = {}

        for session in user_data["sessions"]:
            if session["start_time"] >= start_of_week:
                total_time += (session["end_time"] - session["start_time"]).total_seconds()
                game = session.get("game", "Unknown")
                games_played[game] = games_played.get(game, 0) + 1

        user = bot.get_user(user_data["user_id"])
        if user:
            report = f"Weekly Report:\n- Total Online Time: {total_time / 3600:.2f} hours\n"
            report += "- Games Played:\n" + "\n".join([f"  {game}: {count} sessions" for game, count in games_played.items()])
            await user.send(report)

        reports[user_data["user_id"]] = {"total_time": total_time, "games": games_played}

    moderators_channel = bot.get_channel(moderator_chat)  # Replace with your moderator channel ID
    if moderators_channel:
        master_report = "\n\n".join([f"User: {user_id}\n{report}" for user_id, report in reports.items()])
        await moderators_channel.send(master_report)

# Run the bot
bot.run("bot_token")
