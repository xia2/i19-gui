#!/usr/bin/env python

import Tkinter
import Tkinter, tkFileDialog
from time import gmtime, strftime
import os
import glob

###################################################################################################

# browse bottons:
def visitBrowse():
   global visit
   root = Tkinter.Tk()
   root.withdraw()
   visit = tkFileDialog.askdirectory(parent=root,initialdir="/dls/i19-1/data/2016/",title='Navigate into Desired Directory') + "/"
   if len(visit) > 0:
      print "Visit: " + str(visit)
      visitEntry.delete(0, "end")
      visitEntry.insert(0, visit)
      return visit

def datasetBrowse():
   global datasetPath
   global datasetDir
   global prefix
   if len(visit) > 0:
      root = Tkinter.Tk()
      root.withdraw()
      datasetPath = tkFileDialog.askdirectory(parent=root,initialdir=visit,title='Navigate into Desired Directory') + "/"
      datasetDir = datasetPath.split("/")[-2]
      if len(datasetDir) > 0:
         print "Dataset path: " + datasetPath
         print "Dataset: " + str(datasetDir)
         datasetEntry.delete(0, "end")
         datasetEntry.insert(0, datasetDir)
	 os.chdir(datasetPath)
         for f in glob.iglob("*_00001.cbf"):
            prefix = f[:-12]
         print "Prefix: " + prefix
   else:
      print "please select visit first"
      datasetEntry.delete(0, "end")
      datasetEntry.insert(0, "please select visit first")

# image location
def imageBrowse():
   if len(visit) > 0:
      startDir = visit
      if len(datasetPath) > 0:
         startDir = datasetPath
   else: startDir = "/dls/i19-1/data/2016/"
   root = Tkinter.Tk()
   root.withdraw()
   imagePath = tkFileDialog.askopenfilename(parent=root,initialdir=startDir,title='Select image', filetypes=[('pilatus images','*.cbf')])
   image = imagePath.split("/")[-1]
   if len(image) > 0:
      print "Image: %s" % image
      imageEntry.delete(0, "end")
      imageEntry.insert(0, image)

############# image viewers ############
#albula
def albula():
   print datasetPath
   image = imageEntry.get()
   if len(str(image)) > 0:
      os.system("albula " + datasetPath + image)
   else:
      os.system("albula")
#adxv
def adxv():
   image = imageEntry.get()
   if len(str(image)) > 0:
      os.system("module load adxv")
      os.system("adxv " + datasetPath + image)
   else:
      os.system("adxv")
#dials.image_viewer
def dialsImageViewer():
   image = imageEntry.get()
   if image == int:
      print "*** please selecet an image ***"
   else:
      sum_image = ""
      if len(str(sumEntry.get())) > 0:
         sum_image = " sum_image=" + str(sumEntry.get())

      print "Opening images in Dials"
      print "Starting image: " + image
      time = strftime("%Y%m%d_%H%M%S", gmtime())
      dialsImageDir = visit + "processing/image/" + prefix + "_" + time
      if not os.path.exists(dialsImageDir):
         os.makedirs(dialsImageDir)
      os.chdir(dialsImageDir)
      print "dials.import " + datasetPath + image + " geometry.scan.image_range=1,1700 geometry.scan.extrapolate_scan=true"
      print "dials.image_viewer datablock.json" + sum_image
      os.system("dials.import " + datasetPath + image + " geometry.scan.image_range=1,1700 geometry.scan.extrapolate_scan=true")
      os.system("dials.image_viewer datablock.json" + sum_image)
      os.chdir(datasetPath)

###################################################################################################
def mergeAuto():
   if len(visit) > 0:
      hutch = visit.split("/")[2]
   else:
      print "please select visit"

   if len(mergeAutoEntry.get()) > 0:
       numMerge = " --merge " + str(mergeAutoEntry.get())
   else:
       numMerge = " --merge 10" 
   newPath = "/".join(datasetPath.split("/")[:-2]) + "/" + str(datasetEntry.get()) + "/"
   print newPath
   os.chdir(newPath)
   if str(hutch) == "i19-1":
      print "EH1 data, merging data"
      os.system("python /dls_sw/i19/scripts/BeamlineScripts/mergeAuto.py" + numMerge)
   if str(hutch) == "i19-2":
      print "EH2 data, merging data"
      os.system("python /dls_sw/i19/scripts/BeamlineScripts/mergeAutoEH2.py" + numMerge)
   else:
      "something isn't working, please tell local contact - mergeAuto directory error"
   os.chdir(datasetPath)

