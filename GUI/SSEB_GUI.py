# Description: GUI for the EASTWEB project
# Author: Aashis Lamsal
# Supervisor: Ting-Wu
# Advisor: Mike Wimberly
# Project: EASTWEB

# import python inbuild modules
from Tkinter import *
import tkMessageBox
import gc

# import custom modules
import GetModisImage
import ModisConversion
import Modis_NDVI_Zonal
import ZonalStatistics
import trmmConversion
import trmmZonal
import xmlParser
import Eta
import EtaZnalStat
import ETf
import EtoComposite
import EtoProjection
import DbHandler


class EastWebGui:
    #global variable to hold tile information
    global studyArea
    global tileNo
    studyArea=str()
    gc.enable()
    
    def __init__(self,parent,configfile):

        # SSEB configuration file
        self.configurationFile=configfile
    
        # EASTWeb GUI Gadgets
        # Start GUI
        self.rootForm=Frame(parent)
        self.rootForm.pack()

        # Create Greeting Lable in GUI
        self.lblGreet=Label(self.rootForm,text="Welcome to the EASTWEB Project",font=("Arial",15,"bold"))
        self.lblGreet.grid(row=0,column=2,ipadx=50,sticky=E)

        # Tile Selection for image download
        self.lblTileSelect=Label(self.rootForm,text="Select tile:")
        self.lblTileSelect.grid(row=1,column=4,ipadx=10,sticky=E)

        # Default 'NGP' Selection
        self.var1=StringVar()
        self.var1.set("Select")
        self.optionMenu=OptionMenu(self.rootForm,self.var1,"Select","NGP","ETH","Custom",command= self.SelectTiles)
        self.optionMenu.grid(row=1,column=5)

        # Custom tile lable and entry widget
##        self.lblCustomTile=Label(self.rootForm,text="Tile No:")
##        self.lblCustomTile.grid(row=2,column=4)
##        self.entryTile=Entry(self.rootForm)
##        self.entryTile.grid(row=2,column=5)


        # LST and NDVI Gadgets
        # Create RadioButton to choose the MODEL 
        self.radioVal=IntVar()
        self.radio=Radiobutton(self.rootForm,text="LST & NDVI",value=0,variable=self.radioVal,command= self.RadioSelect)
        self.radio.grid(row=5,column=2,sticky=W)


        # Radios to chosse MOD11A2 or MCD43B4
        self.radModisVal = IntVar()
        self.radioModis1=Radiobutton(self.rootForm,text="MOD11A2",value=1,variable=self.radModisVal,command= self.ModisSelect)
        self.radioModis1.grid(row=7,column=2)

        self.radioModis2=Radiobutton(self.rootForm,text="MCD43B4",value=2,variable=self.radModisVal,command= self.ModisSelect)
        self.radioModis2.grid(row=8,column=2)

        # LST and NDVI Event Handling Buttons
        self.btnGetImageLst=Button(self.rootForm,text="GetImage",command= self.GetModisLst)
        self.btnGetImageLst.grid(row=10,column=2,ipadx=10,sticky=NE)

        self.btnReprojLst=Button(self.rootForm,text="Reprojection",command= self.ReprojectModisLst)
        self.btnReprojLst.grid(row=10,column=3,sticky=E,ipadx=1,padx=15)

        self.btnZonalStatLst=Button(self.rootForm,text="ZonalStatistics",command= self.ZonalstatLst)
        self.btnZonalStatLst.grid(row=10,column=4,sticky=E,ipadx=1,padx=15)

        self.btnTrnasposeLst=Button(self.rootForm,text="Transpose",command= self.TransposeLst)
        self.btnTrnasposeLst.grid(row=10,column=5,sticky=E,ipadx=1,padx=15)

        # TRMM Gadgets
        # Create RadioButton to choose the MODEL

        self.radio=Radiobutton(self.rootForm,text="TRMM",value=1,variable=self.radioVal,command= self.RadioSelect)
        self.radio.grid(row=11,column=2,sticky=W)

        # TRMM Event Handling Buttons
        self.btnGetImageTrmm=Button(self.rootForm,text="GetImage",command= self.TrmmGetImage)
        self.btnGetImageTrmm.grid(row=12,column=2,ipadx=10,sticky=NE)

        self.btnConversionTrmm=Button(self.rootForm,text="Conversion",command= self.TrmmReproject)
        self.btnConversionTrmm.grid(row=12,column=3,sticky=E,ipadx=5,padx=15)

        self.btnZonalStatTrmm=Button(self.rootForm,text="ZonalStatistics",command= self.TrmmZonalstat)
        self.btnZonalStatTrmm.grid(row=12,column=4,sticky=E,ipadx=1,padx=15)

        self.btnTrnasposeTrmm=Button(self.rootForm,text="Transpose",command= self.TrmmTranspose)
        self.btnTrnasposeTrmm.grid(row=12,column=5,sticky=E,ipadx=1,padx=15)

        # ETa and ETo Gadgets
        # Create RadioButton to choose the MODEL

        self.radio=Radiobutton(self.rootForm,text="ETA",value=2,variable=self.radioVal,command= self.RadioSelect)
        self.radio.grid(row=14,column=2,sticky=W)

