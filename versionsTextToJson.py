#!/usr/bin/env python

import sys
import json

# python versionsTextToJson.py version_dump.txt

mockVersionHistory = False

versionHistory = {}
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
                if titleId not in versionHistory:
                    versionHistory[titleId] = {}

                if mockVersionHistory:
                    day = 1;
                    if int(version) == 0:
                        if version not in versionHistory[titleId]:
                            versionHistory[titleId][int(version)] = "1900-01-01"
                    else:                    
                        versionInt = 65536
                        while versionInt <= int(version):
                            versionString = str(versionInt)
                            if versionString not in versionHistory[titleId]:
                                versionHistory[titleId][int(versionString)] = ("1900-01-" + ('%02d' % day))
                            versionInt += 65536
                            day += 1
                else:
                    if version not in versionHistory[titleId]:
                        versionHistory[titleId][int(version)] = "1900-01-01"
                    

with open('versions.json', 'w') as outfile:
    json.dump(versionHistory, outfile, indent=4, sort_keys=True)
