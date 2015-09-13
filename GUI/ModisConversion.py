# Script to batch process MODIS .hdf files using the MODIS reprojection tool (MRT)
# Will process all hdf files in the specified directory, and dump the output
# files into another specified directory
# Other options are specified through the MRT parameter file (e.g., scientific
# data sets to extract, output projection, output pixel size)

# Note - as written, the script assumes that all of the correct .hdf files are
# in Hdfdir in the proper order - i.e., there needs to be exactly three MODIS
# tiles for each processing date. The user needs to check this beforehand.
# Otherwise, the script will end up combining tiles from different dates 
# At some point, this script needs to be made "smarter" so that it checks the
# .hdf files to ensure that the proper tiles are being combined.

import os
import fnmatch
import sys

class ReprojectModis:
    
    # Assinging directory with hdf files and output (tiff) files
    def __init__(self, hdfpath,tiffpath,logpath,mosaictileno,mrtfile):
        self.hdfPath=hdfpath
        self.tiffPath=tiffpath
        self.logPath=logpath
        self.mtileNo=mosaictileno
        self.mrtFile=mrtfile

    # Read already projected files date from log
    def ReadLog(self,path):
        logFilerd=open(path+"prjlog.txt",'r')
        logFilerd.seek(0)
        date=int(logFilerd.read())
        logFilerd.close()
        return date

    # Write already project files date into log    
    def WriteLog(self,path,imagedate):
        logFilewrt=open(path+"prjlog.txt",'w')
        logFilewrt.seek(0)
        logFilewrt.write(imagedate) 
        logFilewrt.close()
        
    # Function Convert *.hdf files into *.tiff. 
    def ConvertTiff(self):
        print self.hdfPath
        print self.tiffPath
        print self.logPath
        print self.mtileNo
        print self.mrtFile
   
        # Local directory with hdf files
        # Hdfdir = input("Enter the local directory containing the hdf files:")

        #Hdfdir = "C:\\TestMODISData\\MOD11A2\\"
        Hdfdir =self.hdfPath
        prjLog=self.logPath
        
        # Local directory to store tiff files
        # Tifdir = input("Enter the local directory where you want to store the tif files:")

        #Tifdir = "C:\\TestMODISData\\tiff\\"
        Tifdir =self.tiffPath

        
        # Name and location of the MRT parameter file
        # MRTfile = input("Enter MODIS Reprojection Tool parameter file:")
        # MRTfile=Tifdir+"MODLST_ngp.prm"

        Outfilename = Tifdir + "temp.txt"
        Outfilename2 = Tifdir + "imagelist.txt"
        Temphdffile= Tifdir + "temphdf.hdf"
        print "Temphdf file ---->"+str(Temphdffile)

        outfile2 = open(Outfilename2, "w")

        # List all the files in this folder
        Filelist=os.listdir(Hdfdir)

        # Set counter for tiles to include in the output mosaic
        Tileno = 1
        outfile = open(Outfilename, "w")
               

        for Filename in Filelist:

            # Process the subset of the list fname that matches the description (only .hdf files) 
            if fnmatch.fnmatch(Filename, '*.hdf'):
                # Split the .hdf filename
                Splitfname = Filename.split(".")
                Mdataset = Splitfname[0]
                Maqdate = Splitfname[1]
                Mlocation = Splitfname[2]
                Myear = Splitfname[3]
                Mprocdate = Splitfname[4]
                Mext1 = Splitfname[5]
                # Extract horizonal and vertical tile numbers (information not used in current script)
                Htile = Mlocation[1:3]
                Vtile = Mlocation[4:6]

                Hdffile = Hdfdir + Filename

                outstr2 = Filename + " "
                # Write list of .hdf files for input to MRT mosaic
                outstr = Hdffile + "\n"
                outfile.write(outstr)
                # Write list of .hdf files processed to the log file
                outstr2 = Filename + " "
                outfile2.write(outstr2)
                #logDate="2010113"
                imageDate= Maqdate[-7:]
                logDate= self.ReadLog(prjLog)
                print imageDate
                if(int(imageDate)>int(logDate)):
                    # For every (7=NGP,4=ETH) .hdf files, mosaic and resample
                    if Tileno ==self.mtileNo:
                        Outtif = Tifdir + Mdataset + "." + Maqdate + "." + Myear + "." + Mprocdate + '.tif'
                        print Outtif
                        # Write end of line to the log file
                        outfile2.write("\n")
                        # Close the imagelist file - will be used as input to MRT mosaic
                        outfile.close()
                        # Run MRT mosaic
                        call_mosaic = "mrtmosaic -i " + Outfilename + " -o " + Temphdffile
                        print call_mosaic
                        
                        os.system(call_mosaic)                        
                        
                        # Run MRT resample
                        call_mrt = "resample -p " + self.mrtFile + " -i " + Temphdffile + " -o " + Outtif
                        #call_mrt = "resample -p MODLST_ngp.prm -i " +Temphdffile+ " -o " + Outtif
                        #raise exit
                        print call_mrt
                        os.system(call_mrt)                         
                        
                        # Open a clean imagelist file
                        outfile = open(Outfilename, "w")
                        # Reset the .hdf file counter
                        Tileno = 1
                        self.WriteLog(prjLog,imageDate)
                        print "Projection Complete for -->"+str(imageDate)
                    else:
                        Tileno = Tileno + 1
                else:
                    print "Already Reprojection is Done for Date--->"+str(Maqdate)

        outfile.close()
        outfile2.close()
        print "MODIS Reprojection is Completed !!!"

##if __name__=="__main__":
##    reprojObj=ReprojectModis("D:\\MODIS_LST_NDVI\\MOD11A2\\","D:\\MODIS_LST_NDVI\\MOD11A2_Tiff\\","D:\\MODIS_LST_NDVI\\Log\\",7,"MODLST_ngp.prm")
##    reprojObj.ConvertTiff()
    
                

                        
                            
                            
                    
                    
    