##        self.btnEtoReproject=Button(self.rootForm,text="GenLstc",command= self.GenLstc)
##        self.btnEtoReproject.grid(row=16,column=2,sticky=E,ipadx=7,padx=0)

        self.btnEtoComposite=Button(self.rootForm,text="EToComposite",command= self.EtoComposite)
        self.btnEtoComposite.grid(row=16,column=3,sticky=E,ipadx=7,padx=0)

        self.btnCalcEtf=Button(self.rootForm,text="ETf",command= self.CalcEtf)
        self.btnCalcEtf.grid(row=16,column=2,sticky=E,ipadx=7,padx=0)

        self.btnCalcEta=Button(self.rootForm,text="ETa",command= self.CalcEta)
        self.btnCalcEta.grid(row=18,column=3,sticky=E,ipadx=7,padx=0)

        self.btnEtaZnalStat=Button(self.rootForm,text="ETaZnal",command= self.EtaZnalStat)
        self.btnEtaZnalStat.grid(row=18,column=4,sticky=E,ipadx=7,padx=0)

        self.btnEtaTranspose=Button(self.rootForm,text="ETaTranspose",command= self.EtaTranspose)
        self.btnEtaTranspose.grid(row=18,column=5,sticky=E,ipadx=7,padx=0)

        # Initially Load Wigets with corresponding visisbility state
        self.btnGetImageLst.config(state=NORMAL)
        self.btnReprojLst.config(state=NORMAL)
        self.btnZonalStatLst.config(state=NORMAL)
        self.btnTrnasposeLst.config(state=NORMAL)
        self.btnGetImageTrmm.config(state=DISABLED)
        self.btnConversionTrmm.config(state=DISABLED)
        self.btnZonalStatTrmm.config(state=DISABLED)
        self.btnTrnasposeTrmm.config(state=DISABLED)
##        self.btnEtoReproject.config(state=DISABLED)
        self.btnEtoComposite.config(state=DISABLED)
        self.btnCalcEtf.config(state=DISABLED)
        self.btnCalcEta.config(state=DISABLED)
        self.btnEtaZnalStat.config(state=DISABLED)
        self.btnEtaTranspose.config(state=DISABLED)

        self.radioModis1.config(state=NORMAL)
        self.radioModis2.config(state=NORMAL)

##        self.lblCustomTile.config(state=DISABLED)
##        self.entryTile.config(state=DISABLED)

        #Create Label to Dispaly
        #self.lblRadioDisplay=Label(rootForm)
        #self.lblRadioDisplay.grid(row=15,column=2)

       

    '''Select the tiles to be downloaded'''
    def SelectTiles(self,value,args=None):
        #Prints the value of selected study area.
        global studyArea
        if(value=="ETH"):            
            studyArea="ETH"        
        if(value=="NGP"):            
            studyArea="NGP"
        if(value=="Custom"):
            studyArea="CUSTOM"
        if(value=="Select"):
            self.tileInfo=str()
            print "Please choose the appropriate Tile"

    '''Return the Tile information to be downloaded'''
    def getTileInfo(self):
        global tileInfo
        if(self.entryTile.get()!=""):
            tileInfo=self.entryTile.get()
        return tileInfo
        
