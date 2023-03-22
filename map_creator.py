# -*- coding: utf-8 -*-
import requests
import json
import folium
import random
from volume_numbers import volume_numbers_list
from folium.plugins import FastMarkerCluster
import re

randomise_coordinates = True
lat_range = 0.0025 #0.0005
long_range = 0.005 #0.001
language_colours = {
    "ga": "#080",
    "en": "#f00",
    "mixed": "#f80",
}

query_colours = ["#f00", "#080", "#008", "#f80", "#80f", "#cc0", "#088", "#f88", "#888", "#840"]
query_shapes = ["●", "■", "▲", "◆", "○", "□", "△", "◇", "◍", "▥"]
use_query_colours = True

no_title = {
    "ga": "(gan teideal)",
    "en": "(no title)",
    "mixed": "(gan teideal/no title)",
}

number_of_markers = 0

points = {
    "ga": [],
    "en": [],
    "mixed": []
}

keyword_search = True

cbes_word_count = 0

#[^\u0000-\u007F\u00a0áéíóúÁÉÍÓÚ“”‘’–—…£½¼¾⅜†°÷·]

while True:
    m_ga = ""
    m_en = ""
    m_mixed = ""
    m_all = ""

    search_queries = []
    found_queries_amounts = []

    number_of_queries = int(input("How many words/phrases? "))
    for i in range(number_of_queries):
        search_queries.append(input("{0}: ".format(i+1)))
        found_queries_amounts.append(0)

    #go through each volume
    for volume_number in volume_numbers_list:
        with open("volumes\\{0}.json".format(volume_number), "r", encoding='utf-8') as read_file:
            data = json.load(read_file)

        print(volume_number)

        volume = data[0]
        parts = volume["parts"]

        for part in parts:
            items = part["items"]

            for item in items:
                    search_queries_found = []
                    #search text for keyword

                    if keyword_search:
                        pages = volume["pages"]
                        item_id = item["id"]

                        for item_page_id in item["pages"]:
                            for page in pages:
                                if page["id"] == item_page_id:
                                    for transcript in page["transcripts"]:
                                        if transcript["itemID"] == item_id:
                                            cbes_word_count += len(transcript["text"].split(" "))
                                            for i in range(number_of_queries):
                                                if re.search(search_queries[i], transcript["text"], re.IGNORECASE) != None:
                                                    if i not in search_queries_found:
                                                        search_queries_found.append(i)
                                                        found_queries_amounts[i] += 1
                                                    characters =  transcript["text"][re.search(search_queries[i], transcript["text"], re.IGNORECASE).start(0)]
                                                    #print("https://www.duchas.ie/ga/cbes/" + str(part["id"]) + "/" + \
                                                    #      str(page["id"]) + "/" + str(item["id"]) + "/\t" + str(characters))
                    else:
                        search_queries_found = [0]
                    #get info about language, informants, collectors and location
                    if (not keyword_search) or len(search_queries_found) > 0:
                        for found_query_id in search_queries_found:
                            if "informants" in item and len(item["informants"]) > 0 and \
                                "addressesIreland" in item["informants"][0] and \
                                    len(item["informants"][0]["addressesIreland"]) > 0:
                                coords = item["informants"][0]["addressesIreland"][0]["coordinates"]
                                speaker_name = item["informants"][0]["names"][0]["fullName"]
                                    
                                if len(item["languages"]) == 2 and "ga" in item["languages"] and "en" in item["languages"]:
                                    item_language = "mixed"
                                elif len(item["languages"]) > 0:
                                    item_language = item["languages"][0]

                                #print("{0}, {1}".format(coords["latitude"], coords["longitude"]))

                                current_lat =  coords["latitude"]
                                current_long =  coords["longitude"]
                                
                                if randomise_coordinates:
                                    current_lat += random.uniform(0-lat_range, lat_range)
                                    current_long += random.uniform(0-long_range, long_range)

                                #folium.Marker((current_lat, current_long), popup=(speaker_name), \
                                #            icon=folium.DivIcon(html="<div style='color: {0}'>●</div>".format(language_colours[item_language]))).add_to(m)
                                
                                if item["title"]: item_title = item["title"]
                                else: item_title = no_title[item_language]

                                popup_info = "<a href=\"https://www.duchas.ie/ga/cbes/{0}/{1}\" target=\"_blank\">{2}</a>".format(\
                                    part["id"], item["firstPageID"], item_title)
                                points[item_language].append([current_lat, current_long, popup_info, query_colours[found_query_id]])

                                number_of_markers += 1



                            elif "collectors" in item and len(item["collectors"]) > 0 and \
                                "addressesIreland" in item["collectors"][0] and \
                                    len(item["collectors"][0]["addressesIreland"]) > 0:
                                coords = item["collectors"][0]["addressesIreland"][0]["coordinates"]
                                speaker_name = item["collectors"][0]["names"][0]["fullName"]
                                    
                                if len(item["languages"]) == 2 and "ga" in item["languages"] and "en" in item["languages"]:
                                    item_language = "mixed"
                                elif len(item["languages"]) > 0:
                                    item_language = item["languages"][0]

                                #print("{0}, {1}".format(coords["latitude"], coords["longitude"]))

                                current_lat =  coords["latitude"]
                                current_long =  coords["longitude"]
                                
                                if randomise_coordinates:
                                    current_lat += random.uniform(0-lat_range, lat_range)
                                    current_long += random.uniform(0-long_range, long_range)

                                #folium.Marker((current_lat, current_long), popup=(speaker_name), \
                                #            icon=folium.DivIcon(html="<div style='color: {0}'>▲</div>".format(language_colours[item_language]))).add_to(m)
                                
                                if item["title"]: item_title = item["title"]
                                else: item_title = no_title[item_language]

                                popup_info = "<a href=\"https://www.duchas.ie/ga/cbes/{0}/{1}\" target=\"_blank\">{2}</a>".format(\
                                    part["id"], item["firstPageID"], item_title)
                                points[item_language].append([current_lat, current_long, popup_info, query_colours[found_query_id]])
                                
                                number_of_markers += 1



                            elif "locationsIreland" in item and len(item["locationsIreland"]) > 0:
                                #print(item["locationsIreland"][0])
                                coords = item["locationsIreland"][0]["coordinates"]
                                #speaker_name = item["informants"][0]["names"][0]["fullName"]
                                
                                if len(item["languages"]) == 2 and "ga" in item["languages"] and "en" in item["languages"]:
                                    item_language = "mixed"
                                elif len(item["languages"]) > 0:
                                    item_language = item["languages"][0]

                                #print("{0}, {1}".format(coords["latitude"], coords["longitude"]))

                                current_lat =  coords["latitude"]
                                current_long =  coords["longitude"]
                                
                                if randomise_coordinates:
                                    current_lat += random.uniform(0-lat_range, lat_range)
                                    current_long += random.uniform(0-long_range, long_range)

                                #folium.Marker((current_lat, current_long), popup=(item["title"]), \
                                #            icon=folium.DivIcon(html="<div style='color: {0}'>+</div>".format(language_colours[item_language]))).add_to(m)

                                if item["title"]: item_title = item["title"]
                                else: item_title = no_title[item_language]

                                popup_info = "<a href=\"https://www.duchas.ie/ga/cbes/{0}/{1}\" target=\"_blank\">{2}</a>".format(\
                                    part["id"], item["firstPageID"], item_title)
                                points[item_language].append([current_lat, current_long, popup_info, query_colours[found_query_id]])
                                
                                number_of_markers += 1
                            else:
                                pass #print("No coords found")

    print("CBÉS word count = {0}".format(cbes_word_count))
    print("Number of markers: {0}".format(number_of_markers))
    print("ga: {0}\nen: {1}\nmixed: {2}".format(len(points["ga"]), len(points["en"]), len(points["mixed"])))

    for i in range(len(search_queries)):
        print("[{0}] {1}: {2}".format(i+1, search_queries[i], found_queries_amounts[i]))
        
    ga_callback2 = """\
    function (row) {
        var marker;
        marker = L.circle(new L.LatLng(row[0], row[1]), {color:'green'});
        return marker;
    };
    """
    ga_callback = ('function (row) {' 
                    'var marker = L.circle(new L.LatLng(row[0], row[1]), {color: row[3]});'
                    "var popup = L.popup({maxWidth: '500'});"
                    "const display_text = {text: row[2]};"
                    "var mytext = $(`<div id='mytext' class='display_text' style='width: 100.0%; height: 100.0%;'> ${display_text.text}</div>`)[0];"
                    "popup.setContent(mytext);"
                    "marker.bindPopup(popup);"
                    'return marker};')

    en_callback = ('function (row) {' 
                    'var marker = L.circle(new L.LatLng(row[0], row[1]), {color: row[3]});'
                    "var popup = L.popup({maxWidth: '500'});"
                    "const display_text = {text: row[2]};"
                    "var mytext = $(`<div id='mytext' class='display_text' style='width: 100.0%; height: 100.0%;'> ${display_text.text}</div>`)[0];"
                    "popup.setContent(mytext);"
                    "marker.bindPopup(popup);"
                    'return marker};')

    mixed_callback = ('function (row) {' 
                    'var marker = L.circle(new L.LatLng(row[0], row[1]), {color: row[3]});'
                    "var popup = L.popup({maxWidth: '500'});"
                    "const display_text = {text: row[2]};"
                    "var mytext = $(`<div id='mytext' class='display_text' style='width: 100.0%; height: 100.0%;'> ${display_text.text}</div>`)[0];"
                    "popup.setContent(mytext);"
                    "marker.bindPopup(popup);"
                    'return marker};')

    chosen_tileset = "OpenStreetMap"
    m_ga = folium.Map((53.43, -7.93), zoom_start=7, tiles=chosen_tileset)
    m_en = folium.Map((53.43, -7.93), zoom_start=7, tiles=chosen_tileset)
    m_mixed = folium.Map((53.43, -7.93), zoom_start=7, tiles=chosen_tileset)
    m_all = folium.Map((53.43, -7.93), zoom_start=7, tiles=chosen_tileset)

    #add legend for each query
    if keyword_search:
        for i in range(number_of_queries):
            folium.Marker((55-i, -15), icon=folium.DivIcon(\
                html=f"""<div style="font-family: sans-serif; font-size: 36pt; color: {query_colours[i]}; width: 500px">{search_queries[i]}</div>""")).add_to(m_ga)
            folium.Marker((55-i, -15), icon=folium.DivIcon(\
                html=f"""<div style="font-family: sans-serif; font-size: 36pt; color: {query_colours[i]}; width: 500px">{search_queries[i]}</div>""")).add_to(m_en)
            folium.Marker((55-i, -15), icon=folium.DivIcon(\
                html=f"""<div style="font-family: sans-serif; font-size: 36pt; color: {query_colours[i]}; width: 500px">{search_queries[i]}</div>""")).add_to(m_mixed)
            folium.Marker((55-i, -15), icon=folium.DivIcon(\
                html=f"""<div style="font-family: sans-serif; font-size: 36pt; color: {query_colours[i]}; width: 500px">{search_queries[i]}</div>""")).add_to(m_all)

    #add markers for each language using FastMarkerCluster
    m_en.add_child(FastMarkerCluster(points["en"], callback=en_callback, disableClusteringAtZoom=7))
    m_mixed.add_child(FastMarkerCluster(points["mixed"], callback=mixed_callback, disableClusteringAtZoom=7))
    m_ga.add_child(FastMarkerCluster(points["ga"], callback=ga_callback, disableClusteringAtZoom=7))

    m_all.add_child(FastMarkerCluster(points["en"], callback=en_callback, disableClusteringAtZoom=7))
    m_all.add_child(FastMarkerCluster(points["mixed"], callback=mixed_callback, disableClusteringAtZoom=7))
    m_all.add_child(FastMarkerCluster(points["ga"], callback=ga_callback, disableClusteringAtZoom=7))

    m_ga.save("map_ga.html")
    m_en.save("map_en.html")
    m_mixed.save("map_mixed.html")
    m_all.save("map_all.html")
