# Objective: To process a list of .tif files of MODIS Daytime and
# Nighttime land surface temperature using a zonal overlay.
# The output is a comma delimited text file with various temperature statistics
# For each zone/date combination, including mean LST and growing degree days

# Modified By:Ashis Lamsal
# Supervisor: Ting-Wu Chuang
# Advisor: Mike Wimberly

# Import system modules
import sys, string, os, arcgisscripting, fnmatch
from dbfpy import dbf
import gc
import DbHandler
import psycopg2

class ZonalStat:
    
    '''Initialize the paths'''
    def __init__(self,tiffpath,temppath,zonalpath,landmask,outputcsv,logpath,griddir,dbhost,dbname,dbuser,dbpassword,inquery):
        self.tiffPath=tiffpath
        self.tempPath=temppath
        self.zonalPath=zonalpath
        self.landMask=landmask
        self.outputCsv=outputcsv
        self.logPath=logpath
        self.gridDir=griddir
        self.dbhost=dbhost
        self.dbname=dbname
        self.dbuser=dbuser
        self.dbpassword=dbpassword
        self.inQuery=inquery

    '''Read already projected files date from log'''
    def ReadLog(self):
        logFilerd=open(self.logPath+"lst_zonal_log.txt",'r')
        logFilerd.seek(0)
        date=int(logFilerd.read())
        logFilerd.close()
        return date

    '''Write already project files date into log'''    
    def WriteLog(self,imagedate):
        logFilewrt=open(self.logPath+"lst_zonal_log.txt",'w')
        logFilewrt.seek(0)
        logFilewrt.write(imagedate) 
        logFilewrt.close()

    '''Insert into the DB'''
    def InsertDB(self,year,day,zone,count,mean,stdev,summ):
        ObjRpyDbHandler=DbHandler.RpyDbHandler(self.dbuser,self.dbpassword,self.dbname,self.dbhost)
        ObjRpyDbHandler.InDB(year,day,zone,count,mean,stdev,summ,self.inQuery)   

    '''Compute zonal STAT '''     
    def ComputeZstat(self):
        print self.tiffPath
        print self.tempPath
        print self.zonalPath
        print self.landMask
        print self.outputCsv
        print self.logPath
        print "Please wait for the Zonal stat computation......"
               
        # Create the Geoprocessor object
        gp = arcgisscripting.create()

        # Check out any necessary licenses
        gp.CheckOutExtension("spatial")

        gp.rasterStatistics = "NONE"

        gp.overwriteoutput = 1

        # Set up input and output files
       
        Tifdir =self.tiffPath        
        Gisdir =self.tempPath
        Griddir=self.gridDir
        SetNull_tmp1 = Gisdir + "\\SetNull_tmp1"
        SetNull_tmp2 = Gisdir + "\\SetNull_tmp2"
        LST_tmp = Gisdir + "\\LST_tmp"
        LST_tmp2 = Gisdir + "\\LST_tmp2"
        LST_tmp3= Gisdir + "\\LST_tmp3"
        Clipout=Gisdir+"\\Clipout"
        Zonal_shape = self.zonalPath       
        Zonal_field = "FIPS"        
        Land_mask =self.landMask      
        Zonal_raster = Gisdir + "\\sdecoreg_gd"
        
        Output_filename = self.outputCsv      

        # Open file in write mode 
        # outfile = open(Output_filename, 'w')
        # Open file in append Mode
        outfile = open(Output_filename,'a')
        
        Zonal_output_table = Gisdir + "\\Zonal_output_table"
        Zonal_output_dbf = Gisdir + "\\Zonal_Output.dbf"

        # Write the header for the output file
        Header_str = "Year, Date, Zone, Count, Mean, Stdev, GDD\n"
        outfile.write(Header_str)

        Zonelist = []

        Firstpass = 1
        Tiflist = os.listdir(Tifdir)        
        Lastband = 0
        Curyear = 1999
        # Counter for LST_Day and LST_Night images
        imageCounter=0
        # Hold day time image information
        imageInfo1="0"
        # Hold night time image information
        imageInfo2="0"
        
        # Read entire directory that contains *.TIFF images
        for fname in Tiflist:
            if fnmatch.fnmatch(fname, '*.tif'):
                # Daytime temperature
                if fnmatch.fnmatch(fname, '*LST_Day*'):
                    In_image1 = Tifdir + "\\" + fname
                    print In_image1
                    Splitfname1 = fname.split(".")
                    Maqdate1 = Splitfname1[1]
                    Year1 = Maqdate1[1:5]
                    Date1 = Maqdate1[5:8]
                    imageInfo1=str(Year1)+str(Date1)
                    
                    # imageCounter should be 2 to retrive Day and Night temperature
                    if(int(imageInfo1)>int(self.ReadLog())):
                        imageCounter=imageCounter+1
                         
                    
                    # When processing the first .tif file, use it as a template to do
                    # vector-raster conversion for the zonal shapefile
                    if Firstpass == 1:                        
                        try:
                            gp.FeatureToRaster_conversion(Zonal_shape, Zonal_field, Zonal_raster,In_image1)
                        except Exception, e:
                            # Specaial attention: Remove all temporary files form the drive 
                            print "Error on Conversion from Feature to Raster"+str(e)

                        # Pull a list of the zones out of the raster table
                        cur = gp.SearchCursor(Zonal_raster)
                        row=cur.Next()
                        while row:
                            # Note - FIPS is hardcoded - will need to be changed for
                            # zones other than counties
                            Zonelist.append(row.FIPS)
                            row = cur.Next()

                        Firstpass = 0
                    # If we have moved to a new year, set the growing degree day
                    # sum to zero
                    if Year1 > Curyear:
                        Curyear = Year1
                        Gddsum = []
                        for zoneindex in Zonelist:
                            Gddsum.append(0)
                         
                # Nighttime temperature
                elif fnmatch.fnmatch(fname, '*LST_Night*'):
                    In_image2 = Tifdir + "\\" + fname
                    print In_image2
                    Splitfname2 = fname.split(".")
                    Maqdate2 = Splitfname1[1]
                    Year2 = Maqdate2[1:5]
                    Date2 = Maqdate2[5:8]
                    Lastband = 1
                    imageInfo2=str(Year2)+str(Date2)
                    if(int(imageInfo1)>int(self.ReadLog())):
                        imageCounter=imageCounter+1   

                # if Lastband == 1, then we have both Daytime and nighttime temperature
                # for a given date

                if ((Lastband == 1)&(int(imageInfo1)==int(imageInfo2))&(int(imageInfo1)>int(self.ReadLog()))&(imageCounter==2)):
                    # Process: Set Null... - QA Filter
                    gp.SetNull_sa(In_image1, In_image1, SetNull_tmp1, "\"Value\" =0")
                    gp.SetNull_sa(In_image2, In_image2, SetNull_tmp2, "\"Value\" =0")