###################################################################################################

#xia2 processing location
def processLocation():
   global prcoessingDir
   root = Tkinter.Tk()
   root.withdraw()
   time = strftime("%Y%m%d_%H%M", gmtime())
   prcoessingDir = tkFileDialog.askdirectory(parent=root,initialdir=visit+"processing/",title='Select a processing location')  + "_" + str(time) + "/"
   if len(prcoessingDir) > 0:
      
      print "Processing location: " + str(prcoessingDir)
      processEntry.delete(0, "end")
      processEntry.insert(0, prcoessingDir)
      return prcoessingDir
   else:
      print "please select visit first"
      datasetEntry.delete(0, "end")
      datasetEntry.insert(0, "please select visit first")

#i19.screen processing location
def processLocationScreen():
   global prcoessingDirScreen
   root = Tkinter.Tk()
   root.withdraw()
   time = strftime("%Y%m%d_%H%M", gmtime())
   prcoessingDirScreen = tkFileDialog.askdirectory(parent=root,initialdir=visit+"processing/",title='Select i19.screen processing location')  + "_" + str(time) + "/"
   if len(prcoessingDirScreen) > 0:
      
      print "i19.screen Processing location: " + str(prcoessingDirScreen)
      processScreenEntry.delete(0, "end")
      processScreenEntry.insert(0, prcoessingDirScreen)
      return prcoessingDirScreen
   else:
      print "please select visit first"
      datasetScreenEntry.delete(0, "end")
      datasetScreenEntry.insert(0, "please select visit first")

##################################################################################
# running i19.screen
def screen():
   print "running gui controlled i19.screen"   
   additionalScreenOptions()
   print "Starting gui controller i19.screen"
   print "i19.screen Processing directory: " + prcoessingDir
   print "i19.screencommand: \n" + "i19.screen " + datasetPath + additionsScreen

   os.chdir(prcoessingDir)
   os.system("i19.screen " + datasetPath + additionsScreen)
   os.chdir(datasetPath)
# i19.screen additional options

def additionalScreenOptions():
   global additionsScreen
   additionsScreen =""
   checkboxes = {}  
   if varScreenRun.get() == 1:
       run = "*0" + str(runScreenEntry.get()) + "_*.cbf"
       additionsScreen=str(run)
   else:
       additionsScreen=str("*_01_*.cbf")
   if varScreenProcess.get() == 0:
      makeDir("standard", "i19screen")
   else:
      makeDir("userDefined")
   for var in checkboxes:
      if checkboxes[var] == 1:
         pass

###############################################################################
# making processing directory:
def makeDir(procDir,program):
   global prcoessingDir
   if procDir == "standard":
      time = strftime("%Y%m%d_%H%M", gmtime())
      prcoessingDir = str(visit + "processing/" + datasetDir + "_" + program + "_" + time)
   else:
      if str(program) == str(xia2):
         prcoessingDir = str(processEntry.get())
      if str(program) == str(i19screen):
         prcoessingDir = str(processScrrenEntry.get())
   if not os.path.exists(prcoessingDir):
      os.makedirs(prcoessingDir)
   print "processing folder: " + str(prcoessingDir)
   return prcoessingDir
  
###################################################################################   
# runing xia2
def xia2():
   additionalOptions()
   print "Starting xia2"
   print "Processing directory: " + prcoessingDir
   os.chdir(prcoessingDir)
   os.system("xia2 -small_molecule " + additionalRun + datasetPath + additions)
   os.chdir(datasetPath)

def additionalOptions():
   global additions
   global additionalRun
   additions =""
   checkboxes = {  
            "varUnit": varUnit.get(),
            "varBeam": varBeam.get(),
            "varDMax": varDMax.get(),
            "varDMin": varDMin.get(),
            "varMS": varMS.get(),             
   }    
   if varRun.get() == 1:
      run = prefix + "0" + str(runEntry.get()) + "_00001.cbf"
      additions=str(run)
      additionalRun = "image="
   else:
      additionalRun = ""
   if varProcess.get() == 0:
      makeDir("standard", "xia2")
   else:
      makeDir("userDefined")
   for var in checkboxes:
      if checkboxes[var] == 1:
         if str(var) == "varUnit":
            unitCell = " unit_cell=" + str(unitCellEntry.get()) + " space_group=" + str(spaceGroupEntry.get())
            additions+=str(unitCell)
         if str(var) == "varBeam":
            beamCentre = " beam_centre=" + str(x_beam_centreEntry.get()) + "," + str(y_beam_centreEntry.get())
            additions+=str(beamCentre)
         if str(var) == "varDMax":
            dmax = " d_max=" + str(d_maxEntry.get())
            additions+=str(dmax)
         if str(var) == "varDMin":
            dmin = " d_min=" + str(d_minEntry.get())
            additions+=str(dmin)
         if str(var) == "varMS":
            additions+=" multi_sweep_indexing=true"
   additions+=" read_all_image_headers=false"
   print "Selected additional options: " + str(additions)

