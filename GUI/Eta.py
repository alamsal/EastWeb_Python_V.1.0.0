#Tool Description: To Multiply ETo and ETf raster files
#Author: Aashis Lamsal
#Supervisor: Ting-Wu
#Advisor:Mike Wimberly
# Import System Modules

import sys,string,os,arcgisscripting,gc
class ComputeEta:

    def __init__(self,etopath,etfpath,etapath,logpath,):
        gc.enable()
        self.etoPath=etopath
        self.etfPath=etfpath
        self.etaPath=etapath
        self.logPath=logpath
    
    '''Read already projected files date from log'''
    def ReadLog(self):
            logFilerd=open(self.logPath+"etalog.txt",'r')
            logFilerd.seek(0)
            date=int(logFilerd.read())
            logFilerd.close()
            return date

    '''Write already project files date into log'''    
    def WriteLog(self,imagedate):
            logFilewrt=open(self.logPath+"etalog.txt",'w')
            logFilewrt.seek(0)
            logFilewrt.write(imagedate) 
            logFilewrt.close()

    def EtaCalculation(self):
       
        # Create Geoprocessing object

        gp = arcgisscripting.create()

        # Check out any License

        gp.CheckOutExtension("spatial")

        # Overwriting the Output

        gp.OverwriteOutput =1

        #Define output path
        outRaster=self.etaPath

        #Creating Lists
        fList=list() #Read etf Rasters
        oList=list() # Read eto Rasters

        etfList=list() # To add etf Rasters
        etoList=list() # To add eto Rasters

        #change the work space and starting to read ETF files 
        gp.workspace=self.etfPath
        fList=gp.ListRasters("*")
        etf=fList.Next()
        etfList.append(etf)

        while etf:
            etf=fList.Next()
            etfList.append(etf)

        print "\t ETf List \t"
        for etf in etfList:
           
            print etf
            
        print "-------------"


        #change the work space and starting to read reprojected ETO files

        roList=list() # Read resampled eto Rasters
        retoList=list() # To add resampled eto Rasters

        gp.workspace=self.etoPath
        roList=gp.ListRasters("*")
        reto=roList.Next()
        retoList.append(reto)

        while reto:
            reto=roList.Next()
            retoList.append(reto)
        
        print"\t ETo List \t"
        for eto in retoList:
           
            print eto
            
        print "-------------"


        # Using times tool to multiply the eto and etf rasters.
        for j in range(0,(len(etfList)-1),1):
            i=0
            #print "j--->" + str(etfList[j])
            while(i<(len(retoList)-1)):
                #print "i--->"+str(i)               
                dayEto=retoList[i][-3:]
                dayEtf=etfList[j][-3:]    
                yearEto=retoList[i][-7:-3]
                yearEtf=etfList[j][-7:-3]

                etoInfo=int(yearEto+dayEto)
                etfInfo=int(yearEtf+dayEtf)
                etaInfo=self.ReadLog()

                #print dayEto,dayEtf,yearEto,yearEtf
                if((etoInfo<=etaInfo) and (etfInfo<=etaInfo)):
                    print"ETa alreay comuted for-"
                    print"ETf: "+str(etfList[j])
                    print"ETo: "+str(retoList[i])
                    print"\n"
                    
                elif(dayEto==dayEtf and yearEto==yearEtf):
                    
                    print "Multiply \t"+retoList[i] +"\t and \t "+ etfList[j]
                    gp.Times_sa(self.etfPath+etfList[j],self.etoPath+retoList[i],(outRaster+"ETa"+str(yearEto)+str(dayEto).zfill(3)))
                    
                    print "Successfully Completed"
                    self.WriteLog(str(etoInfo))
                    break
                
                else:
                    
                    print "Unmatched ETf -->"+self.etfPath+etfList[j]+" and ETo -->"+self.etoPath+retoList[i]
                    
                i=i+1
            
        
##if __name__=="__main__":
##
##    #def __init(self,etopath,etfpath,etapath,logpath,):
##    ObjComputeEta=ComputeEta("D:\\MODIS_ETa\\Data\\Eto_reproject\\","D:\\MODIS_ETa\\Output\\Etf\\2000\\","D:\\MODIS_ETa\\Output\\Eta\\","D:\\MODIS_ETa\\Log\\")
##    ObjComputeEta.EtaCalculation()
    
    
                    
            

