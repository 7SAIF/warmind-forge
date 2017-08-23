#!/usr/bin/python3.6
import os, re, sys, random
import discord, asyncio
from datetime import datetime
from destinygotg import Session, loadConfig
from initdb import PvPAggregate, PvEAggregate, Base, Discord, Account, AccountMedals, Character, ClassReference
from sqlalchemy import exists, desc, func, and_
from decimal import *
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt; plt.rcdefaults()
from warmind import Fireteam_Actions
from warmind import SQL_Actions
from warmind import AI_Actions
from warmind.Global_Variables import *

import sqlite3

playerList = [item[0] for item in Session().query(Account.display_name).all()]

statDict = { "kd"           :(PvPAggregate, "killsDeathsRatio", "Kill/Death Ratio")
            ,"kda"          :(PvPAggregate, "killsDeathsAssists", "Kill/Assists/Death Ratio")
            ,"wl"           :(PvPAggregate, "winLossRatio", "Win/Loss Ratio")
            ,"bgs"          :(PvPAggregate, "bestSingleGameScore", "Best Single Game Score")
            ,"lks"          :(PvPAggregate, "longestKillSpree", "Longest Kill Spree")
            ,"suicides"     :(PvPAggregate, "suicides", "Total Number of Suicides")
            ,"spg"          :(PvPAggregate, "suicidespg", "Suicides per Game")
            ,"mk"           :(PvPAggregate, "bestSingleGameKills", "Best Single Game Kills")
            ,"kills"        :(PvPAggregate, "kills", "Total Number of Kills")
            ,"kpg"          :(PvPAggregate, "killspg", "Kills per Game")
            ,"deaths"       :(PvPAggregate, "deaths", "Total Number of Deaths")
            ,"dpg"          :(PvPAggregate, "deathspg", "Deaths per Game")
            ,"assists"      :(PvPAggregate, "assists", "Total Number of Assists")
            ,"apg"          :(PvPAggregate, "assistspg", "Assists Per Game")
            ,"cr"           :(PvPAggregate, "combatRating", "Combat Rating")
            ,"pkills"       :(PvPAggregate, "precisionKills", "Total Number of Precision Kills")
            ,"score"        :(PvPAggregate, "score", "Total score")
            ,"scpg"         :(PvPAggregate, "scorepg", "Score per Game")
            ,"crucibletime" :(PvPAggregate, "secondsPlayed", "Total Seconds in the Crucible")
            ,"akills"       :(PvPAggregate, "abilityKills", "Total Number of Ability Kills")
            ,"akpg"         :(PvPAggregate, "abilityKillspg", "Ability Kills per Game")
            ,"games"        :(PvPAggregate, "activitiesEntered", "Total Number of Activities Entered")
            ,"wins"         :(PvPAggregate, "activitiesWon", "Total Number of Activities Won")
            ,"lsl"          :(PvPAggregate, "longestSingleLife", "Longest Single Life")
            }

