#Open enkele benodigde Python libraries. Deze voegen functies toe aan dit stukje code.
import discord
from discord.ext import commands

# Discord.py bevat al een aantal functies en waarden waarmee het kan communiceren met discord. Om hiervan gebruik te maken hoeven we deze alleen maar in te roepen.

bot = commands.Bot(command_prefix='?', description="Beschrijving")

# Zodra de bot zich heeft aangemeld bij discord en is opgestart.
@bot.event
async def on_ready():
    # Toon in het terminal scher,
    print('Logged in as:')
    print('Username: ', bot.user)
    print('UserID: ', bot.user.id)
    print('------')


# Zodra een gebruiker de server joint.
@bot.event
async def on_member_join(member):
    # Controleer of dat op de server waarop dit gebeurt een system channel is.
    # Laten we eerst member.guild.system_channel ontleden:
    # member: geeft aan dat wij informatie willen hebben over diegene die de server joint,
    # guild: bevat informatie over de guild waarin dit gebeurt,
    # system_channel: bevat een variabele, een nummer waarin het channelid staat van het system channel. Als ik als server eigenaar een kanaal maak met de naam #test.
    #                 Dan krijgt #test een id, hernoem je #test naar #appelsap dan behoud het dat id.
    #                 We hebben hier te maken met een system channel, dus dit is het ene kanaal waarvan de server eigenaar in de server instellingen heeft aangegeven dat dit het kanaal is voor server berichten.
    #                 Als er geen system channel is dan bevat deze niet een id maar is deze leeg (None).
    if member.guild.system_channel is not None:
        # Als er een system channel is stuur er een bericht naar toe en heet de nieuwe gebruiker welkom.
        await member.guild.system_channel.send('Welkom {} op {}!'.format(member.mention, member.guild.name))


# Zodra een gebruiker de server verlaat.
@bot.event
async def on_member_remove(member):
    # Controleer of dat op de server waarop dit gebeurt een system channel is.
    if member.guild.system_channel is not None:
        # Als er een system channel is stuur er een bericht naar toe en laat weten dat gebruiker de server heeft verlaten.
        await member.guild.system_channel.send(
            '{} heeft {} verlaten, we zullen je missen!'.format(member.mention, member.guild.name))


# Zodra er een bericht binnenkomt.
@bot.event
async def on_message(message):
    # Als de afzender van het bericht een bot is.
    if message.author.bot == True:
        # Doe niets met het bericht.
        return

    # Een klein lijstje met 'scheldwoorden'.
    scheldwoorden = ['appelflap', 'perenboom']

    # Controleer voor iedere woord in het bericht of dat het voorkomt in de lijst met schelwoorden.
    if any(woord in message.content for woord in scheldwoorden):
        # Als het bericht een van deze woorden bevat, verwijder het bericht.
        await message.delete()
        # Stuur in het kanaal waaruit het bericht komt een melding en mention hierbij de dader.
        await message.channel.send('Foei {}, deed een bobba!'.format(message.author.mention))

    # Indien het niet een van de bovenstaande is voer de commando's uit.
    await bot.process_commands(message)


# Een commando zonder argumenten.
# Dit commando is bedoeld om te testen of dat de bot er nog is. Soms kunnen ze even vastlopen of lijkt het alsof ze online zijn.
# Wanneer je dit commando uitvoert met: ?ping
# Krijgt de gebruiker deze tekst te zien in het huidige kanaal vanaf waar de gebruiker het commando heeft uitgevoerd:
# Pong, ik ben er nog @Gebruiker
@bot.command()
async def ping(ctx):
    await ctx.message.channel.send("Pong, ik ben er nog {}.".format(ctx.message.author.mention))


# Een commando met meerdere argumenten. De hoeveelheid argumenten is vooraf aangegeven, maar de gebruiker mag ook minder
# argumenten neerzetten. Zijn het er meer geen probleem. Met al die extra argumenten wordt niets gedaan.
# Dit commando toont de quotes van Trump, Louis van Gaal en Louis van Dijk (geen idee wie dit is).
# Om de Trump quote te zien doe je het volgende: ?quote Trump
# Voor die van Louis van Gaal: ?quote Louis van Gaal
# Voor die van Louis van Dijk: ?quote Louis van Dijk
# Helaas is dit hoofdlettergevoelig, aan jou de taak om dit te fixen.
@bot.command()
async def quote(ctx, *args):
    await ctx.message.delete()
    if args[0] == "Trump":
        await ctx.message.channel.send("Despite the constant negative press covfefe - Trump 2019.")
    elif args[0] == "Louis":
        if args[1] == "van":
            if args[2] == "Gaal":
                await ctx.message.channel.send("The Death or the Gladiolus - Louis van Haal 2015.")
            elif args[2] == "Dijk":
                await ctx.channel.send("Klooien op de piano - Louis van Dijk.")
    else:
        await ctx.message.channel.send("Helaas wij hebben nog niet een quote van: {} {} {}".format(args[0], args[1], args[2]))

@quote.error
async def quote_error(ctx, error):
   await ctx.message.channel.send("Probeer eens: ?quote {voornaam} {tussenvoegsel} {achternaam}")

# Een commando met een oneindigaantal argumenten.
# Dit commando datgene laten zeggen dat achter de naam van het commando staat.
# Bijvoorbeeld bij: ?say Goedemorgen iedereen, hoe is het?
# Goedemorgen iedereen, hoe is het?
@bot.command()
async def zeg(ctx, *args):
    await ctx.message.delete()
    await ctx.message.channel.send(" ".join(args))

bot.run('change_me')
