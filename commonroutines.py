# Explicit feedback for climate modeling
# Copyright (C) 2020  Ben Kravitz
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
    
# Common routines
#
# Written by Ben Kravitz (bkravitz@iu.edu or ben.kravitz.work@gmail.com)
# Last updated 11 July 2019
#
# This script provides some common routines that you might use for processing
# model output.  It includes things like global averages.  You can add to
# this file as needed.
#
# This script is written in native python format.  Be careful with brackets [],
# white space, and making sure everything that needs to be a string is actually
# a string by putting it in quotes ''.  All lines beginning with # are comments.

import itertools

# makes an array of weights that is len(lons) by len(lats)
# you can use this for area weighting
def makeweights(lats,lons):
    nlats=len(lats)
    nlons=len(lons)
    latdiff=numpy.diff(lats,n=1,axis=0)
    temparray=numpy.arange(-90+latdiff[1]/2,90,latdiff[1])
    latedges=numpy.hstack((-90,temparray,90))
    colatedges=math.pi/2-latedges*(math.pi)/180
    dphi=(lons[3]-lons[2])*math.pi/180
    areaout=abs(numpy.diff(numpy.cos(colatedges)))*dphi
    biggest=max(areaout)
    mapcols=areaout/biggest
    weights=(numpy.tile(mapcols,(nlons,1))).transpose()
    return weights

# calculates global mean
def gmean(infield,weights):
    a=list(infield.shape)
    b=list(weights.shape)
    otherinds=len(a)*[-1]
    for k in range(len(b)):
        otherinds[k]=a.index(b[k])
    otherinds.pop(otherinds.index(-1))
    for i in range(len(a)):
        if a[i] not in b:
            timeind=i
    # want time to be last
    c=list(itertools.permutations(a))
    d=tuple(b+[a[timeind]])
    i=c.index(d)
    e=list(itertools.permutations([0,1,2]))
    infield2=numpy.transpose(infield,e[i])
    w3=numpy.reshape(numpy.tile(weights,tuple([1]+[a[timeind]])),d)
    theprod=infield2*w3
    f=theprod.shape
    theprod2=theprod
    w4=w3
    while len(f)>1:
        theprod2=numpy.sum(theprod2,axis=0)
        w4=numpy.sum(w4,axis=0)
        f=theprod2.shape
    outfield=theprod2/w4
    return outfield

# calculates L1 mean
def l1mean(infield,weights,lats):
    a=list(infield.shape)
    b=list(weights.shape)
    otherinds=len(a)*[-1]
    for k in range(len(b)):
        otherinds[k]=a.index(b[k])
    otherinds.pop(otherinds.index(-1))
    for i in range(len(a)):
        if a[i] not in b:
            timeind=i
    # want time to be last
    c=list(itertools.permutations(a))
    d=tuple(b+[a[timeind]])
    i=c.index(d)
    e=list(itertools.permutations([0,1,2]))
    infield2=numpy.transpose(infield,e[i])
    w3=numpy.reshape(numpy.tile(weights,tuple([1]+[a[timeind]])),d)
    lats2=numpy.transpose(numpy.tile(lats,(12,b[1],1)),[2,1,0])
    sinlats=numpy.sin(numpy.deg2rad(lats2))
    theprod=infield2*w3*sinlats
    f=theprod.shape
    theprod2=theprod
    w4=w3
    while len(f)>1:
        theprod2=numpy.sum(theprod2,axis=0)
        w4=numpy.sum(w4,axis=0)
        f=theprod2.shape
    outfield=theprod2/w4
    return outfield

# calculates L2 mean
def l2mean(infield,weights,lats):
    a=list(infield.shape)
    b=list(weights.shape)
    otherinds=len(a)*[-1]
    for k in range(len(b)):
        otherinds[k]=a.index(b[k])
    otherinds.pop(otherinds.index(-1))
    for i in range(len(a)):
        if a[i] not in b:
            timeind=i
    # want time to be last
    c=list(itertools.permutations(a))
    d=tuple(b+[a[timeind]])
    i=c.index(d)
    e=list(itertools.permutations([0,1,2]))
    infield2=numpy.transpose(infield,e[i])
    w3=numpy.reshape(numpy.tile(weights,tuple([1]+[a[timeind]])),d)
    lats2=numpy.transpose(numpy.tile(lats,(12,b[1],1)),[2,1,0])
    sinlats=numpy.sin(numpy.deg2rad(lats2))
    sinlats2=1.5*numpy.power(sinlats,2)-0.5
    theprod=infield2*w3*sinlats2
    f=theprod.shape
    theprod2=theprod
    w4=w3
    while len(f)>1:
        theprod2=numpy.sum(theprod2,axis=0)
        w4=numpy.sum(w4,axis=0)
        f=theprod2.shape
    outfield=theprod2/w4
    return outfield
