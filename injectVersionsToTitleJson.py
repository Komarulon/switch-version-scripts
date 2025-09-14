#!/usr/bin/env python

import sys
import json

# python injectVersionsToTitleJson.py version_dump.txt titles.json

reduceSize = True

titlesJson = {}
with open(sys.argv[2], 'r') as titlesJsonFile:
    titlesJson = json.load(titlesJsonFile)

with open(sys.argv[1], 'r') as my_file:        
    for line in my_file:
        splitLine = line.rstrip().split("|");
        if len(splitLine) > 2:
            titleId = splitLine[0]
            version = splitLine[2]
            
            # titleIds all end in 800 for some reason... updating to 000:
            titleIdList = list(titleId)
            titleIdList[len(titleIdList) - 1] = "0"
            titleIdList[len(titleIdList) - 2] = "0"
            titleIdList[len(titleIdList) - 3] = "0"
            titleId = ''.join(titleIdList)
            
            if (len(titleId) == 16):
                if titleId not in titlesJson:
                    titlesJson[titleId] = {}
                if "bannerUrl" not in titlesJson[titleId] or titlesJson[titleId]['bannerUrl'] is None:
                    titlesJson[titleId]["bannerUrl"] = "https://img-eshop.cdn.nintendo.net/i/c42553b4fd0312c31e70ec7468c6c9bccd739f340152925b9600631f2d29f8b5.jpg"
                if "iconUrl" not in titlesJson[titleId] or titlesJson[titleId]['iconUrl'] is None:
                    titlesJson[titleId]["iconUrl"] = "https://img-eshop.cdn.nintendo.net/i/ad4d31f664a1ce704f0219da2805f8459595bc3c01c3f04df2e32ba34a05b8c6.jpg"
                if "name" not in titlesJson[titleId] or titlesJson[titleId]['name'] is None:
                    titlesJson[titleId]["name"] = titleId
                titlesJson[titleId]["version"] = int(version)
                titlesJson[titleId]["id"] = titleId
                    
if reduceSize:
    for titleId in titlesJson:
        if "category" in titlesJson[titleId]:
            titlesJson[titleId].pop("category")
        if "description" in titlesJson[titleId]:
            titlesJson[titleId].pop("description")
        if "developer" in titlesJson[titleId]:
            titlesJson[titleId].pop("developer")
        if "frontBoxArt" in titlesJson[titleId]:
            titlesJson[titleId].pop("frontBoxArt")
        if "intro" in titlesJson[titleId]:
            titlesJson[titleId].pop("intro")
        if "isDemo" in titlesJson[titleId]:
            titlesJson[titleId].pop("isDemo")
        if "key" in titlesJson[titleId]:
            titlesJson[titleId].pop("key")
        if "language" in titlesJson[titleId]:
            titlesJson[titleId].pop("language")
        if "languages" in titlesJson[titleId]:
            titlesJson[titleId].pop("languages")
        if "nsuId" in titlesJson[titleId]:
            titlesJson[titleId].pop("nsuId")
        if "numberOfPlayers" in titlesJson[titleId]:
            titlesJson[titleId].pop("numberOfPlayers")
        if "publisher" in titlesJson[titleId]:
            titlesJson[titleId].pop("publisher")
        if "rank" in titlesJson[titleId]:
            titlesJson[titleId].pop("rank")
        if "rating" in titlesJson[titleId]:
            titlesJson[titleId].pop("rating")
        if "ratingContent" in titlesJson[titleId]:
            titlesJson[titleId].pop("ratingContent")
        if "regions" in titlesJson[titleId]:
            titlesJson[titleId].pop("regions")
        if "releaseDate" in titlesJson[titleId]:
            titlesJson[titleId].pop("releaseDate")
        if "rightsId" in titlesJson[titleId]:
            titlesJson[titleId].pop("rightsId")
        if "screenshots" in titlesJson[titleId]:
            titlesJson[titleId].pop("screenshots")
        if "size" in titlesJson[titleId]:
            titlesJson[titleId].pop("size")



with open('titles-injected.json', 'w') as outfile:
    json.dump(titlesJson, outfile, indent=4, sort_keys=False)