medalDict = { "activities"        :(AccountMedals, "activitiesEntered", "Activities Entered")
             ,"totalmedals"       :(AccountMedals, "allMedalsEarned", "Total Number of Medals")
             ,"totalscore"        :(AccountMedals, "allMedalsScore", "Total Medal Score")
             ,"stormbringer"      :(AccountMedals, "medalsAbilityArcLightningKillMulti", "Storm Bringer")
             ,"wayofthegun"       :(AccountMedals, "medalsAbilityGhostGunKillMulti", "Way of the Gun")
             ,"cryhavoc"          :(AccountMedals, "medalsAbilityHavocKillMulti", "Cry Havoc")
             ,"spacemagic"        :(AccountMedals, "medalsAbilityNovaBombKillMulti", "Space Magic")
             ,"scorchedearth"     :(AccountMedals, "medalsAbilityRadianceGrenadeKillMulti", "Scorched Earth")
             ,"gutted"            :(AccountMedals, "medalsAbilityShadowStrikeKillMulti", "Gutted")
             ,"hammerandtongs"    :(AccountMedals, "medalsAbilityThermalHammerKillMulti", "Hammer and Tongs")
             ,"wildhunt"          :(AccountMedals, "medalsAbilityVoidBowKillMulti", "Wild Hunt")
             ,"blastshield"       :(AccountMedals, "medalsAbilityWardDeflect", "Blast Shield")
             ,"objectivelycorrect":(AccountMedals, "medalsActivityCompleteControlMostCaptures", "Objectively Correct")
             ,"thecycle"          :(AccountMedals, "medalsActivityCompleteCycle", "The Cycle")
             ,"unbroken"          :(AccountMedals, "medalsActivityCompleteDeathless", "Mark of the Unbroken")
             ,"onthebrightside"   :(AccountMedals, "medalsActivityCompleteHighestScoreLosing", "On the Bright Side...")
             ,"thebestaround"     :(AccountMedals, "medalsActivityCompleteHighestScoreWinning", "The Best... Around")
             ,"lonewolf"          :(AccountMedals, "medalsActivityCompleteLonewolf", "Lone Wolf")
             ,"saboteur"          :(AccountMedals, "medalsActivityCompleteSalvageMostCancels", "Saboteur")
             ,"shutout"           :(AccountMedals, "medalsActivityCompleteSalvageShutout", "Shutout")
             ,"perfectrunner"     :(AccountMedals, "medalsActivityCompleteSingularityPerfectRunner", "Perfect Runner")
             ,"decisivevictory"   :(AccountMedals, "medalsActivityCompleteVictoryBlowout", "Decisive Victory")
             ,"victory"           :(AccountMedals, "medalsActivityCompleteVictory", "Victory")
             ,"trialbyfire"       :(AccountMedals, "medalsActivityCompleteVictoryElimination", "Trial by Fire")
             ,"bulletproof"       :(AccountMedals, "medalsActivityCompleteVictoryEliminationPerfect", "Bulletproof")
             ,"annihilation"      :(AccountMedals, "medalsActivityCompleteVictoryEliminationShutout", "Annihilation")
             ,"clutch"            :(AccountMedals, "medalsActivityCompleteVictoryExtraLastSecond", "Clutch")
             ,"comeback"          :(AccountMedals, "medalsActivityCompleteVictoryLastSecond", "Comeback")
             ,"nomercy"           :(AccountMedals, "medalsActivityCompleteVictoryMercy", "No Mercy")
             ,"sumofalltears"     :(AccountMedals, "medalsActivityCompleteVictoryRumbleBlowout", "Sum of all Tears")
             ,"aloneatthetop"     :(AccountMedals, "medalsActivityCompleteVictoryRumble", "Alone at the Top")
             ,"wontbebeat"        :(AccountMedals, "medalsActivityCompleteVictoryRumbleLastSecond", "Won't be Beat")
             ,"heartbreaker"      :(AccountMedals, "medalsActivityCompleteVictoryRumbleSuddenDeath", "Heartbreaker")
             ,"zerohour"          :(AccountMedals, "medalsActivityCompleteVictorySuddenDeath", "Zero Hour")
             ,"avenger"           :(AccountMedals, "medalsAvenger", "Avenger")
             ,"medic"             :(AccountMedals, "medalsBuddyResurrectionMulti", "Medic!")
             ,"angeloflight"      :(AccountMedals, "medalsBuddyResurrectionSpree", "Angel of Light")
             ,"narrowescape"      :(AccountMedals, "medalsCloseCallTalent", "Narrow Escape")
             ,"backinaction"      :(AccountMedals, "medalsComebackKill", "Back in Action")
             ,"domination"        :(AccountMedals, "medalsDominationKill", "Domination")
             ,"hattrick"          :(AccountMedals, "medalsDominionZoneCapturedSpree", "Hat Trick")
             ,"defender"          :(AccountMedals, "medalsDominionZoneDefenseKillSpree", "Defender")
             ,"atanycost"         :(AccountMedals, "medalsDominionZoneOffenseKillSpree", "At any Cost")
             ,"neversaydie"       :(AccountMedals, "medalsEliminationLastStandKill", "Never Say Die")
             ,"fromthebrink"      :(AccountMedals, "medalsEliminationLastStandRevive", "From the Brink")
             ,"ace"               :(AccountMedals, "medalsEliminationWipeQuick", "Ace")
             ,"wreckingball"      :(AccountMedals, "medalsEliminationWipeSolo", "Wrecking Ball")
             ,"firstblood"        :(AccountMedals, "medalsFirstBlood", "First Blood")
             ,"uprising"          :(AccountMedals, "medalsFirstPlaceKillSpree", "Uprising")
             ,"getitoff"          :(AccountMedals, "medalsGrenadeKillStick", "Get it Off!")
             ,"hazardpay"         :(AccountMedals, "medalsHazardKill", "Hazard Pay")
             ,"iseeyou"           :(AccountMedals, "medalsHunterKillInvisible", "I See You")
             ,"unsunghero"        :(AccountMedals, "medalsKillAssistSpree", "Unsung Hero")
             ,"enemyofmyenemy"    :(AccountMedals, "medalsKillAssistSpreeFfa", "Enemy of my Enemy")
             ,"bullseye"          :(AccountMedals, "medalsKillHeadshot", "Bullseye")
             ,"enforcer"          :(AccountMedals, "medalsKilljoy", "Enforcer")
             ,"endoftheline"      :(AccountMedals, "medalsKilljoyMega", "End of the Line")
             ,"doubledown"        :(AccountMedals, "medalsKillMulti2", "Double Down")
             ,"tripledown"        :(AccountMedals, "medalsKillMulti3", "Triple Down")
             ,"breaker"           :(AccountMedals, "medalsKillMulti4", "Breaker")
             ,"slayer"            :(AccountMedals, "medalsKillMulti5", "Slayer")
             ,"reaper"            :(AccountMedals, "medalsKillMulti6", "Reaper")
             ,"seventhcolumn"     :(AccountMedals, "medalsKillMulti7", "Seventh Column")
             ,"postmortem"        :(AccountMedals, "medalsKillPostmortem", "Postmortem")
             ,"merciless"         :(AccountMedals, "medalsKillSpree1", "Merciless")
             ,"relentless"        :(AccountMedals, "medalsKillSpree2", "Relentless")
             ,"reignofterror"     :(AccountMedals, "medalsKillSpree3", "Reign of Terror")
             ,"weranoutofmedals"  :(AccountMedals, "medalsKillSpreeAbsurd", "We Ran Out of Medals")
             ,"phantom"           :(AccountMedals, "medalsKillSpreeNoDamage", "Phantom")
             ,"stickaround"       :(AccountMedals, "medalsMeleeKillHunterThrowingKnifeHeadshot", "Stick Around")
             ,"payback"           :(AccountMedals, "medalsPaybackKill", "Payback")
             ,"andstaydown"       :(AccountMedals, "medalsRadianceShutdown", "...And Stay Down!")
             ,"overwatch"         :(AccountMedals, "medalsRescue", "Overwatch")
             ,"disruption"        :(AccountMedals, "medalsSalvageProbeCanceled", "Disruption")
             ,"salvagecrew"       :(AccountMedals, "medalsSalvageProbeCompleteSpree", "Salvage Crew")
             ,"improbeable"       :(AccountMedals, "medalsSalvageProbeDefenseKill", "Im-probe-able")
             ,"cleansweep"        :(AccountMedals, "medalsSalvageProbeOffenseKillMulti", "Clean Sweep")
             ,"relichunter"       :(AccountMedals, "medalsSalvageZoneCapturedSpree", "Relic Hunter")
             ,"unstoppableforce"  :(AccountMedals, "medalsSingularityFlagCaptureMulti", "Unstoppable Force")
             ,"denied"            :(AccountMedals, "medalsSingularityFlagHolderKilledClose", "Denied")
             ,"immovableobject"   :(AccountMedals, "medalsSingularityFlagHolderKilledMulti", "Immovable Object")
             ,"clearapath"        :(AccountMedals, "medalsSingularityRunnerDefenseMulti", "Clear a Path")
             ,"afistfulofcrests"  :(AccountMedals, "medalsSupremacy", "A Fistful of Crests...")
             ,"forafewcrestsmore" :(AccountMedals, "medalsSupremacyConfirmStreakLarge", "And For a Few Crests More")
             ,"honorguard"        :(AccountMedals, "medalsSupremacyDenyMulti", "Honor Guard")
             ,"mineallmine"       :(AccountMedals, "medalsSupremacyMostConfirms", "Mine! All Mine!")
             ,"handsoff"          :(AccountMedals, "medalsSupremacyMostDenies", "Hands Off")
             ,"illdoitmyself"     :(AccountMedals, "medalsSupremacyMostSelfConfirms", "I'll Do It Myself")
             ,"pickupthepieces"   :(AccountMedals, "medalsSupremacyMulti", "Pick Up the Pieces")
             ,"nevergonnagetit"   :(AccountMedals, "medalsSupremacyNeverCollected", "Never Gonna Get It")
             ,"nevermindfoundit"  :(AccountMedals, "medalsSupremacySelfDeny", "Never Mind, Found It")
             ,"lockdown"          :(AccountMedals, "medalsTeamDominationHold1m", "Lockdown")
             ,"strengthofthewolf" :(AccountMedals, "medalsTeamKillSpree", "Strength of the Wolf")
             ,"unknown"           :(AccountMedals, "medalsUnknown", "Unknown")
             ,"gunner"            :(AccountMedals, "medalsVehicleFotcTurretKillSpree", "Gunner")
             ,"bulldozer"         :(AccountMedals, "medalsVehicleInterceptorKillSplatter", "Bulldozer")
             ,"chariotoffire"     :(AccountMedals, "medalsVehicleInterceptorKillSpree", "Chariot of Fire")
             ,"skewered"          :(AccountMedals, "medalsVehiclePikeKillSplatter", "Skewered")
             ,"fallenangel"       :(AccountMedals, "medalsVehiclePikeKillSpree", "Fallen Angel")
             ,"neverspeakofthis"  :(AccountMedals, "medalsVehicleSparrowKillSplatter", "Never Speak of This Again")
             ,"automatic"         :(AccountMedals, "medalsWeaponAutoRifleKillSpree", "Automatic")
             ,"masterblaster"     :(AccountMedals, "medalsWeaponFusionRifleKillSpree", "Master Blaster")
             ,"deadmanshand"      :(AccountMedals, "medalsWeaponHandCannonHeadshotSpree", "Dead Man's Hand")
             ,"machinelord"       :(AccountMedals, "medalsWeaponMachineGunKillSpree", "Machine Lord")
             ,"fingeronthepulse"  :(AccountMedals, "medalsWeaponPulseRifleKillSpree", "Finger on the Pulse")
             ,"splashdamage"      :(AccountMedals, "medalsWeaponRocketLauncherKillSpree", "Splash Damage")
             ,"scoutshonor"       :(AccountMedals, "medalsWeaponScoutRifleKillSpree", "Scout's Honor")
             ,"buckshotbruiser"   :(AccountMedals, "medalsWeaponShotgunKillSpree", "Buckshot Bruiser")
             ,"sidekick"          :(AccountMedals, "medalsWeaponSidearmKillSpree", "Sidekick")
             ,"marksman"          :(AccountMedals, "medalsWeaponSniperRifleHeadshotSpree", "Marksman")
             ,"swordatagunfight"  :(AccountMedals, "medalsWeaponSwordKillSpree", "Sword at a Gun Fight")
             ,"nailinthecoffin"   :(AccountMedals, "medalsWinningScore", "Nail in the Coffin")
             ,"bline"             :(AccountMedals, "medalsZoneCapturedBInitial", "B-Line")
             }

