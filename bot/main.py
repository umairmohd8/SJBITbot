import discord
from private import keys

client = discord.Client()


@client.event
async def on_ready():
    ch = client.get_channel(846778354157355109)

    message = 'We have logged in as {0.user}'.format(client)
    await ch.send(message)
    # logger.send_log(message, client)
    print(message)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


client.run(keys.TOKEN)