############# make shelx files ############
def makeShelx():
   print "Starting xia.to_shelx"
   if len(str(atomsEntry.get())) > 0:
      atoms = " " + str(atomsEntry.get())
   else:
      atoms = " C12H12O12"
   if os.path.exists(prcoessingDir + "/DataFiles/"):
      os.chdir(prcoessingDir)
      print "calculating unit cell errors"
      os.system("xia2.get_unit_cell_errors")
      os.chdir(prcoessingDir + "/DataFiles/")
      if os.path.isfile("AUTOMATIC_DEFAULT_scaled_unmerged.mtz"):
         if os.path.isfile("../xia2.get_unit_cell_errors.json"):
            print "Making shelx files, command: xia2.to_shelx -c ../xia2.get_unit_cell_errors.json AUTOMATIC_DEFAULT_scaled_unmerged.mtz " + datasetDir + atoms
            os.system("xia2.to_shelx -c ../xia2.get_unit_cell_errors.json AUTOMATIC_DEFAULT_scaled_unmerged.mtz " + datasetDir + atoms)     
         else:
            print "Making shelx files, command: xia2.to_shelx AUTOMATIC_DEFAULT_scaled_unmerged.mtz " + datasetDir + atoms
            os.system("xia2.to_shelx AUTOMATIC_DEFAULT_scaled_unmerged.mtz " + datasetDir + atoms)  
         if varSheltx.get() == 1:
            if os.path.isfile(datasetDir  + ".ins"):
               os.system("shelxt " + datasetDir)
      else: 
        print "xia2 has not completed, please run xia and retry"
   print "xia2 has not completed, please run xia and retry"
   os.chdir(datasetPath)

############# log graphs ############
def loggraphs():
   print "Starting log graphs"
   print prcoessingDir + "/LogFiles"
   if os.path.exists(prcoessingDir + "/LogFiles"): 
      os.chdir(prcoessingDir + "/LogFiles")
      if os.path.isfile("AUTOMATIC_DEFAULT_aimless.log"):
         os.system("loggraph AUTOMATIC_DEFAULT_aimless.log")
      else: 
         print "xia2 has not completed, please run xia and retry"
   else: 
      print "xia2 has not completed, please run xia and retry"
   os.chdir(datasetPath)

############# screen log graphs ############
def screenloggraphs():
   print "Starting log graphs"
   print prcoessingDir + "/LogFiles"
   if os.path.exists(prcoessingDir + "/LogFiles"): 
      os.chdir(prcoessingDir + "/LogFiles")
      if os.path.isfile("AUTOMATIC_DEFAULT_aimless.log"):
         os.system("loggraph AUTOMATIC_DEFAULT_aimless.log")
      else: 
         print "xia2 has not completed, please run xia and retry"
   else: 
      print "xia2 has not completed, please run xia and retry"
   os.chdir(datasetPath)

############# log graphs ############
def reciprocal():
   print "Opening reciprocal"
   if len(str(reciprocalRunEntry.get())) > 0:
      runReciprocal = str(reciprocalRunEntry.get())
   else: 
      runReciprocal = str(1)
   print prcoessingDir + "/DEFAULT/NATIVE/SWEEP"+runReciprocal+"/index"
   if os.path.exists(prcoessingDir + "/DEFAULT/NATIVE/SWEEP"+runReciprocal+"/index"): 
      os.chdir(prcoessingDir + "/DEFAULT/NATIVE/SWEEP"+runReciprocal+"/index")
      print "command: "
      print "dials.reciprocal_lattice_viewer *_SWEEP"+runReciprocal+"_datablock.json *_SWEEP"+runReciprocal+"_strong.pickle"
      os.system("dials.reciprocal_lattice_viewer *_SWEEP"+runReciprocal+"_datablock.json *_SWEEP"+runReciprocal+"_strong.pickle")
   else: 
      print "xia2 has not completed, please run xia and retry"
   os.chdir(datasetPath)