##    '''Clear the Contents from the Entry Box'''
##    def EmptyEntryBox(self):
##        self.entryTile.delete(0,END)
        

    '''Returns the total no. of tiles that should be mosaic'''
    def GetTileNo(self):
        global tileNo
        if (len(self.getTileInfo())>0):
            tileNo=int(len(self.getTileInfo().split(",")))
            if(self.entryTile.get()!=""):
                tileNo=self.entryTile.get()
            #print "tileno"+str(tileNo)
            return tileNo
        else:
            print "Select the no. of tiles to be mosaic and reprojected "

    ''' Select the states of LST n NDVI, TRMM, and ETA'''
    def RadioSelect(self):
        radSelect="You Choose"+str(self.radioVal.get())
        #self.lblRadioDisplay.config(text=radSelect)
        # Check for LST & NDVI stuffs
        if (self.radioVal.get()==0):

            self.btnGetImageLst.config(state=NORMAL)
            self.btnReprojLst.config(state=NORMAL)
            self.btnZonalStatLst.config(state=NORMAL)
            self.btnTrnasposeLst.config(state=NORMAL)
            self.radioModis1.config(state=NORMAL)
            self.radioModis2.config(state=NORMAL)
            self.btnGetImageTrmm.config(state=DISABLED)
            self.btnConversionTrmm.config(state=DISABLED)
            self.btnZonalStatTrmm.config(state=DISABLED)
            self.btnTrnasposeTrmm.config(state=DISABLED)
##            self.btnEtoReproject.config(state=DISABLED)
            self.btnEtoComposite.config(state=DISABLED)
            self.btnCalcEtf.config(state=DISABLED)
            self.btnCalcEta.config(state=DISABLED)
            self.btnEtaZnalStat.config(state=DISABLED)
            self.btnEtaTranspose.config(state=DISABLED)
            
        #Check for TRMM stuffs 
        if (self.radioVal.get()==1):

            self.btnGetImageTrmm.config(state=NORMAL)
            self.btnConversionTrmm.config(state=NORMAL)
            self.btnZonalStatTrmm.config(state=NORMAL)
            self.btnTrnasposeTrmm.config(state=NORMAL)
            self.btnGetImageLst.config(state=DISABLED)
            self.btnReprojLst.config(state=DISABLED)
            self.btnZonalStatLst.config(state=DISABLED)
            self.btnTrnasposeLst.config(state=DISABLED)
##            self.btnEtoReproject.config(state=DISABLED)
            self.btnEtoComposite.config(state=DISABLED)
            self.btnCalcEtf.config(state=DISABLED)
            self.btnCalcEta.config(state=DISABLED)
            self.btnEtaZnalStat.config(state=DISABLED)
            self.btnEtaTranspose.config(state=DISABLED)
            self.radioModis1.config(state=DISABLED)
            self.radioModis2.config(state=DISABLED)


        #Check for ETA stuffs
        if (self.radioVal.get()==2):

##            self.btnEtoReproject.config(state=NORMAL)
            self.btnEtoComposite.config(state=NORMAL)
            self.btnCalcEtf.config(state=NORMAL)
            self.btnCalcEta.config(state=NORMAL)
            self.btnEtaZnalStat.config(state=NORMAL)
            self.btnEtaTranspose.config(state=NORMAL)
            self.btnGetImageLst.config(state=DISABLED)
            self.btnReprojLst.config(state=DISABLED)
            self.btnZonalStatLst.config(state=DISABLED)
            self.btnTrnasposeLst.config(state=DISABLED)
            self.btnGetImageTrmm.config(state=DISABLED)
            self.btnConversionTrmm.config(state=DISABLED)
            self.btnZonalStatTrmm.config(state=DISABLED)
            self.btnTrnasposeTrmm.config(state=DISABLED)
            self.radioModis1.config(state=DISABLED)
            self.radioModis2.config(state=DISABLED)
            
    # Processing LST & NDVI Images

    '''Get Modis Image'''
    def GetModisLst(self):
        getModDict={}
        modVal=self.ModisCheck()
        if(studyArea):            
            if(modVal==1):            
                print str(modVal)
                objParseXml=xmlParser.ParseXml("area","type",studyArea,"lst",self.configurationFile)
                getModDict=objParseXml.ParseLstNdvi()
                #print getModDict["id"]
                try:
                    '''parameters(hostName,userName,passWord,hdfpath,logpath,ftpdir,tileInfo)'''
                    gtmdObj=GetModisImage.GetModis(getModDict["hostname"],getModDict["username"],getModDict["password"],getModDict["hdfdir"],getModDict["logdir"],getModDict["ftpdir"],getModDict["id"])
                    gtmdObj.RetriveData()
                    
                except Exception, e:
                    print "Error !!. Couldn't connect to the server:-: "+str(e)

