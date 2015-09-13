# Program Objective: Summarized(Zonal Stat for NGP-AEA)daily Temperature from ESRI GRID and feed into the PostgreSQL DB 
# Author:Aashis Lamsal
# Supervisor: Ting-Wu Chuang
# Advisor: Mike Wimberly

# Import system modules
import sys, string, os, arcgisscripting, fnmatch
from dbfpy import dbf
import psycopg2
import gc
import DbHandler

class TrmmZonalStat:

    global Zonelist

    '''Constructor for Assigning paths'''
    def __init__(self,gridpath,znlpath,shppath,outcsvpath,trmmlog,dbhost,dbname,dbuser,dbpassword,inquery):
        gc.enable()
        self.gridPath=gridpath
        self.znlPath=znlpath
        self.shpPath=shppath
        self.outcsvPath=outcsvpath
        self.trmmLog=trmmlog
        self.dbhost=dbhost
        self.dbname=dbname
        self.dbuser=dbuser
        self.dbpassword=dbpassword
        self.inQuery=inquery

    ''' Read already projected files date from log'''
    def ReadLog(self):
        logFilerd=open(self.trmmLog+"\\TrmmZonal.txt",'r')
        logFilerd.seek(0)
        date=int(logFilerd.read())
        logFilerd.close()
        return date

    ''' Write already project files date into log '''   
    def WriteLog(self,date):
        logFilewrt=open(self.trmmLog+"\\TrmmZonal.txt",'w')
        logFilewrt.seek(0)
        logFilewrt.write(date) 
        logFilewrt.close()

    '''Insert into the DB'''
    def InsertDB(self,year,day,zone,count,mean,stdev,summ):
        ObjRpyDbHandler=DbHandler.RpyDbHandler(self.dbuser,self.dbpassword,self.dbname,self.dbhost)
        ObjRpyDbHandler.InDB(year,day,zone,count,mean,stdev,summ,self.inQuery)   
  
    '''Calculate the Zonal Summary'''
    def ComputeZonal(self):
        try:
            print "Wait for Progam Response ..............."
            # Create the Geoprocessor object
            gp = arcgisscripting.create()
            gp.rasterStatistics = "NONE"
            # Check out any necessary licenses
            gp.CheckOutExtension("spatial")
            gp.overwriteoutput = 1
            

            # Set up input and output files

            gp.Workspace = self.gridPath

            # OutWorkSpace = r"D:\RSData\TRMM"
            Gisdir = self.znlPath      
            Zonal_shape = self.shpPath 
            print"zonal_shape-->"+str(Zonal_shape)
            #Zonal_shape = sys.argv[2]
            Zonal_field = "FIPS"
            
            #Zonal_field = sys.argv[3]
            Zonal_raster = Gisdir + "\\trmm_grid"
            Output_filename = self.outcsvPath
            #Output_filename = sys.argv[6]
            outfile = open(Output_filename, 'a')
            Zonal_output_table = Gisdir + "\\Zonal_output_table"
            Zonal_output_dbf = Gisdir + "\\Zonal_Output.dbf"
           
            Zonelist = []
            Firstpass = 1

            #Get the raster datasets in the input workspace and loop through them from the start
            InputRasters = gp.ListRasters()
            InputRasters.reset()
            InputRaster = InputRasters.next()
            while InputRaster:
                print InputRaster
                Splitfname1 = InputRaster.split("_")
                Maqdate1 = Splitfname1[1]
                print Maqdate1

                if(int(Maqdate1)>int(self.ReadLog())):
                        
                    Year1 = Maqdate1[0:4]
                    Date1 = Maqdate1[4:8]
                    print "-->"+str(Year1)
                    print "-->"+str(Date1)

                    # When processing the first the file, use it as a template to do
                    # vector-raster conversion for the zonal shapefile
                    try:
                        
                        gp.FeatureToRaster_conversion(Zonal_shape, Zonal_field, Zonal_raster)
                        #InputRaster = InputRasters.next()
                        print"Converted to Raster!"
                    except:
                        print" Can not converted to Raster"
                        #outfile.close()
                        #raise exit

                    if Firstpass == 1:
                        #gp.FeatureToRaster_conversion(Zonal_shape, Zonal_field, Zonal_raster, In_image1)
                        # Pull a list of the zones out of the raster table
                        cur = gp.SearchCursor(Zonal_shape)
                        row=cur.Next()
                        while row:
                                    # Note - FIPS is hardcoded - will need to be changed for
                                    # zones other than counties                    
                            Zonelist.append(row.FIPS)
                            row = cur.Next()

                        # Write the header for the output file
                        #Header_str = "Year, Date, Zone, Count, Mean, Sum, Stdev\n"
                        #outfile.write(Header_str)

                        Firstpass = 0
                  
                        # Process: Zonal Statistics as Table...
                    try:
                        gp.ZonalStatisticsAsTable_sa(Zonal_raster, "Value", InputRaster, Zonal_output_table, "NODATA")
                        print"Process: Zonal Statistics as Table..."
                     # Process: Convert from ESRI table to .dbf
                        gp.CopyRows_management(Zonal_output_table, Zonal_output_dbf, "")

                        db = dbf.Dbf(Zonal_output_dbf) 
                       # Retrieve data from .dbf file
                        i=0
                        for rec in db:
                                year = Year1
                                day= Date1
                                valuecode = rec["VALUE"]
                                fipsval = Zonelist[i]
                                i=i+1
                                zone =fipsval
                                count = rec["COUNT"]
                                mean = rec["MEAN"]
                                summ = rec["SUM"]
                                stddev = rec["STD"]
                                self.InsertDB(year,day,zone,count,mean,stddev,summ)
                                
                        
                        # Close files and clean up
                        db.close()
                        gp.delete_management(Zonal_output_table)
                        call_delete = "del " + Zonal_output_dbf
                        os.system(call_delete)
                        InputRaster = InputRasters.next()
                        self.WriteLog(Maqdate1)
                        print "Completed the Zonal Stat for-->"+str(Maqdate1)
                        Firstpass = 0
                        
                    except Exception,e:
                        print"Can not compute Zonal Statistics"+str(e)
                        raise exit
                else:
                    print "Zonal stat is already calculated for -->"+str(InputRaster)
                    InputRaster = InputRasters.next()
     
            # Remove Temporary files
            outfile.close()
            if (os.path.exists(self.znlPath+"\\trmm_grid.aux")):
                os.remove(self.znlPath+"\\trmm_grid.aux")
            if(os.path.exists(self.znlPath+"\\Zonal_Output.dbf.xml")):
                os.remove(self.znlPath+"\\Zonal_Output.dbf.xml")
            if os.path.exists(self.znlPath+"\\trmm_grid"):
                for files in os.listdir(self.znlPath+"\\trmm_grid"):
                    #print files
                    os.remove(self.znlPath+"\\trmm_grid\\"+files)
                os.removedirs(self.znlPath+"\\trmm_grid")

            print "TRMM Zonal Stat Finished !!!"
            
        except Exception,e:
            print str(e)

        finally:
            del gp

            
##if __name__=="__main__":
##
##    #def __init__(self,gridpath,znlpath,shppath,outcsvpath):
##    znalstatObj= TrmmZonalStat( r"D:\MODIS_TRMM\GridFile",r"D:\MODIS_TRMM",r"D:\MODIS_TRMM\ecoregions\NGP_AEA.shp",r"D:\MODIS_TRMM\TRMM_summary.csv",r"D:\MODIS_TRMM\Logs")
##    znalstatObj.ComputeZonal()
##  
    
            
  
