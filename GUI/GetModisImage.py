# This is a Python script that automatically downloads historical
# MODIS data from the LP DAAC FTP site


# Initailly historical date for Data transfer must be set on "lpdacc.txt".

# Modified By: Aashis Lamsal
# Supervisor: Ting-Wu Chuang
# Advisor: Mike Wimberly 


import os, ftplib,sys,string

class GetModis:
    
    global Dirlist
    global Filelist
    global Namelist
    global ftpserv
    global LocalFile    
    

    def __init__(self,hostName,userName,passWord,hdfpath,logpath,ftpdir,tileinfo):

        self.hostName=hostName
        self.userName=userName
        self.passWord=passWord
        self.hdfpath=hdfpath
        self.logPath=logpath
        self.ftpDir=ftpdir
        self.tileInformation=tileinfo


    def RetriveData(self):    
        
        # Get user inputs
        # Base directory for the MODIS data

        # Basedir = input("Enter the LP DAAC directory containing the dataset you want to download:")
        #Basedir="MOLT/MOD11A2.005"
        Basedir=self.ftpDir
        print "The LP DAAC directory to download :-:  " +str(Basedir)

        # Local directory for data storage
        #Hdfdir = input("Enter the local directory where you want to store the hdf files:")
        Hdfdir=self.hdfpath
        print "The local directory to store :-: " +str(Hdfdir)
        # Empty lists for the collector functions
        Dirlist = []
        Filelist = []
        Namelist=[]

        mylog=open(self.logPath+"getmodislog.txt",'w',)
           
        # Assigning Global ariables 
        i=0
        k=0
        flag=0
        filecounter=0
        
        try:
            
            # Define helper functions that are used to read files/subdirectories from the
            # ftp site and store them as lists
            def collector(line = ''):            
                Dirlist.append(line)

            def collector2(line = ''):           
                Filelist.append(line)
            
            # Open ftp connection

            print self.hostName
            print self.userName
            print self.passWord
            print self.hdfpath
            print self.logPath
            print self.ftpDir
            print self.tileInformation

            print "Opening FTP connection....."
            global ftpserv
            ftpserv = ftplib.FTP(self.hostName,self.userName,self.passWord)
            print "FTP connected Sucessfully..."

            # Go to the directory containing the dataset of interest
            ftpserv.cwd(Basedir)
            #print ftp.pwd()

            # Involke the LIST ftp function, calling the collector function to store the
            # results to Dirlist in list format
            ftpserv.retrlines("LIST", collector)

            # Get Directory listing only (Without including the sub directories)
            mainDirlist=[]
            myDirlist=[]
            ftpserv.dir(mainDirlist.append)
            myDirlist=mainDirlist[1:]
            # parsing the Directory list
            dirInfo=""

            for mainDir in myDirlist:
            # parsing the directory name only[2002.12.03]   
                mainDirname= mainDir[37:47]    
                dd=mainDirname[8:10]
                mm=mainDirname[5:7]
                yyyy=mainDirname[0:4]
            # Extracging yyyy mm dd to compare with log file information
                dirInfo=str(yyyy)+str(mm)+str(dd)    
                print mainDirname
                print dirInfo
                
            # Read the log file to retrive the information of latest downloaded data
                logFileread=open(self.logPath+"lpdaac.txt",'r')
                logFileread.seek(0)
                logInfo=int(logFileread.read())
                logFileread.close()

                print"Local Drive Recent Log Dir # "+str(logInfo)    
                mylog.write("Local Drive Recent Log Dir # "+str(logInfo)+'\n')
                
            # Coparing the logfile(already downloaded data) with recent datas in the ftp        
                if(int(logInfo)<int(dirInfo)):
                    print "current path -->"+str(ftpserv.pwd())
                    if(flag==1):        # if flag matches the criteria reset the counters
                        ftpserv.cwd("..")
                        k=0
                        flag=0
                        Filelist = []
                        Namelist=[]
                        
                    # List all the files in the subdirectory            
                    path=str(mainDirname)
                    ftpserv.cwd(path) 
                    print "New path -->"+str(ftpserv.pwd())
                    # Filelist = ftp.dir()
                    ##FTP Directory bhitra chire pni file ma chire ko chhina
                    ftpserv.retrlines("LIST", collector2)
                    #ftp.retrlines("LIST")
                    # Download data from the MODIS tiles that we are interested in
                    for Currow2 in Filelist:               
                        Splitrow2 = Currow2.split()
                        Permissions = Splitrow2[0]

                        # Skip over the jpeg browse images - some of these cause problems
                        if Permissions[0:3] == "-rw":
                            global LocalFile
                            Directories = Splitrow2[1]
                            Group = Splitrow2[2]
                            Size = Splitrow2[3]
                            Month = Splitrow2[4]
                            Date = Splitrow2[5]
                            Time = Splitrow2[6]
                            Filename = Splitrow2[7]                    
                            mylog.write(Filename)
                            LocalFile = Hdfdir + Filename
                            Splitfname = Filename.split(".")

                            # Split the header file name into its various components
                            Splitfname = Filename.split(".")
                            Mdataset = Splitfname[0]
                            Maqdate = Splitfname[1]
                            Mlocation = Splitfname[2]
                            Mprocdate = Splitfname[3]
                            Mext1 = Splitfname[4]
                            Mext2 = Splitfname[5]

                            # Pull out the horizontal and vertical tile numbers
                            Htile = Mlocation[1:3]
                            Vtile = Mlocation[4:6]                
                            # Total no. of tiles to be downloaded
                            tileInfo=self.tileInformation
                            tileSplit=tileInfo.split(",")
                            tileNo=int(len(tileSplit))
                            # print tileNo
                            for tilerange in tileSplit:
                                # print tilerange[1:3]+"--"+tilerange[4:]

                                if((Htile==tilerange[1:3])&(Vtile==tilerange[4:])):
                                    Namelist.append(Filename)
                                    print "listlength--->"+str(len(Namelist))                                     
                                    k=k+1

                                else:
                                    print i
                                    i=i+1
                                    print "loginfor-->"+str(logInfo)
                                    print "dirInfor-->"+str(dirInfo)
                                    print "Dirname-->"+str(mainDirname)
                                    print "Filename-->"+str(Filename)
                                    mylog.write("loginfor-->"+str(logInfo)+'\n')
                                    mylog.write("dirInfor-->"+str(dirInfo)+'\n')
                                    mylog.write("Dirname-->"+str(mainDirname)+'\n')
                                    mylog.write("Filename-->"+str(Filename)+'\n')

                    # Download the *.hdf images
                    if(int(k)==int(tileNo*2)): # tileNo*2 i.e, one for .hdf, another for .hdf.xml
                        for record in Namelist:
                            print record
                            ftpserv.retrbinary("RETR "+ record, open(Hdfdir+record, "wb").write)
                        # Write download information in the log file
                        logFwrite=open(self.logPath+"lpdaac.txt",'w')   
                        logFwrite.seek(0)
                        logFwrite.write(dirInfo)
                        #logFwrite.write(dirInfo)
                        logFwrite.close()                                      
                        flag=1
                    else:
                        # Write download information in the log file
                        logFwrite=open(self.logPath+"lpdaac.txt",'w')   
                        logFwrite.seek(0)
                        logFwrite.write(dirInfo)
                        #logFwrite.write(dirInfo)
                        logFwrite.close()                                      
                        flag=1
                        print "Could not Download from Dirname------->"+str(mainDirname)
                        print "Could not Download file---->"+str(Filename)
                        mylog.write("Could not Download from Dirname------->"+str(mainDirname)+'\n')
                        mylog.write("Could not Download file---->"+str(Filename)+'\n')
                else:
                    print "Already downloaded in our local drive" +str(mainDirname)
                    mylog.write( "Already downloaded in our local drive" +str(mainDirname)+'\n')
        finally:    
            ftpserv.quit()
            ftpserv.close()
            print "Closing FTP"
            mylog.write("Closing FTP")
            mylog.close()
            
##if __name__=="__main__":
##    gtmdObj=GetModis("e4ftl01u.ecs.nasa.gov","anonymous","@anonymous","D:\\MODIS_LST_NDVI\\MOD11A2\\","D:\\MODIS_LST_NDVI\\Log\\","MOLT/MOD11A2.005")
##    gtmdObj.RetriveData()