##                '''parameters(hostName,userName,passWord,hdfpath,logpath,ftpdir,tileInfo)'''
##                gtmdObj=GetModisImage.GetModis("e4ftl01u.ecs.nasa.gov","anonymous","@anonymous","D:\\MODIS_LST_NDVI\\MOD11A2\\","D:\\MODIS_LST_NDVI\\Log\\","MOLT/MOD11A2.005",self.getTileInfo())
##                #gtmdObj=GetModisImage.GetModis("e4ftl01u.ecs.nasa.gov","anonymous","@anonymous","D:\\MODIS_LST_NDVI\\MOD11A2\\","D:\\MODIS_LST_NDVI\\Log\\","MOLT/MOD11A2.005")
##                gtmdObj.RetriveData()

            elif(modVal==2):                                      
                print str(modVal)
                objParseXml=xmlParser.ParseXml("area","type",studyArea,"ndvi",self.configurationFile)
                getModDict=objParseXml.ParseLstNdvi()
                try:
                    '''parameters(hostName,userName,passWord,hdfpath,logpath,ftpdir,tileInfo)'''
                    gtmdObj1=GetModisImage.GetModis(getModDict["hostname"],getModDict["username"],getModDict["password"],getModDict["hdfdir"],getModDict["logdir"],getModDict["ftpdir"],getModDict["id"])
                    gtmdObj1.RetriveData()
                    
                except Exception, e:
                     print "Error !!. Couldn't connect to the server:-: "+str(e)
            else:
                print "Throw Error.."

##                    '''parameters(hostName,userName,passWord,hdfpath,logpath,ftpdir,tileInfo)'''
##                    gtmdObj= GetModisImage.GetModis("e4ftl01u.ecs.nasa.gov","anonymous","@anonymous","D:\\MODIS_LST_NDVI\\MCD43B4\\","D:\\MODIS_LST_NDVI\\MCD43B4_Log\\","MOTA/MCD43B4.005",self.getTileInfo())
##                    gtmdObj.RetriveData()

        else:
            print"Error!!. Select Appropriate Study Area...."


    '''Re Project Modis Image'''    
    def ReprojectModisLst(self):
        reProjetDitc={}    
        modVal=self.ModisCheck()
        if(studyArea):
            print studyArea
            if(modVal==1):
                print str(modVal)
                objParseXml=xmlParser.ParseXml("area","type",studyArea,"lst",self.configurationFile)
                reProjetDitc=objParseXml.ParseLstNdvi()
                print reProjetDitc
                try:
                    mdcovrObj=ModisConversion.ReprojectModis(reProjetDitc["hdfdir"],reProjetDitc["tiffdir"],reProjetDitc["logdir"],int(reProjetDitc["mosaictilenum"]),reProjetDitc["prjfile"])
                    mdcovrObj.ConvertTiff()
                except Exception, e:
                    print "Error !!. Couldn't reproject the MODIS LST:-: "+str(e)

##                    '''parameters(hdfpath,tiffpath,logpath,no_of_tiles_tobe_mosaic)'''
##                    mdcovrObj=ModisConversion.ReprojectModis("D:\\MODIS_LST_NDVI\\MOD11A2\\","D:\\MODIS_LST_NDVI\\MOD11A2_Tiff\\","D:\\MODIS_LST_NDVI\\Log\\",self.GetTileNo())
##                    mdcovrObj.ConvertTiff()

            elif(modVal==2):
                print str(modVal)
                objParseXml=xmlParser.ParseXml("area","type",studyArea,"ndvi",self.configurationFile)
                reProjetDitc=objParseXml.ParseLstNdvi()
                try:
                    mdcovrObj=ModisConversion.ReprojectModis(reProjetDitc["hdfdir"],reProjetDitc["tiffdir"],reProjetDitc["logdir"],int(reProjetDitc["mosaictilenum"]),reProjetDitc["prjfile"])
                    mdcovrObj.ConvertTiff()                    
                except Exception, e:
                    print "Error !!. Couldn't reproject the MODIS LST image "+str(e)

