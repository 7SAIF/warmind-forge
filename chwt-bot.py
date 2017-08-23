#!/bin/python3

import asyncio
import sqlite3
import discord
import random
from warmind import Fireteam_Actions
from warmind import SQL_Actions
from warmind import AI_Actions
from warmind.Global_Variables import *

ai_actions = AI_Actions.AIFunctions()
sql_actions = SQL_Actions.SQLFunctions()
fireteam_actions = Fireteam_Actions.FireteamFunctions()

fireteam_actions.expired_calendar_cleanup()
current_jugs = "(.) (.)"

server = "https://discordapp.com/api/servers/209503319205478401/widget.json"
channel = discord.Object(id='209695933796057089')
client = discord.Client()


def join_server():
    devid = "209508738011365377"
    devserver = "https://discordapp.com/api/servers/" + devid + "/widget.json"
    devchannel = discord.Object(id='209508738011365377')
    devclient = discord.Client()
    url = "https://discordapp.com/oauth2/authorize?client_id=213354402235416576&scope=bot&permissions=536345663"


@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    # yield from client.send_message(discord.Message.channel, 'AI-COMS: Initializing Channel Interface')
    print('------')


# 209695933796057089
@asyncio.coroutine
def my_background_task():
    yield from client.wait_until_ready()
    intercom_select = random.randint(0, intercom_quantity)
    intercom_message = intercom[intercom_select]
    channel = discord.Object(id='209695933796057089')
    yield from client.send_message(channel, 'AI-COMS // Initializing Channel Interface')
    # while not client.is_closed:
    #     yield from client.send_message(channel, "INTERCOM // "+intercom_message)
    #     yield from asyncio.sleep(randint(1080,2880)) # task runs randomly between 18 minutes and 48 minutes