############# screen log graphs ############
def screenreciprocal():
   print "Opening reciprocal"
   if len(str(reciprocalRunEntry.get())) > 0:
      runReciprocal = str(reciprocalRunEntry.get())
   else: 
      runReciprocal = str(1)
   print prcoessingDir + "/DEFAULT/NATIVE/SWEEP"+runReciprocal+"/index"
   if os.path.exists(prcoessingDir + "/DEFAULT/NATIVE/SWEEP"+runReciprocal+"/index"): 
      os.chdir(prcoessingDir + "/DEFAULT/NATIVE/SWEEP"+runReciprocal+"/index")
      print "command: "
      print "dials.reciprocal_lattice_viewer *_SWEEP"+runReciprocal+"_datablock.json *_SWEEP"+runReciprocal+"_strong.pickle"
      os.system("dials.reciprocal_lattice_viewer *_SWEEP"+runReciprocal+"_datablock.json *_SWEEP"+runReciprocal+"_strong.pickle")
   else: 
      print "xia2 has not completed, please run xia and retry"
   os.chdir(datasetPath)

################# html ################
def html():
   print "Opening html report"
   if os.path.exists(prcoessingDir + "/LogFiles"): 
      os.chdir(prcoessingDir + "/LogFiles")
      if os.path.isfile("AUTOMATIC_DEFAULT_NATIVE_report.html"):
         os.system("xdg-open AUTOMATIC_DEFAULT_NATIVE_report.html")
      else: 
         print "xia2 has not completed, please run xia and retry"
   else: 
      print "xia2 has not completed, please run xia and retry"
   os.chdir(datasetPath)

################# htmlscreen ################
def screenhtml():
   print "Opening html report"
   if os.path.exists(prcoessingDir + "/LogFiles"): 
      os.chdir(prcoessingDir + "/LogFiles")
      if os.path.isfile("AUTOMATIC_DEFAULT_NATIVE_report.html"):
         os.system("xdg-open AUTOMATIC_DEFAULT_NATIVE_report.html")
      else: 
         print "xia2 has not completed, please run xia and retry"
   else: 
      print "xia2 has not completed, please run xia and retry"
   os.chdir(datasetPath)

################# help ################
def visitQ():
   vHelpText = ''' Please select a visit
   e.g. mt13000-1
   *** Navigate into Desired Directory for selection ***
   '''
   vHelp = Tkinter.Tk()
   vHelp.wm_title("Select visit help")
   vHelpLbl = Tkinter.Label(vHelp, text=vHelpText)
   vHelpLbl.grid(row=0, column=0, sticky='W', padx=5, pady=2) 

def datasetQ():
   dHelpText = ''' Please select a dataset folder
   e.g. compound_2
   *** Navigate into Desired Directory for selection ***
   cbf images must be contained within the selected folder
   '''
   dHelp = Tkinter.Tk()
   dHelp.wm_title("Select visit help")
   dHelpLbl = Tkinter.Label(dHelp, text=dHelpText)
   dHelpLbl.grid(row=0, column=0, sticky='W', padx=5, pady=2) 

def mergeQ():
   screenHelpText = ''' 
mergeAuto is a tool for merging together pilatus images for prcoessing in crysalispro

1)  Standard processing:
		Click 'Run mergeAuto button' - no additional information is required.
		Will merge together 10 images.
		Data will be saved in:
		'visit_number/processing/mergeing/prefix/merged_1_deg_yyyymmdd_hhmm' folder.

2) Additional information:
	"Number of images to merge":
      		Specify the nuymber of image you want to be merged.
'''
   screenHelp = Tkinter.Tk()
   screenHelp.wm_title("mergeAuto Help")
   screenHelpLbl = Tkinter.Label(screenHelp, text=screenHelpText, justify="left")
   screenHelpLbl.grid(row=0, column=0, sticky='W', padx=5, pady=2) 

def screenQ():
   screenHelpText = ''' 
i19.screen is an quick intensity checking tool to ensure that reflections do not 
exceed the maximium photons/s threshold taking into account mosaic spread. 
i19.screen is writting by Markus Gerstel.

1)  Standard processing:
		Click 'Run i19.scrren button' - no additional information is required.
		Data will be saved in 'visit_number/processing/prefix_i19screen_yyyymmdd_hhmm' folder.

2) Additional information:
	"Processing location":
      		Only check if you want to use a specific location for the generated files.
		Use the 'browse' button to selected desired folder.
	\"Run\":
		Enter run number you wish to be analysied (auto: run 1).
		e.g. 4
'''
   screenHelp = Tkinter.Tk()
   screenHelp.wm_title("i19.scrren Help")
   screenHelpLbl = Tkinter.Label(screenHelp, text=screenHelpText, justify="left")
   screenHelpLbl.grid(row=0, column=0, sticky='W', padx=5, pady=2) 
   