##                    gp.SetNull_sa(In_image1, In_image1, SetNull_tmp1,"VALUE=0")
##                    gp.SetNull_sa(In_image2, In_image2, SetNull_tmp2,"VALUE=0")

                    # Process: Compute mean LST
                    LST_expression1 = "(" + SetNull_tmp2 + " + " + SetNull_tmp1 + ") / 2" 
                    #LST_expression1 = "(SetNull_tmp1 - SetNull_tmp2) / (SetNull_tmp1 + SetNull_tmp2)"
                    gp.SingleOutputMapAlgebra(LST_expression1, LST_tmp)

                    # Process: Set Null - Land/Water
                    LST_expression2 = LST_tmp + " / " + Land_mask
                    gp.SingleOutputMapAlgebra(LST_expression2, LST_tmp2)

                    # output GRID raster files
                    LST_expression3="(" + LST_tmp2 + " / 50 ) - 273.15"
                    gp.SingleOutputMapAlgebra(LST_expression3, LST_tmp3)
                    gp.ExtractByMask_sa(LST_tmp3, Zonal_shape, Clipout)

                    OutName = Griddir + "//" + "lst" + Year2 + Date2
                    gp.SingleOutputMapAlgebra(Clipout, OutName)

                    # Process: Zonal Statistics as Table...
                    gp.ZonalStatisticsAsTable_sa(Zonal_raster, "VALUE", LST_tmp2, Zonal_output_table, "DATA")

                    # Process: Convert from ESRI table to .dbf
                    gp.CopyRows_management(Zonal_output_table, Zonal_output_dbf, "")

                    db = dbf.Dbf(Zonal_output_dbf)

                    # Retrieve data from .dbf file
                    for rec in db:
                        year = Year1
                        day= Date1
                        valuecode = rec["VALUE"]
                        fipsval = Zonelist[valuecode - 1]
                        zone = fipsval
                        count = rec["COUNT"]
                        # Convert temps to degrees C
                        mean = rec["MEAN"] * 0.02 - 273.15
                        stddev = rec["STD"] * 0.02

                        # Compute growing degree days
                        curgd = (rec["MEAN"]*0.02 - 273.15) - 14.3
                        if(curgd > 0):
                            Gddsum[valuecode - 1] = Gddsum[valuecode - 1] + curgd * 8

                        summ =Gddsum[valuecode - 1]
                        
                        self.InsertDB(year,day,zone,count,mean,stddev,summ)

                    # Reset the counter
                    Lastband = 0
                    imageCounter=0

                    # Write state variable into log
                    self.WriteLog(imageInfo1)

                    # Closing and Clearing Unwanted temporary files    
                    db.close()                  
                    gp.delete_management(SetNull_tmp1)
                    gp.delete_management(SetNull_tmp2)
                    gp.delete_management(LST_tmp)
                    gp.delete_management(LST_tmp2)
                    gp.delete_management(LST_tmp3)
                    gp.delete_management(Clipout)
                    os.remove(self.tempPath+"\\Zonal_Output.dbf")
                    os.remove(self.tempPath+"\\Zonal_Output.dbf.xml")
 
                else:
                    print "Zonal stat is proceeding !!!"
        outfile.close()
        #gp.delete_management(Zonal_raster)                   
        print "Computing Zonal Statistics is Completed"

##if __name__=="__main__":
##    mdznalObj=ZonalStat("D:\\MODIS_LST_NDVI\\MOD11A2_Tiff\\","D:\\MODIS_LST_NDVI\\Tempoo","D:\\MODIS_LST_NDVI\\NGP_AEA\\NGP_AEA.shp","D:\\MODIS_LST_NDVI\\WaterMask\\rec_watermask","D:\\MODIS_LST_NDVI\\MOD11A2_Znal\\mod11a2_znal.csv","D:\\MODIS_LST_NDVI\\Log\\","D:\\MODIS_LST_NDVI\\MOD11A2_Grid\\")
##    mdznalObj.ComputeZstat()
    
    

    

    