@client.event
@asyncio.coroutine
def on_message(message):
    # we do not want the bot to reply to itself
    author = str(message.author)
    if message.author == client.user:
        return

    if message.content.startswith('!help'):
        msg = ('AI-COMS // {0.author.mention} COMMAND SYNTAX: '
               '\n `!light` conveys last culled light levels '
               '\n `!event` schedules an incursion '
               '\n `!court` conveys Tier 3 Court of Oryx Challenger '
               '\n `!kfraid` conveys the Challenge Mode '
               '\n `!nightfall` coveys Nightfall maps and skulls'
               '\n `!coe` coveys Challenge of the Elders data'
               '\n `!heroic` coveys Daily Heroic Strike data'
               '\n `!strike` coveys Vanguard Strike data'
               '\n `!dcp` coveys Daily Crucible data'
               '\n `!wcp` coveys Weekly Crucible data'
               '\n `!test` repeats !test message'
               '\n `!hello` to say hello ').format(message)
        yield from client.send_message(message.channel, msg)

    if message.content.startswith('!fraggle') and author == "MtnFraggle#9145":
        msg = '{0.author.mention} 9er asked me to tell you this: ' \
              'To quote: Hey glorious leader, go to take selfie video while you read this `!morefraggle` \n' \
              'You are to send me the video of you examining and using these instructions. ' \
              'Next communication is from 9er'.format(message)
        yield from client.send_message(message.channel, msg)

    if message.content.startswith('!morefraggle') and author == "MtnFraggle#9145":
        msg = 'VIDEO DAMN IT. Read this then issue `!event help` \n' \
              'I hope you really like this. It took me about 2 weeks to create. \n' \
              'I thought this might be a good starting block for events if you wanted to move to discord. \n' \
              'like everything, it will get better over time and I think it is pretty damn cool. \n' \
              '\n `!event` << a new function ' \
              '\n `!event help` << a help function ' \
              '\n `!event list` << lists events ' \
              '\n `!event join` # << change # to the INCURSION ID to join the fireteam' \
              '\n `!event leave` # << to leave the fireteam '.format(message)
        yield from client.send_message(message.channel, msg)

    if message.content.startswith('!jugs') or message.content.startswith('!juggz') or \
            message.content.startswith('!JUGGZ') or message.content.startswith('!JUGZ') or \
            message.content.startswith('!juggs'):
        print(current_jugs)
        this_jugs = ai_actions.random_jugs(current_jugs)
        msg = ('{0.author.mention} // '+this_jugs).format(message)
        yield from client.send_message(message.channel, msg)

    if message.content.startswith('!hand') or message.content.startswith('!blow') or message.content.startswith(
            '!fuck') or message.content.startswith('!suck'):
        msg = '{0.author.mention} // PLEASE SEE TESS EVERIS, REQUEST A "CUSTOM SERVICE KIT"'.format(message)
        yield from client.send_message(message.channel, msg)

    if message.content.startswith('!dickinabox'):
        msg = '{0.author.mention} // PLEASE SEE RUSTY (SWEEPER BOT-63) TO PROCURE A BOX.\n1. Cut a hole in the box\n' \
              '2. Put your junk in that box\n3. Make her open the box'.format(message)
        yield from client.send_message(message.channel, msg)

    if message.content.startswith('!clean') or message.content.startswith('!pay') or message.content.startswith('!die'):
        msg = '{0.author.mention} // PLEASE SEE RUSTY (SWEEPER BOT-63), REQUEST "DOMESTIC ASSISTANCE"'.format(message)
        yield from client.send_message(message.channel, msg)

    if (message.content.startswith('!test')) and (("N1N3 13#7837" == author) or ("Irronies#9467" == author)):
        entered = message.content
        entered = entered.split(' ', 1)
        entered = str(entered[1])
        msg1 = ('{0.author.mention} you entered: '.format(message) + entered)
        yield from client.send_message(message.channel, msg1)
        out = ai_actions.get_activity("Weekly Heroic Strike")
        msg2 = ('{0.author.mention} // Weekly Heroic Strike // ' + out[1] + '\n'
                '   SKULLS // ' + out[2]).format(message)
        yield from client.send_message(message.channel, msg2)

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        yield from client.send_message(message.channel, msg)

    if message.content.startswith('!light'):
        sep = "#"
        this_author = str(message.author)
        this_author = this_author.split(sep, 1)[0]
        msg = ai_actions.check_light(this_author)
        yield from client.send_message(message.channel, msg.format(message))

    if message.content.startswith('!court'):
        out = ai_actions.get_activity("Court of Oryx")
        # print(repr(out))
        msg = ('{0.author.mention} // Court of Oryx Tier 3 Challenger // ' + out[1]).format(message)
        yield from client.send_message(message.channel, msg)

    if message.content.startswith('!kfraid'):
        out = ai_actions.get_activity("King's Fall")
        msg = ('{0.author.mention} // Kings Fall Speculation // ' + out[1]).format(message)
        yield from client.send_message(message.channel, msg)

    if message.content.startswith('!nightfall'):
        out = ai_actions.get_activity("Nightfall Strike")
        msg = ('{0.author.mention} // Nightfall Strike // ' + out[1] + '\n'
               '   SKULLS // ' + out[2]).format(message)
        yield from client.send_message(message.channel, msg)

    if message.content.startswith('!coe'):
        out = ai_actions.get_activity("Challenge of the Elders")
        msg = ('{0.author.mention} // Challenge of the Elders // ' + out[1] + '\n'
               '   SKULLS // ' + out[2]).format(message)
        yield from client.send_message(message.channel, msg)

    if message.content.startswith('!heroic'):
        out = ai_actions.get_activity("Weekly Heroic Strike")
        msg = ('{0.author.mention} // Weekly Heroic Strike // ' + out[1] + '\n'
               '   SKULLS // ' + out[2]).format(message)
        yield from client.send_message(message.channel, msg)

    if message.content.startswith('!strike'):
        out = ai_actions.get_activity("Daily Story Mission")
        msg = ('{0.author.mention} // Daily Story Mission // ' + out[1]).format(message)
        yield from client.send_message(message.channel, msg)

    if message.content.startswith('!dcp'):
        out = ai_actions.get_activity("Daily Crucible Playlist")
        msg = ('{0.author.mention} // Daily Crucible Playlist // ' + out[1]).format(message)
        yield from client.send_message(message.channel, msg)

    if message.content.startswith('!wcp'):
        out = ai_actions.get_activity("Weekly Crucible Playlist")
        msg = ('{0.author.mention} // Weekly Crucible Playlist // ' + out[1]).format(message)
        yield from client.send_message(message.channel, msg)

    if message.content.startswith('!message'):
        counter = 0
        tmp = yield from client.send_message(message.channel, 'Calculating messages...')
        # asyncio.async
        for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        yield from client.edit_message(tmp, 'You have {} messages.'.format(counter))

    if message.content.startswith('!event'):
        sep = "#"
        this_author = str(message.author)
        this_author = this_author.split(sep, 1)[0]
        entered = message.content
        entered = entered.split(' ', 2)
        if len(entered) <= 1:
            yield from client.send_message(message.channel, (
            'AI-COMS // COMMAND SYNTAX ERROR // {0.author.mention} ISSUE `!event help`').format(message))
        else:
            # HELP
            if (str(entered[1]) == 'help') or (len(entered) <= 1):
                msg = fireteam_actions.incursion_event_help()
                yield from client.send_message(message.channel, (msg.format(message)))
            # Clean DB
            elif str(entered[1]) == 'clean':
                fireteam_actions.expired_calendar_cleanup()
                yield from client.send_message(message.channel, 'AI-HANDLER // DB CLEANED')
            # Create a Test Event
            elif str(entered[1]) == 'testevent':
                this_event_id = None
                this_event_occurs = '2016-09-22 19:30:00'
                this_event_name = "Fraggle's test"
                this_type = 'raid'
                this_activity = 'VoG'
                this_author = 'MtnFraggle'
                slot1 = "OPEN"
                slot2 = "OPEN"
                slot3 = "OPEN"
                slot4 = "OPEN"
                slot5 = "OPEN"
                alt1 = "OPEN"
                alt2 = "OPEN"
                alt3 = "OPEN"
                suppress = "0"
                fireteam_actions.incursion_update(this_event_id, this_event_name, this_event_occurs, this_type,
                                                  this_activity, this_author, slot1, slot2, slot3, slot4, slot5,
                                                  alt1, alt2, alt3, suppress)
                yield from client.send_message(message.channel, 'Added test event!'.format(message))
            # Create a leave fireteam event
            elif str(entered[1]) == '1-testevent':
                this_event_id = None
                this_event_occurs = '2016-09-22 19:30:00'
                this_event_name = "The PT-109 Excursion"
                this_type = 'raid'
                this_activity = 'VoG'
                this_author = 'MtnFraggle'
                slot1 = 'N1N3 13'
                slot2 = "OPEN"
                slot3 = "OPEN"
                slot4 = "OPEN"
                slot5 = "OPEN"
                alt1 = "OPEN"
                alt2 = "OPEN"
                alt3 = "OPEN"
                suppress = "0"
                fireteam_actions.incursion_update(this_event_id, this_event_name, this_event_occurs, this_type,
                                                  this_activity, this_author, slot1, slot2, slot3, slot4, slot5,
                                                  alt1, alt2, alt3, suppress)
                yield from client.send_message(message.channel, 'Added test event!'.format(message))
            # Create a leave fireteam event
            elif str(entered[1]) == '2-testevent':
                this_event_id = None
                this_event_occurs = '2016-09-22 19:30:00'
                this_event_name = "Leave test"
                this_type = 'raid'
                this_activity = 'VoG'
                this_author = 'N1N3 13'
                slot1 = "OPEN"
                slot2 = "OPEN"
                slot3 = "OPEN"
                slot4 = 'MtnFraggle'
                slot5 = "OPEN"
                alt1 = "OPEN"
                alt2 = "OPEN"
                alt3 = "OPEN"
                suppress = "0"
                fireteam_actions.incursion_update(this_event_id, this_event_name, this_event_occurs, this_type,
                                                  this_activity, this_author, slot1, slot2, slot3, slot4, slot5,
                                                  alt1, alt2, alt3, suppress)
                yield from client.send_message(message.channel, 'Added test event!'.format(message))

            # LIST
            elif str(entered[1]) == 'list':
                out = fireteam_actions.incursion_query(0)
                if not out or out is None:
                    yield from client.send_message(message.channel, 'AI-HANDLER // NO INCURSION EVENTS SCHEDULED')
                else:
                    yield from client.send_message(message.channel, 'AI-HANDLER // CURRENT INCURSION EVENTS SCHEDULED')
                    for row in out:
                        msg = ('**INCURSION ID:**  ' + str(row[0]) + '  //  **DATE: **' + str(
                            row[2]) + '  //  **NAME: **' + str(row[1]).title() + '\n **INCURSION TYPE:**  ' + str(
                            row[3]) + '  //  **TARGET:**  ' + str(row[4]) + '\n **FIRETEAM LEADER:**  ' + str(
                            row[5]) + '\n **FIRETEAM:**  ' + str(row[6]) + ', ' + str(row[7]) + ', ' + str(
                            row[8]) + ', ' + str(row[9]) + ', ' + str(row[10]) + '\n **ALTERNATES:** ' + str(
                            row[11]) + ', ' + str(row[12]) + ', ' + str(row[13]))
                        yield from client.send_message(message.channel, msg)

            elif str(entered[1]) == 'suppressed-list':
                out = fireteam_actions.incursion_query(1)
                if not out or out is None:
                    yield from client.send_message(message.channel, 'AI-HANDLER // NO INCURSION EVENTS SCHEDULED')
                else:
                    yield from client.send_message(message.channel, 'AI-HANDLER // PAST INCURSION EVENTS SCHEDULED')
                    for row in out:
                        msg = ('**INCURSION ID:**  ' + str(row[0]) + '  //  **DATE: **' + str(
                            row[2]) + '  //  **NAME: **' + str(row[1]).title() + '\n **INCUSION TYPE:**  ' + str(
                            row[3]) + '  //  **TARGET:**  ' + str(row[4]) + '\n **FIRETEAM LEADER:**  ' + str(
                            row[5]) + '\n **FIRETEAM:**  ' + str(row[6]) + ', ' + str(row[7]) + ', ' + str(
                            row[8]) + ', ' + str(row[9]) + ', ' + str(row[10]) + '\n **ALTERNATES** ' + str(
                            row[11]) + ', ' + str(row[12]) + ', ' + str(row[13]))
                        yield from client.send_message(message.channel, msg)

            elif str(entered[1]) == 'all-list':
                out = fireteam_actions.incursion_query(4)
                if not out or out is None:
                    yield from client.send_message(message.channel, 'AI-HANDLER // NO INCURSION EVENTS SCHEDULED')
                else:
                    yield from client.send_message(message.channel,
                                                   'AI-HANDLER // ALL CURRENT AND PAST INCURSION EVENTS SCHEDULED')
                    for row in out:
                        msg = ('**INCURSION ID:**  ' + str(row[0]) + '  //  **DATE: **' + str(
                            row[2]) + '  //  **NAME: **' + str(row[1]).title() + '\n **INCUSION TYPE:**  ' + str(
                            row[3]) + '  //  **TARGET:**  ' + str(row[4]) + '\n **FIRETEAM LEADER:**  ' + str(
                            row[5]) + '\n **FIRETEAM:**  ' + str(row[6]) + ', ' + str(row[7]) + ', ' + str(
                            row[8]) + ', ' + str(row[9]) + ', ' + str(row[10]) +'\n **ALTERNATES** ' + str(
                            row[11]) + ', ' + str(row[12]) + ', ' + str(row[13]))
                        yield from client.send_message(message.channel, msg)

            # JOIN
            elif str(entered[1]) == 'join':
                this_event_id = entered[2]
                msg = fireteam_actions.incursion_join_fireteam(this_author, this_event_id)
                yield from client.send_message(message.channel,(msg).format(message))
            # ALT-JOIN
            elif str(entered[1]) == 'alt-join':
                this_event_id = entered[2]
                msg = fireteam_actions.incursion_join_alternate(this_author, this_event_id)
                yield from client.send_message(message.channel, (msg).format(message))
            # LEAVE
            elif str(entered[1]) == 'leave':
                this_event_id = entered[2]
                msg = fireteam_actions.incursion_leave_fireteam(this_author, this_event_id)
                yield from client.send_message(message.channel, msg.format(message))

            elif str(entered[1]) == 'alt-leave':
                this_event_id = entered[2]
                msg = fireteam_actions.incursion_leave_alternate(this_author, this_event_id)
                yield from client.send_message(message.channel, msg.format(message))

            # DELETE EVENT
            elif str(entered[1]) == 'delete':
                # this_event = entered[1].split('|')
                this_event_id = entered[2]
                print("entered[2]: ",repr(entered[2]))
                event_row = fireteam_actions.incursion_lookup_by_id(this_event_id)
                # check for author in any slot
                # print('AI-HANDLER // RECEIVED DELETE REQUEST FOR \"'+str(event_row[1]).upper()+'\" FROM '+this_author)
                if this_author in event_row[5]:
                    fireteam_actions.incursion_delete(this_event_id)
                    yield from client.send_message(message.channel, 'AI-HANDLER // INCURSION EVENT ID ' + str(
                        this_event_id) + ' EXPUNGED')
                else:
                    yield from client.send_message(message.channel,
                                                   'AI-HANDLER // ONLY THE FIRETEAM LEADER MAY EXPUNGE AN INCURSION')
            # OVERRIDE DELETE
            elif str(entered[1]) == 'override-delete':
                # this_event = entered[1].split('|')
                this_event_id = entered[2]
                # lookup event
                fireteam_actions.incursion_delete(this_event_id)
                yield from client.send_message(message.channel, 'AI-HANDLER // INCURSION EVENT EXPUNGED VIA OVERRIDE')
            # ADD INCURSION
            elif str(entered[1]) == 'add':
                this_event = entered[2].split('|')
                msg = fireteam_actions.incursion_create(this_author, this_event)
                yield from client.send_message(message.channel, msg.format(message))

    elif message.content.startswith('!sleep'):
        yield from asyncio.sleep(5)
        yield from client.send_message(message.channel, 'AI-COMS // Warminds do not sleep')

    else:
        pass


@client.event
@asyncio.coroutine
def on_member_join(member):
    server = member.server
    msg = 'Guardian {0.mention} now registered online with {1.name}!'
    yield from client.send_message(server, msg.format(member, server))
    # yield from client.send_message(discord.Message.channel, fmt.format(discord.Message))
    # member, server


current_jugs = ai_actions.random_jugs(current_jugs)
client.loop.create_task(my_background_task())
