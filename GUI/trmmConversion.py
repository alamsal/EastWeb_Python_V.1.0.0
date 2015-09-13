#Objective:To convert NetCDF files of MODIS TRMM into ESRI Grid files
#Author: Aashis Lamsal
#Project Name: EastWeb
#Supervisor: Ting-Wu Chuang

# Import system modules
import sys, string, os, arcgisscripting, fnmatch
from dbfpy import dbf
import gc

class CdftoGrid:    
    '''Initialize paths'''
    def __init__(self,cdfpath,gridpath,logpath):
        gc.enable()
        self.cdfPath=cdfpath
        self.gridPath=gridpath
        self.conversionLog=logpath

    ''' Read already projected files date from log'''
    def ReadLog(self):
        logFilerd=open(self.conversionLog+"\\CdftoGrid.txt",'r')
        logFilerd.seek(0)
        date=int(logFilerd.read())
        logFilerd.close()
        return date

    ''' Write already project files date into log '''   
    def WriteLog(self,date):
        logFilewrt=open(self.conversionLog+"\\CdftoGrid.txt",'w')
        logFilewrt.seek(0)
        logFilewrt.write(date) 
        logFilewrt.close()
        
    '''It converts NetCdf files to ESRI Grid'''
    def ConvertoGrid(self):
        
        # Create the Geoprocessor object
        gp = arcgisscripting.create()

        # Check out any necessary licenses
        gp.CheckOutExtension("spatial")

        gp.overwriteoutput = 1

        # Local directory with NetCDF files
        NetCDFdir = self.cdfPath
        # Local directory to store GRID files
        Griddir = self.gridPath

        # List all the files in this folder
        Filelist=os.listdir(NetCDFdir)

        try:
                
            for Filename in Filelist:

                # Process the subset of the list fname that matches the description 
                if fnmatch.fnmatch(Filename, '*.nc'):
                    # Split the .nc filename
                    Splitfname = Filename.split(".")
                    Mdataset = Splitfname[0]
                    Myear = Splitfname[1]
                    Mmon = Splitfname[2]
                    Mday = Splitfname[3]
                    Mver = Splitfname[4]
                    Mext = Splitfname[5]

                    imageInfo=Myear+Mmon+Mday

                    if((int(imageInfo)>int(self.ReadLog()))):

                        NetCDFfile = NetCDFdir + Filename

                        #Set local variables
                        InNetCDFFile = NetCDFfile
                        InVariable = "hrf"
                        InXDimension = "longitude"
                        InYDimension = "latitude"
                        OutRasterLayer = "hrf_Layer"

                        # Process: MakeNetCDFRasterLayer
                        gp.MakeNetCDFRasterLayer(InNetCDFFile, InVariable, InXDimension, InYDimension, OutRasterLayer)
                    
                        # convert to GRID
                        OutName = Griddir + "//" +"TRMM" +"_" + Myear + Mmon + Mday
                        gp.SingleOutputMapalgebra(OutRasterLayer, OutName)
                       
                        self.WriteLog(imageInfo)
                        print "Successfully converted to Grid "+str(Filename)
                        #raise exit
                    else:
                        print "Already Converted From NetCDF to Grid -->"+str(Filename)
                    print "Conversion completed..."
        except Exception, e:
            print "Could not get the Net Cdf file list" +str(e)
        # Remove all the contents from 'info' folder created by the script inorder to erase the previous states of the script.
        finally:
            if(os.path.exists(self.gridPath+"info")):
                for files in os.listdir(self.gridPath+"info"):
                    # print files
                    os.remove(self.gridPath+"info\\"+files)
                os.removedirs(self.gridPath+"info")
            
        
##if __name__=="__main__":
##    gridconObj=CdftoGrid(r"D:\MODIS_TRMM\NetCDFile",r"D:\MODIS_TRMM\GridFile",r"D:\MODIS_TRMM\Logs")
##    gridconObj.ConvertoGrid()
    
    




        

        



