import xml.dom.minidom
from xml.dom.minidom import Node
import gc

class ParseXml:

    '''Initialize the path variables'''
    def __init__(self,areatag,typetag,studyarea,studytype,filename):
        gc.enable()
        self.areaElement=areatag
        self.typeElement=typetag
        self.fileName=filename
        self.studyArea=studyarea
        self.studyType=studytype
        #self.xmlDoc= xml.dom.minidom.parse("config.xml")
        self.configDoc= xml.dom.minidom.parse(self.fileName)
        

    '''Retrive LSTNDVI configurations''' 
    def ParseLstNdvi(self):
        lstNdviDict={}
        for node in self.configDoc.getElementsByTagName(self.areaElement):
            areaName=node.getAttribute("name")
            print areaName
            if areaName==self.studyArea:            
                for lstndvi in node.getElementsByTagName(self.typeElement):
                    typeName=lstndvi.getAttribute("name")
                    if typeName==self.studyType:
                        
##                      for node2 in node1.getElementsByTagName("hostname"):
##                      print node2.childNodes[0].nodeValue

                        self.id= lstndvi.getElementsByTagName("id")[0].childNodes[0].nodeValue
                        self.hostname= lstndvi.getElementsByTagName("hostname")[0].childNodes[0].nodeValue
                        self.username=lstndvi.getElementsByTagName("username")[0].childNodes[0].nodeValue
                        self.password=lstndvi.getElementsByTagName("password")[0].childNodes[0].nodeValue
                        self.ftpdir= lstndvi.getElementsByTagName("ftpdir")[0].childNodes[0].nodeValue
                        self.hdfdir= lstndvi.getElementsByTagName("hdfdir")[0].childNodes[0].nodeValue
                        self.tiffdir= lstndvi.getElementsByTagName("tiffdir")[0].childNodes[0].nodeValue
                        self.lstgriddir=lstndvi.getElementsByTagName("griddir")[0].childNodes[0].nodeValue
                        self.tempdir= lstndvi.getElementsByTagName("tempdir")[0].childNodes[0].nodeValue
                        self.logdir= lstndvi.getElementsByTagName("logdir")[0].childNodes[0].nodeValue
                        self.mosaictilenum= lstndvi.getElementsByTagName("mosaictilenum")[0].childNodes[0].nodeValue
                        self.shpfile= lstndvi.getElementsByTagName("shpfile")[0].childNodes[0].nodeValue
                        self.watermask= lstndvi.getElementsByTagName("watermask")[0].childNodes[0].nodeValue
                        self.zonalcsv= lstndvi.getElementsByTagName("zonalcsv")[0].childNodes[0].nodeValue
                        self.intermediatecsv= lstndvi.getElementsByTagName("intermediatecsv")[0].childNodes[0].nodeValue
                        self.finalcsv= lstndvi.getElementsByTagName("finalcsv")[0].childNodes[0].nodeValue
                        self.prjfile=lstndvi.getElementsByTagName("prjfile")[0].childNodes[0].nodeValue
                        self.inquery=lstndvi.getElementsByTagName("inquery")[0].childNodes[0].nodeValue
                        self.outquery=lstndvi.getElementsByTagName("outquery")[0].childNodes[0].nodeValue
                        self.transposedoutput=lstndvi.getElementsByTagName("transposedoutput")[0].childNodes[0].nodeValue


                        # Dict to hold lstNdvi config variables
                        lstNdviDict["id"]=self.id
                        lstNdviDict["hostname"]=self.hostname
                        lstNdviDict["username"]=self.username
                        lstNdviDict["password"]=self.password
                        lstNdviDict["ftpdir"]=self.ftpdir
                        lstNdviDict["hdfdir"]=self.hdfdir
                        lstNdviDict["tiffdir"]=self.tiffdir
                        lstNdviDict["griddir"]=self.lstgriddir
                        lstNdviDict["tempdir"]=self.tempdir
                        lstNdviDict["logdir"]=self.logdir
                        lstNdviDict["mosaictilenum"]=self.mosaictilenum
                        lstNdviDict["shpfile"]=self.shpfile
                        lstNdviDict["watermask"]=self.watermask
                        lstNdviDict["zonalcsv"]=self.zonalcsv
                        lstNdviDict["intermediatecsv"]=self.intermediatecsv
                        lstNdviDict["finalcsv"]=self.finalcsv  
                        lstNdviDict["prjfile"]=self.prjfile
                        lstNdviDict["inquery"]=self.inquery
                        lstNdviDict["outquery"]=self.outquery
                        lstNdviDict["transposedoutput"]=self.transposedoutput

                        return lstNdviDict

    '''Retrive Trmm configurations''' 
    def ParseTrmm(self):
        trmmDict={}        
        trmm=self.configDoc.getElementsByTagName("trmm")[0]

        self.netcdfdir=trmm.getElementsByTagName("netcdfdir")[0].childNodes[0].nodeValue
        self.griddir=trmm.getElementsByTagName("griddir")[0].childNodes[0].nodeValue
        self.logdir= trmm.getElementsByTagName("logdir")[0].childNodes[0].nodeValue
        self.shpfile= trmm.getElementsByTagName("shpfile")[0].childNodes[0].nodeValue
        self.workspace= trmm.getElementsByTagName("workspace")[0].childNodes[0].nodeValue
        self.zonalcsv= trmm.getElementsByTagName("zonalcsv")[0].childNodes[0].nodeValue
        self.intermediatecsv= trmm.getElementsByTagName("intermediatecsv")[0].childNodes[0].nodeValue
        self.finalcsv= trmm.getElementsByTagName("finalcsv")[0].childNodes[0].nodeValue
        self.inquery=trmm.getElementsByTagName("inquery")[0].childNodes[0].nodeValue
        self.outquery=trmm.getElementsByTagName("outquery")[0].childNodes[0].nodeValue
        self.transposedoutput=trmm.getElementsByTagName("transposedoutput")[0].childNodes[0].nodeValue

        # Dict to hold TRMM config variables

        trmmDict["netcdfdir"]=self.netcdfdir
        trmmDict["griddir"]=self.griddir
        trmmDict["logdir"]=self.logdir
        trmmDict["shpfile"]=self.shpfile
        trmmDict["workspace"]=self.workspace
        trmmDict["zonalcsv"]=self.zonalcsv
        trmmDict["intermediatecsv"]=self.intermediatecsv
        trmmDict["finalcsv"]=self.finalcsv
        trmmDict["inquery"]=self.inquery
        trmmDict["outquery"]=self.outquery
        trmmDict["transposedoutput"]=self.transposedoutput

        return trmmDict
        
    '''Retrive Database configurations''' 
    def ParseDB(self):

        dbDict={}
        dbase=self.configDoc.getElementsByTagName("database")[0]

        self.dbhost=dbase.getElementsByTagName("host")[0].childNodes[0].nodeValue
        self.dbname=dbase.getElementsByTagName("dbname")[0].childNodes[0].nodeValue
        self.dbuser=dbase.getElementsByTagName("user")[0].childNodes[0].nodeValue
        self.dbpassword=dbase.getElementsByTagName("password")[0].childNodes[0].nodeValue

        # Dict to hold Database config variables

        dbDict["dbhost"]=self.dbhost
        dbDict["dbname"]=self.dbname
        dbDict["dbuser"]=self.dbuser
        dbDict["dbpassword"]=self.dbpassword

        return dbDict

    '''Retrive ETa configurations''' 
    def ParseEta(self):

        etaDict={}
        eta=self.configDoc.getElementsByTagName("eta")[0]

        self.etorepjctdir=eta.getElementsByTagName("etorepjctdir")[0].childNodes[0].nodeValue
        self.etfdir=eta.getElementsByTagName("etfdir")[0].childNodes[0].nodeValue
        self.etadir=eta.getElementsByTagName("etadir")[0].childNodes[0].nodeValue
        self.logdir=eta.getElementsByTagName("logdir")[0].childNodes[0].nodeValue
        self.shpfile=eta.getElementsByTagName("shpfile")[0].childNodes[0].nodeValue
        self.tempdir=eta.getElementsByTagName("tempdir")[0].childNodes[0].nodeValue
        self.year=eta.getElementsByTagName("year")[0].childNodes[0].nodeValue
        self.inquery=eta.getElementsByTagName("inquery")[0].childNodes[0].nodeValue
        self.outquery=eta.getElementsByTagName("outquery")[0].childNodes[0].nodeValue
        self.transposedoutput=eta.getElementsByTagName("transposedoutput")[0].childNodes[0].nodeValue

        
        # Dict to hold ETa config variables

        etaDict["etorepjctdir"]=self.etorepjctdir
        etaDict["etfdir"]=self.etfdir
        etaDict["etadir"]=self.etadir
        etaDict["logdir"]=self.logdir
        etaDict["shpfile"]=self.shpfile
        etaDict["tempdir"]=self.tempdir
        etaDict["year"]=self.year
        etaDict["inquery"]=self.inquery
        etaDict["outquery"]=self.outquery
        etaDict["transposedoutput"]=self.transposedoutput


        return etaDict

    '''Retrive ETf configurations'''     
    def ParseEtf(self):
        etfDict={}
        etf=self.configDoc.getElementsByTagName("etf")[0]

        self.etfdir=etf.getElementsByTagName("etfdir")[0].childNodes[0].nodeValue
        self.tempdir=etf.getElementsByTagName("tempdir")[0].childNodes[0].nodeValue
        self.csvtable=etf.getElementsByTagName("csvtable")[0].childNodes[0].nodeValue
        self.lstcdir=etf.getElementsByTagName("lstcdir")[0].childNodes[0].nodeValue
        self.logdir=etf.getElementsByTagName("logdir")[0].childNodes[0].nodeValue
        self.year=etf.getElementsByTagName("year")[0].childNodes[0].nodeValue

        # Dict to hold ETf config variables

        etfDict["etfdir"]=self.etfdir
        etfDict["tempdir"]=self.tempdir
        etfDict["csvtable"]=self.csvtable
        etfDict["lstcdir"]=self.lstcdir
        etfDict["logdir"]=self.logdir
        etfDict["year"]=self.year

        return etfDict

    '''Retrive ETo configurations'''    
    def ParseEto(self):
        etoDict={}
        eto=self.configDoc.getElementsByTagName("eto")[0]

        self.dailyetodir=eto.getElementsByTagName("dailyetodir")[0].childNodes[0].nodeValue
        self.compositedir=eto.getElementsByTagName("compositedir")[0].childNodes[0].nodeValue
        self.reprojectdir=eto.getElementsByTagName("reprojectdir")[0].childNodes[0].nodeValue
        self.projection=eto.getElementsByTagName("projection")[0].childNodes[0].nodeValue
        self.datum=eto.getElementsByTagName("datum")[0].childNodes[0].nodeValue
        self.samplesize=eto.getElementsByTagName("samplesize")[0].childNodes[0].nodeValue
        self.logdir=eto.getElementsByTagName("logdir")[0].childNodes[0].nodeValue
        self.tempdir1=eto.getElementsByTagName("tempdir1")[0].childNodes[0].nodeValue
        self.tempdir2=eto.getElementsByTagName("tempdir2")[0].childNodes[0].nodeValue
        self.year=eto.getElementsByTagName("year")[0].childNodes[0].nodeValue

        # Dict to hold ETo config variables

        etoDict["dailyetodir"]=self.dailyetodir
        etoDict["compositedir"]=self.compositedir
        etoDict["reprojectdir"]=self.reprojectdir
        etoDict["projection"]=self.projection
        etoDict["datum"]=self.datum
        etoDict["samplesize"]=self.samplesize
        etoDict["logdir"]=self.logdir
        etoDict["tempdir1"]=self.tempdir1
        etoDict["tempdir2"]=self.tempdir2
        etoDict["year"]=self.year

        return etoDict

##if __name__=="__main__":
##
##    objParseXml=ParseXml("area","type","NGP","lst","config.xml")
##
##    print "\n"
##    print objParseXml.ParseLstNdvi()
##    print "\n"
##    print objParseXml.ParseTrmm()
##    print "\n"
##    print objParseXml.ParseDB()
##    print "\n"
##    print objParseXml.ParseEto()
##    print "\n"
##    print objParseXml.ParseEtf()
##    print "\n"
##    print objParseXml.ParseEta()
##    print "\n"

          
           



