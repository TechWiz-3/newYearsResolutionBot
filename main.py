# Created by #Zac the Wise#1381 with help from #iamkneel#2359

# Update created by Zac on 4/Jan

# Cleaned up large portion of document, added backlogs, addded comments and revised variable names up until view_goals function

# Version 2.8.0

import asyncio
from discord.commands import Option
from discord.ext import commands
from dotenv import load_dotenv
import os
import mysql.connector
from datetime import date, timedelta
from discord.utils import get
import discord
import random
# import aiohttp
# from discord import Webhook

load_dotenv()
BOT_TOKEN = os.getenv("TOKEN")
DB_HOST = os.getenv("MYSQLHOST")
DB_USER = os.getenv("MYSQLUSER")
DB_PASSWORD = os.getenv("MYSQLPASSWORD")
DB_NAME = os.getenv("MYSQLDATABASE")
PORT = os.getenv("MYSQLPORT")
DEV_GUILD_ID = 864438892736282625
PROD_GUILD_ID = 867597533458202644

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="goals!", intents=intents)

db = mysql.connector.connect(
    host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME, port=PORT
)

cursor = db.cursor(buffered=True)
secondcursor = db.cursor(buffered=True)
thirdcursor = db.cursor(buffered=True)
fourthCursor = db.cursor(buffered=True)
fifthCursor = db.cursor(buffered=True)

reminderFunnyText = ["The force wishes me to remind you of your goals, here they are.", "Did you think I'd let you forget about your goals? NOT A CHANCE", "How's it going mate?", "*Mighty presense decscends from sky to deliver a reminder to you*", "Ay bro, it's been some time, keep working at it", "Gravity Destroyers 2022 checking in with you"]
reminderForOneAchieved = ["You've made the first step, now it's time for the second one <:lezgooo:925286931221344256>", "Hard work, smart work let's go <:lezgooo:925286931221344256> <:lezgooo:925286931221344256>", "You got this baby, second goal achieve coming soon <:stronk_doge:925285801921769513>", "*Mighty presense decscends from sky to deliver a reminder to you*"]
reminderForTwoAchieved = ["Two goals achieved mate, the thirds gonna be a special one ;)", "Someones going for their 3rd goal this year <:lezgooo:925286931221344256>", "Third times a charm"]
reminderForThreePlusAchieved = ["This mans on a roll, keep it going bro", "Did you think I'd let you forget about your goals? NOT A CHANCE. You've come THIS far, next goal let's go", "Accountability session king achiever howsit going?", "Sup warrior, time to check in :sunglasses:"]
specificGoalDeleted = ["Can someone explain why?", "Who deletes their goals huh", "You just deleted a goal bruh, better make it up by adding two more", "Insane", "What is the meaning of life????? Humans make me doubt myself :rolling_eyes:"]
allGoalsDeleted = ["WTH THIS PEEP IS CRAZY", "Dude is on a KILLING RAMPAGE", "Somebody get the police, dude just deleted all his goals", "If you don't got goals you can't achieve em"]
reminderDeleted = ["Oh no, why did you delete your reminder T_T", "He deleted his reminders :(", "Man doesn't want to be reminded anymore?? Is this real??"]

# class sql:
#     def getGoals(self, cursorInstance):
#         getGoals = "query here"
#         return getGoals

@bot.event
async def on_ready():
    server = bot.get_guild(867597533458202644) # get Grav Destroyers server
    channel = server.get_channel(867599113825812481) #g et bots channel
    await channel.send("<@760345587802964010> remember to run the initialisation command") # ping me to remind me to run init command
    while True:
        # alternate between two bot statuses
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you achieve your goals"))
        await asyncio.sleep(5)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="get started | /help"))
        await asyncio.sleep(5)

@bot.slash_command(guild_ids=[DEV_GUILD_ID, PROD_GUILD_ID])
async def help(ctx):
    """Helps you use the bots commands"""
    about = f"**About Me**\nI'm a bot specifically created for Gravity Destroyers. My purpose is simple:\n<:agreentick:875244017833639956> Log users goals\n<:agreentick:875244017833639956> Remind users about their goals\n<:agreentick:875244017833639956> Help motivate and remind users to keep working at and achieve their goals :muscle:"
    await ctx.respond(
        f"{about}\n\n**New Year Goal Command**\nTo use this command, type `/newyeargoal` and click space, enter or tab, then type in your goal, type one goal at a time and keep it to raw text.\n\n**View Goals Command**\nTo use this command, type `/view_goals`\n\n**View Ids Command**\nTo use this command, type `/view_ids`. Each goal will be displayed with it's corresponding ID in bold.\n\n**Goal Achieved**\nTo use this command, type `/goal_achieved` then press tab and enter the ID corresponding to the goal you wish to mark as achieved.\n\n**Remind Me Command**\nThis command instructs the bot to remind you of your goals. To use it type `/remindme` then press tab and enter how often you wish to be reminded of your goals in days."
    )

