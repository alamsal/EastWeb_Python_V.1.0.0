# This script is designed to process a list of .tif files of MODIS BRDF-corrected
# reflectance to generate vegetation indices (NDVI) and carry out a zonal overlay
# The output is a comma delimited text file with various NDVI statistics
# For each zone/date combination, including mean NDVI and cumulative NDVI for
# the current growing season.

# Modified By:Aashis lamsal
# Supervisor: Ting-Wu Chuang
# Advisor: Mike Wimberly

# Import system modules
import sys, string, os, arcgisscripting, fnmatch
from dbfpy import dbf
import gc
import DbHandler
import psycopg2

class ZonalStatNdvi:
    
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

    def ReadLog(self):
        logFilerd=open(self.logPath+"ndvi_zonal_log.txt",'r')
        logFilerd.seek(0)
        date=int(logFilerd.read())
        logFilerd.close()
        return date

    def WriteLog(self,imagedate):
        logFilewrt=open(self.logPath+"ndvi_zonal_log.txt",'w')
        logFilewrt.seek(0)
        logFilewrt.write(imagedate) 
        logFilewrt.close()

    '''Insert into the DB'''
    def InsertDB(self,year,day,zone,count,mean,stdev,summ):
        ObjRpyDbHandler=DbHandler.RpyDbHandler(self.dbuser,self.dbpassword,self.dbname,self.dbhost)
        ObjRpyDbHandler.InDB(year,day,zone,count,mean,stdev,summ,self.inQuery)   

    def ZonalNdvi(self):
        print "please wait....."
        # Create the Geoprocessor object
        gp = arcgisscripting.create()

        # Check out any necessary licenses
        gp.CheckOutExtension("spatial")
        gp.rasterStatistics = "NONE"
        gp.overwriteoutput = 1

        # Set up input and output files
        # Can either be hard coded or entered by the user
        Tifdir =self.tiffPath       
        Gisdir =self.tempPath
        Griddir=self.gridDir
        SetNull_tmp1 = Gisdir + "\\SetNull_tmp1"
        SetNull_tmp2 = Gisdir + "\\SetNull_tmp2"
        NDVI_tmp = Gisdir + "\\NDVI_tmp"
        NDVI_tmp2 = Gisdir + "\\NDVI_tmp2"
        NDVI_tmp3=Gisdir + "\\NDVI_tmp3"
        Clipout=Gisdir+"\\Clipout"
        Zonal_shape = self.zonalPath 
        Zonal_field = "FIPS"
        Land_mask =self.landMask
        Zonal_raster = Gisdir + "\\sdecoreg_gd"
        Output_filename =self.outputCsv
        outfile = open(Output_filename, 'a')
        Zonal_output_table = Gisdir + "\\Zonal_output_table"
        Zonal_output_dbf = Gisdir + "\\Zonal_Output.dbf"
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
                # Band 1
                if fnmatch.fnmatch(fname, '*Band1*'):
                    In_image1 = Tifdir + "\\" + fname
                    print In_image1
                    Splitfname1 = fname.split(".")
                    Maqdate1 = Splitfname1[1]
                    Year1 = Maqdate1[1:5]
                    Date1 = Maqdate1[5:8]
                    imageInfo1=str(Year1)+str(Date1)

                    # imageCounter should be 2 to retrive Band 1 and Band 2
                    if(int(imageInfo1)>int(self.ReadLog())):
                        imageCounter=imageCounter+1
                        
                    # When processing the first .tif file, use it as a template to do
                    # vector-raster conversion for the zonal shapefile
                    if Firstpass == 1:
                        try:
                            gp.FeatureToRaster_conversion(Zonal_shape, Zonal_field, Zonal_raster, In_image1)
                        except Exception, e:
                            print "Error on conversion from Feature to Raster"+str(e)

                        # Pull a list of the zones out of the raster table
                        cur = gp.SearchCursor(Zonal_raster)
                        row=cur.Next()
                        while row:
                            # Note - FIPS is hardcoded - will need to be changed for
                            # zones other than counties                    
                            Zonelist.append(row.FIPS)
                            row = cur.Next()

                        # Write the header for the output file
                        Header_str = "Year, Date, Zone, Count, Mean, Stdev, Cum\n"
                        outfile.write(Header_str)

                        Firstpass = 0
                    # If we have moved to a new year, set the growing degree day
                    # sum to zero
                    if Year1 > Curyear:
                        Curyear = Year1
                        Gddsum = []
                        for zoneindex in Zonelist:
                            Gddsum.append(0)
                            
                # Band 2        
                elif fnmatch.fnmatch(fname, '*Band2*'):
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

                # if Lastband == 1, then we have Bands 1 and 2
                # for a given date
                if ((Lastband == 1)&(int(imageInfo1)==int(imageInfo2))&(int(imageInfo1)>int(self.ReadLog()))&(imageCounter==2)):

                    # Process: Set Null... - QA Filter
                    gp.SetNull_sa(In_image1, In_image1, SetNull_tmp1, "\"Value\" =32767")
                    gp.SetNull_sa(In_image2, In_image2, SetNull_tmp2, "\"Value\" =32767")
                
                    # Process: Compute NDVI
                    NDVI_expression1 = "10000 * (" + SetNull_tmp2 + " - " + SetNull_tmp1 + ") / (" + SetNull_tmp2 + " + " + SetNull_tmp1 + ")"
                    #NDVI_expression1 = "(SetNull_tmp1 - SetNull_tmp2) / (SetNull_tmp1 + SetNull_tmp2)"
                    gp.SingleOutputMapAlgebra(NDVI_expression1, NDVI_tmp)

                    # Process: Set Null - Land/Water
                    NDVI_expression2 = NDVI_tmp + " / " + Land_mask
                    #NDVI_expression2 = "SetNull_temp1 * Land_mask"
                    gp.SingleOutputMapAlgebra(NDVI_expression2, NDVI_tmp2)

                    # output GRID raster files
                    NDVI_expression3 = "(" + NDVI_tmp + " / " + Land_mask + ") / 10000.00"
                    gp.SingleOutputMapAlgebra(NDVI_expression3, NDVI_tmp3)
                    gp.ExtractByMask_sa(NDVI_tmp3, Zonal_shape, Clipout)

                    OutName = Griddir + "//" + "ndvi" + Year2 + Date2
                    gp.SingleOutputMapAlgebra(Clipout, OutName)

                    # Process: Zonal Statistics as Table...
                    gp.ZonalStatisticsAsTable_sa(Zonal_raster, "VALUE", NDVI_tmp2, Zonal_output_table, "DATA")

                    # Process: Convert from ESRI table to .dbf
                    gp.CopyRows_management(Zonal_output_table, Zonal_output_dbf, "")

                    db = dbf.Dbf(Zonal_output_dbf)

                    for rec in db:
                        year = Year1
                        day= Date1
                        valuecode = rec["VALUE"]
                        fipsval = Zonelist[valuecode - 1]
                        zone =fipsval
                        count =rec["COUNT"]
                        mean =rec["MEAN"] / 10000 
                        stddev =rec["STD"] / 10000 

                        # Compute cumulative NDVI index, start from day 113 with threshold vaue=0.25
                        curgd = rec["MEAN"] / 10000 - 0.25
                        if ((curgd > 0) & (int(Date1)>105)):            
                            Gddsum[valuecode - 1] = (float(Gddsum[valuecode - 1]) + float(curgd * 8))
       
                            
                        elif (int(Date1) < 113):
                            Gddsum[valuecode - 1]="0"

                        summ=Gddsum[valuecode - 1]
                        self.InsertDB(year,day,zone,count,mean,stddev,summ)

                    # Reset the Counter
                    Lastband = 0
                    imageCounter=0

                    # Write state variable into log
                    self.WriteLog(imageInfo1)

                    # Close files and clearn up
                    db.close()
                    gp.delete_management(SetNull_tmp1)
                    gp.delete_management(SetNull_tmp2)
                    gp.delete_management(NDVI_tmp)
                    gp.delete_management(NDVI_tmp2)
                    gp.delete_management(NDVI_tmp3)
                    gp.delete_management(Clipout)
                    gp.delete_management(Zonal_output_table)
                    os.remove(self.tempPath+"\\Zonal_Output.dbf")
                    os.remove(self.tempPath+"\\Zonal_Output.dbf.xml")
                else:                    
                    print "Zonal stat is computaion proceeding......."    
       
        outfile.close()

        print "Computing Zonal Statistics is Completed"
        
##if __name__=="__main__":
##    #def __init__(self,tiffpath,temppath,zonalpath,landmask,outputcsv,logpath):
##    objZonalNdvi=ZonalStatNdvi("D:\\MODIS_LST_NDVI\\MCD43B4_Tiff\\","D:\\MODIS_LST_NDVI\\MCD_Tempoo\\","D:\\MODIS_LST_NDVI\\NGP_AEA\\NGP_AEA.shp","D:\\MODIS_LST_NDVI\\WaterMask\\rec_watermask","D:\\MODIS_LST_NDVI\\MCD43B4_Znal\\MCD43B4.csv","D:\\MODIS_LST_NDVI\\MCD43B4_Log\\","D:\\MODIS_LST_NDVI\\MCD43B4_Grid\\")
##    objZonalNdvi.ZonalNdvi()
    