def xai2Q():
   xai2HelpText = ''' 
Xia2 is an automated processing tool (index, integrate and scale) specifically designed for Pilatus synchrotron data. 

1)  Standard processing:
		Click 'Run xia2 button' - no additional information is required.
		Shelx input files can be created after by using the Make shelx button at the bottom of gui. 
		Data will be saved in 'visit_number/processing/prefix_xia2_yyyymmdd_hhmm' folder.

2) Additional information:
	"Processing location":
      		Only check if you want to use a specific location for the generated files.
		Use the 'browse' button to selected desired folder.
	\"Unit cell\":
		Enter unit cell dimentions without spaces.
		e.g. 6.1,7.2,8.3,90,90,90    
		Must also provide a space group.
	\"Space group\":
		Enter space group without spaces.
		e.g. P21/c   
	\"Beam centre\": 
		Enter beam centre positions.
		Important for EH2 data. 
		e.g. 52.36
		     40.8
	\"Single Run\":
		Use this option is you want to use xia2 to process the data from a single run.
	\"d_min\":
    		Use this option if you ant to specify the resolution cut off.
		Can be useful if the scaling fails.
	\"Index all runs together\":
		Indexes the data using all runs. 
		Highly recommended.  

3) After Xia2 processing it is possible to make shelx file and analyse your data:
	\"Make shelx\":
		Creates shelx files ready for use in the refinement packages.
		Use the formula input and shelxt for automated structure solution.
	"Reciprocal Lattice": 
		Open up the reciprocal space viewer for the provided run.
	"Log Graphs"
		Displays graphs from processing.
		e.g. Completness, Rint vs resolution etc.
	"HTML Results"
		Displays processing results in a html formate.
'''
   xia2Help = Tkinter.Tk()
   xia2Help.wm_title("Xia2 Help")
   xia2HelpLbl = Tkinter.Label(xia2Help, text=xai2HelpText, justify="left")
   xia2HelpLbl.grid(row=0, column=0, sticky='W', padx=5, pady=2) 
   
######################################################################################################
######################################################################################################
########## Script starts here ########################################################################
if __name__ == "__main__":
   form = Tkinter.Tk()
   # program title
   form.wm_title('i19 gui - MRW')
   
   visit = ""
   # xia2 varibles
   varProcess = Tkinter.IntVar()
   varUnit = Tkinter.IntVar()
   varBeam = Tkinter.IntVar()
   varRun = Tkinter.IntVar()
   varDMax = Tkinter.IntVar()
   varDMin = Tkinter.IntVar()
   varMS = Tkinter.IntVar()
   varSheltx = Tkinter.IntVar()
   # i19.screen varibles
   varScreenProcess = Tkinter.IntVar()
   varScreenRun = Tkinter.IntVar()
   # mergeAuto varibles
   varMergeAuto = Tkinter.IntVar()
###########################################################################    
# section title 1
   stepOne = Tkinter.LabelFrame(form, text=" Enter Details: ")
   stepOne.grid(row=0, columnspan=7, sticky='W', padx=15, pady=5, ipadx=5, ipady=5)
# section title Merge
   stepImages = Tkinter.LabelFrame(form, text=" Viewing Images: ")
   stepImages.grid(row=1, columnspan=7, sticky='W', padx=15, pady=5, ipadx=5, ipady=5)
# section title Merge
   stepMerge = Tkinter.LabelFrame(form, text=" Merging Images: ")
   stepMerge.grid(row=2, columnspan=7, sticky='W', padx=15, pady=5, ipadx=5, ipady=5)
# section title 2
   stepTwo = Tkinter.LabelFrame(form, text=" i19.Screen: ")
   stepTwo.grid(row=3, columnspan=7, sticky='W', padx=15, pady=5, ipadx=5, ipady=5)
# section title 3
   stepThree = Tkinter.LabelFrame(form, text=" Xia2: ")
   stepThree.grid(row=4, columnspan=7, sticky='W', padx=15, pady=5, ipadx=5, ipady=5)

###########################################################################

