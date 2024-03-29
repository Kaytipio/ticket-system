import discord
from discord.ext import commands
import datetime
import discord.ui
from discord.ui import View, Button, Select


bot = commands.Bot(command_prefix=".", intents=discord.Intents.all(), status=discord.Status.online, activity=discord.Game(name=".helpme"))




async def ticketcallback(interaction):
    guild = interaction.guild
    role = discord.utils.get(guild.roles, name="Kaytipio")
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        interaction.user: discord.PermissionOverwrite(view_channel=True),
        role: discord.PermissionOverwrite(view_channel=True)
    }

    select = Select(options=[
        discord.SelectOption(label="Hire Kaytipio", value="01", emoji="🎫", description="This will open a ticket to hire Kaytipio"),
        discord.SelectOption(label="Help ticket", value="02", emoji="🎟️", description="This will open a ticket to recive help")
    ])

    async def my_callback(interaction):
        if select.values[0] == "01":
            category = discord.utils.get(guild.categories, name="Hire Kaytipio")
            channel = await guild.create_text_channel(f"{interaction.user.name}-ticket", category=category, overwrites=overwrites)
            await interaction.response.send_message(f"Created ticket - {channel.id}", ephemeral=True)
            await channel.send("Hello, how i can help you")
        
        elif select.values[0] == "02":
            category = discord.utils.get(guild.categories, name="Helping Tickets")
            channel = await guild.create_text_channel(f"{interaction.user.name}-ticket", category=category, overwrites=overwrites)
            await interaction.response.send_message(f"Created ticket - {channel.id}", ephemeral=True)
            await channel.send("Hello, how i can help you")
    select.callback = my_callback
    view = View(timeout=None)
    view.add_item(select)
    await interaction.response.send_message("Chose an option bellow", view=view, ephemeral=True)
    
@bot.command()
async def ticket(ctx):
    button = Button(label="📥 Create a ticket", style=discord.ButtonStyle.green)
    button.callback = ticketcallback
    view = View(timeout=None)
    view.add_item(button)
    await ctx.send("Open a ticket bellow", view=view)

@bot.command()
async def close(ctx):
    if not ctx.channel.name.endswith("-ticket"):
        return await ctx.send("This command is only for a tickets.")

    if not ctx.author.guild_permissions.manage_channels:  
        return await ctx.send("You dont have permsions to close tickets.")

    try:
        await ctx.channel.delete()
        await ctx.send(f"Ticket closed by {ctx.author.mention}")
    except discord.HTTPException as e:
        await ctx.send(f"Error to close the ticket: {e}")



bot.run("Your token here")
