#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, urllib2


os.system("cls")

print "Radial Engraving Conversion Engine."
print "Copyright 2014 Dave Finch.\n\n"

fName = "input.nc"
oName = "output.nc"
diameter = 63.5
stripStart = 8
stripEnd = 5
headerName = "header.txt"
footerName = "footer.txt"
acuStr = "%.2f"

def quitOnError(es, en):
    print es
    if en:
        print "I/O error({0}): {1}".format(en.errno, en.strerror)
    os._exit(0)

def authenticateUse():
    try:
        page = urllib2.urlopen("http://www.domain.com")
        content = page.read()
        if "dominicanhall" in content:
            return
        else:
            quitOnError("Failed to authenticate program.", 0)
    except urllib2.HTTPError as e:
        quitOnError("Failed to authenticate program.", e)

print "Authenticating program...."
#authenticateUse()

sac = 1
while True:
    try:
        if sys.argv[sac] == "-i":
            fName = sys.argv[sac + 1]
            sac += 2
        if sys.argv[sac] == "-o":
            oName = sys.argv[sac + 1]
            sac += 2
        if sys.argv[sac] == "-d":
            diameter = float(sys.argv[sac + 1])
            sac += 2
        if sys.argv[sac] == "-s":
            stripStart = int(sys.argv[sac + 1])
            sac += 2
        if sys.argv[sac] == "-e":
            stripEnd = int(sys.argv[sac + 1])
            sac += 2
        if sys.argv[sac] == "-h":
            headerName = sys.argv[sac + 1]
            sac += 2
        if sys.argv[sac] == "-f":
            footerName = sys.argv[sac + 1]
            sac += 2
        if sys.argv[sac] == "-a":
            if int(sys.argv[sac +1]) < 0:
                quitOnError("Error. Accuracy argument '-a' must be a positive integer.", 0)
            acuStr = "%." + sys.argv[sac + 1] + "f"
            sac += 2
    except:
        break
        

pi = 3.1415926

try:
    f = open(headerName, "r")
    header = f.read()
    f.close
except IOError as e:
    quitOnError("Error. Can't open header file : " + headerName, e)

try:
    f = open(footerName, "r")
    footer = f.read()
    f.close
except IOError as e:
    quitOnError("Error. Can't open footer file : " + footerName, e)

try:    
    inFile = open(fName, "r")
except IOError as e:
    quitOnError("Error. Can't open input file : " + fName, e)

for i in range(0, stripStart):
    scrap = inFile.readline()
    if scrap == "":
        quitOnError("Error stripping " + str(stripStart) + " lines from input file.", 0)

strList = []
while True:
    inStr = inFile.readline()
    if inStr == "":
        break
    for i in range(0, len(inStr)):
        if inStr[i] in "GXYZ":
            break
    ns = ""
    for j in range(i, len(inStr)):
        ns += inStr[j]
    strList.append(ns)
inFile.close()

try:
    for i in range(0, stripEnd):
        strList.pop()
except:
    quitOnError("Error stripping " + str(stripEnd) + " lines from input file.", 0)

linesRead = len(strList)
print str(linesRead) + " lines read.\n"

try:
    outFile = open(oName, "w")
except IOError as e:
    quitOnError("Error creating or opening output file.", e)

try:
    outFile.write(header)
except IOError as e:
    quitOnError("Error. Can't write to output file.", e)
    
print "Processing...."
outCount = 0
for s in strList:
    sg = sx = sy = sz = ""
    ss = "1234567890-."

    p = s.find("G")
    if p > -1:
        sg += "G"
        p += 1
        while s[p] in ss:
            sg += s[p]
            p += 1
    p = s.find("X")
    if p > -1:
        p += 1
        while s[p] in ss:
            sx += s[p]
            p += 1
        na = float(sx)
        sx = "X" + acuStr % na
    p = s.find("Y")
    if p > -1:
        p += 1
        while s[p] in ss:
            sy += s[p]
            p += 1
        na = float(sy)
        na = ((360 / (pi * diameter)) * na) + 180
        sy = "A" + acuStr % na
    p = s.find("Z")
    if p > -1:
        p += 1
        while s[p] in ss:
            sz += s[p]
            p += 1
        na = float(sz)
        sz = "Z" + "%.1f" % na
    
    outStr = sg + sx + sy + sz + "\n"
    try:
        outFile.write(outStr)
        outCount += 1
    except IOError as e:
        quitOnError("Error. Can't write to output file.", e)

print "\n" + str(outCount + header.count("\n") + footer.count("\n")) + " lines written to " + oName
print "\nComplete.\n"

try:
    outFile.write(footer)
except IOError as e:
    quitOnError("Error. Can't write to output file.", e)

outFile.close()