# visit
   # lable
   visitLbl = Tkinter.Label(stepOne, text="Visit:")
   visitLbl.grid(row=0, column=0, sticky='W', padx=5, pady=2)
   #file text
   visitEntry = Tkinter.Entry(stepOne)
   visitEntry.grid(row=0, column=1, columnspan=24, sticky="WE",pady=2)
   # Browse button
   visitBrowseBtn = Tkinter.Button(stepOne, text="Browse ...", command = visitBrowse)
   visitBrowseBtn.grid(row=0, column=25, sticky='WE', padx=5, pady=2)
   # ?
   visitQBtn = Tkinter.Button(stepOne, text="?", command = visitQ)    
   visitQBtn.grid(row=0, column=30, sticky='W', padx=2, pady=2)

# dataset
   datasetLbl = Tkinter.Label(stepOne, text="Dataset:")
   datasetLbl.grid(row=1, column=0, sticky='W', padx=5, pady=2)

   datasetEntry = Tkinter.Entry(stepOne)
   datasetEntry.grid(row=1, column=1, columnspan=24, sticky="WE", pady=2)

   datasetBrowseBtn = Tkinter.Button(stepOne, text="Browse ...", command = datasetBrowse)
   datasetBrowseBtn.grid(row=1, column=25, sticky='W', padx=5, pady=2)
   # ?
   datasetQBtn = Tkinter.Button(stepOne, text="?", command = datasetQ)    
   datasetQBtn.grid(row=1, column=30, sticky='W', padx=2, pady=2)

##### viewing images ######################################################################
# image
   imageLbl = Tkinter.Label(stepImages, text="Image:")
   imageLbl.grid(row=2, column=0, sticky='W', padx=5, pady=2)

   imageEntry = Tkinter.Entry(stepImages)
   imageEntry.grid(row=2, column=1, columnspan=6, sticky="WE", pady=2)

   imageBrowseBtn = Tkinter.Button(stepImages, text="Browse ...", command = imageBrowse)
   imageBrowseBtn.grid(row=2, column=8, sticky='W', padx=5, pady=2)

# Albula
   albulaBtn = Tkinter.Button(stepImages, text="Albula Viewer", command = albula)
   albulaBtn.grid(row=3, column=0, sticky='W', padx=5, pady=2)
# Adxv
   adxvBtn = Tkinter.Button(stepImages, text="Adxv Viewer", command = adxv)
   adxvBtn.grid(row=3, column=1, sticky='W', padx=5, pady=2)

# DialsImageViewer
   dialsImageViewerBtn = Tkinter.Button(stepImages, text="Dials Viewer", command = dialsImageViewer)
   dialsImageViewerBtn.grid(row=4, column=0, sticky='W', padx=5, pady=2)
   #lable
   yLbl = Tkinter.Label(stepImages, text="Image Sum (e.g. 10):")
   yLbl.grid(row=4, column=1, columnspan=1, pady=2, padx=2, sticky='W')
   #file text
   sumEntry = Tkinter.Entry(stepImages)
   sumEntry.grid(row=4, column=2, columnspan=6, pady=2, padx=4, sticky="WE")

##### merging ######################################################################
   # Run button
   mergeBtn = Tkinter.Button(stepMerge, text="Run mergeAuto", command = mergeAuto, font="Helvetica 18 bold", bg = "palevioletred")    
   mergeBtn.grid(row=0, column=0, sticky='WE', padx=10, pady=10)
   # ?
   mergeQBtn = Tkinter.Button(stepMerge, text="?", command = mergeQ)    
   mergeQBtn.grid(row=0, column=3, sticky='W', padx=2, pady=2)

   #check button
   mergeAutoChk = Tkinter.Checkbutton(stepMerge, text="Number of images to merge (auto 10): ",variable=varMergeAuto, onvalue=1, offvalue=0)
   mergeAutoChk.grid(row=1, column=0, columnspan=3, pady=2, padx=4, sticky='W')
   #file text
   mergeAutoEntry = Tkinter.Entry(stepMerge)
   mergeAutoEntry.grid(row=1, column=3, columnspan=6, pady=2, padx=4, sticky="WE")

##### i19.screen ######################################################################
# Run i19.screen:
   # Run button
   screenBtn = Tkinter.Button(stepTwo, text="Run i19.screen", command = screen, font="Helvetica 18 bold", bg = "palevioletred")    
   screenBtn.grid(row=0, column=0, sticky='WE', padx=10, pady=10)
   # ?
   screenQBtn = Tkinter.Button(stepTwo, text="?", command = screenQ)    
   screenQBtn.grid(row=0, column=3, sticky='W', padx=2, pady=2)

