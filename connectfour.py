from discord.ext import commands
import ConnectFourAI
from itertools import cycle
import time
import random
import discord


class ConnectFour(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def connect_four(self, ctx):

        def check_reaction(reaction, user):
            if reaction.emoji in ['💢']:
                return reaction.message.id == sent_embed.id and user == ctx.author
            if reaction.emoji in reactions:
                for k, emoji in enumerate(reactions):
                    if emoji == reaction.emoji:
                        if board[0][k] == '⚪':
                            return reaction.message.id == sent_embed.id and user == current_player
            return False

        reactions = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬']
        # board = [['⚪']*7 for i in range(6)]
        board = [['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'],  # board[0][0-6]
                 ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'],  # board[1][0-6}
                 ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'],
                 ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'],
                 ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪'],
                 ['⚪', '⚪', '⚪', '⚪', '⚪', '⚪', '⚪']]
        p1 = ctx.author
        emoji_list = ['🔴', '🔵']
        random.shuffle(emoji_list)
        alt_emoji = cycle(emoji_list)
        loading_gifs = ['https://cdn.discordapp.com/attachments/488700267060133889/779516535425335307/giphy.gif',
                        'https://cdn.discordapp.com/attachments/488700267060133889/779518965923184641/tvnJsU7.gif',
                        'https://cdn.discordapp.com/attachments/488700267060133889/779518988194938960/giphy_1.gif',
                        'https://cdn.discordapp.com/attachments/488700267060133889/779519005941170186/custom-loading-'
                        'icon.gif',
                        'https://cdn.discordapp.com/attachments/488700267060133889/779519030301294592/giphy_2.gif',
                        'https://cdn.discordapp.com/attachments/488700267060133889/779519058936070164/thA1t5G.gif',
                        'https://cdn.discordapp.com/attachments/488700267060133889/779519089998692372/giphy_3.gif',
                        'https://cdn.discordapp.com/attachments/488700267060133889/779519118672003072/giphy-downsized.'
                        'gif',
                        'https://cdn.discordapp.com/attachments/488700267060133889/779519144869494804/187917b0606c80a6'
                        'c295da1f19ff3e40.gif',
                        'https://cdn.discordapp.com/attachments/488700267060133889/779519172622155806/7dfd95dd9ad07e7'
                        'af1eaff34a890b322.gif']
        working = True

        # Options Menu #
        embed = discord.Embed(description=f'{ctx.author.mention} is waiting... \n 📲: **Join the game**',
                              color=0xff0000)
        embed.set_author(name='Connect Four', icon_url='https://cdn.discordapp.com/attachments/488700267060133889/6993'
                                                       '43937965654122/ezgif-7-6d4bab9dedb9.gif')
        sent_embed = await ctx.send(embed=embed)
        await sent_embed.add_reaction('💢')
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
        await sent_embed.clear_reactions()

        # Loading Connect4 #
        embed.description = 'Loading...'
        embed.set_thumbnail(url=random.choice(loading_gifs))
        await sent_embed.edit(embed=embed)
        for emoji in reactions:
            await sent_embed.add_reaction(emoji)
        sent_embed = await self.bot.get_channel(ctx.channel.id).fetch_message(sent_embed.id)

        if reaction.emoji == '💢':
            depth = 7
            bot_time = 10
            turns = 0
            p_time = 0
            p_list = [self.bot.user, p1]
            random.shuffle(p_list)
            alt_player = cycle(p_list)
            longest_time = 0
            prev_nodes = 0
            lowest_score = 0
            highest_score = 0
            odd = False
            if next(alt_player) == self.bot.user:
                odd = True
            bot_mark = next(alt_emoji)
            p_mark = next(alt_emoji)
            next(alt_player)

            # Actual Game #
            while working:
                current_player = next(alt_player)
                current_emoji = next(alt_emoji)
                other_player = next(alt_player)
                other_emoji = next(alt_emoji)
                next(alt_player)
                next(alt_emoji)
                joined_board = ["|".join(reactions), "|".join(board[0]), "|".join(board[1]), "|".join(board[2]),
                                "|".join(board[3]), "|".join(board[4]), "|".join(board[5])]
                current_heursitic = ConnectFourAI.board_heuristic(board=board, bot_piece=bot_mark, player_piece=p_mark,
                                                                  odd=odd)
                if current_heursitic < lowest_score:
                    lowest_score = current_heursitic
                elif current_heursitic > highest_score:
                    highest_score = current_heursitic
                if bot_time > longest_time:
                    longest_time = bot_time
                turns += 1

                # Player's turn
                if current_player == p1:
                    embed.set_thumbnail(url=embed.Empty)
                    embed.description = f'{p1.mention}({current_emoji}) Make your move \n \n Current bot score: ' \
                        f'{current_heursitic} \n \n I took **{bot_time} seconds** \n \n I explored **{prev_nodes} ' \
                        f'nodes** \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n ' \
                        f'{joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]}'
                    await sent_embed.edit(embed=embed)
                    start = time.time()
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=300.0, check=check_reaction)
                    await sent_embed.remove_reaction(reaction.emoji, user)
                    for i, emoji in enumerate(reactions):
                        if emoji == reaction.emoji:
                            for row in reversed(board):
                                if row[i] == '⚪':
                                    row[i] = current_emoji
                                    break
                    end = time.time()
                    p_time = round(end - start, 2)

                # AI's Turn #
                elif current_player == self.bot.user:
                    embed.set_thumbnail(url=random.choice(loading_gifs))
                    embed.description = f'{self.bot.user.mention}({current_emoji}) is thinking... \n \n Current bot ' \
                        f'score: {current_heursitic} \n \n You took **{p_time} seconds** \n \n {joined_board[0]} \n ' \
                        f'{joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} \n {joined_board[4]} \n ' \
                        f'{joined_board[5]} \n {joined_board[6]}'
                    await sent_embed.edit(embed=embed)
                    start = time.time()
                    move, nodes_explored = ConnectFourAI.find_best_move(board=board, bot_piece=bot_mark,
                                                                        player_piece=p_mark, depth=depth, odd=not odd)
                    prev_nodes = nodes_explored
                    board[move[0]][move[1]] = current_emoji
                    end = time.time()
                    bot_time = round(end - start, 2)

                # Evaluate Board #
                joined_board = ["|".join(reactions), "|".join(board[0]), "|".join(board[1]), "|".join(board[2]),
                                "|".join(board[3]), "|".join(board[4]), "|".join(board[5])]
                result = ConnectFourAI.check_board_state(board)
                if result == 'TIE':
                    embed.set_thumbnail(url=embed.Empty)
                    working = False
                    embed.description = f'Tie between {current_player.mention}({current_emoji}) and ' \
                        f'{other_player.mention}({other_emoji}) \n \n My **highest score** was **{highest_score}** ' \
                        f'\n My **lowest score** was **{lowest_score}** \n My **longest move** took **{longest_time} ' \
                        f'seconds** \n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n ' \
                        f'{joined_board[3]} \n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]}'
                    embed.set_footer(text='')
                    await sent_embed.edit(embed=embed)
                    await sent_embed.clear_reactions()
                elif result in ['🔴', '🔵']:
                    embed.set_thumbnail(url=embed.Empty)
                    working = False
                    embed.description = f'{current_player.mention}({current_emoji}) Wins \n {other_player.mention}' \
                        f'({other_emoji}) Loses \n \n My **highest score** was **{highest_score}** \n My **lowest ' \
                        f'score** was **{lowest_score}** \n My **longest move** took **{longest_time} seconds** ' \
                        f'\n \n {joined_board[0]} \n {joined_board[1]} \n {joined_board[2]} \n {joined_board[3]} ' \
                        f'\n {joined_board[4]} \n {joined_board[5]} \n {joined_board[6]}'
                    embed.set_footer(text='')
                    await sent_embed.edit(embed=embed)
                    await sent_embed.clear_reactions()


def setup(bot):
    bot.add_cog(ConnectFour(bot))
