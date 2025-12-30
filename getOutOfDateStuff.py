#!/usr/bin/env python

import sys
import os
import json
import re
import webbrowser

# INSTRUCTIONS:
# 1. Set this variable:
root = "D:\\Nintendo Switch Homebrew\\Game Backups";
# 2. Download this file, next to the python script: https://nx-missing.ghostland.at/data/working.txt
# 3. Run this script:
# python getOutOfDateStuff.py working.txt

# Useful URLs:
# https://nx-content.ghostland.at/?view=content&page=1
# https://nx-missing.ghostland.at/data/working.json
# https://nx-missing.ghostland.at/data/working.txt
# https://github.com/trembon/switch-library-manager - these guys generally keep an eye on this stuff being out-of-date:
# https://github.com/trembon/switch-library-manager/issues/97
# https://github.com/blawar/titledb - frequently out-of-date
# https://github.com/masagrator/version_dump - could be used as alternative source, all you'd have to do is change these:
# if len(splitLine) > 2:
#    titleId = splitLine[0]
#    version = int(splitLine[2])




logUpToDate = False;


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input();
        if default is not None and choice == "":
            return valid[default]
        elif choice.lower() in valid:
            return valid[choice.lower()]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

def titleIdsInList(titleId1, titleIdList):
    for titleId in titleIdList:
        if titleIdsEqual(titleId1, titleId, 3):
            return True;
    return False;

# Checks all but last N characters
def titleIdsEqual(titleId1, titleId2, numCharacters):
    return titleId1[:-numCharacters] == titleId2[:-numCharacters];

def isPotentiallyDlcForTitle(titleId1, titleIdList):
    for titleId in titleIdList:
        if titleIdsEqual(titleId1, titleId, 4):
            return True;
    return False;

myTitles = [];
for item in os.listdir(root):
    filesInFolder = os.listdir(root + "\\" + item);
    titleIds = [];
    dlcIds = [];
    version = 0;
    for toCheck in filesInFolder:
        if "." in toCheck and "[" in toCheck:
            baseMatch = re.search('.*(\\[[0-9A-F]*\\])(\\[[v0-9A-F]*\\])(\\[Base\\])', toCheck, re.IGNORECASE);
            updateMatch = re.search('.*(\\[[0-9A-F]*\\])(\\[[v0-9A-F]*\\])(\\[Update\\])', toCheck, re.IGNORECASE);
            dlcMatch = re.search('.*(\\[[0-9A-F]*\\])(\\[[v0-9A-F]*\\])(\\[DLC[\\s0-9]*\\])', toCheck, re.IGNORECASE);
            if baseMatch:
                titleParsed = baseMatch.group(1).strip("[]");
                if titleParsed not in titleIds:
                    titleIds.append(titleParsed);

            if updateMatch:
                versionString = updateMatch.group(2);
                versionParse = int(versionString.strip('v[]'));
                if (versionParse > version):
                    version = versionParse;
                titleParsed = updateMatch.group(1).strip("[]");
                if titleParsed not in titleIds:
                    titleIds.append(titleParsed);

            if dlcMatch:
                dlcTitleId = dlcMatch.group(1).strip("[]");
                dlcVersion = dlcMatch.group(2).strip("v[]");
                dlcNumber = dlcMatch.group(3).strip("[]");
                dlcDict = { "name": item, "dlcNumber": dlcNumber, "titleId": dlcTitleId, "version": dlcVersion, "latestVersion": -1, "upToDate": False, "found": False };
                dlcIds.append(dlcDict);
                
    if len(titleIds) == 0:
        print("Couldn't get code for " + item)

    titleDict = { "name": item, "titleIds": titleIds, "dlcIds": dlcIds, "version": version, "latestVersion": -1, "upToDate": False, "found": False, "anyDlcNeedUpdate": False, "missingDlc": False, "missingDlcs": [] };
    myTitles.append(titleDict);