@bot.slash_command(guild_ids=[DEV_GUILD_ID, PROD_GUILD_ID])
async def newyeargoal(ctx, *, goal: Option("Type the name of the goal (one only)", required=True)):
    """Log a goal, one at a time"""
    person = str(ctx.author) # get name
    personId = str(ctx.author.id) # get id
    status = False # set status if achieved to false
    finalValues = (person, goal, status, personId)
    insertGoals = "INSERT INTO 2022_Goals (user, goals, status, userId) VALUES (%s, %s, %s, %s)"
    cursor.execute(insertGoals, finalValues) # execute
    db.commit()
    await ctx.respond(
        f"Yessir\nYour goal is `{goal}`\n**I've logged it for you, NOW LET'S GO GET IT <:lezgooo:923128327970099231>**\nOh and also, remember to do `/remindme` to let me know how often to remind you about it!"
        )

@bot.slash_command(guild_ids=[DEV_GUILD_ID, PROD_GUILD_ID])
async def remindme(ctx, *, days: Option(int, "Enter how often you'd like to be reminded in days", required=True)):  # time in days
    """Tells the bot to remind you about your goals every x days"""
    goalsSet = False # automatically assume that goals haven't been set
    checkGoals = "SELECT * FROM 2022_Goals WHERE user = %s" # check if goals have been set
    values = (str(ctx.author),) # get the users name
    cursor.execute(checkGoals, values) # execute
    for entry in cursor: # loop through results if there are any
        goalsSet = True # goals indeed have been set
    if goalsSet == True: # go ahead to next check
        reminderSetPreviously = False # assume that a reminder has not been set before
        getReminders = "SELECT days FROM reminders WHERE user = %s" # find reminders set previously
        values = (str(ctx.author),) # users name
        secondcursor.execute(getReminders, values) # execute
        for reminder in secondcursor: # loop through results if they exist
            reminderSetPreviously = True # reminder has been set prevously
        if reminderSetPreviously == True: # reminder has been set previously
            # tell them off
            await ctx.respond(
                "MATE, like BRUH lmao :joy:\nYou've already set a reminder, are you trying to break me?\nBut what you can do... is reset your reminder time with `/change_reminder_interval`. Also if you don't wish to be reminded type `/stop_reminding`"
                    )
        else: # if reminder hasn't been set previously
            # finally execute remind me command
            setReminder = "INSERT INTO reminders (user, days) VALUES (%s, %s)" # insert days interval
            values = (str(ctx.author), days)
            cursor.execute(setReminder, values) # execute
            # set next reminder to today
            nextReminder = str(date.today()).replace(",", "-").replace(" ", "") # do i even need all the replace replace
            values = (str(ctx.author), nextReminder)
            # insert date into db
            setDate = "INSERT INTO nextDateReminder (user, next_date) VALUES (%s, %s)"
            cursor.execute(setDate, values)
            db.commit()
            await ctx.respond(
                f"Going to be reminding you every `{days}`\nTo check your next reminder `/next_reminder`\n\n*Good job bruh, now time to get to work <:stronk_doge:925285801921769513> <:lezgooo:925286931221344256> If you need help, we got you <#867600399879372820>*"
            )
    elif goalsSet == False: # if goals haven't been set
            await ctx.respond(
            "Well it's great that you want to be reminded, but make sure you set goals first `/newyeargoal` :grin:"
            )

