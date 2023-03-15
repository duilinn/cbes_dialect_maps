# cbes_linguistic_maps

Takes a set of regex queries and returns 4 Folium maps that show hits for those queries in the Schools' Collection (Bailiúchán na Scol) in English, Irish, mixed texts and all 3 combined. Only items in the collection with associated geographical data are shown.

Due to copyright reasons the volumes themselves can't be included here, so obtain an API key from ![gaois.ie](https://www.gaois.ie/en/technology/developers/login/), put the API key in a file called api_key.py and run volumes_downloader.py. The volumes are about 420 MB in JSON format.

![A map of Ireland showing the various words for "potato" in Irish dialects. "Préata" in Donegal in the northwest (coloured red), "fata" in Connacht in the west (coloured green), and "práta" in Munster in the south (coloured blue).](https://raw.githubusercontent.com/duilinn/cbes_linguistic_maps/main/examples/potatoes_ga.png)