with open(sys.argv[1], 'r') as my_file:
    for line in my_file:
        splitLine = line.rstrip().split("|");
        if len(splitLine) > 1:
            titleId = splitLine[0]
            version = int(splitLine[1])
            matchesSomething = False;
            for title in myTitles:
                if titleIdsInList(titleId, title["titleIds"]): # Must match except last 3 characters
                    # is base game, or update
                    title["found"] = True;
                    matchesSomething = True;
                    if title["latestVersion"] == -1:
                        title["latestVersion"] = version;
                    elif title["latestVersion"] < version:
                        title["latestVersion"] = version;

                for dlc in title["dlcIds"]:
                    if dlc["titleId"] == titleId: # Must match EXACTLY
                        matchesSomething = True;
                        if dlc["latestVersion"] == -1:
                            dlc["latestVersion"] = version;
                        elif dlc["latestVersion"] < version:
                            dlc["latestVersion"] = version;
                
                # If we found a row in the source text file that didn't match the base game, or updates
                # we also don't have a DLC in our files for it
                # AND the titleId in the source text matches this title - it's a DLC we don't have
                if not matchesSomething and isPotentiallyDlcForTitle(titleId, title["titleIds"]):
                    title["missingDlc"] = True;
                    title["anyDlcNeedUpdate"] = True;
                    if titleId not in title["missingDlcs"]:
                        title["missingDlcs"].append(titleId);
                        
                        
for title in myTitles:
    title["upToDate"] = str(title["latestVersion"]) == str(title["version"]);
    for dlc in title["dlcIds"]:
        dlc["upToDate"] = str(dlc["latestVersion"]) == str(dlc["version"]);
        if not dlc["upToDate"]:
            title["anyDlcNeedUpdate"] = True;

toOpen = [];
toPrint1 = [];
toPrint2 = [];
toPrint3 = [];
toPrint4 = [];
toPrint5 = [];
toPrint6 = [];
allToPrint = [toPrint1, toPrint2, toPrint3, toPrint4, toPrint5, toPrint6];
def addTitleToOpen(title):
    url = "https://rutracker.org/forum/tracker.php?nm=" + title["name"];
    if url not in toOpen:
        toOpen.append(url);

for title in myTitles:
    if title["upToDate"]:
        if not title["anyDlcNeedUpdate"]:
            if logUpToDate:
                toPrint1.append("Up To Date - " + title["name"] + " - v" + str(title["version"]));
                for dlc in title["dlcIds"]:
                    toPrint1.append("             " + dlc["titleId"] + " - " + dlc["dlcNumber"] + " - v" + str(title["version"]));
        elif title["missingDlc"]:
            toPrint2.append("Missing DLC for " + title["name"] + ": " + ", ".join(title["missingDlcs"]));
            addTitleToOpen(title);
        else:
            toPrint3.append("Need DLC Update - " + title["name"]);
            addTitleToOpen(title);
            for dlc in title["dlcIds"]:
                if dlc["latestVersion"] == -1:
                    toPrint3.append("                  " + dlc["dlcNumber"] + " - v" + str(dlc["version"]) + " (" + dlc["titleId"] + ") not in source file");
                else:
                    toPrint3.append("                  " + dlc["dlcNumber"] + " - v" + str(dlc["version"]) + " to v" + str(dlc["latestVersion"]));
    elif not title["found"]:
        toPrint4.append("Not in source file - [" + ", ".join(title["titleIds"]) + "] " + title["name"] + " - v" + str(title["version"]));
        addTitleToOpen(title);
    else:
        if title["version"] > title["latestVersion"]:
            toPrint5.append("Source file shows downgrade - [" + ", ".join(title["titleIds"]) + "] " + title["name"] + " - v" + str(title["version"]) + " to v" + str(title["latestVersion"]));
            addTitleToOpen(title);
        else:
            toPrint6.append("Needs Update - [" + ", ".join(title["titleIds"]) + "] " + title["name"] + " - v" + str(title["version"]) + " to v" + str(title["latestVersion"]));
            addTitleToOpen(title);
            

for toPrintArr in allToPrint:
    for line in toPrintArr:
        print(line);
if query_yes_no("Open search for missing items?", "no"):
    for url in toOpen:
        webbrowser.open(url);