@bot.slash_command(guild_ids=[DEV_GUILD_ID, PROD_GUILD_ID])
async def view_goals(ctx):
    """Displays your currently logged and achieved goals"""
    goalsSet = False
    final = ""
    finalAchieved = ""
    goalsCounter = 0
    goalsAchievedCounter = 0
    author = (str(ctx.author),)
    getGoals = "SELECT goals FROM 2022_Goals WHERE user = %s"
    cursor.execute(getGoals, author)
    for x in cursor:
        goalsSet = True
        final += str(x)
        goalsCounter += 1
        # if achieved add a green tick to the message
        # add a counter to say that another goal has been achieved
    final = (
        final.replace("(", "").replace(")", "").replace("'", "``").replace(",", "\n")
    )
    cursor.execute(
        "SELECT goals FROM 2022_Goals WHERE user = %s AND status = '1'", (author)
    )
    for x in cursor:
        finalAchieved += str(x)
        goalsAchievedCounter += 1
    print(goalsAchievedCounter)
    # check the status for each goal with the username
    if goalsAchievedCounter > 0:
        await ctx.respond(
            f"Your goals are...\n\n{final}\n**<:pepe_hypers:925274715214458880> You have achieved __{goalsAchievedCounter}__ out of __{goalsCounter}__ goals**\nKEEP GRINDING <:pepebuff:874499841407983647> <:pepebuff:874499841407983647>"
        )
    elif goalsSet == True:
        await ctx.respond(
            f"Your goals are...\n\n{final}\nYou haven't achieved any of your {goalsCounter} goals, but that doesn't matter, **TRAIN HARD TRAIN SMART** (that's what Gravity Destroyers is for) and you'll get there <:lezgooo:925286931221344256> <:lezgooo:925286931221344256>"
        )
    elif goalsSet == False:
        await ctx.respond("You need to set your goals first before viewing them -_-\n\n*However, I live go serve bright human... these commands may help...* `/help` `/newyeargoal`")

@bot.slash_command(guild_ids=[DEV_GUILD_ID, PROD_GUILD_ID])
async def view_ids(ctx):
    """Displays each logged called and it's unique ID to access"""
    author = str(ctx.author)
    print(author)
    final = ""
    author = (str(ctx.author),)
    print(author)
    sql = "SELECT goals, id FROM 2022_Goals WHERE user = %s"
    cursor.execute(sql, (author))
    for x in cursor:
        xx = (
            str(x)
            .replace(",", "  **")
            .replace("'", "``")
            .replace("(", "")
            .replace(")", "**\n")
        )
        final += str(xx)
    await ctx.respond(final)


@bot.slash_command(guild_ids=[DEV_GUILD_ID, PROD_GUILD_ID])
async def goal_achieved(ctx, id: Option(int, "Enter the ID of the goal you wish to mark as achieved", required=True)):
    """Log when you achieve a goal by goal ID"""
    final = ""
    fetchByID = tuple(id)
    cursor.execute("SELECT goals FROM 2022_Goals WHERE id = %s", (fetchByID))
    for x in cursor:
        print(x)
        xx = (
            str(x)
            .replace(",", " ")
            .replace("'", "")
            .replace("(", "")
            .replace(")", "\n")
        )
        final += str(xx)
    value = tuple(id)
    print(value)
    sql = "UPDATE 2022_Goals SET status = '1' WHERE id = %s"
    cursor.execute(sql, value)
    db.commit()
    await ctx.respond(
        f"**Congratulations...**\n<:pepe_hypers:925274715214458880> You have ACHIEVED `{final}`**Collect your trophy:**\n:trophy:"
    )