# process location:
   #check button
   processScreenChk = Tkinter.Checkbutton(stepTwo, text="Process location: ",variable=varScreenProcess, onvalue=1, offvalue=0)
   processScreenChk.grid(row=1, column=0, columnspan=3, pady=2, padx=4, sticky='W')
   #file text
   processScreenEntry = Tkinter.Entry(stepTwo)
   processScreenEntry.grid(row=1, column=3, columnspan=6, pady=2, padx=4, sticky="WE")
   # Browse button
   processScreenEntryBrowseBtn = Tkinter.Button(stepTwo, text="Browse ...", command = processLocationScreen)    
   processScreenEntryBrowseBtn.grid(row=1, column=10, sticky='WE', padx=5, pady=2)

# runs: 
   #check button
   runScreenChk = Tkinter.Checkbutton(stepTwo, text="Which run: ", variable=varScreenRun, onvalue=1, offvalue=0)
   runScreenChk.grid(row=6, column=0, columnspan=3, pady=2, padx=4, sticky='W')
   #file text
   runScreenEntry = Tkinter.Entry(stepTwo)
   runScreenEntry.grid(row=6, column=3, columnspan=6, pady=2, padx=4, sticky="WE",)

# reciprocal_lattice_viewer:
   # Button
   reciprocalBtn = Tkinter.Button(stepTwo, text="Reciprocal Lattice", command = screenreciprocal)    
   reciprocalBtn.grid(row=7, column=0, sticky='WE', padx=3, pady=3)
   # lable
   reciprocalLbl = Tkinter.Label(stepTwo, text="Which Run (e.g. 2):")
   reciprocalLbl.grid(row=7, column=3, columnspan=1, pady=2, padx=1, sticky='WE')
   # run entry
   reciprocalRunEntry = Tkinter.Entry(stepTwo)
   reciprocalRunEntry.grid(row=7, column=4, columnspan=4, pady=2, padx=1, sticky="W") 
  
# Make loggraphs:
   # Run button
   logGraphsBtn = Tkinter.Button(stepTwo, text="Log Graphs", command = screenloggraphs)    
   logGraphsBtn.grid(row=13, column=0, sticky='WE', padx=3, pady=3)

# html:
   # Run button
   htmlBtn = Tkinter.Button(stepTwo, text="HTML Results", command = screenhtml)    
   htmlBtn.grid(row=13, column=3, sticky='WE', padx=3, pady=3)    

##### xia2 ######################################################################

# Run xia2:
   # Run button
   xia2Btn = Tkinter.Button(stepThree, text="Run Xia2", command = xia2, font="Helvetica 18 bold", bg = "palevioletred")    
   xia2Btn.grid(row=0, column=0, sticky='WE', padx=10, pady=10)

   # ?
   xia2QBtn = Tkinter.Button(stepThree, text="?", command = xai2Q)    
   xia2QBtn.grid(row=0, column=3, sticky='W', padx=2, pady=2)
    
# process location:
   #check button
   processChk = Tkinter.Checkbutton(stepThree, text="Process location: ",variable=varProcess, onvalue=1, offvalue=0)
   processChk.grid(row=1, column=0, columnspan=3, pady=2, padx=4, sticky='W')
   #file text
   processEntry = Tkinter.Entry(stepThree)
   processEntry.grid(row=1, column=3, columnspan=6, pady=2, padx=4, sticky="WE")
   # Browse button
   processEntryBrowseBtn = Tkinter.Button(stepThree, text="Browse ...", command = processLocation)    
   processEntryBrowseBtn.grid(row=1, column=10, sticky='WE', padx=5, pady=2)

# unitCell: 
   #check button 
   unitCellChk = Tkinter.Checkbutton(stepThree, text="Unit cell: ", variable=varUnit, onvalue=1, offvalue=0)
   unitCellChk.grid(row=2, column=0, columnspan=3, pady=2, padx=4, sticky='W')
   #file text
   unitCellEntry = Tkinter.Entry(stepThree)
   unitCellEntry.grid(row=2, column=3, columnspan=6, pady=2, padx=4, sticky="WE",)


# spaceGroup:
   #check button
   spaceGroupLbl = Tkinter.Label(stepThree, text="Space group: ")
   spaceGroupLbl.grid(row=3, column=0, columnspan=3, pady=2, padx=24, sticky='W')
   #file text
   spaceGroupEntry = Tkinter.Entry(stepThree)
   spaceGroupEntry.grid(row=3, column=3, columnspan=6, pady=2, padx=4, sticky="WE")