def runBot(engine):
    # The regular bot definition things
    client = discord.Client()

    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        # await client.send_message(discord.Message.channel, 'AI-COMS: Initializing Channel Interface')
        print('------')

    @client.event
    async def queryDatabase(channel, statement, connection):
        result = connection.execute(statement)
        resultList = [row for row in result]
        await client.send_message(channel, resultList)
    
    @client.event
    async def registerHandler(discordAuthor):
        discId = discordAuthor.id
        session = Session()
        userIsRegistered = session.query(exists().where(Discord.id == discId)).scalar()
        if userIsRegistered:
            destinyName = session.query(Account.display_name).join(Discord).filter(Discord.id == discId).first()[0]
        else:
            destinyName = await registerUser(discordAuthor)
        return destinyName

    @client.event
    async def registerUser(discordAuthor):
        session = Session()
        def checkIfValidUser(userName):
            return session.query(exists().where(Account.display_name == userName)).scalar()
        #Need to send a DM requesting the PSN name
        destination = discordAuthor
        discName = discordAuthor.name
        await client.send_message(destination, discName+", please enter your PSN display name.")
        nameMsg = await client.wait_for_message(author=discordAuthor,check=checkIfValidUser(discName))
        destName = nameMsg.content
        discordDict = {}
        discordDict['id'] = discordAuthor.id
        discordDict['discord_name'] = discordAuthor.name
        discordDict['membership_id'] = session.query(Account.id).filter(Account.display_name == destName).first()[0]
        new_discord_user = Discord(**discordDict)
        session.add(new_discord_user)
        session.commit()
        await client.send_message(destination, discName+", you have been successfully registered!")
        return destName

    @client.event
    async def on_message(message):
        author = str(message.author)
        if message.author == client.user:
            return None

        elif message.content.startswith('!help'):
            #TODO: Send a dm to user with contents of help command
            #TODO: Add all commands to body of help response
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
            await  client.send_message(message.channel, msg)

        elif message.content.startswith('!timeleft'):
            output = timeLeft()
            await client.send_message(message.channel, output)

        elif message.content.startswith('Right Gary?'):
            await client.send_message(message.channel, 'Right.')

        elif message.content.startswith('Say goodbye'):
            await client.send_message(message.channel, 'beep boop')

        #Don't turn this one on
        #elif message.content.startswith('!sql'):
        #    roleList = [role.name for role in message.author.roles]
        #    if "@administrator" in roleList and "@bot-developer" in roleList:
        #        statement = message.content[5:]
        #        connection = engine.connect()
        #        channel = message.channel
        #        await queryDatabase(channel, statement, connection)
        #    else:
        #        await client.send_message(message.channel, "Permission denied!")

        #elif message.author.name == "Roscroft" and message.channel.is_private:
        #    if not message.content == "Roscroft":
        #        await client.send_message(discord.Object(id='322173351059521537'), message.content)

        elif message.content.startswith('!channel-id'):
            print(message.channel.id)

        elif message.content.startswith("!stat"):
            player = await registerHandler(message.author)
            content = message.content
            #if message.channel.id is not '342754108534554624':
           #     await client.send_message(message.channel, "Please use the #stat channel for stat requests.")
            #else:
            valid, players, code, stat = validate(player, content)
            if valid and len(players) == 0:
                output = singleStatRequest(player, code, stat)
                #await client.send_message(discord.Object(id='342754108534554624'), output)
                await client.send_message(message.channel, output)# embed=output)
            elif valid and len(players) > 0:
                players.append(player)
                output = multiStatRequest(players, code, stat)
                await client.send_message(message.channel, embed=output)
            else:
                await client.send_message(message.channel, "```Invalid stat request.```")

        elif message.content.startswith("!clangraph"):
            content = message.content
            player = await registerHandler(message.author)
            valid, authplayer, code, stat = validateClanStat(player, content)
            output = clanGraphRequest(authplayer, code, stat)
            await client.send_file(message.channel, './Figures/hist.png')

        elif message.content.startswith("!clanstat"):
            pass


        elif (message.content.startswith('!test')) and (("N1N3 13#7837" == author) or ("Irronies#9467" == author)):
            entered = message.content
            entered = entered.split(' ', 1)
            entered = str(entered[1])
            msg1 = (f"{author.mention} you entered: {entered}")
            await client.send_message(message.channel, msg1)
            out = ai_actions.get_activity("Weekly Heroic Strike")
            msg2 = ('{0.author.mention} // Weekly Heroic Strike // ' + out[1] + '\n'
                    '   SKULLS // ' + out[2]).format(message)
            await client.send_message(message.channel, msg2)

        elif message.content.startswith('!hello'):
            msg = f"Hello {author.mention}"
            await client.send_message(message.channel, msg)

        elif message.content.startswith('!light'):
            player = await registerHandler(message.author)
            data = lightLevelRequest(player)
            output = ""
            for item in data:
                output += f"{item[1]}: {item[0]} "
            await client.send_message(message.channel, output)

        elif message.content.startswith('!court'):
            out = ai_actions.get_activity("Court of Oryx")
            msg = f"{author.mention} // Court of Oryx Tier 3 Challenger // {out[1]}"
            await client.send_message(message.channel, msg)

        elif message.content.startswith('!kfraid'):
            out = ai_actions.get_activity("King's Fall")
            msg = f"{author.mention} // King's Fall Speculation // {out[1]}"
            await client.send_message(message.channel, msg)
        
        #TODO: Figure out how these get printed
        elif message.content.startswith('!nightfall'):
            out = ai_actions.get_activity("Nightfall Strike")
            msg = ('{0.author.mention} // Nightfall Strike // ' + out[1] + '\n'
                '   SKULLS // ' + out[2]).format(message)
            await client.send_message(message.channel, msg)

        elif message.content.startswith('!coe'):
            out = ai_actions.get_activity("Challenge of the Elders")
            msg = ('{0.author.mention} // Challenge of the Elders // ' + out[1] + '\n'
                '   SKULLS // ' + out[2]).format(message)
            await client.send_message(message.channel, msg)

        elif message.content.startswith('!heroic'):
            out = ai_actions.get_activity("Weekly Heroic Strike")
            msg = ('{0.author.mention} // Weekly Heroic Strike // ' + out[1] + '\n'
                '   SKULLS // ' + out[2]).format(message)
            await client.send_message(message.channel, msg)

        elif message.content.startswith('!strike'):
            out = ai_actions.get_activity("Daily Story Mission")
            msg = f"{author.mention} // Daily Story Mission // {out[1]}"
            await client.send_message(message.channel, msg)

        elif message.content.startswith('!dcp'):
            out = ai_actions.get_activity("Daily Crucible Playlist")
            msg = f"{author.mention} // Daily Crucible Playlist // {out[1]}"
            await client.send_message(message.channel, msg)

        elif message.content.startswith('!wcp'):
            out = ai_actions.get_activity("Weekly Crucible Playlist")
            msg = f"{author.mention} // Weekly Crucible Playlist // {out[1]}"
            await client.send_message(message.channel, msg)

        elif message.content.startswith('!message'):
            counter = 0
            tmp = await client.send_message(message.channel, 'Calculating messages...')
            for log in client.logs_from(message.channel, limit=100):
                if log.author == message.author:
                    counter += 1
            await client.edit_message(tmp, 'You have {} messages.'.format(counter))

        elif message.content.startswith('!event'):
            #sep = "#"
            #this_author = str(message.author)
            #this_author = this_author.split(sep, 1)[0]
            this_author = message.content.name
            entered = message.content
            entered = entered.split(' ', 2)
            if len(entered) <= 1:
                await client.send_message(message.channel, (
                'AI-COMS // COMMAND SYNTAX ERROR // {0.author.mention} ISSUE `!event help`').format(message))
            else:
                # HELP
                if (str(entered[1]) == 'help') or (len(entered) <= 1):
                    msg = fireteam_actions.incursion_event_help()
                    await client.send_message(message.channel, (msg.format(message)))
                # Clean DB
                elif str(entered[1]) == 'clean':
                    fireteam_actions.expired_calendar_cleanup()
                    await client.send_message(message.channel, 'AI-HANDLER // DB CLEANED')
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
                    await client.send_message(message.channel, 'Added test event!'.format(message))
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
                    await client.send_message(message.channel, 'Added test event!'.format(message))
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
                    await client.send_message(message.channel, 'Added test event!'.format(message))

                # LIST
                elif str(entered[1]) == 'list':
                    out = fireteam_actions.incursion_query(0)
                    if not out or out is None:
                        await client.send_message(message.channel, 'AI-HANDLER // NO INCURSION EVENTS SCHEDULED')
                    else:
                        await client.send_message(message.channel, 'AI-HANDLER // CURRENT INCURSION EVENTS SCHEDULED')
                        for row in out:
                            msg = ('**INCURSION ID:**  ' + str(row[0]) + '  //  **DATE: **' + str(
                                row[2]) + '  //  **NAME: **' + str(row[1]).title() + '\n **INCURSION TYPE:**  ' + str(
                                row[3]) + '  //  **TARGET:**  ' + str(row[4]) + '\n **FIRETEAM LEADER:**  ' + str(
                                row[5]) + '\n **FIRETEAM:**  ' + str(row[6]) + ', ' + str(row[7]) + ', ' + str(
                                row[8]) + ', ' + str(row[9]) + ', ' + str(row[10]) + '\n **ALTERNATES:** ' + str(
                                row[11]) + ', ' + str(row[12]) + ', ' + str(row[13]))
                            await client.send_message(message.channel, msg)

                elif str(entered[1]) == 'suppressed-list':
                    out = fireteam_actions.incursion_query(1)
                    if not out or out is None:
                        await client.send_message(message.channel, 'AI-HANDLER // NO INCURSION EVENTS SCHEDULED')
                    else:
                        await client.send_message(message.channel, 'AI-HANDLER // PAST INCURSION EVENTS SCHEDULED')
                        for row in out:
                            msg = ('**INCURSION ID:**  ' + str(row[0]) + '  //  **DATE: **' + str(
                                row[2]) + '  //  **NAME: **' + str(row[1]).title() + '\n **INCUSION TYPE:**  ' + str(
                                row[3]) + '  //  **TARGET:**  ' + str(row[4]) + '\n **FIRETEAM LEADER:**  ' + str(
                                row[5]) + '\n **FIRETEAM:**  ' + str(row[6]) + ', ' + str(row[7]) + ', ' + str(
                                row[8]) + ', ' + str(row[9]) + ', ' + str(row[10]) + '\n **ALTERNATES** ' + str(
                                row[11]) + ', ' + str(row[12]) + ', ' + str(row[13]))
                            await client.send_message(message.channel, msg)

                elif str(entered[1]) == 'all-list':
                    out = fireteam_actions.incursion_query(4)
                    if not out or out is None:
                        await client.send_message(message.channel, 'AI-HANDLER // NO INCURSION EVENTS SCHEDULED')
                    else:
                        await client.send_message(message.channel,
                                                    'AI-HANDLER // ALL CURRENT AND PAST INCURSION EVENTS SCHEDULED')
                        for row in out:
                            msg = ('**INCURSION ID:**  ' + str(row[0]) + '  //  **DATE: **' + str(
                                row[2]) + '  //  **NAME: **' + str(row[1]).title() + '\n **INCUSION TYPE:**  ' + str(
                                row[3]) + '  //  **TARGET:**  ' + str(row[4]) + '\n **FIRETEAM LEADER:**  ' + str(
                                row[5]) + '\n **FIRETEAM:**  ' + str(row[6]) + ', ' + str(row[7]) + ', ' + str(
                                row[8]) + ', ' + str(row[9]) + ', ' + str(row[10]) +'\n **ALTERNATES** ' + str(
                                row[11]) + ', ' + str(row[12]) + ', ' + str(row[13]))
                            await client.send_message(message.channel, msg)

                # JOIN
                elif str(entered[1]) == 'join':
                    this_event_id = entered[2]
                    msg = fireteam_actions.incursion_join_fireteam(this_author, this_event_id)
                    await client.send_message(message.channel,(msg).format(message))
                # ALT-JOIN
                elif str(entered[1]) == 'alt-join':
                    this_event_id = entered[2]
                    msg = fireteam_actions.incursion_join_alternate(this_author, this_event_id)
                    await client.send_message(message.channel, (msg).format(message))
                # LEAVE
                elif str(entered[1]) == 'leave':
                    this_event_id = entered[2]
                    msg = fireteam_actions.incursion_leave_fireteam(this_author, this_event_id)
                    await client.send_message(message.channel, msg.format(message))

                elif str(entered[1]) == 'alt-leave':
                    this_event_id = entered[2]
                    msg = fireteam_actions.incursion_leave_alternate(this_author, this_event_id)
                    await client.send_message(message.channel, msg.format(message))

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
                        await client.send_message(message.channel, 'AI-HANDLER // INCURSION EVENT ID ' + str(
                            this_event_id) + ' EXPUNGED')
                    else:
                        await client.send_message(message.channel,
                                                    'AI-HANDLER // ONLY THE FIRETEAM LEADER MAY EXPUNGE AN INCURSION')
                # OVERRIDE DELETE
                elif str(entered[1]) == 'override-delete':
                    # this_event = entered[1].split('|')
                    this_event_id = entered[2]
                    # lookup event
                    fireteam_actions.incursion_delete(this_event_id)
                    await client.send_message(message.channel, 'AI-HANDLER // INCURSION EVENT EXPUNGED VIA OVERRIDE')
                # ADD INCURSION
                elif str(entered[1]) == 'add':
                    this_event = entered[2].split('|')
                    msg = fireteam_actions.incursion_create(this_author, this_event)
                    await client.send_message(message.channel, msg.format(message))

        elif message.content.startswith('!sleep'):
            await asyncio.sleep(5)
            await client.send_message(message.channel, 'AI-COMS // Warminds do not sleep')

        elif message.content.startswith('!fraggle') and author == "MtnFraggle#9145":
            msg = '{0.author.mention} 9er asked me to tell you this: ' \
                'To quote: Hey glorious leader, go to take selfie video while you read this `!morefraggle` \n' \
                'You are to send me the video of you examining and using these instructions. ' \
                'Next communication is from 9er'.format(message)
            await client.send_message(message.channel, msg)

        elif message.content.startswith('!morefraggle') and author == "MtnFraggle#9145":
            msg = 'VIDEO DAMN IT. Read this then issue `!event help` \n' \
                'I hope you really like this. It took me about 2 weeks to create. \n' \
                'I thought this might be a good starting block for events if you wanted to move to discord. \n' \
                'like everything, it will get better over time and I think it is pretty damn cool. \n' \
                '\n `!event` << a new function ' \
                '\n `!event help` << a help function ' \
                '\n `!event list` << lists events ' \
                '\n `!event join` # << change # to the INCURSION ID to join the fireteam' \
                '\n `!event leave` # << to leave the fireteam '.format(message)
            await client.send_message(message.channel, msg)

        elif message.content.startswith('!jugs') or message.content.startswith('!juggz') or \
                message.content.startswith('!JUGGZ') or message.content.startswith('!JUGZ') or \
                message.content.startswith('!juggs'):
            print(current_jugs)
            this_jugs = ai_actions.random_jugs(current_jugs)
            msg = ('{0.author.mention} // '+this_jugs).format(message)
            await client.send_message(message.channel, msg)

        elif message.content.startswith('!hand') or message.content.startswith('!blow') or message.content.startswith(
                '!fuck') or message.content.startswith('!suck'):
            msg = f"{author.mention} // PLEASE SEE TESS EVERIS, REQUEST A 'CUSTOM SERVICE KIT'"
            await client.send_message(message.channel, msg)

        elif message.content.startswith('!dickinabox'):
            msg = f"{author.mention} // PLEASE SEE RUSTY (SWEEPER BOT-63) TO PROCURE A BOX.\n1. Cut a hole in the box\n' \
                '2. Put your junk in that box\n3. Make her open the box"
            await client.send_message(message.channel, msg)

        elif message.content.startswith('!clean') or message.content.startswith('!pay') or message.content.startswith('!die'):
            msg = f"{author.mention} // PLEASE SEE RUSTY (SWEEPER BOT-63), REQUEST 'DOMESTIC ASSISTANCE'"
            await client.send_message(message.channel, msg)

        else:
            pass
    client.run(os.environ['DISCORD_APIKEY'])

