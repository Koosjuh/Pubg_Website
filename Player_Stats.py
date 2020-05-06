from pubg_python import PUBG, Shard
import copy
from enum import Enum
import requests
from contextlib import suppress
import requests
import csv
import requests
import json
import secrets

pubg_api = PUBG(secrets.pubg_key, Shard.PSN)
username = input("Please specify a username: ")
username
player_list = [username]
players = pubg_api.players().filter(player_names=player_list)

try:
    for player in players:
        player_name = player.name
        player_id = player.id
        print(player_name)
        print(player)
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
            playerlistitem += [match]
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
            if match.game_mode == "solo" :
                p_gamemode_solo = p_gamemode_solo + 1
            elif match.game_mode == "duo" :
                p_gamemode_duo = p_gamemode_duo + 1
            elif match.game_mode == "squad":
                p_gamemode_squad = p_gamemode_squad + 1
            roster = match.rosters
            print(len(roster))
            loop_roster = len(roster)
            i = 0
            r = 0
            while i < loop_roster:
                try:
                    print("==================Team ID: " + str(roster[i]) + " Team number: " + str(i + 1) + "==================")
                    i = i + 1
                    p_roster = match.rosters[int(r)]
                    name_p_roster = p_roster.participants[0]
                    participant_name = name_p_roster.name
                    name_p_roster1 = p_roster.participants[1]
                    participant_name1 = name_p_roster1.name
                    #name_p_roster2 = p_roster.participants[2]
                    #participant_name2 = name_p_roster2.name
                    #name_p_roster3 = p_roster.participants[3]
                    #participant_name3 = name_p_roster3.name
                    print (player_name)
                    print(r)
                    print(name_p_roster)
                    print(name_p_roster1)
                    if player_name in participant_name or participant_name1:
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
                        print("PSN Username: " + participant_name1)
                        print(str(name_p_roster1.damage_dealt) + " total damage dealt this match.")
                        print(str(name_p_roster1.kills) + " kills made.")
                        print(str(name_p_roster1.road_kills) + " road kills made.")
                        print(str(name_p_roster1.headshot_kills) + " headshot kills made.")
                        print(str(name_p_roster1.heals) + " times healed.")
                        survival_time_p1 = name_p_roster.time_survived / int(60)
                        print(str(survival_time_p1) + " minutes survived in match.")
                        print(str(name_p_roster1.ride_distance) + " Meters in vehicle.")
                        print(str(name_p_roster1.walk_distance) + " Meters by foot.")
                        r = r + 1
                    else:
                        r = r + 1
                        print("Else Loop")
                        print(r)
                        print(name_p_roster)
                        print(name_p_roster1)
                except(IndexError):
                    print("Index Error")
                    print(IndexError)
                    print(r)
                    print(name_p_roster)
                    print(name_p_roster1)
                    r = r + 1
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