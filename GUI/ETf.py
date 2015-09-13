# DESC:This tool computes the Etf
# AUTHOR: Stefanie Bohms
# MODIFIED BY: Aashis Lamsal
# SUPERVISOR: Ting-Wu
# Advisor: Mike Wimberly

# Import system modules
import sys, string, os, arcgisscripting,csv,math,gc

class ComputeEtf:

        '''Constructor to assign state/path information'''
        def __init__(self,etfpath,tempath,csvtable,lstcpath,logpath,year):
                gc.enable()        
                self.etfPath=etfpath
                self.tempPath=tempath
                self.csvTable=csvtable
                self.lstcPath=lstcpath
                self.logPath=logpath
                self.year=year

        '''Read already projected files date from log'''
        def ReadLog(self):
                logFilerd=open(self.logPath+"etflog.txt",'r')
                logFilerd.seek(0)
                date=int(logFilerd.read())
                logFilerd.close()
                return date

        '''Write already project files date into log'''    
        def WriteLog(self,imagedate):
                logFilewrt=open(self.logPath+"etflog.txt",'w')
                logFilewrt.seek(0)
                logFilewrt.write(imagedate) 
                logFilewrt.close()

        ''' Engine to generate ETf '''
        def genETF(self,rsLSTC,ThotD,Thot_cold,day,TcoldD,Thot1,Tcold1):

                gp1 = arcgisscripting.create()

                # Assign Paht variables
                grid2 = self.tempPath+"grid2"
                etf = self.tempPath+"etf"
                finalEtf=self.etfPath
                inTrueRaster=0
                #print grid2
                print"\n"
                print "Extracted Variables: THOT1= "+str(Thot1)+ " & TCOLD1= "+str(Tcold1) +" (ONLY FOR TEST PURPOSE)"
                print "Raster Name:"+str(rsLSTC)
                print "Year of the Day:"+str(day)
                print "Average Cold Pixel Value:"+str(TcoldD)
                print "Average Hot Pixel Value:"+str(ThotD)
                print "Differnce between Hot and Cold Pixels:"+str(Thot_cold)

                # average hot pixel value - LSTc raster = raster grid2
                print "Process: Minus..."
                gp1.Minus_sa(ThotD,rsLSTC,grid2)

                # raster grid2 / (average hot pixel value-average cold pixel value) = ETfgrid
                print"Process: Divide..."
                gp1.Divide_sa(grid2, Thot_cold, etf)

                #set all values <0 to zero
                print "Process: Con..."
                gp1.Con_sa(etf, inTrueRaster,finalEtf+"etf"+str(self.year)+str(day).zfill(3),etf, "VALUE < 0")

                # deletes all intermediate rasters besides the output raster
                gp1.Delete_management(grid2, "Raster Dataset")
                gp1.Delete_management(etf, "Raster Dataset")  
                


        '''This function pasres the CSV and walk through the Directroy to find the updated raster for ETf computation'''        
        def EtfCalculation(self):
                                                          
                # Create the Geoprocessor object
                gp = arcgisscripting.create()

                # Set the necessary product code
                gp.SetProduct("ArcInfo")

                # Check out any necessary licenses
                gp.CheckOutExtension("spatial")

                #Overwriting the Output
                gp.OverwriteOutput = 1

                # Location for Hot and Cold pixel values
                inTable = self.csvTable

                # Define Workspace
                gp.Workspace=self.lstcPath

                # List lstc Rasters
                rsList=gp.ListRasters("*")
                rsLSTC=rsList.Next()

                # Computation on Hot and Cold pixel values to compute average
                Line = 0

                counter=0
                reader=csv.reader(open(inTable,"rb"))

                for row in reader:
                        # Check for Header Text
                        if(row[1]!="DAY"):
                                #Check for Updated files
                                if(int(self.ReadLog())<int(row[1])):
                                        # Check for Empty temp. Cell in CSV file
                                        if(row[2]==""):
                                                print "Empty Temperature(OR Raster not Existed) value"+"Day--->"+str(row[1])

                                        else:
                                                # Walk through the New raster to compute Etf
                                                while(int(rsLSTC[-3:])!=int(row[1].zfill(3))):
                                                        print"ETf already computed for :-: "+str(rsLSTC)
                                                        rsLSTC=rsList.Next()

                                                print"\n"
                                                print"New Raster for ETf:-: "+str(rsLSTC)
                                                print "rsLSTC"+str(int(rsLSTC[-3:]))
                                                print "log value:-: "+str(self.ReadLog())
                                                
                                                # New raster date match with csv year day       
                                                if(int(rsLSTC[-3:].zfill(3))==int(row[1].zfill(3))):
                                                                
                                                        Thot1 =str(row[2])  # Thot1 field in row
                                                        Thot2 =str(row[3])  # Thot2 field in row
                                                        Thot3 =str(row[4])  # Thot3 field in row                    
                                                        Thot = float(Thot1)+float(Thot2)+float(Thot3)  # summed up
                                                        ThotD = Thot/3                                 # average
                                                        
                                                        Tcold1 =str(row[5])  # Tcold1 field in row
                                                        Tcold2 =str(row[6])  # Tcold2 field in row
                                                        Tcold3 =str(row[7])  # Tcold3 field in row
                                                        Tcold = float(Tcold1) +float(Tcold2) +float(Tcold3) # summed up
                                                        TcoldD = Tcold/3 # average
                                                        day=row[1]

                                                        Thot_cold = ThotD - TcoldD 

                                                        # Function to compute ETF
                                                        self.genETF(rsLSTC,ThotD,Thot_cold,day,TcoldD,Thot1,Tcold1)

                                                        # Write State on Log file
                                                        self.WriteLog(str(day))
                                                        print "Successfully Completed: "+"etf"+str(self.year)+str(day).zfill(3)
                                                        print "\n"
 
                                else:
                                        print "Etf already Computed for day:-: "+str(row[1])
                                        print "\n"

                        else:
                                
                                print"Got Csv Header..."
                        

##if __name__=="__main__":
##        #def __init__(self,etfpath,tempath,csvtable,lstpath):
##        ObjComputeEtf=ComputeEtf("D:\\MODIS_ETa\\Output\\Etf\\2003\\","D:\\MODIS_ETa\\Output\\Temp\\","D:\\MODIS_ETa\\Data\\tables\\ETf_2003.csv","D:\\MODIS_ETa\\Data\\lstc\\2003\\lstc\\","D:\\MODIS_ETa\\Log\\",2003)
##        ObjComputeEtf.EtfCalculation()
           
        


        
    
    