# Stat number codes - 0: Not a stat, 1: PvP/PvE aggregate, 2: Medal
def validate(player, content):
    statList = content.split(" ")[1:]
    stat = statList[0]
    trackCode = 0
    if stat in statDict.keys():
        trackCode = 1
    elif stat in medalDict.keys():
        trackCode = 2
    elif stat[:-2] in medalDict.keys() and stat[-2:] == "pg":
        trackCode = 3
        stat = stat[:-2]
    players = []
    isValid = (trackCode != 0)
    if len(statList) > 1:
        isVs = statList[1] == "vs"
        players = statList[2:]
        if players == ["all"]:
            players = playerList
        areValidPlayers = [player in playerList for player in players]
        isValid = (trackCode != 0) and isVs and (False not in areValidPlayers)
    return (isValid, players, trackCode, stat)

def validateClanStat(player, content):
    stat = content.split(" ")[1]
    trackCode = 0
    if stat in statDict.keys():
        trackCode = 1
    elif stat in medalDict.keys():
        trackCode = 2
    elif stat[:-2] in medalDict.keys() and stat[-2:] == "pg":
        trackCode = 3
        stat = stat[:-2]
    isValidPlayer = player in playerList
    playerName = ""
    if isValidPlayer:
        playerName = player
    return ((trackCode != 0), playerName, trackCode, stat)

