from pubg_python import PUBG, Shard
import copy
from enum import Enum
import csv
import requests
import json
import secrets
import time
import pymongo
import datetime
import dns
from datetime import datetime

now = datetime.now().time()
now2 = datetime.today().strftime('%Y-%m-%d')

current_timestamp = str(now2) + str(now)

client = pymongo.MongoClient("mongodb+srv://" + secrets.mongo_db_url + "p0oey.azure.mongodb.net/test?retryWrites=true&w=majority")
pubgstats = client["pubgstats"]

dblist = client.list_database_names()
if pubgstats in dblist:
  print("The database exists.")
else:
    print("Database is being created.....")

players_col = client.pubgstats["Players"]
matches_col = client.pubgstats["Matches"]
teams_col = client.pubgstats["Teams"]
participant_col = client.pubgstats["Participants"]
summary_col = client.pubgstats["Summary"]

pubg_api = PUBG(secrets.pubg_key, Shard.PSN)
username = input("Please specify a username: ")
username
player_list = [username]
players = pubg_api.players().filter(player_names=player_list)
psnplayers_col = client.pubgstats[username]
playermatches_col = client.pubgstats[username+"_Matches"]

try:
    for player in players:
        player_name = player.name
        player_id = player.id
        match_count =0
        match_time = 0
        vikendi_count = 0
        erangel_count = 0
        miramar_count = 0
        sanhok_count = 0
        karakin_count = 0
        playerlistitem = []
        p_gamemode_solo = 0
        p_gamemode_duo = 0
        p_gamemode_squad = 0
        for match in player.matches:
            match = pubg_api.matches().get(match.id)
            match_count = match_count + 1
            asset = match.assets[0]
            r = 0
            i = 0
            playerlistitem += [match]
            roster = match.rosters
            print(len(roster))
            loop_roster = len(roster)
            print("==================================MATCH STATISTICS==================================")
            if match.map_name == "DihorOtok_Main":
                print("Map Name: Vikendi")
                vikendi_count = vikendi_count +1
            elif match.map_name == "Desert_Main":
                print ("Map Name: Miramar")
                miramar_count = miramar_count +1
            elif match.map_name == "Baltic_Main":
                print("Map Name: Erangel")
                erangel_count = erangel_count +1
            elif match.map_name == "Summerland_Main":
                print("Map Name: Karakin")
                karakin_count = karakin_count +1
            elif match.map_name == "Savage_Main":
                print("Map Name: Sanhok")
                sanhok_count = sanhok_count +1
            else:
                 print ("Map is unknown: " + str(match.map_name) + " Please update code.")
            print("Game Mode: "+ str(match.game_mode))
            add_player = {
                "_id": player_id,
                "User ID": player_id,
                "PSN USer": username,
            }

            add_match = {
                "_id": match.id,
                "Match Date/Time": match.created_at,
                "Number of Teams": len(roster),
                "Game Mode": match.game_mode,
                "Map": match.map_name,
            }
            add_summary = {
                "_id": current_timestamp,
                "User ID": player_id,
                "PSN USer": username,
                "Matches Played": match_count,
                "Played Vikendi": vikendi_count,
                "Played Miramar": miramar_count,
                "Played Erangel": erangel_count,
                "Played Karakin": karakin_count,
                "Played Sanhok": sanhok_count,
                "Solo Matches": p_gamemode_solo,
                "Duo Matches": p_gamemode_duo,
                "Squad Matches": p_gamemode_squad,
            }
            if match.game_mode == "solo" :
                p_gamemode_solo = p_gamemode_solo + 1
                matches_col.insert_one(add_match)
                playermatches_col.insert_one(add_match)
                while i < loop_roster:
                    try:
                        team_id = roster[i]
                        team_number = i + 1
                        add_teams = {
                            "_id": str(match.game_mode) + "_" + str(match.created_at) + "_" + str(name_p_roster.name + "_TEAMID_" + str(team_number)),
                            "Team Number": team_number,
                            "PSN USer": participant_name,
                        }
                        print("==================Team ID: " + str(roster[i]) + " Team number: " + str(i + 1) + "==================")
                        i = i + 1
                        p_roster = match.rosters[int(r)]
                        name_p_roster = p_roster.participants[0]
                        participant_name = name_p_roster.name
                        print("Match Date: " + match.created_at)
                        print("PSN Username: " + participant_name)
                        print(str(name_p_roster.damage_dealt) + " total damage dealt this match.")
                        print(str(name_p_roster.kills) + " kills made.")
                        print(str(name_p_roster.road_kills) + " road kills made.")
                        print(str(name_p_roster.headshot_kills) + " headshot kills made.")
                        print(str(name_p_roster.heals) + " times healed.")
                        survival_time_p1 = name_p_roster.time_survived / int(60)
                        print(str(survival_time_p1) + " minutes survived in match.")
                        print(str(name_p_roster.ride_distance) + " Meters in vehicle.")
                        print(str(name_p_roster.walk_distance) + " Meters by foot.")
                        r = r + 1
                        add_participants = {
                            "Participant ID": str(name_p_roster),
                            "PSN Username": str(participant_name),
                            "Team ID" : match.game_mode + "_" + match.created_at + "_" + name_p_roster.name + "_TEAMID_" + str(team_number),
                            "Damage Dealt": name_p_roster.damage_dealt,
                            "Kills": name_p_roster.kills,
                            "Road Kills": name_p_roster.road_kills,
                            "Headshot Kills": name_p_roster.headshot_kills,
                            "Times healed": name_p_roster.heals,
                            "Match Survival Time": survival_time_p1,
                            "Ride Distance": name_p_roster.ride_distance,
                            "Walk Distance": name_p_roster.walk_distance,
                        }
                        participant_col.insert_one(add_participants)
                        teams_col.insert_one(add_teams)
                    except(IndexError):
                        r = r + 1
                        print("Index Error Solo")
                        pass
            elif match.game_mode == "duo" :
                p_gamemode_duo = p_gamemode_duo + 1
                matches_col.insert_one(add_match)
                playermatches_col.insert_one(add_match)
                while i < loop_roster:
                    try:
                        team_id = roster[i]
                        team_number = i + 1
                        print("==================Team ID: " + str(roster[i]) + " Team number: " + str(
                            i + 1) + "==================")
                        i = i + 1
                        p_roster = match.rosters[int(r)]
                        name_p_roster = p_roster.participants[0]
                        participant_name = name_p_roster.name
                        print("Match Date: " + match.created_at)
                        print("PSN Username: " + participant_name)
                        print(str(name_p_roster.damage_dealt) + " total damage dealt this match.")
                        print(str(name_p_roster.kills) + " kills made.")
                        print(str(name_p_roster.road_kills) + " road kills made.")
                        print(str(name_p_roster.headshot_kills) + " headshot kills made.")
                        print(str(name_p_roster.heals) + " times healed.")
                        survival_time_p1 = name_p_roster.time_survived / int(60)
                        print(str(survival_time_p1) + " minutes survived in match.")
                        print(str(name_p_roster.ride_distance) + " Meters in vehicle.")
                        print(str(name_p_roster.walk_distance) + " Meters by foot.")
                        name_p_roster1 = p_roster.participants[1]
                        participant_name1 = name_p_roster1.name
                        print("PSN Username: " + participant_name1)
                        print(str(name_p_roster1.damage_dealt) + " total damage dealt this match.")
                        print(str(name_p_roster1.kills) + " kills made.")
                        print(str(name_p_roster1.road_kills) + " road kills made.")
                        print(str(name_p_roster1.headshot_kills) + " headshot kills made.")
                        print(str(name_p_roster1.heals) + " times healed.")
                        print(str(name_p_roster1.ride_distance) + " Meters in vehicle.")
                        print(str(name_p_roster1.walk_distance) + " Meters by foot.")
                        r = r + 1
                        add_teams = {
                            "_id": match.game_mode + "_" + match.created_at + "_" + name_p_roster.name + "_TEAMID_" + str(team_number),
                            "Team Number": team_number,
                            "UserID": participant_name,
                            "UserID": participant_name1,
                        }
                        add_participants = {
                            "Participant ID": str(name_p_roster),
                            "PSN Username": str(participant_name),
                            "Team ID": match.game_mode + "_" + match.created_at + "_" + name_p_roster.name + "_TEAMID_" + str(
                                team_number),
                            "Damage Dealt": name_p_roster.damage_dealt,
                            "Kills": name_p_roster.kills,
                            "Road Kills": name_p_roster.road_kills,
                            "Headshot Kills": name_p_roster.headshot_kills,
                            "Times healed": name_p_roster.heals,
                            "Match Survival Time": survival_time_p1,
                            "Ride Distance": name_p_roster.ride_distance,
                            "Walk Distance": name_p_roster.walk_distance,
                            "Participant ID": str(name_p_roster1),
                            "PSN Username": str(participant_name1),
                            "Damage Dealt": name_p_roster1.damage_dealt,
                            "Kills": name_p_roster1.kills,
                            "Road Kills": name_p_roster1.road_kills,
                            "Headshot Kills": name_p_roster1.headshot_kills,
                            "Times healed": name_p_roster1.heals,
                            "Match Survival Time": survival_time_p1,
                            "Ride Distance": name_p_roster1.ride_distance,
                            "Walk Distance": name_p_roster1.walk_distance,
                        }
                        teams_col.insert_one(add_teams)
                        participant_col.insert_one(add_participants)
                    except(IndexError):
                        r = r + 1
                        print("Index Error Duo, user was solo in this match")
                        pass
            elif match.game_mode == "squad":
                p_gamemode_squad = p_gamemode_squad + 1
                try:
                    matches_col.insert_one(add_match)
                except:
                    print("Duplicate match")
                    pass
                try:
                     playermatches_col.insert_one(add_match)
                except:
                    print("Duplicate")
                    pass
                while i < loop_roster:
                    try:
                        team_id = roster[i]
                        team_number = i + 1
                        print("==================Team ID: " + str(roster[i]) + " Team number: " + str(i + 1) + "==================")
                        i = i + 1
                        p_roster = match.rosters[int(r)]
                        name_p_roster = p_roster.participants[0]
                        participant_name = name_p_roster.name
                        print("Match Date: " + match.created_at)
                        print("PSN Username: " + participant_name)
                        print(str(name_p_roster.damage_dealt) + " total damage dealt this match.")
                        print(str(name_p_roster.kills) + " kills made.")
                        print(str(name_p_roster.road_kills) + " road kills made.")
                        print(str(name_p_roster.headshot_kills) + " headshot kills made.")
                        print(str(name_p_roster.heals) + " times healed.")
                        survival_time_p1 = name_p_roster.time_survived / int(60)
                        print(str(survival_time_p1) + " minutes survived in match.")
                        print(str(name_p_roster.ride_distance) + " Meters in vehicle.")
                        print(str(name_p_roster.walk_distance) + " Meters by foot.")
                        name_p_roster1 = p_roster.participants[1]
                        participant_name1 = name_p_roster1.name
                        print("PSN Username: " + participant_name1)
                        print(str(name_p_roster1.damage_dealt) + " total damage dealt this match.")
                        print(str(name_p_roster1.kills) + " kills made.")
                        print(str(name_p_roster1.road_kills) + " road kills made.")
                        print(str(name_p_roster1.headshot_kills) + " headshot kills made.")
                        print(str(name_p_roster1.heals) + " times healed.")
                        survival_time_p2 = name_p_roster1.time_survived / int(60)
                        print(str(survival_time_p1) + " minutes survived in match.")
                        print(str(name_p_roster1.ride_distance) + " Meters in vehicle.")
                        print(str(name_p_roster1.walk_distance) + " Meters by foot.")
                        name_p_roster2 = p_roster.participants[2]
                        participant_name2 = name_p_roster2.name
                        print("PSN Username: " + participant_name2)
                        print(str(name_p_roster2.damage_dealt) + " total damage dealt this match.")
                        print(str(name_p_roster2.kills) + " kills made.")
                        print(str(name_p_roster2.road_kills) + " road kills made.")
                        print(str(name_p_roster2.headshot_kills) + " headshot kills made.")
                        print(str(name_p_roster2.heals) + " times healed.")
                        survival_time_p3 = name_p_roster2.time_survived / int(60)
                        print(str(survival_time_p2) + " minutes survived in match.")
                        print(str(name_p_roster2.ride_distance) + " Meters in vehicle.")
                        print(str(name_p_roster2.walk_distance) + " Meters by foot.")
                        name_p_roster3 = p_roster.participants[3]
                        participant_name3 = name_p_roster3.name
                        print("PSN Username: " + participant_name3)
                        print(str(name_p_roster3.damage_dealt) + " total damage dealt this match.")
                        print(str(name_p_roster3.kills) + " kills made.")
                        print(str(name_p_roster3.road_kills) + " road kills made.")
                        print(str(name_p_roster3.headshot_kills) + " headshot kills made.")
                        print(str(name_p_roster3.heals) + " times healed.")
                        survival_time_p4 = name_p_roster3.time_survived / int(60)
                        print(str(survival_time_p3) + " minutes survived in match.")
                        print(str(name_p_roster3.ride_distance) + " Meters in vehicle.")
                        print(str(name_p_roster3.walk_distance) + " Meters by foot.")
                        r = r + 1
                        add_teams = {
                            "_id": match.game_mode + "_" + match.created_at + "_" + name_p_roster.name + "_TEAMID_" + str(team_number),
                            "Team Number": team_number,
                            "UserID": participant_name,
                            "UserID": participant_name1,
                            "UserID": participant_name2,
                            "UserID": participant_name3,
                        }
                        add_participants = {
                            "Participant ID": str(name_p_roster),
                            "PSN Username": str(participant_name),
                            "Team ID": match.game_mode + "_" + match.created_at + "_" + name_p_roster.name + "_TEAMID_" + str(
                                team_number),
                            "Damage Dealt": name_p_roster.damage_dealt,
                            "Kills": name_p_roster.kills,
                            "Road Kills": name_p_roster.road_kills,
                            "Headshot Kills": name_p_roster.headshot_kills,
                            "Times healed": name_p_roster.heals,
                            "Match Survival Time": survival_time_p1,
                            "Ride Distance": name_p_roster.ride_distance,
                            "Walk Distance": name_p_roster.walk_distance,
                            "Participant ID": str(name_p_roster2),
                            "PSN Username": str(participant_name2),
                            "Damage Dealt": name_p_roster2.damage_dealt,
                            "Kills": name_p_roster2.kills,
                            "Road Kills": name_p_roster2.road_kills,
                            "Headshot Kills": name_p_roster2.headshot_kills,
                            "Times healed": name_p_roster2.heals,
                            "Match Survival Time": survival_time_p2,
                            "Ride Distance": name_p_roster1.ride_distance,
                            "Walk Distance": name_p_roster1.walk_distance,
                            "Participant ID": str(name_p_roster2),
                            "PSN Username": str(participant_name2),
                            "Damage Dealt": name_p_roster2.damage_dealt,
                            "Kills": name_p_roster2.kills,
                            "Road Kills": name_p_roster2.road_kills,
                            "Headshot Kills": name_p_roster2.headshot_kills,
                            "Times healed": name_p_roster2.heals,
                            "Match Survival Time": survival_time_p2,
                            "Ride Distance": name_p_roster2.ride_distance,
                            "Walk Distance": name_p_roster2.walk_distance,
                            "Participant ID": str(name_p_roster3),
                            "PSN Username": str(participant_name3),
                            "Damage Dealt": name_p_roster3.damage_dealt,
                            "Kills": name_p_roster3.kills,
                            "Road Kills": name_p_roster3.road_kills,
                            "Headshot Kills": name_p_roster3.headshot_kills,
                            "Times healed": name_p_roster3.heals,
                            "Match Survival Time": survival_time_p3,
                            "Ride Distance": name_p_roster3.ride_distance,
                            "Walk Distance": name_p_roster3.walk_distance,
                        }
                        teams_col.insert_one(add_teams)
                        participant_col.insert_one(add_participants)
                    except(IndexError):
                        r = r + 1
                        print ("Index Error Squad, user did not have a full squad.")
                        pass
            total_match_time = match.duration / 60
            match_time = match_time + total_match_time
            print("Game took " + str(total_match_time) + " minutes")
        print("===============SUMMARY " + player_name + "===============")
        print("Statistics past 2 weeks          : ")
        print("Total matches played past 2 weeks: " + str(match_count))
        print("Played the map Erangel   : " + str(erangel_count) + " times.")
        print("Played the map Miramar   : " + str(miramar_count) + " times.")
        print("Played the map Sanhok    : " + str(sanhok_count) + " times.")
        print("Played the map Vikendi   : " + str(vikendi_count) + " times.")
        print("Played the map Karakin   : " + str(karakin_count) + " times.")
        print("Played gamemode solo     : " + str(p_gamemode_solo) + " times.")
        print("Played gamemode duo      : " + str(p_gamemode_duo) + " times.")
        print("Played gamemode squad    : " + str(p_gamemode_squad) + " times.")
        try:
            matches_col.insert_one(add_match)
            summary_col.insert_one(add_summary)
            psnplayers_col.insert_one(add_player)
        except:
            print("Double entry")
            pass
except():
    print("An error has occured. Was " + player_name + " active past 14 days?")
    pass
    total_match_time = match.duration / 60
    match_time = match_time + total_match_time
    print("Game took " + str(total_match_time) + " minutes")
    print ("===============SUMMARY "+ player_name + "===============")
    print("Statistics past 2 weeks          : ")
    print("Total matches played past 2 weeks: " + str(match_count))
    print("Played the map Erangel   : " + str(erangel_count) + " times.")
    print("Played the map Miramar   : " + str(miramar_count) + " times.")
    print("Played the map Sanhok    : " + str(sanhok_count) + " times.")
    print("Played the map Vikendi   : " + str(vikendi_count) + " times.")
    print("Played the map Karakin   : " + str(karakin_count) + " times.")
    print("Played gamemode solo     : " + str(p_gamemode_solo) + " times.")
    print("Played gamemode duo      : " + str(p_gamemode_duo) + " times.")
    print("Played gamemode squad    : " + str(p_gamemode_squad) + " times.")
