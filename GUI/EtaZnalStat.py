# Program Description:This script generates Zonal Statistics (temperature) from Raster file(MODIS)
# Author: Aashis Lamsal
# Supervisor: Ting-Wu
# Advisor: Mike Wimberly

# Import System Modules
import sys,string,os,arcgisscripting,fnmatch
import psycopg2
from dbfpy import dbf
import DbHandler
import gc

class EtaZnal:
    
    def __init__(self,etapath,znalshapepath,temppath,logpath,dbhost,dbname,dbuser,dbpassword,inquery):
        gc.enable() 
        self.etaPath=etapath
        self.znalshapePath=znalshapepath
        self.tempPath=temppath        
        self.logPath=logpath        
        self.dbhost=dbhost
        self.dbname=dbname
        self.dbuser=dbuser
        self.dbpassword=dbpassword
        self.inQuery=inquery

    '''Read already projected files date from log'''
    def ReadLog(self):
            logFilerd=open(self.logPath+"etaznal.txt",'r')
            logFilerd.seek(0)
            date=int(logFilerd.read())
            logFilerd.close()
            return date

    '''Write already project files date into log'''    
    def WriteLog(self,imagedate):
            logFilewrt=open(self.logPath+"etaznal.txt",'w')
            logFilewrt.seek(0)
            logFilewrt.write(imagedate) 
            logFilewrt.close()

    '''Insert into the DB'''
    def InsertDB(self,year,day,zone,count,mean,stdev,summ):
        ObjRpyDbHandler=DbHandler.RpyDbHandler(self.dbuser,self.dbpassword,self.dbname,self.dbhost)
        ObjRpyDbHandler.InDB(year,day,zone,count,mean,stdev,summ,self.inQuery)   

        
    def ComputeZnalStat(self):
        try:
            print "Please wait..........10 sec"

            # Create Geoprocessing object
            gp = arcgisscripting.create()

            # Check out any License
            gp.CheckOutExtension("spatial")

            # Overwriting the Output
            gp.OverwriteOutput =1
            gp.rasterStatistics = "NONE"

            #Location for ETa files
            masterFolder=self.etaPath

            #Define workspace dierctory
            gp.Workspace=masterFolder

            #Zonal shape file location
            zoneShape=self.znalshapePath

            #Zone Field
            zoneField="FIPS"

            #Zone output table location (temporary location but required)
            outputTable=self.tempPath+"temp.dbf"
            #Zone output dbf location
            
            outputDbf=self.tempPath

            # Generate zonal summary and feed into the DATABASE
            def CustomizeSummary(name,year,day):
                db = dbf.Dbf(name)
                for rec in db:
                    zone= rec["FIPS"]
                    count=rec["COUNT"]
                    summ=rec["SUM"]
                    mean=rec["MEAN"]
                    stddev=rec["STD"]
                    self.InsertDB(year,day,zone,count,mean,stddev,summ)
     
            #Read ETa rasters
            etaList=list() # list to read eta files
            etaList=gp.ListRasters("*")
            eta=etaList.Next()

            # Generate ETa summary table
            while eta:
                if(int(self.ReadLog())<int(eta[3:10])):                    
                    if fnmatch.fnmatch(eta,'ETa*'):
                        year=eta[3:7]
                        day=eta[7:10]

                        try:
                            gp.ZonalStatisticsAsTable_sa(zoneShape,zoneField,masterFolder+eta,outputTable,"DATA")
                        except Exception,e:
                            print "Could not compute ZonalStatisticsAsTable_sa:-: "+str(e)
                        gp.CopyRows_management(outputTable,outputDbf+eta+".dbf","")
                        CustomizeSummary(outputDbf+eta+".dbf",year,day)

                        self.WriteLog(str(eta[3:10]))

                        gp.delete_management(outputDbf+eta+".dbf")
                        gp.delete_management(outputTable)
                else:
                    print "Zonal stat already computed for :-: "+str(eta)
                eta=etaList.Next()
            print"Zonal stat Computation Finished... !!!"
        except Exception,e:
            print str(e)
        finally:
            del gp
            
      
##if __name__=="__main__":
##
##    #def __init__(self,etapath,shapepath,temppath,outputpath,logpath):
##    ObjEtaZnal=EtaZnal("D:\\MODIS_ETa\\Data\\Eta\\","D:\\MODIS_LST_NDVI\\NGP_AEA\\NGP_AEA.shp","D:\\MODIS_ETa\\Output\\Temp\\","D:\\MODIS_ETa\\Output\\EtaZnal\\","D:\\MODIS_ETa\\Log\\","localhost","db_EastWeb","postgres","eastweb1")
##    ObjEtaZnal.ComputeZnalStat()
   
    

    
    
        
   
    

    
    