def lightLevelRequest(player):
    """Retrieves the character light levels of a player"""
    session = Session()
    data = session.query(Character.light_level, ClassReference.class_name).join(Account).join(ClassReference, and_(ClassReference.id==Character.class_hash)).filter(Account.display_name == player).all()
    return data

def singleStatRequest(player, code, stat):
    """Actually retrieves the stat and returns the stat info in an embed"""
    session = Session()
    message = ""
    if code == 1:
        (table, col, message) = statDict[stat]
        columns = [col]
        res = session.query(*(getattr(table, column) for column in columns), Account.display_name).join(Account).filter(Account.display_name == player).first()
        #Returns a tuple containing the stat, but only the first element is defined for some reason.
        num = truncateDecimals(res[0])
        name = res[1]
    elif code == 2:
        (table, col, message) = medalDict[stat]
        columns = [col]
        res = session.query(func.sum(*(getattr(table, column) for column in columns))).join(Account).filter(Account.display_name == player).group_by(AccountMedals.id).first()
        num = res[0]
        name = player
        if message != "Activities Entered" and message != "Total Number of Medals" and message != "Total Medal Score":
            message = f"Total {message} Medals"
    elif code == 3:
        (table, col, message) = medalDict[stat]
        columns = [col]
        res = session.query(func.sum(*(getattr(table, column) for column in columns))).join(Account).filter(Account.display_name == player).group_by(AccountMedals.id).first()
        num = float(res[0])
        denominator = session.query(PvPAggregate.activitiesEntered).join(Account).filter(Account.display_name == player).first()
        act = denominator[0]
        num = num/act
        name = player
        if message != "Activities Entered" and message != "Total Number of Medals" and message != "Total Medal Score":
            message = f"{message} Medals per Game"
        else:
            message = f"{message} per Game"
    #em = discord.Embed(title = f"{author}{message}{result}", colour=0xADD8E6)
    em = f"```{message} for {name}: {num}```"
    return em

