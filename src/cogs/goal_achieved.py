from discord.commands import (  # Importing the decorator that makes slash commands.
    slash_command
)
from discord.ext import commands
from dotenv import load_dotenv
import os
import mysql.connector
from discord.commands import Option

load_dotenv()
DB_HOST = os.getenv("MYSQLHOST")
DB_USER = os.getenv("MYSQLUSER")
DB_PASSWORD = os.getenv("MYSQLPASSWORD")
DB_NAME = os.getenv("MYSQLDATABASE")
PORT = os.getenv("MYSQLPORT")

db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    port=PORT,
    pool_size=24
        )
cursor = db.cursor(buffered=True)

class GoalAchieved(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def goal_achieved(self, ctx, id: Option(int, "Enter the ID of the goal you wish to mark as achieved", required=True)):  # type: ignore
        """Log when you achieve a goal by goal ID"""
        db.commit()
        user_goal_id_verified = False
        achieved_goal_name = ""
        fetch_by_id = (id,)
        cursor.execute("SELECT user_id, goal FROM goal WHERE id = %s", fetch_by_id) # finds the goal corresponding to provided id
        for userandGoal in cursor: # loops through results
            user_id, goal = userandGoal # unpacks the resuts
            if user_id == str(ctx.author.id): # if the user of the requested goal is equal to the command invoker
                user_goal_id_verified = True # this is the right user
                achieved_goal_name = goal # gets the text of the goal
        if user_goal_id_verified == True: # if the user is correct
            value = (id,)
            mark_achieved = "UPDATE goal SET status = '1' WHERE id = %s"
            cursor.execute(mark_achieved, value)
            db.commit()
            await ctx.respond(
                f"**Congratulations...**\n<:pepe_hypers:925274715214458880> You have ACHIEVED `{achieved_goal_name}`\n**Collect your trophy:**\n:trophy:"
                )
        elif user_goal_id_verified == False: # if it's the wrong user
            await ctx.respond(
                "Hmm, something sus be going on here, maybe you made an error with the id? I'm not sure... but I wasn't able to log the goal as achieved T_T"
                    )

def setup(bot):
    bot.add_cog(GoalAchieved(bot))