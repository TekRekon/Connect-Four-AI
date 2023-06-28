import asyncio
import random
import time

import discord
import randfacts
from discord.ext import commands

import Board
import ConnectFourAI
import constants as c


class ConnectFour(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print("ConnectFour initiated")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def connect_four(self, ctx):

        def check_reaction(reaction, user):
            if reaction.emoji in ['📲']:
                return reaction.message.id == sent_embed.id and user == ctx.author
            if reaction.emoji in c.reactions:
                if bd.get_board()[0][c.reactions.index(reaction.emoji)] == '⚪':
                    return reaction.message.id == sent_embed.id and user == p_list[curr_ind]
            return False

        # Options Menu #
        embed = discord.Embed(description=f'{ctx.author.mention} is waiting... \n 📲: **Play the AI**', color=0xff0000)
        embed.set_author(name='Connect Four', icon_url=c.connect_four_icon)
        sent_embed = await ctx.send(embed=embed)
        await sent_embed.add_reaction('📲')
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check_reaction)
        await sent_embed.clear_reactions()

        # Loading Connect4 #
        embed.description = 'Loading...'
        embed.set_thumbnail(url=random.choice(c.loading_gifs))
        await sent_embed.edit(embed=embed)
        for emoji in c.reactions: await sent_embed.add_reaction(emoji)
        sent_embed = await self.bot.get_channel(ctx.channel.id).fetch_message(sent_embed.id)

        working = True

        if reaction.emoji == '📲':
            depth = 8
            bot_time = 0
            p_time = 0
            turns = 0
            bot_longest_time = 0
            bot_total_time = 0
            player_longest_time = 0
            player_total_time = 0
            max_nodes = 0
            total_nodes = 0
            prev_play = 0
            prev_nodes = 0
            prev_score = 0
            p_list = [ctx.author, self.bot.user]
            emoji_list = c.emoji_list
            random.shuffle(emoji_list)
            emoji_list = emoji_list[0:2]
            random.shuffle(p_list)
            curr_ind = 0
            odd = False
            bot_ind = 1
            if p_list[0] == self.bot.user:
                odd = True # If the bot goes first, it will be odd
                bot_ind = 0
            bd = Board.Board(emoji_list[0], emoji_list[1])

            # Actual Game #
            while working:

                # Player's turn
                if p_list[curr_ind] == ctx.author:
                    embed.set_thumbnail(url=p_list[curr_ind].avatar_url)
                    embed.description = f'{p_list[curr_ind].mention}({emoji_list[curr_ind]}) Make your move \n \n' \
                                        f'I took **{bot_time}** seconds \n \n I explored **{prev_nodes}** nodes \n \n My move score was {prev_score} \n \n My move was {c.reactions[prev_play]} \n \n {bd.get_printable_board()}'
                    await sent_embed.edit(embed=embed)
                    start = time.time()
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=500.0, check=check_reaction)
                    await sent_embed.remove_reaction(reaction.emoji, user)
                    i = c.reactions.index(reaction.emoji)
                    bd.make_move(i, curr_ind+1)
                    end = time.time()
                    p_time = round(end - start, 2)
                    player_total_time += p_time
                    if p_time>player_longest_time: player_longest_time = p_time


                # AI's Turn #
                elif p_list[curr_ind] == self.bot.user:
                    embed.set_thumbnail(url=random.choice(c.loading_gifs))
                    embed.description = f'{self.bot.user.mention}({emoji_list[curr_ind]}) is thinking... \n \n' \
                                        f'You took **{p_time}** seconds \n \n {bd.get_printable_board()}'
                    embed.set_footer(text=f'{randfacts.getFact(filter=False)}')
                    await sent_embed.edit(embed=embed)
                    start = time.time()
                    move, nodes_explored, score = ConnectFourAI.find_best_move(bd=bd, bot_piece=emoji_list[curr_ind],
                                                                               player_piece=emoji_list[1 - curr_ind],
                                                                               depth=depth, turns=turns, ind=curr_ind)
                    prev_nodes = nodes_explored
                    prev_score = score
                    prev_play = move
                    total_nodes += prev_nodes
                    if prev_nodes > max_nodes: max_nodes = prev_nodes
                    bd.make_move(move, curr_ind + 1)
                    end = time.time()
                    bot_time = round(end - start, 2)
                    bot_total_time += bot_time
                    if bot_time > bot_longest_time: bot_longest_time = bot_time
                    await asyncio.sleep(1)

                # Evaluate Board #
                turns += 1
                bd.bitboard_to_board()
                result = bd.get_board_state()
                if result == 'TIE':
                    embed.set_thumbnail(url=embed.Empty)
                    working = False
                    embed.description = f'Tie between {p_list[0].mention}({emoji_list[0]}) and ' \
                        f'{p_list[1].mention}({emoji_list[1]}) \n \n My longest move took **{bot_longest_time}** ' \
                        f'seconds \n \n Your longest move took **{player_longest_time}** seconds \n \n My average turn took **{round(bot_total_time/(turns/2), 2)}** seconds \n \n Your average turn took **{round(player_total_time/(turns/2), 2)}** seconds \n \n Total nodes explored: **{total_nodes}** \n \n Max nodes explored in a turn: **{max_nodes}** \n \n Game ended in **{turns}** turns \n \n Total game time: **{player_total_time+bot_total_time}** seconds \n \n {bd.get_printable_board()}'
                    embed.set_footer(text='')
                    await sent_embed.edit(embed=embed)
                    await sent_embed.clear_reactions()
                elif result in emoji_list:
                    embed.set_thumbnail(url=embed.Empty)
                    working = False
                    embed.description = f'{p_list[curr_ind].mention}({emoji_list[curr_ind]}) Wins \n {p_list[1-curr_ind].mention}' \
                                        f'({emoji_list[1 - curr_ind]}) Loses \n \n My longest move took **{bot_longest_time}** seconds ' \
                                        f'\n \n Your longest move took **{player_longest_time}** seconds \n \n My average turn took **{round(bot_total_time / (turns / 2), 2)}** seconds \n \n Your average turn took **{round(player_total_time / (turns / 2), 2)}** seconds \n \n Total nodes explored: **{total_nodes}** \n \n Max nodes explored in a turn: **{max_nodes}** \n \n Game ended in **{turns}** turns \n \n Total game time: **{round(player_total_time + bot_total_time, 2)}** seconds \n \n {bd.get_printable_board()}'
                    embed.set_footer(text='')
                    await sent_embed.edit(embed=embed)
                    await sent_embed.clear_reactions()

                if curr_ind == 0: curr_ind = 1
                else: curr_ind = 0


def setup(bot):
    bot.add_cog(ConnectFour(bot))
