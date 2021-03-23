#! /usr/bin/env python
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

# Main setup script
#
# Written by Ben Kravitz (bkravitz@iu.edu or ben.kravitz.work@gmail.com)
# Last updated 11 July 2019
#
# This script provides the main information about the run.  Note that everything
# here is specific to an individual run.  Each run should have its own copy
# of the feedback suite.
#
# This script is written in native python format.  Be careful with brackets [],
# white space, and making sure everything that needs to be a string is actually
# a string by putting it in quotes ''.  All lines beginning with # are comments.
#
# Things you need to specify:
#
################## GLOBAL SETUP PARAMETERS ##################
#
#   casepath = The path where this specific case is built and run.
#
#   maindir = The path where the control suite sits.
#
#   scratchdir = The script will need to extract and process some of the model
#                output.  This is the path where it will do that.  The scratchdir
#                will be removed after the script is done processing everything,
#                so make sure this does not point to a directory that you care about.
#
#   runname = The name of the case you're running.
#
#   frequency = How often you want the controller to operate.  This
#              includes two pieces of information:  a number and a letter.
#              The letters can be d (days), w (weeks), m (months),
#              or y (years).  For example, if you want the controller to run
#              every 23 days, you would put '23d' (the quotes are important
#              because this is a string).  You're probably going to mostly use
#              '1m' or '1y'.  There is currently no capability of having sub-daily
#              frequency.  If the frequency of the model output is not concordant
#              with what you select here (e.g., you only output monthly, but you
#              select frequency='2w'), you will get unpredictable behavior.
#
#   maxrest = The number of times you want the controller to restart.
#              For example, if you want a 50 year simulation, and if
#              frequency='1y', then maxrest=49.
#
#   pathtocontrol = The absolute path of the feedback algorithm.
#
################## VARIABLE-SPECIFIC SETUP PARAMETERS ##################
# These are lists that are specific to each variable.
#
#   variables = The variables that the feedback algorithm needs.  Note that
#     for now, all variables must be 2-D fields (i.e., no vertical component).
#
#   archivepaths = The paths where all of your archived output is stored, one
#     for each variable.  This is split apart in case you want to call for inputs
#     from two different model components (e.g., atmosphere and ocean).
#     
#   varlocs = The locations of the variables to be extracted.  Examples include
#     'cam.h0', 'cam.h2', or 'pop.h.nday1'.

runname='b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001'

casepath='/glade/work/geostrat/cases/'+runname
maindir=casepath+'/controller'
scratchdir='/glade/scratch/geostrat/'+runname+'/allthetemporarystuff/'
frequency='1y'
maxrest=1000

pathtocontrol=maindir+'/PIcontrol.py'

variables=['TREFHT']
archivepaths=len(variables)*['/glade/scratch/geostrat/archive/'+runname+'/atm/hist'] # do NOT include a '/' at the end of each path
varlocs=len(variables)*['cam.h0']

###########################
### CALLING MAIN SCRIPT ###
###########################

execfile(maindir+"/driver.py")