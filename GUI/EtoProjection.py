#Tools Description:Raster Projection
#Author:Ashis Lamsal
#Supervisor: Ting-Wu
#Advisor: Mike Wimberly

# Import System Modules

import sys,string,os,arcgisscripting

class EtoReprojection:

    def __init__(self,rasterfile,yearday,year,datum,projection,samplesize,compositedir,reprojectdir):

        self.rasterFile=rasterfile
        self.yearDay=yearday
        self.year=year
        self.datum=datum
        self.projection=projection
        self.sampleSize=samplesize
        self.reprojectDir=reprojectdir
        self.compositeDir=compositedir
        
    def Reproject(self):

        print "upto here -->1"
        rs=self.rasterFile
        print rs
        # Create Geoprocessing object
        GP = arcgisscripting.create()

        # set Toolbox
        GP.toolbox = "management"

        # Check out any License
        GP.CheckOutExtension("spatial")

        # Overwriting the Output
        GP.OverwriteOutput =1

        # Define Workspace
        #GP.workspace="D:\\MODIS_ETa\\Output\\Eto_composite\\"
        GP.workspace=self.compositeDir

       
        # Assigning Projection types
        #cs="C:\Program Files (x86)\\ArcGIS\\Coordinate Systems\\Projected Coordinate Systems\\Continental\\North America\\North America Albers Equal Area Conic.prj"
        cs=self.projection
        
        #coordsys="C:\\Program Files (x86)\\ArcGIS\\Coordinate Systems\\Geographic Coordinate Systems\\North America\North American Datum 1983.prj"
        coordsys=self.datum

        print "Try to define Projections........."

            ## Define the projection and Coordinate System
        GP.defineprojection(rs, coordsys)

        print "Definition completed........."
        try:
            print "Try to reproject raster  "+rs

            ##Reproject Raster into Albers Equals Area
            #GP.ProjectRaster_management(InFileName, OutFileName, out_coordinate, resample, cell, geo_tran, reg_point, in_coordinate)
            GP.ProjectRaster_management(rs,self.reprojectDir+"PrjETo"+str(self.year)+str(self.yearDay).zfill(3),cs,"NEAREST",self.sampleSize,"","",coordsys)
            print "Reprojection Done"
            print "upto here -->2"
            
        except:
            GP.GetMessages()
            raise "exit"
        
##if __name__=="__main__":
##    ObjEtoReprojection=EtoReprojection(r"D:\MODIS_ETa\Output\Eto_composite\eto2008009","9")
##    ObjEtoReprojection.Reproject()
    
    
    

           
           
