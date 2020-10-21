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

# Driver Routines
#
# Written by Ben Kravitz (bkravitz@iu.edu or ben.kravitz.work@gmail.com)
# Last updated 11 July 2019
#
# This script contains all of the under-the-hood stuff that the explicit feedback
# code suite uses.
#
# This script is written in native python format.  Be careful with brackets [],
# white space, and making sure everything that needs to be a string is actually
# a string by putting it in quotes ''.  All lines beginning with # are comments.

#########################################################
###############     CODE BEGINS HERE      ###############
###############  MODIFY AT YOUR OWN RISK  ###############
#########################################################

import os
import sys
import numpy
import math
import datetime

# Subroutine that converts read in text file lines into a list
def linestolist(linesraw,linelist):
    delimiter = ''
    for k in range(len(linelist)):
        temp = linelist[k]
        temp4 = list(temp)
        for j in range(len(temp4)):
            if temp4[j]=='\n':
                del temp4[j]
        temp5 = delimiter.join(temp4)
        temp6 = temp5.split(',')
        linelist[k] = temp6

# Subroutine that converts read in text file lines into a list
def linestolist2(linesraw,linelist):
    delimiter = ''
    for k in range(len(linelist)):
        temp = linelist[k]
        temp4 = list(temp)
        for j in range(len(temp4)):
            if temp4[j]=='\n':
                del temp4[j]
        temp5 = delimiter.join(temp4)
        temp6 = temp5.split(' ')
        linelist[k] = temp6

# Turns partially extracted CESM output (netcdf file containing all times but one variable)
#   into a numpy array that can be passed to the controller
# infile refers to the absolute path of the file
# Note that this is hard-coded for 2-D fields (i.e., there is currently no capability for
#   a vertical dimension).
def readfile(infile,varname):
    os.system('ncdump '+infile+' > '+scratchdir+'/temp.txt') # hackish, but it doesn't rely on netcdf python libraries
    f=open(scratchdir+'/temp.txt','r')
    r=f.readlines()
    f.close()
    i=r.index('data:\n')
    r2=r[i:]
    for j in range(len(r2)):
        if 'lat' in r2[j]:
            c1=j
    for j in range(c1,len(r2)):
        if ';' in r2[j]:
            c2=j
            break
    latstemp=r2[c1:c2+1]        
    lats=(''.join((''.join(''.join(latstemp).split('\n'))).split(' '))).split(',')
    temp=lats[0].split('=')
    lats[0]=temp[1]
    temp=lats[-1].split(';')
    lats[-1]=temp[0]
    for j in range(len(r2)):
        if 'lon' in r2[j]:
            c1=j
    for j in range(c1,len(r2)):
        if ';' in r2[j]:
            c2=j
            break
    lonstemp=r2[c1:c2+1]        
    lons=(''.join((''.join(''.join(lonstemp).split('\n'))).split(' '))).split(',')
    temp=lons[0].split('=')
    lons[0]=temp[1]
    temp=lons[-1].split(';')
    lons[-1]=temp[0]
    for j in range(len(r2)):
        if 'time' in r2[j] and 'bnds' not in r2[j]:
            c1=j
    for j in range(c1,len(r2)):
        if ';' in r2[j]:
            c2=j
            break
    timetemp=r2[c1:c2+1]        
    time=(''.join((''.join(''.join(timetemp).split('\n'))).split(' '))).split(',')
    temp=time[0].split('=')
    time[0]=temp[1]
    temp=time[-1].split(';')
    time[-1]=temp[0]
    for j in range(len(r2)):
        if varname in r2[j]:
            c1=j
    for j in range(c1,len(r2)):
        if ';' in r2[j]:
            c2=j
            break
    keepvals=r2[c1+1:c2+1]
    keepvals2=(''.join((''.join(''.join(keepvals).split('\n'))).split(' '))).split(',')
    temp=keepvals2[-1].split(';')
    keepvals2[-1]=temp[0]
    for j in range(len(keepvals2)):
        if keepvals2[j]=='_':
            keepvals2[j]=numpy.nan
    nlats=len(lats)
    nlons=len(lons)
    ntimes=len(time)
    b=numpy.asarray([float(i) for i in keepvals2])
    c=b.reshape((ntimes,nlats,nlons))
    lonsarray=numpy.asarray([float(i) for i in lons])
    latsarray=numpy.asarray([float(i) for i in lats])
    return c,latsarray,lonsarray,time