##                    '''parameters(hdfpath,tiffpath,logpath,no_of_tiles_tobe_mosaic)'''
##                    mdcovrObj=ModisConversion_NDVI.ReprojectModisNdvi("D:\\MODIS_LST_NDVI\\MCD43B4\\","D:\\MODIS_LST_NDVI\\MCD43B4_Tiff\\","D:\\MODIS_LST_NDVI\\MCD43B4_Log\\",self.GetTileNo())
##                    mdcovrObj.ConvertTiffNdvi()

            else:
                print"Throw Error.."
                
        else:
            print"Error!!. Select Appropriate Study Area...."

    '''Compute Zonal Stat from Modis Image'''   
    def ZonalstatLst(self):
        zonalStatDict={}
        modVal=self.ModisCheck()
        if(studyArea):
            print studyArea
            if(modVal==1):
                print str(modVal)
                zonalStatDict={}
                lstDB={}
                objParseXml=xmlParser.ParseXml("area","type",studyArea,"lst",self.configurationFile)
                zonalStatDict=objParseXml.ParseLstNdvi()
                lstDB=objParseXml.ParseDB()
                try:
                    mdznalObj=ZonalStatistics.ZonalStat(zonalStatDict["tiffdir"],zonalStatDict["tempdir"],zonalStatDict["shpfile"],zonalStatDict["watermask"],zonalStatDict["zonalcsv"],zonalStatDict["logdir"],zonalStatDict["griddir"],lstDB["dbhost"],lstDB["dbname"],lstDB["dbuser"],lstDB["dbpassword"],zonalStatDict["inquery"])
                    mdznalObj.ComputeZstat()
                except Exception, e:
                    print "Error !!. Couldn't compute the Zonal statistics:-: "+str(e)
                  
##                '''parameters(tiffpath,temppath,zonalpath,landmask,outputcsv,logpath)'''
##                mdznalObj=ZonalStatistics.ZonalStat("D:\\MODIS_LST_NDVI\\MOD11A2_Tiff\\","D:\\MODIS_LST_NDVI\\Tempoo","D:\\MODIS_LST_NDVI\\NGP_AEA\\","D:\\MODIS_LST_NDVI\\WaterMask\\rec_watermask","D:\\MODIS_LST_NDVI\\MOD11A2_Znal\\mod11a2_znal.csv","D:\MODIS_LST_NDVI\Log\\")
##                mdznalObj.ComputeZstat()

            elif(modVal==2):
                print str(modVal)
                zonalStatDict={}
                ndviDB={}
                objParseXml=xmlParser.ParseXml("area","type",studyArea,"ndvi",self.configurationFile)
                zonalStatDict=objParseXml.ParseLstNdvi()
                ndviDB=objParseXml.ParseDB()
                try:
                    mdznalObj=Modis_NDVI_Zonal.ZonalStatNdvi(zonalStatDict["tiffdir"],zonalStatDict["tempdir"],zonalStatDict["shpfile"],zonalStatDict["watermask"],zonalStatDict["zonalcsv"],zonalStatDict["logdir"],zonalStatDict["griddir"],ndviDB["dbhost"],ndviDB["dbname"],ndviDB["dbuser"],ndviDB["dbpassword"],zonalStatDict["inquery"])
                    mdznalObj.ZonalNdvi()
                except Exception, e:
                    print "Error !!. Couldn't compute the Zonal statistics:-: "+str(e)
                    
##                '''parameters(tiffpath,temppath,zonalpath,landmask,outputcsv,logpath)'''
##                mdznalObj=ZonalStatistics.ZonalStat("D:\\MODIS_LST_NDVI\\MCD43B4_Tiff\\","D:\\MODIS_LST_NDVI\\MCD_Tempoo","D:\\MODIS_LST_NDVI\\NGP_AEA\\","D:\\MODIS_LST_NDVI\\WaterMask\\rec_watermask","D:\\MODIS_LST_NDVI\\MCD43B4_Znal\\mcd_znal.csv","D:\\MODIS_LST_NDVI\\MCD43B4_Log\\")
##                mdznalObj.ComputeZstat()

            else:
                print"Throw Error.."
        else:
            print"Error!!. Select Appropriate Study Area...."

    '''Compute Transpose from Zonal stat'''   
    def TransposeLst(self):
        lstTransposeDict={}
        modVal=self.ModisCheck()
        if(studyArea):
            print studyArea
            if(modVal==1):
                print str(modVal)
                lstDict={}
                lstDB={}
                objParseXml=xmlParser.ParseXml("area","type",studyArea,"lst",self.configurationFile)
                lstDict=objParseXml.ParseLstNdvi()
                lstDB=objParseXml.ParseDB()
                try:
                    ObjRpyDbHandler=DbHandler.RpyDbHandler(lstDB["dbuser"],lstDB["dbpassword"],lstDB["dbname"],lstDB["dbhost"])
                    ObjRpyDbHandler.Transpose(lstDict["outquery"],lstDict["transposedoutput"])                   
                except Exception,e:
                    print "Error !!. Couldn't Transpose the Zonal Stat:-:"+str(e)
                