def multiStatRequest(players, code, stat):
    session = Session()
    data = []
    if code == 1:
        (table, col, message) = statDict[stat]
        columns = [col]
        res = session.query(*(getattr(table, column) for column in columns), Account.display_name).join(Account).filter(Account.display_name.in_(players)).order_by(Account.display_name).all()
        data = [(item[1], truncateDecimals(item[0])) for item in res if item[0] is not None]
    elif code == 2 or code == 3:
        (table, col, message) = medalDict[stat]
        columns = [col]
        res = session.query(func.sum(*(getattr(table, column) for column in columns)), Account.display_name).join(Account).filter(Account.display_name.in_(players)).group_by(AccountMedals.id).order_by(Account.display_name).all()
        if code == 2:
            data = [(item[1], truncateDecimals(item[0])) for item in res if item[0] is not None]
        elif code == 3:
            numActivities = session.query(PvPAggregate.activitiesEntered).join(Account).filter(Account.display_name.in_(players)).order_by(Account.display_name).all()
            data = [(res[i][1], truncateDecimals(float(res[i][0])/numActivities[i][0])) for i in range(len(res)) if res[i][0] is not None]
    data = sorted(data, key=lambda x: x[1], reverse=True)
    if (code == 2 or code == 3) and message != "Activities Entered" and message != "Total Number of Medals" and message != "Total Medal Score":
        message = f"Total {message} Medals"
    em = discord.Embed(title = f"{message}", colour=0xADD8E6)
    if len(data) > 10:
        data = data[:9]
    for (name, num) in data:
        em.add_field(name=name, value=num)
    return em

