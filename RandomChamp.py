import discord
import random
import requests

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$randomchamp'):
        champ_list_url = 'http://ddragon.leagueoflegends.com/cdn/14.14.1/data/en_US/champion.json'
        response = requests.get(champ_list_url)
        if response.status_code != 200:
            await message.channel.send("❌ Failed to load champion list.")
            return

        champ_data = response.json()['data']
        champ_names = list(champ_data.keys())
        random_champ = random.choice(champ_names)

        champ_info_url = f"http://ddragon.leagueoflegends.com/cdn/14.14.1/data/en_US/champion/{random_champ}.json"
        detail_response = requests.get(champ_info_url)
        if detail_response.status_code != 200:
            await message.channel.send(f"❌ Failed to fetch info for {random_champ}.")
            return

        champ_details = detail_response.json()['data'][random_champ]
        title = champ_details['title']
        blurb = champ_details['blurb']
        lore = champ_details['lore']
        tags = ', '.join(champ_details['tags'])
        image_url = f"http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{random_champ}_0.jpg"

        # Passive ability
        passive = champ_details['passive']
        passive_name = passive['name']
        passive_desc = passive['description']

        # Basic abilities
        spells = champ_details['spells']
        abilities = ""
        spell_keys = ['Q', 'W', 'E', 'R']
        for i, spell in enumerate(spells):
            abilities += f"**{spell_keys[i]} - {spell['name']}**: {spell['description']}\n"

        # Build the embed
        embed = discord.Embed(
            title=f"🎲 Random Champion: {random_champ} - {title}",
            description=blurb,
            color=discord.Color.purple()
        )
        embed.set_image(url=image_url)
        embed.add_field(name="Role(s)", value=tags, inline=False)
        embed.add_field(name="Lore", value=lore[:1024] + "..." if len(lore) > 1024 else lore, inline=False)
        embed.add_field(name=f"Passive - {passive_name}", value=passive_desc, inline=False)
        embed.add_field(name="Abilities", value=abilities[:1024] + "..." if len(abilities) > 1024 else abilities, inline=False)

        await message.channel.send(embed=embed)

# Be sure to store your token securely, not directly in your code
client.run("YOUR_BOT_TOKEN")