##                '''parameters(zonalcsv,intermediatecsv,finalcsv)'''
##                ##datatransObj=Transpose.DataTranspose(r"D:\MODIS_LST_NDVI\MOD11A2_Znal\mod11a2_znal.csv",r"D:\MODIS_LST_NDVI\MOD11A2_Znal\intermediate.csv",r"D:\MODIS_LST_NDVI\MOD11A2_Znal\final.csv")
##                ##datatransObj.ExecuteTranspose()
            elif(modVal==2):
                print str(modVal)
                ndviDict={}
                ndviDB={}
                objParseXml=xmlParser.ParseXml("area","type",studyArea,"ndvi",self.configurationFile)
                ndviDict=objParseXml.ParseLstNdvi()
                ndviDB=objParseXml.ParseDB()
                try:
                    ObjRpyDbHandler=DbHandler.RpyDbHandler(ndviDB["dbuser"],ndviDB["dbpassword"],ndviDB["dbname"],ndviDB["dbhost"])
                    ObjRpyDbHandler.Transpose(ndviDict["outquery"],ndviDict["transposedoutput"])                    
                except Exception,e:
                    print"Error !!. Couldn't Transpose the Zonal Stat:-:"+str(e)
                    
##                '''parameters(zonalcsv,intermediatecsv,finalcsv)'''
##                datatransObj=Transpose.DataTranspose(r"D:\\MODIS_LST_NDVI\\MCD43B4_Znal\\mcd_znal.csv",r"D:\MODIS_LST_NDVI\MCD43B4_Znal\intermediate.csv",r"D:\MODIS_LST_NDVI\MCD43B4_Znal\final.csv")
##                datatransObj.ExecuteTranspose()
            else:
                print"Throw Error.."
        else:
            print"Error!!. Select Appropriate Study Area....!!"

    # Selecting MOD11A2 and MCD43B4 Radio 
    def ModisSelect(self):
        self.ModisCheck()    

    # Checking Radio, whether it is selected or not.    
    def ModisCheck(self):
        if( self.radModisVal.get()==1):
            print "MOD11A2 Selected"
            return  self.radModisVal.get()
        elif( self.radModisVal.get()==2):
            print "MCD43B4 Selected"
            return  self.radModisVal.get()
        else:
            tkMessageBox.showerror(title="Error",message="Select MOD11A2 or MCD43B4")
            return 0


    # Processing TRMM Images

    '''Get Rainfall data automatically'''
    def TrmmGetImage(self):
        # self.ModisCheck()
        print "Need to Automate the system to convert *.bin TRMM to NetCDF or ESRI' Grid"

    '''Reproject Rainfall data from Net CDF to grid'''
    def TrmmReproject(self):
        trmmReDict={}
        objParseXml=xmlParser.ParseXml("area","type",studyArea,"lst",self.configurationFile)
        trmmReDict=objParseXml.ParseTrmm()
        try:
            '''parameters(cdfpath,gridpath,logpath)'''
            gridconObj=trmmConversion.CdftoGrid(trmmReDict["netcdfdir"],trmmReDict["griddir"],trmmReDict["logdir"])
            gridconObj.ConvertoGrid()        