def clanGraphRequest(player, code, stat):
    session = Session()
    rawdata = []
    message = ""
    if code == 1:
        (table, col, message) = statDict[stat]
        columns = [col]
        res = session.query(*(getattr(table, column) for column in columns), Account.display_name).join(Account).all()
        rawdata = [(item[1], truncateDecimals(item[0])) for item in res if item[0] is not None]
    elif code == 2:
        (table, col, message) = medalDict[stat]
        columns = [col]
        res = session.query(func.sum(*(getattr(table, column) for column in columns)), Account.display_name).join(Account).group_by(AccountMedals.id).all()
        rawdata = [(item[1], truncateDecimals(item[0])) for item in res if item[0] is not None]
    elif code == 3:
        (table, col, message) = medalDict[stat]
        
        columns = [col]
        res = session.query(func.sum(*(getattr(table, column) for column in columns)), Account.display_name).join(Account).group_by(AccountMedals.id).all()
        numActivities = session.query(PvPAggregate.activitiesEntered, Account.display_name).join(Account).all()
        #Need to associate numActivities with the correct username
        rawdata = [(item[1], truncateDecimals(item[0])/float(activity[0])) for item in res for activity in numActivities if item[1] == activity[1] and item[0] is not None and activity[0] is not None]
    if (code == 2 or code == 3) and message != "Activities Entered" and message != "Total Number of Medals" and message != "Total Medal Score":
        message = f"Total {message} Medals"
    data = sorted(rawdata, key=lambda x: x[1])
    plt.clf()
    #num_bins = 45
    #n, bins, patches = plt.hist(nums, num_bins, facecolor='blue', alpha=0.5)
    #plt.xlabel('Kill/Death Ratio')
    #plt.ylabel('Guardians')
    #plt.title('Histogram of K/D')
    objects = [item[0] for item in data]
    #objects = [" " if item != player else item for item in objects]
    values = [item[1] for item in data]
    
    fig, ax = plt.subplots(figsize=(14,6))
    index = np.arange(len(objects))
    plt.bar(index, values, alpha=0.4, color='b', align='center')
    plt.xlabel("Guardians")
    plt.ylabel(f"{message}")
    plt.title(f"Clan {message} Comparison")
    plt.xticks(index, objects)
    fig.autofmt_xdate()
    plt.tight_layout()
    plt.savefig('./Figures/hist.png')

