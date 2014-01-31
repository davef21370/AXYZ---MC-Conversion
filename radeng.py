#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


fName = "input.nc"
oName = "output.nc"
diameter = 63.5
stripStart = 8
stripEnd = 5

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
    except:
        break
        

pi = 3.1415926

inFile = open(fName, "r")

for i in range(0, stripStart):
    scrap = inFile.readline()
    
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

for i in range(0, stripEnd):
    strList.pop()

outFile = open(oName, "w")

outFile.write(":9\nT9M6\nG0X0Y0Z100S6000M3H32\nG1F300\nG0\nM11\n")

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
        sx = "X" + "%.2f" % na
    p = s.find("Y")
    if p > -1:
        p += 1
        while s[p] in ss:
            sy += s[p]
            p += 1
        na = float(sy)
        na = ((360 / (pi * diameter)) * na) + 180
        sy = "A" + "%.2f" % na
    p = s.find("Z")
    if p > -1:
        p += 1
        while s[p] in ss:
            sz += s[p]
            p += 1
        na = float(sz)
        sz = "Z" + "%.1f" % na
    
    outStr = sg + sx + sy + sz + "\n"
    outFile.write(outStr)

outFile.write("Z200\nY250\nM02")
outFile.close()