##        gridconObj=trmmConversion.CdftoGrid(r"D:\MODIS_TRMM\NetCDFile",r"D:\MODIS_TRMM\GridFile",r"D:\MODIS_TRMM\Logs")
##        gridconObj.ConvertoGrid()
        except Exception,e:
            print"Could not reproject TRMM data :-:"+str(e)


    '''Compute Zonal Stat from GRID files'''
    def TrmmZonalstat(self):
        trmmZnDict={}
        trmmDB={}
        objParseXml=xmlParser.ParseXml("area","type",studyArea,"lst",self.configurationFile)
        trmmZnDict=objParseXml.ParseTrmm()
        trmmDB=objParseXml.ParseDB()
        try:                        
            '''parameters(gridpath,znlpath,shppath,outcsvpath,trmmlog,dbhost,dbname,dbuser,dbpassword,inquery)'''
            znalstatObj=trmmZonal.TrmmZonalStat( trmmZnDict["griddir"],trmmZnDict["workspace"],trmmZnDict["shpfile"],trmmZnDict["zonalcsv"],trmmZnDict["logdir"],trmmDB["dbhost"],trmmDB["dbname"],trmmDB["dbuser"],trmmDB["dbpassword"],trmmZnDict["inquery"])
            znalstatObj.ComputeZonal()
##        znalstatObj=trmmZonal.TrmmZonalStat( r"D:\MODIS_TRMM\GridFile",r"D:\MODIS_TRMM",r"D:\MODIS_TRMM\ecoregions\NGP_AEA.shp",r"D:\MODIS_TRMM\TRMM_summary.csv",r"D:\MODIS_TRMM\Logs")
##        znalstatObj.ComputeZonal()
        except Exception,e:
            print"Could not compute Zonal Stat :-:"+str(e)


    '''Transpose Zonal STAT'''
    def TrmmTranspose(self):
        trmmTrDict={}
        trmmTrDB={}
        objParseXml=xmlParser.ParseXml("area","type",studyArea,"lst",self.configurationFile)
        trmmTrDict=objParseXml.ParseTrmm()
        trmmTrDB=objParseXml.ParseDB()
        try:                        
            '''parameters(trmmsmrypath,trmmintermdtpath,trmmfinalpath)'''
            ObjRpyDbHandler=DbHandler.RpyDbHandler(trmmTrDB["dbuser"],trmmTrDB["dbpassword"],trmmTrDB["dbname"],trmmTrDB["dbhost"])
            ObjRpyDbHandler.Transpose(trmmTrDict["outquery"],trmmTrDict["transposedoutput"])

##            trmmtransObj=trmmTranspose.TrmmTranspose(trmmTrDict["zonalcsv"],trmmTrDict["intermediatecsv"],trmmTrDict["finalcsv"])
##            trmmtransObj.ExecuteTranspose()
            
##        trmmtransObj=trmmTranspose.TrmmTranspose(r"D:\MODIS_TRMM\TRMM_summary.csv",r"D:\MODIS_TRMM\TRMM_Intermediate.csv",r"D:\MODIS_TRMM\TRMM_Final.csv")
##        trmmtransObj.ExecuteTranspose()
        except Exception,e:
            print"Could not transpose TRMM data :-:"+str(e)

#########################################################################################################################
    # parent-child box code  block  

    def ZonalTop(self):
        #global znalEntry
        print (self.znalEntry.get())
        
    def tlevel(self):
        global znalEntry
        self.top = Toplevel()
        self.top.title("Zonal Satistics")
        self.znalEntry=Entry(top)
        self.znalEntry.pack()
        self.msg =self.Message(top, text="Enter Zonal variables")
        self.msg.pack()
        
        self.button1 = Button(top, text="Dismiss",command=top.destroy)
        self.button1.pack()
        self.button2=Button(top,text="Done",command=ZonalTop)
        self.button2.pack()

#########################################################################################################################

    # Processing ETa and ETo    

##    def EtaSummary(self):
##        print "EtaSummary"
##        
##    def GenLstc(self):
##        print "Generate LSTC is temporarily not working............"   
        
    def EtoComposite(self):
        print "EtoComposite"

        etoDict={}
        objParseXml=xmlParser.ParseXml("area","type",studyArea,"lst",self.configurationFile)
        etoDict=objParseXml.ParseEto()
        print etoDict
        ObjEtoComposite=EtoComposite.EtoComposite(etoDict["tempdir1"],etoDict["tempdir2"],etoDict["compositedir"],etoDict["dailyetodir"],etoDict["logdir"],etoDict["year"],etoDict["datum"],etoDict["projection"],etoDict["samplesize"],etoDict["reprojectdir"])
        ObjEtoComposite.EightDayComposite()
        