# Extracts one variable (but all times) from the raw CESM output
# Then calls the readfile subroutine
# Returned values are numpy arrays that can be fed into the controller
def extractvars(varname,varloc,runname,whichnames,archivedir,scratchdir):
    os.system('mkdir -p '+scratchdir)
    for k in range(len(whichnames)):
        fname=whichnames[k]
        preamble=len(runname+'.'+varloc+'.')
        post=len('.nc')
        whichtime=fname[preamble:-post]
        os.system('ncks -v '+varname+' '+archivedir+'/'+fname+' '+scratchdir+'/'+varname+'_'+whichtime+'.nc')
    os.system('ncrcat '+scratchdir+'/*.nc '+scratchdir+'/'+varname+'_out.nc')
    vals,lats,lons,times=readfile(scratchdir+'/'+varname+'_out.nc',varname)
    os.system('rm -r '+scratchdir)
    return vals,lats,lons,times

# Once the controller returns the namelist values, this replaces/appends those values
#   into the 'user_nl_XXX' file
# whichfile describes the filename (like 'user_nl_cam')
# invals is a list of pairs.  The first item in the pair is the namelist parameter to
#   be modified, and the second item is the new value.
def fixnamelist(whichfile,invals,casepath):
    n=len(invals)
    paramnames=[]
    paramvals=[]
    for i in range(n):
        if i%2==0:
	    paramnames.append(invals[i])
	else:
	    paramvals.append(invals[i])
    print paramnames
    print paramvals
    f=file(casepath+'/'+whichfile)
    newlines=[]
    flags=n/2*[0]
    for line in f:
        for k in range(n/2):
            if paramnames[k] in line:
                line=paramnames[k]+'='+paramvals[k]+'\n'
                flags[k]=1
        newlines.append(line)
    for k in range(len(flags)):
        if flags[k]==0:
            theline=paramnames[k]+'='+paramvals[k]+'\n'
            newlines.append(theline)
    f.close()
    outfile=file(casepath+'/'+whichfile+'_mod','w')
    for q in range(len(newlines)):
        outfile.write(newlines[q])
    outfile.close()
    os.system('mv '+casepath+'/'+whichfile+'_mod '+casepath+'/'+whichfile)

# does the same thing as fixnamelist but allows for more generic strings
# it will search for the first item in the invals pair and replace the entire line with
#  the second item of the pair
def fixnamelist2(whichfile,invals,casepath):
    n=len(invals)
    paramnames=[]
    paramvals=[]
    for i in range(n):
        if i%2==0:
	    paramnames.append(invals[i])
	else:
	    paramvals.append(invals[i])
    f=file(casepath+'/'+whichfile)
    newlines=[]
    flags=n/2*[0]
    for line in f:
        for k in range(n/2):
            if paramnames[k] in line:
                line=paramvals[k]
                flags[k]=1
        newlines.append(line)
    for k in range(len(flags)):
        if flags[k]==0:
            theline=paramvals[k]
            newlines.append(theline)
    f.close()
    outfile=file(casepath+'/'+whichfile+'_mod','w')
    for q in range(len(newlines)):
        outfile.write(newlines[q])
    outfile.close()
    os.system('mv '+casepath+'/'+whichfile+'_mod '+casepath+'/'+whichfile)

## This modifies env_run.xml to ensure that it resubmits
#def fixenvrun(casepath):
#    cwd=os.getcwd()
#    os.chdir(casepath)
#    os.system('./xmlchange -file env_run.xml -id RESUBMIT -val '+str(maxrest))
#    os.chdir(cwd)

# When messing with days/months, sometimes the leading zero gets cut off.  This puts it
#   back when appropriate.
def zeropad(innum):
    if innum<10:
        outnum='0'+str(innum)
    else:
        outnum=str(innum)
    return outnum