# beam_centre: 
   #check button
   xChk = Tkinter.Checkbutton(stepThree, text="Beam centre", variable=varBeam, onvalue=1, offvalue=0)
   xChk.grid(row=4, column=0, columnspan=3, pady=2, padx=2, sticky='W')
   #lable
   xLbl = Tkinter.Label(stepThree, text="x:")
   xLbl.grid(row=4, column=2, columnspan=1, pady=2, padx=2, sticky='W')
   #lable
   yLbl = Tkinter.Label(stepThree, text="y:")
   yLbl.grid(row=5, column=2, columnspan=1, pady=2, padx=2, sticky='W')
   #file text
   x_beam_centreEntry = Tkinter.Entry(stepThree)
   x_beam_centreEntry.grid(row=4, column=3, columnspan=6, pady=2, padx=4, sticky="WE",)
   #file text
   y_beam_centreEntry = Tkinter.Entry(stepThree)
   y_beam_centreEntry.grid(row=5, column=3, columnspan=6, pady=2, padx=4, sticky="WE",)
    
# runs: 
   #check button
   runChk = Tkinter.Checkbutton(stepThree, text="SingleRun: ", variable=varRun, onvalue=1, offvalue=0)
   runChk.grid(row=6, column=0, columnspan=3, pady=2, padx=4, sticky='W')
   #file text
   runEntry = Tkinter.Entry(stepThree)
   runEntry.grid(row=6, column=3, columnspan=6, pady=2, padx=4, sticky="WE",)
    
# d_min:
   #check button
   d_minChk = Tkinter.Checkbutton(stepThree, text="d_min: ", variable=varDMin, onvalue=1, offvalue=0)
   d_minChk.grid(row=8, column=0, columnspan=3, pady=2, padx=4, sticky='W')
   #file text
   d_minEntry = Tkinter.Entry(stepThree)
   d_minEntry.grid(row=8, column=3, columnspan=6, pady=2, padx=4, sticky="WE")

# multiSweep: 
   #check button
   multiSweepChk = Tkinter.Checkbutton(stepThree, text="Index all runs together", variable=varMS, onvalue=1, offvalue=0)
   multiSweepChk.grid(row=9, column=0, columnspan=3, pady=2, padx=4, sticky='W')

# after xia2 lable
   afterXiaLbl = Tkinter.Label(stepThree, text="After Xia2 Tools")
   afterXiaLbl.grid(row=10, column=0, columnspan=3, pady=2, padx=4, sticky='W')

# Make shelx:
   # Run button
   xia2Btn = Tkinter.Button(stepThree, text="Make Shelx", command = makeShelx)    
   xia2Btn.grid(row=11, column=0, sticky='WE', padx=3, pady=3)
   #file text
   afterXiaLbl = Tkinter.Label(stepThree, text="Atoms (e.g. C6H12O6):")
   afterXiaLbl.grid(row=11, column=3, columnspan=1, pady=2, padx=1, sticky='WE')
   atomsEntry = Tkinter.Entry(stepThree)
   atomsEntry.grid(row=11, column=4, columnspan=4, pady=2, padx=1, sticky="W")   
   #check button
   d_maxChk = Tkinter.Checkbutton(stepThree, text="Run shelxt: ", variable=varSheltx, onvalue=1, offvalue=0)
   d_maxChk.grid(row=11, column=8, columnspan=3, pady=2, padx=8, sticky='WE')

# reciprocal_lattice_viewer:
   # Button
   reciprocalBtn = Tkinter.Button(stepThree, text="Reciprocal Lattice", command = reciprocal)    
   reciprocalBtn.grid(row=12, column=0, sticky='WE', padx=3, pady=3)
   # lable
   reciprocalLbl = Tkinter.Label(stepThree, text="Which Run (e.g. 2):")
   reciprocalLbl.grid(row=12, column=3, columnspan=1, pady=2, padx=1, sticky='WE')
   # run entry
   reciprocalRunEntry = Tkinter.Entry(stepThree)
   reciprocalRunEntry.grid(row=12, column=4, columnspan=4, pady=2, padx=1, sticky="W") 
  
# Make loggraphs:
   # Run button
   logGraphsBtn = Tkinter.Button(stepThree, text="Log Graphs", command = loggraphs)    
   logGraphsBtn.grid(row=13, column=0, sticky='WE', padx=3, pady=3)

# html:
   # Run button
   htmlBtn = Tkinter.Button(stepThree, text="HTML Results", command = html)    
   htmlBtn.grid(row=13, column=3, sticky='WE', padx=3, pady=3)
#########################################################################################################
       
   form.mainloop()

