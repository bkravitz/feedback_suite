Last login: Tue Mar 23 09:13:30 on console

The default interactive shell is now zsh.
To update your account to use zsh, please run `chsh -s /bin/zsh`.
For more details, please visit https://support.apple.com/kb/HT208050.
(base) Danieles-Air:~ danielevisioni$ ssh -X visioni@cheyenne.ucar.edu
Token_Response: 
Last login: Mon Mar 15 12:36:33 2021 from 67.249.80.19

******************************************************************************
*                  Welcome to Cheyenne - March 22,2021
******************************************************************************
            Today in the Daily Bulletin (dailyb.cisl.ucar.edu)
    
	- Systems downtime for week of March 22-26
	- Upcoming changes to Casper services
	- Python tutorial March 24: Matplotlib
	- New Casper HTC nodes ready for PBS jobs
	- Starting Casper Jobs with PBS Pro: March 30 tutorial
	- April 6-7 XSEDE workshop: Big Data and Machine Learning

HPSS Update:          193 days until HPSS will be decommissioned.
Quick Start:          www2.cisl.ucar.edu/resources/cheyenne/quick-start-cheyenne
User environment:     www2.cisl.ucar.edu/resources/cheyenne/user-environment
Key module commands:  module list, module avail, module spider, module help
CISL Help:            support.ucar.edu -- 303-497-2400
--------------------------------------------------------------------------------

visioni@cheyenne6:~> sodux geostrat
If 'sodux' is not a typo you can use command-not-found to lookup the package that contains it, like this:
    cnf sodux
visioni@cheyenne6:~> sudox geostrat
Token_Response: 
geostrat@cheyenne6:/glade/u/home/visioni> cd /glade/work/geostrat/
geostrat@cheyenne6:/glade/work/geostrat> cd cases/
geostrat@cheyenne6:/glade/work/geostrat/cases> ls -ltr
total 19
-rw-r--r--  1 geostrat geostrat 13328 Mar  3 14:10 ALLVARIABLES_user_nl_cam
drwxr-xr-x  9 geostrat geostrat  4096 Mar 12 10:57 b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001.OLD
drwxr-xr-x  7 geostrat geostrat  4096 Mar 12 14:48 b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001-TSMLT-GAUSS-DEFAULT.t001
drwxr-xr-x 10 geostrat geostrat  4096 Mar 22 13:56 b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001
geostrat@cheyenne6:/glade/work/geostrat/cases> cd cd b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001
bash: cd: cd: No such file or directory
geostrat@cheyenne6:/glade/work/geostrat/cases> cd b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001
geostrat@cheyenne6:/glade/work/geostrat/cases/b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001> cd controller/
geostrat@cheyenne6:/glade/work/geostrat/cases/b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001/controller> ls -ltr
total 65
-rwxr-xr-x 1 geostrat geostrat  4590 Mar 22 12:42 commonroutines.py
-rwxr-xr-x 1 geostrat geostrat  5373 Mar 22 12:42 PIcontrol.py
-rwxr-xr-x 1 geostrat geostrat 13549 Mar 22 12:42 driver.py
-rwxr-xr-x 1 geostrat geostrat  4146 Mar 22 12:55 main.py
-rw-r--r-- 1 geostrat geostrat   346 Mar 22 13:56 ControlLog_b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001.txt
geostrat@cheyenne6:/glade/work/geostrat/cases/b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001/controller> vim main.py 
geostrat@cheyenne6:/glade/work/geostrat/cases/b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001/controller> vim PIcontrol.py 
geostrat@cheyenne6:/glade/work/geostrat/cases/b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001/controller> vim PIcontrol.py 
geostrat@cheyenne6:/glade/work/geostrat/cases/b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001/controller> vim ControlLog_b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001.txt 
geostrat@cheyenne6:/glade/work/geostrat/cases/b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001/controller> ./main.py 
Traceback (most recent call last):
  File "./main.py", line 94, in <module>
    execfile(maindir+"/driver.py")
  File "/glade/work/geostrat/cases/b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001/controller/driver.py", line 357, in <module>
    execfile(pathtocontrol)
  File "/glade/work/geostrat/cases/b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001/controller/PIcontrol.py", line 84, in <module>
    ramp_up = dt2/x
NameError: name 'x' is not defined
geostrat@cheyenne6:/glade/work/geostrat/cases/b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001/controller> vim PIcontrol.py 
geostrat@cheyenne6:/glade/work/geostrat/cases/b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001/controller> ./main.py 
ERROR: case.setup must be run prior to running preview_namelists
geostrat@cheyenne6:/glade/work/geostrat/cases/b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001/controller> vim ControlLog_b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001.txt 
geostrat@cheyenne6:/glade/work/geostrat/cases/b.e21.BW.f09_g17.SSP245-TSMLT-GAUSS-DEFAULT.001/controller> vim main.py 

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
"main.py" 94L, 4146C                                                                                                                                                                                                                    81,14         72%
