#Tool Description: To compute average of raster files
#Author: Aashis Lamsal
#Supervisor: Ting-Wu
#Advisor: Mike Wimberly
# Import System Modules

import sys,string,os,arcgisscripting
import EtoProjection
import gc

class EtoComposite:
        
        def __init__(self,temppath,temppath1,compositedir,dailyeto,logpath,year,datum,projection,samplesize,reprojectdir):
                gc.enable()
                self.tempPath=temppath
                self.tempPath1=temppath1
                self.finalPath=compositedir
                self.workSpace=dailyeto
                self.logPath=logpath
                # variables send to Eto projection
                self.year=year
                self.datum=datum
                self.projection=projection
                self.sampleSize=samplesize
                self.reprojectDir=reprojectdir
                
        '''Read already projected files date from log'''
        def ReadLog(self,filename):
                logFilerd=open(self.logPath+filename,'r')
                logFilerd.seek(0)
                date=int(logFilerd.read())
                logFilerd.close()
                return date

        '''Write already project files date into log'''    
        def WriteLog(self,filename,imagedate):
                logFilewrt=open(self.logPath+filename,'w')
                logFilewrt.seek(0)
                logFilewrt.write(imagedate) 
                logFilewrt.close()

                
        def EightDayComposite(self):
                
                print "Please wait..........10 sec"

                # Create Geoprocessing object
                gp = arcgisscripting.create()

                # Check out any License
                gp.CheckOutExtension("spatial")

                # Overwriting the Output
                gp.OverwriteOutput =1

                #Define Workspace
                temppath=self.tempPath # Temporary path for raster computation
                temppath1=self.tempPath1
                finalpath=self.finalPath # Final Destination of raster files
                gp.workspace=self.workSpace

                listArray= list()
                overArray= list()

                # Reading all raster files
                rsList=gp.ListRasters("*")  

                # Raster Counter
                # global counter
                counter=1

                # Use tracking to calculate day of the year
                yearDay=self.ReadLog("yearday.txt")
                

                rs=rsList.Next()
                       
                print "Keep your patience while running it might takes hours..."

                try:                        
                        while rs:
                                rastInfo=self.ReadLog("etolog.txt")
                                print int(rastInfo)
                                print int(rs[-6:])

                                if(int(rastInfo)<int(rs[-6:])):                                                
                                        gp.workspace=self.workSpace
                                        print "Available raster:-: "+str(rs)
                                        # Making group of 8 files 
                                        if(counter<=8):                       
                                                listArray.append(rs)
                                                print listArray
                                                if((len(listArray)==8)and(yearDay<=353)):
                                                        #print listArray

                                                        #Creating list to store temporary paths
                                                        outraster= [(temppath+str(0)),(temppath+str(1)),(temppath+str(2)),(temppath+str(3)),(temppath+str(4)),(temppath+str(5)),(temppath+str(6)),(temppath+str(7))]
                                                        #print outraster[0],outraster[1],outraster[2]

                                                        # Make final raster name as julian day date        
                                                        finalraster=finalpath+"ETo"+str(self.year)+str(yearDay).zfill(3)
                                                        #offset=(counter-1)
                                                        offset=counter
                                                        
                                                        counter=0 # reset counter                        
                                                        print "offset "+str(offset)
                                                        
                                                        # Add 8 rasters together
                                                        print"Raster Addition Progressing ........."  
                                                        gp.Plus_sa(listArray[0],0,outraster[0])
                                                        print listArray[0]+" :Added with: "+"0"+" :Temp output: "+outraster[0]
                                                        print "Complete Step\t"+ str(0)                        
                                                        for i in range(1,offset):
                                                                                           
                                                                try:
                                                                        print"Continue Progressing ........."                                                                             
                                                                        gp.Plus_sa((listArray[i]),outraster[i-1],outraster[i])
                                                                        print listArray[i]+" :Added with: "+outraster[i-1]+" :Temp output: "+outraster[i]
                                                                        # print listArray[i]+ outraster[i-1]+ outraster[i]
                                                                        print "Complete Step\t"+ str(i)
                                                                except:
                                                                        print"Raster Addition Error"
                                                                        raise "exit"                                       
                                                           
                                                        # Calculate Average raster value
                                                        print "Calculating Average Raster "
                                                        gp.Divide_sa(outraster[i],offset,finalraster)

                                                        # Display Program Status in the IDLE Screen
                                                        print "output raster-->"+outraster[i]
                                                        print "final raster -->"+finalraster

                                                        # Reprojction ETo raster into AEA
                                                        ObjEtoReprojection=EtoProjection.EtoReprojection(finalraster,yearDay,self.year,self.datum,self.projection,self.sampleSize,self.finalPath,self.reprojectDir)
                                                        ObjEtoReprojection.Reproject()
                                                        
                                                        print "Deleting intermediate Rasters........"                                        

                                                        # Delete Intermediate rasters
                                                        gp.Delete_management(outraster[0], "Raster Dataset")
                                                        gp.Delete_management(outraster[1], "Raster Dataset")
                                                        gp.Delete_management(outraster[2], "Raster Dataset")
                                                        gp.Delete_management(outraster[3], "Raster Dataset")
                                                        gp.Delete_management(outraster[4], "Raster Dataset")
                                                        gp.Delete_management(outraster[5], "Raster Dataset")
                                                        gp.Delete_management(outraster[6], "Raster Dataset")
                                                        gp.Delete_management(outraster[7], "Raster Dataset")

                                                        print "Raster yearday:-: "+str(yearDay)+" completed!!."
                                                        print "\n"
                                                        print "\n"

                                                        # write to log
                                                        
                                                        self.WriteLog("etolog.txt",listArray[7][-6:])

                                                        # Empty list increment day and ready for next Cycle
                                                        yearDay=yearDay+offset

                                                        #          
                                                        self.WriteLog("yearday.txt",str(yearDay))
                                                        listArray=list()


                                                elif(yearDay>353):
                                                        overCounter=0
                                                        print"upto here----->1"
                                                        listArray=list()                                             
                                                        
                                                        finalraster=finalpath+"ETo"+str(self.year)+str(361).zfill(3)
                                                        
                                                        #Creating list to store temporary paths
                                                        outputraster=[(temppath1+str(0)),(temppath1+str(1)),(temppath1+str(2)),(temppath1+str(3)),(temppath1+str(4)),(temppath1+str(5)),(temppath1+str(6)),(temppath1+str(7))]
                                                        

                                                        while rs:
                                                                overArray.append(rs)
                                                                rs=rsList.Next()                
                                                                overCounter=overCounter+1
                                                        print "overArray"+str(overArray)
                                                        print"Raster Addition Progressing beyond "+str(353)
                                                        print "Total no. of files after 353:-: "+str(overCounter) 
                                                        gp.Plus_sa(overArray[0],0,outputraster[0])
                                                        print "Complete Step\t"+ str(0)
                                                        
                                                        for x in range(1,overCounter):
                                                                try:
                                                                        print"Continue Progressing ........."                                                                             
                                                                        gp.Plus_sa((overArray[x]),outputraster[x-1],outputraster[x]) ##########
                                                                        print overArray[x]+ outputraster[x-1]+ outputraster[x]
                                                                        print "Complete Step\t"+ str(x)
                                                                except:
                                                                        print gp.GetMessages()
                                                        # Calculate Average raster value
                                                        print "Calculating Average Raster "+str(overCounter)
                                                        gp.Divide_sa(outputraster[x],overCounter,finalraster) ########

                                                        # Display Program Status in the IDLE Screen
                                                        print "output raster-->"+outputraster[x]
                                                        print "final raster -->"+finalraster

                                                        # Reprojction ETo raster into AEA
                                                        ObjEtoReprojection=EtoProjection.EtoReprojection(finalraster,361)
                                                        ObjEtoReprojection.Reproject()

                                                        print "Deleting intermediate Rasters........"
                                                        self.WriteLog("yearday.txt","361")
                                                        self.WriteLog("etolog.txt","0")
                                                
                                                        # Delete Intermediate rasters
                                                        if(overCounter==1):
                                                                gp.Delete_management(outputraster[0], "Raster Dataset")
                                                        if(overCounter==2):
                                                                gp.Delete_management(outputraster[0], "Raster Dataset")
                                                                gp.Delete_management(outputraster[1], "Raster Dataset")                                                        
                                                        if(overCounter==3):
                                                                gp.Delete_management(outputraster[0], "Raster Dataset")
                                                                gp.Delete_management(outputraster[1], "Raster Dataset")
                                                                gp.Delete_management(outputraster[2], "Raster Dataset")
                                                        if(overCounter==4):
                                                                gp.Delete_management(outputraster[0], "Raster Dataset")
                                                                gp.Delete_management(outputraster[1], "Raster Dataset")
                                                                gp.Delete_management(outputraster[2], "Raster Dataset")
                                                                gp.Delete_management(outputraster[3], "Raster Dataset")
                                                        if(overCounter==5):
                                                                gp.Delete_management(outputraster[0], "Raster Dataset")
                                                                gp.Delete_management(outputraster[1], "Raster Dataset")
                                                                gp.Delete_management(outputraster[2], "Raster Dataset")
                                                                gp.Delete_management(outputraster[3], "Raster Dataset")
                                                                gp.Delete_management(outputraster[4], "Raster Dataset")
                                                        if(overCounter==6):
                                                                gp.Delete_management(outputraster[0], "Raster Dataset")
                                                                gp.Delete_management(outputraster[1], "Raster Dataset")
                                                                gp.Delete_management(outputraster[2], "Raster Dataset")
                                                                gp.Delete_management(outputraster[3], "Raster Dataset")
                                                                gp.Delete_management(outputraster[4], "Raster Dataset")
                                                                gp.Delete_management(outputraster[5], "Raster Dataset")
                                                        if(overCounter==7):
                                                                gp.Delete_management(outputraster[0], "Raster Dataset")
                                                                gp.Delete_management(outputraster[1], "Raster Dataset")
                                                                gp.Delete_management(outputraster[2], "Raster Dataset")
                                                                gp.Delete_management(outputraster[3], "Raster Dataset")
                                                                gp.Delete_management(outputraster[4], "Raster Dataset")
                                                                gp.Delete_management(outputraster[5], "Raster Dataset")
                                                                gp.Delete_management(outputraster[6], "Raster Dataset")
                                                        if(overCounter==8):
                                                                gp.Delete_management(outputraster[0], "Raster Dataset")
                                                                gp.Delete_management(outputraster[1], "Raster Dataset")
                                                                gp.Delete_management(outputraster[2], "Raster Dataset")
                                                                gp.Delete_management(outputraster[3], "Raster Dataset")
                                                                gp.Delete_management(outputraster[4], "Raster Dataset")
                                                                gp.Delete_management(outputraster[5], "Raster Dataset")
                                                                gp.Delete_management(outputraster[6], "Raster Dataset")
                                                                gp.Delete_management(outputraster[7], "Raster Dataset")                     

                                                        print"upto here------>2"
                                                        print"ETO composite finished !!!"
                                                else:
                                                        if(counter<8):
                                                                print "Wait for new rasters to make 8 days Composite...."
                                                        elif(counter==8):
                                                                print "Ready for rasters composite........."
                                                        
                                                        
                                                rs=rsList.Next()
                                               
                                                counter=counter+1
                                                                
                                        else:
                                               print "Error !!!........Counter > 8. "
                                else:
                                        print"Eto already computed...."
                                        rs=rsList.Next()
         

                except:
                        print gp.GetMessages()

##if __name__=="__main__":
##
##        #(temppath,finalpath,workspace,logpath):
##        ObjEtoComposite=EtoComposite("D:\\MODIS_ETa\\Output\\Temp\\","D:\\MODIS_ETa\\Output\\Temp1\\","D:\\MODIS_ETa\\Output\\Eto_composite\\","D:\\MODIS_ETa\\Data\\2008\\","D:\\MODIS_ETa\\Log\\")
##        ObjEtoComposite.EightDayComposite()
        
        #leap year's ko pachi dayofyear and raster again 0 garne.........ki ke??
                                

    
                   
                
                