def truncateDecimals(num):
    #Apparently I have to write my own damn significant figures checker
    if num%1==0:
        result = num
    elif num > 10000:
        result = Decimal(num).quantize(Decimal('1.'))
    else:
        def firstPowerOfTen(power, num):
            if num > power:
                return power
            else:
                return firstPowerOfTen(power/10, num)
        power = firstPowerOfTen(1000, num)
        prec = power/1000
        result = Decimal(num).quantize(Decimal(str(prec)))
    return result

def timeLeft():
    release = datetime.date(2017,9,6)
    today = datetime.date.today()
    untilRelease = str((release-today).days)
    output = "There are "+untilRelease+" days until release!"
    return output

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

# 209695933796057089
async def my_background_task():
    await client.wait_until_ready()
    intercom_select = random.randint(0, intercom_quantity)
    intercom_message = intercom[intercom_select]
    channel = discord.Object(id='209695933796057089')
    await client.send_message(channel, 'AI-COMS // Initializing Channel Interface')
    # while not client.is_closed:
    #     await client.send_message(channel, "INTERCOM // "+intercom_message)
    #     await asyncio.sleep(randint(1080,2880)) # task runs randomly between 18 minutes and 48 minutes

@client.event
async def on_member_join(member):
    server = member.server
    msg = 'Guardian {0.mention} now registered online with {1.name}!'
    await client.send_message(server, msg.format(member, server))
    # await client.send_message(discord.Message.channel, fmt.format(discord.Message))
    # member, server

current_jugs = ai_actions.random_jugs(current_jugs)
client.loop.create_task(my_background_task())