@bot.command()
async def initialise(ctx):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send(content=f"**{ctx.author.mention} You don't have the right permissions for that.**\n||But between you and me, nice try lmao, sadly Zac foresaw that clever bois like you would try stuff like that\nAlso, DON'T TELL HIM I SAID THIS, imma delete the message||", delete_after = 7)
        return
    counter = 0
    while True:
        goals = ""
        sql = "SELECT user, days FROM reminders"  # select the username and their selected reminder interval
        cursor.execute(sql)  # execute sql query
        for (username, howOften) in cursor:  # loop through the results of the sql query
            sql = "SELECT user, next_date FROM nextDateReminder WHERE user = %s"
            value = (username,)
            secondcursor.execute(sql, value)
            for dateEntry in secondcursor:
                userForThirdQuery, unpackedDate = dateEntry
                server = bot.get_guild(PROD_GUILD_ID)
                reminderChannel = server.get_channel(867599113825812481)
                slashEmoji = discord.utils.get(bot.emojis, name="aslash")
                greenTickEmoji = discord.utils.get(bot.emojis, name="epicTick")
                if unpackedDate == date.today():
                    sql = "SELECT goals,status,userId FROM 2022_Goals WHERE user = %s"  # request for the users goals in the goals table
                    userRequest = (userForThirdQuery,)
                    thirdcursor.execute(sql, userRequest)  # execute sql query
                    statusCounter = 0
                    global memberObject
                    for (
                        goalAndStatus
                    ) in thirdcursor:  # loop the the results of the latest query
                        goal,status,idByMember = goalAndStatus #assign the variables returned
                        idByMember = int(idByMember)
                        try:
                            memberObject = bot.get_user(int(idByMember))
                        except:
                            memberObject = f'User mention failed {userForThirdQuery}'
                            print('Issue occured, none was returned as memberObject as shown here', memberObject)
                        if status == 1:
                            goals += f'{greenTickEmoji} `{goal}`\n'
                            statusCounter+=1
                        elif status == 0:
                            goals += f'{slashEmoji} `{goal}`\n'   
                    if statusCounter == 0:
                        sendFunnyText = random.choice(reminderFunnyText)
                        try:
                            await reminderChannel.send(
                                f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                        except:
                            await reminderChannel.send(
                                f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                    elif statusCounter == 1:
                        sendFunnyText = random.choice(reminderForOneAchieved)
                        try:
                            await reminderChannel.send(
                                f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                        except:
                            await reminderChannel.send(
                                f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                    elif statusCounter == 2:
                        sendFunnyText = random.choice(reminderForTwoAchieved)
                        try:
                            await reminderChannel.send(
                                f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                        except:
                            await reminderChannel.send(
                                f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                    elif statusCounter > 2:
                        sendFunnyText = random.choice(reminderForThreePlusAchieved)
                        try:
                            await reminderChannel.send(
                                f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                        except:
                            await reminderChannel.send(
                                f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                    goals = "" #reset goals variable
                    # insertSql = "INSERT INTO nextDateReminder (user, next_date) VALUES (%s, %s)"
                    updateSql = "UPDATE nextDateReminder SET next_date = %s WHERE user = %s"
                    nextDate = date.today() + timedelta(days=howOften)
                    valuesForChangingDate = (nextDate, userForThirdQuery)
                    fourthCursor.execute(updateSql, valuesForChangingDate)
                    db.commit()
                    await ctx.send("**End of mighty reminder message**")
                elif unpackedDate < date.today(): #if the table is outdated
                    print("Date smaller than current date triggered for", userForThirdQuery)
                    sql = "SELECT goals,status,userId FROM 2022_Goals WHERE user = %s"  # request for the users goals in the goals table
                    userRequest = (userForThirdQuery,)
                    thirdcursor.execute(sql, userRequest)  # execute sql query
                    statusCounter = 0
                    for (
                        goalAndStatus
                    ) in thirdcursor:  # loop the the results of the latest query
                        goal,status,idByMember = goalAndStatus #assign the variables returned
                        try:
                            memberObject = bot.get_user(int(idByMember))
                        except:
                            memberObject = f'User mention failed {userForThirdQuery}'
                            print('Issue occured, none was returned as memberObject as shown here', memberObject)
                        if status == 1:
                            goals += f'{greenTickEmoji} `{goal}`\n'
                            statusCounter +=1
                        elif status == 0:
                            goals += f'{slashEmoji} `{goal}`\n'
                    #print users goals to remind them
                    if statusCounter == 0:
                        sendFunnyText = random.choice(reminderFunnyText)
                        await reminderChannel.send(f"{sendFunnyText}\n{goals}")  # print the users goals
                    elif statusCounter == 1:
                        sendFunnyText = random.choice(reminderForOneAchieved)
                        try:
                            await reminderChannel.send(
                                f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                        except:
                            await reminderChannel.send(
                                f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                    elif statusCounter == 2:
                        sendFunnyText = random.choice(reminderForTwoAchieved)
                        try:
                            await reminderChannel.send(
                                f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                        except:
                            await reminderChannel.send(
                                f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                    elif statusCounter > 2:
                        sendFunnyText = random.choice(reminderForThreePlusAchieved)
                        try:
                            await reminderChannel.send(
                                f"{memberObject.mention}\n**{sendFunnyText}**\n\n{goals}"
                                ) # print the users goals
                        except:
                            await reminderChannel.send(
                                f"{memberObject}\n**{sendFunnyText}**\n\n{goals}"
                                )  # print the users goals
                    goals = "" #reset goals variable
                    updateSql = "UPDATE nextDateReminder SET next_date = %s WHERE user = %s"
                    nextDate = date.today() + timedelta(days=howOften)
                    valuesForChangingDate = (nextDate, userForThirdQuery)
                    fourthCursor.execute(updateSql, valuesForChangingDate)
                    db.commit()
                    await ctx.send("**End of mighty reminder message**")
        
        await asyncio.sleep(120)

@bot.slash_command(guild_ids=[DEV_GUILD_ID, PROD_GUILD_ID])
async def clear_goals(ctx, id: Option(int, "Enter the ID of the goal you wish to delete", required=False)):
    """Delete all logged goals, or a specific goal based on ID"""
    if id == None:
        deleteGoals = "DELETE FROM 2022_Goals WHERE user = %s"
        deleteReminderEntries = "DELETE FROM reminders WHERE user = %s"
        deleteDateReminderEntries = "Delete FROM nextDateReminder WHERE user = %s"
        user = (str(ctx.author),)
        cursor.execute(deleteGoals, user)
        cursor.execute(deleteReminderEntries, user)
        cursor.execute(deleteDateReminderEntries, user)
        db.commit()
        await ctx.respond(
            f"All goals deleted. {random.choice(allGoalsDeleted)}\nNow time to put new ones in `/newyeargoal`\n*Also, your reminders have been removed*"
            )
    else:
        sql = "DELETE FROM 2022_Goals WHERE user = %s AND id = %s"
        user = str(ctx.author)
        goalId = int(id)
        values = (user, goalId)
        cursor.execute(sql, values)
        db.commit()
        await ctx.respond(
            f"Specific goal deleted {random.choice(specificGoalDeleted)}"
            )

@bot.slash_command(guild_ids=[DEV_GUILD_ID, PROD_GUILD_ID])
async def stop_reminding(ctx):
    """Stops the bot from reminding you about your goals"""
    deleteReminderEntries = "DELETE FROM reminders WHERE user = %s"
    deleteDateReminderEntries = "Delete FROM nextDateReminder WHERE user = %s"
    user = (str(ctx.author),)
    cursor.execute(deleteReminderEntries, user)
    cursor.execute(deleteDateReminderEntries, user)
    db.commit()
    await ctx.respond(
        f"{random.choice(reminderDeleted)}\nDo `/remindme` again to change the interval. If not then we're sad to see you go... all the best"
    )

@bot.slash_command(guild_ids=[DEV_GUILD_ID, PROD_GUILD_ID])
async def change_reminder_interval(ctx, how_often: int):
    """Adjusts how often you're reminded of your goals"""
    adjustInterval = "UPDATE reminders SET days = %s WHERE user = %s"
    values = (how_often, str(ctx.author))
    cursor.execute(adjustInterval, values)
    adjustIntervalDate = "UPDATE nextDateReminder SET next_date = %s WHERE user = %s"
    values = (
        str(date.today()),
        str(ctx.author)
        )
    cursor.execute(adjustIntervalDate, values)
    db.commit()
    cooldoge = discord.utils.get(bot.emojis, name="cooldoge")
    await ctx.respond(
        f"{cooldoge} Well, that went well. Your interval is now `{how_often}` day(s). Achievement time babyy"
        )

@bot.slash_command(guild_ids=[DEV_GUILD_ID, PROD_GUILD_ID])
async def next_reminder(ctx):
    """Shows you how often you'll be reminded as well as your next reminder date"""
    reminderSet = False
    howOften = 0
    nextDate = None
    getReminderInterval = "SELECT days FROM reminders WHERE user = %s"
    values = (str(ctx.author),)
    cursor.execute(getReminderInterval, values)
    for entry in cursor:
        reminderSet = True
        howOften, = entry
    getNextReminderDate = "SELECT next_date FROM nextDateReminder WHERE user = %s"
    secondcursor.execute(getNextReminderDate, values)
    for dateEntry in secondcursor:
        nextDate, = dateEntry
    if reminderSet == True:
        await ctx.respond(
            f"You have set to be reminded every `{howOften}` day(s) and your next reminder is on `{nextDate}` meanwhile... KEEP GRINDING <:lezgooo:925286931221344256>"
            )    
    elif reminderSet == False:
        umEmoji = discord.utils.get(bot.emojis, name="um")
        await ctx.respond(
            f"{umEmoji} you need to set a reminder first before viewing it... `/remindme`"
            )

@bot.slash_command(guild_ids=[DEV_GUILD_ID, PROD_GUILD_ID])
async def get_started(ctx):
    """Helps you get started :)"""
    interaction = await ctx.respond(
        f"Ayo {ctx.author.mention} so you want to get after those goals and make this year, YOUR year. Well GOOD NEWS, I'm here to help..."
        )
    async with ctx.typing():
        await asyncio.sleep(7)
    content = "**This is how I help you:**\n`/help` The help command is your go to command to understand anything, but here's the recommended sequence of commands:"
    await interaction.followup.send(content=content)
    async with ctx.typing():
        await asyncio.sleep(10)
    content = "Run`**/newyeargoal`** for **each** new year goal you wish to achieve.\nRun **`/view_goals`** to ensure that all your goals havee been logged.\nRun **`/remindme`** to set how often you'll be reminded."
    await interaction.followup.send(content=content)
    async with ctx.typing():
        await asyncio.sleep(7)
    content = "For more command use the `/help` command. If you enounter any issues pls ping `@Zac the Wise#1381` :)"
    await interaction.followup.send(content=content)

bot.run(BOT_TOKEN)