##        ObjEtoComposite=EtoComposite.EtoComposite("D:\\MODIS_ETa\\Output\\Temp\\","D:\\MODIS_ETa\\Output\\Temp1\\","D:\\MODIS_ETa\\Output\\Eto_composite\\","D:\\MODIS_ETa\\Data\\2008\\","D:\\MODIS_ETa\\Log\\")
##        ObjEtoComposite.EightDayComposite()

    def CalcEtf(self):
##        print "CalcEtf"

        etfDict={}
        objParseXml=xmlParser.ParseXml("area","type",studyArea,"lst",self.configurationFile)
        etfDict=objParseXml.ParseEtf()
##        print etfDict

        ObjComputeEtf=ETf.ComputeEtf(etfDict["etfdir"],etfDict["tempdir"],etfDict["csvtable"],etfDict["lstcdir"],etfDict["logdir"],etfDict["year"])
        ObjComputeEtf.EtfCalculation()
        

##        ObjComputeEtf=ETf.ComputeEtf("D:\\MODIS_ETa\\Output\\Etf\\2003\\","D:\\MODIS_ETa\\Output\\Temp\\","D:\\MODIS_ETa\\Data\\tables\\ETf_2003.csv","D:\\MODIS_ETa\\Data\\lstc\\2003\\lstc\\","D:\\MODIS_ETa\\Log\\",2003)
##        ObjComputeEtf.EtfCalculation()

    def CalcEta(self):        
        print "CalcEta"

        etaDict={}
        objParseXml=xmlParser.ParseXml("area","type",studyArea,"lst",self.configurationFile)
        etaDict=objParseXml.ParseEta()
##        print etaDict
        
        ObjComputeEta=Eta.ComputeEta(etaDict["etorepjctdir"],etaDict["etfdir"],etaDict["etadir"],etaDict["logdir"])
        ObjComputeEta.EtaCalculation()
        
##        ObjComputeEta=Eta.ComputeEta("D:\\MODIS_ETa\\Data\\Eto_reproject\\","D:\\MODIS_ETa\\Output\\Etf\\2000\\","D:\\MODIS_ETa\\Output\\Eta\\","D:\\MODIS_ETa\\Log\\")
##        ObjComputeEta.EtaCalculation()
        
    def EtaZnalStat(self):
        print "EtaZnalStat"
       
        etaznalDict={}
        etaDB={}
        objParseXml=xmlParser.ParseXml("area","type",studyArea,"lst",self.configurationFile)
        etaznalDict=objParseXml.ParseEta()
        etaDB=objParseXml.ParseDB()
        print etaznalDict

        ObjEtaZnal=EtaZnalStat.EtaZnal(etaznalDict["etadir"],etaznalDict["shpfile"],etaznalDict["tempdir"],etaznalDict["logdir"],etaDB["dbhost"],etaDB["dbname"],etaDB["dbuser"],etaDB["dbpassword"],etaznalDict["inquery"])
        ObjEtaZnal.ComputeZnalStat()
        
##        ObjEtaZnal=EtaZnal("D:\\MODIS_ETa\\Data\\Eta\\","D:\\MODIS_LST_NDVI\\NGP_AEA\\NGP_AEA.shp","D:\\MODIS_ETa\\Output\\Temp\\","D:\\MODIS_ETa\\Log\\","localhost","db_EastWeb","postgres","eastweb1")
##        ObjEtaZnal.ComputeZnalStat()

    def EtaTranspose(self):
        etaTrnsDict={}
        etaTransDB={}
        objParseXml=xmlParser.ParseXml("area","type",studyArea,"lst",self.configurationFile)
        etaTrnsDict=objParseXml.ParseEta()
        etaTransDB=objParseXml.ParseDB()
        
        ObjRpyDbHandler=DbHandler.RpyDbHandler(etaTransDB["dbuser"],etaTransDB["dbpassword"],etaTransDB["dbname"],etaTransDB["dbhost"])
        ObjRpyDbHandler.Transpose(etaTrnsDict["outquery"],etaTrnsDict["transposedoutput"])

def main():
   root=Tk()  
   EastWebGui(root,"config.xml")
   root.title("EASTWEB Project")
   root.mainloop() 

if __name__=="__main__":
    main()








        
    


