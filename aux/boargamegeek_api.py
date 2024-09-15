
import re
import requests
import os
import requests
import xml.etree.ElementTree as ET
import time
import urllib.parse
import time
import pandas as pd
import streamlit as st

def teste():
    return "teste"

def get_game_info(batch_ids):

    url = f'https://boardgamegeek.com/xmlapi/boardgame/{batch_ids}'
    response = requests.get(url)

    game_info = False

    if response.status_code == 200:

        root = ET.fromstring(response.content)
        boardgames = root.findall("boardgame")
    
        list_of_games = []

        for boardgame in boardgames:

            primary_name = boardgame.find(".//name[@primary='true']").text
            yearpublished = boardgame.find("yearpublished").text
            minplayers = boardgame.find("minplayers").text
            maxplayers = boardgame.find("maxplayers").text
            playingtime = boardgame.find("playingtime").text
            game_id = boardgame.get('objectid')

            try:
                thumbnail = boardgame.find("thumbnail").text
            except:
                thumbnail = "https://cf.geekdo-images.com/zxVVmggfpHJpmnJY9j-k1w__itemrep/img/Py7CTY0tSBSwKQ0sgVjRFfsVUZU=/fit-in/246x300/filters:strip_icc()/pic1657689.jpg"

            game_info = {
                        "game_id":game_id,
                        "name": primary_name,
                        "year":yearpublished,
                        "minplayers":minplayers,
                        "maxplayers":maxplayers,
                        "playingtime":playingtime,
                        "thumbnail":thumbnail,
                        "url":f"https://boardgamegeek.com/boardgame/{game_id}"
                        }
            list_of_games.append(game_info)

    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

    df_games = pd.DataFrame(list_of_games)
    return df_games

def query_boardgamegeek(query):

    query = urllib.parse.quote(query)
    url = f'https://boardgamegeek.com/xmlapi/search?search={query}'
    response = requests.get(url)

    game_ids = []
    games_df = pd.DataFrame()

    if response.status_code == 200:
        
        root = ET.fromstring(response.content)
        items = root.findall("boardgame")
        batch_ids = []

        for index, item in enumerate(items,start=1):
            
            game_id = item.get('objectid')
            batch_ids.append(game_id)

            if index % 20 == 0:
                joined_ids = ",".join(batch_ids)
                game_ids.append(joined_ids)
                batch_ids = []

        if batch_ids:
            joined_ids = ",".join(batch_ids)
            game_ids.append(joined_ids)

        number_of_batches = 1


        for index, batch_id in enumerate(game_ids,start=1):
                    
            game_info_df = get_game_info(batch_id)
            games_df = pd.concat([game_info_df,games_df])
            if index == number_of_batches:
                break
            
            else:
                time.sleep(2)

    
    return games_df