# Returns a list of file names that the script is to extract to feed into the above subroutines.
#  The purpose of this routine is to figure out which times to extract (as opposed to
#  doing everything that's sitting in the archive directory).
# This also calculates whether we have reached the end of the run (as specified by
#   maxrest.  If so, it returns a flag that will call for termination of the script.
def whichfiles(archivepaths,casepath,runname,frequency,varlocs,maxrest):
    stopflag=0
    outlist=[]
    for k in range(len(varlocs)):
        theloc=varlocs[k]
        os.system('ls '+archivepaths[k]+'/*.'+varlocs[k]+'.* > '+casepath+'/archivedfiles.txt')
        filesfile=open(casepath+'/archivedfiles.txt')
        fileslines=filesfile.readlines()
        fileslineslist=list(fileslines)
        linestolist(fileslines,fileslineslist)
        filesfile.close()
        os.system('rm '+casepath+'/archivedfiles.txt')
        thelist=fileslineslist
        preamble=len(archivepaths[k]+'/'+runname+'.'+varlocs[k]+'.')
        post=len('-00000.nc') # This is hard-coded.  We currently do not support sub-daily timescales.
        post=len('.nc')
        alltimes=[]
        for j in range(len(thelist)):
	    alltimes.append(thelist[j][0][preamble:-post])
        lastone=alltimes[-1]
        globalfirstone=alltimes[0]
        n=len(lastone)
        freqnum=int(frequency[:-1])
        freqlet=frequency[-1]
        if freqlet=='y':
            thedelt=datetime.timedelta(days=freqnum*365)
        elif freqlet=='m':
            thedelt=datetime.timedelta(days=round(freqnum*365/12)) # Months don't have uniform lengths, but this is good enough.
        elif freqlet=='w':
            thedelt=datetime.timedelta(weeks=freqnum)
        elif freqlet=='d':
            thedelt=datetime.timedelta(days=freqnum)
        timestoextract=[]
        if n==10: # output is daily
            theyear=lastone[0:4]
            theday=lastone[-2:]
            themonth=lastone[5:7]
            lastdate=datetime.date(int(theyear),int(themonth),int(theday))
            globalfirstdate=datetime.date(int(globalfirstone[0:4]),int(globalfirstone[5:7]),int(globalfirstone[-2:]))
            firstdate=lastdate-thedelt+datetime.timedelta(days=1)
            firstone=str(firstdate.year)+'-'+zeropad(firstdate.month)+'-'+zeropad(firstdate.day)
            i=alltimes.index(firstone)
            for q in range(i,len(alltimes)):
                timestoextract.append(runname+'.'+varlocs[k]+'.'+alltimes[q]+'.nc')
        elif n==7: # output is monthly
            theyear=lastone[0:4]
            themonth=lastone[-2:]
            lastdate=datetime.date(int(theyear),int(themonth),1)
            globalfirstdate=datetime.date(int(globalfirstone[0:4]),int(globalfirstone[5:7]),1)
            firstdate=lastdate-thedelt+datetime.timedelta(days=31)
            firstone=str(firstdate.year)+'-'+zeropad(firstdate.month)
            i=alltimes.index(firstone)
            for q in range(i,len(alltimes)):
                timestoextract.append(runname+'.'+varlocs[k]+'.'+alltimes[q]+'.nc')
        elif n==4: # output is annual
            lastdate=datetime.date(int(theyear),1,1)
            globalfirstdate=datetime.date(int(globalfirstone[0:4]),1,1)
            firstdate=lastdate-thedelt+datetime.timedelta(days=365)
            firstone=str(firstdate.year)
            i=alltimes.index(firstone)
            for q in range(i,len(alltimes)):
                timestoextract.append(runname+'.'+varlocs[k]+'.'+alltimes[q]+'.nc')
        outlist.append(timestoextract)
        globaldelt=lastdate-globalfirstdate
        if (globaldelt.days/thedelt.days)>datetime.timedelta(maxrest).days:
            stopflag=1
    return outlist,stopflag

def readlog(logfile):
    f=open(logfile,'r')
    loglines=f.readlines()
    loglist=list(loglines)
    linestolist2(loglines,loglist)
    f.close()
    loglist2=[]
    for k in range(len(loglist)):
	temp=[]
	for j in range(len(loglist[k])):
            if loglist[k][j]!='':
	        temp.append(loglist[k][j])
	loglist2.append(temp)
    return loglist2

def writelog(logfile,listtowrite):
    f=open(logfile,'w')
    for item in listtowrite:
        for k in range(len(item)):
            f.write("%s " % item[k])
        f.write('\n')
    f.close()

#########################################################
##################  MAIN SCRIPT BELOW  ##################
#########################################################

# extracts files
filestoextract,stopflag=whichfiles(archivepaths,casepath,runname,frequency,varlocs,maxrest)
if stopflag==1:
    sys.exit('End of run reached')

# reads in files, one variable at a time
outvals=[]
for k in range(len(variables)):
    vals,lats,lons,times=extractvars(variables[k],varlocs[k],runname,filestoextract[k],archivepaths[k],scratchdir)
    outvals.append(vals)

# loads in some common analysis subroutines like area weighting or global mean averaging
execfile(maindir+"/commonroutines.py")

# executes controller
# inputs are outvals, lats, lons, times
# outputs are nlvals
execfile(pathtocontrol)

# modifies CESM namelist
# currently do not have the flexibility to specify more than one namelist file
fixnamelist2('user_nl_cam',nlvals,casepath)

# populates the namelist
os.system(casepath+'/preview_namelists')
