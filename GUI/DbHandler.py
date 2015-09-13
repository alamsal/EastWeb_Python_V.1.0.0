# Program Description: 
# Author:Aashis Lamsal
# Supervisor:Ting-Wu Chuang
# Advisor:Mike Wimberly

import sys,string,os
from rpy2 import *
from rpy2.robjects import r
import psycopg2
import gc

class RpyDbHandler():

    def __init__(self,dbuser,dbpassword,dbname,dbhost):
        gc.enable()
        self.dbuser='"'+dbuser+'"'
        self.dbpassWord='"'+dbpassword+'"'
        self.dbname='"'+dbname+'"'
        self.dbhost='"'+dbhost+'"'

        self.dbuser1=dbuser
        self.dbpassWord1=dbpassword
        self.dbname1=dbname
        self.dbhost1=dbhost
        

    '''Transpose data to the wider format'''    
    def Transpose(self,outquery,outputcsv):
        
        #outputCsv='file="D:/Rscripts/test.csv"'
        self.sqlQuery='"'+outquery+'"'
        self.outputCsv='"'+outputcsv+'"'

        print self.dbuser
        print self.dbpassWord
        print self.dbname
        print self.dbhost
        print self.sqlQuery
        print self.outputCsv

        try:
            #Load required R libraries        
            r('library(rJava)')
            r('library(DBI)')
            r('library(RJDBC)')
            r('library(RpgSQL)')

            #Define our connection string
            #r('con <- dbConnect(pgSQL(), user = "postgres", password = "eastweb1", dbname = "db_EastWeb",host="localhost")')
            #r('con <- dbConnect(pgSQL(), user = %s, password = %s, dbname = %s,host= %s)'%(self.dbuser,self.dbpassWord,self.dbname,self.dbhost))
            r('.jinit(classpath=NULL,parameters=getOption("-Xmx512m"),silent=FALSE,force.init=TRUE)')
            r('drv <- dbDriver("pgSQL")')
            r('con <- dbConnect(drv, user = %s, password = %s, dbname = %s,host= %s)'%(self.dbuser,self.dbpassWord,self.dbname,self.dbhost))

            r('result<-dbGetQuery(con,%s)'%self.sqlQuery)
            r('dbDisconnect(con)')
            #Transpose from the longer format to the wider format
            r('transpose<-reshape(result,idvar=c("zone","year"),timevar="day",direction="wide",v.names=c("count","mean","stdev","sum"))')

            # Write into CSV file
            r('write.csv(transpose,file=%s)'%self.outputCsv)

            # Display message in Console
            final=r('transpose') 
            print final
        except Exception,e:
            print str(e)

            
       
           

    '''Insert into the DB'''
    def InDB(self,year,day,zone,count,mean,stdev,summ,inquery):
      
        # Define our connection string
        conn_string = "host="+self.dbhost1+" dbname="+self.dbname1+" user="+self.dbuser1+" password="+self.dbpassWord1
        
        # print the connection string we will use to connect
        # print "Connecting to database:-:\n %s" % (conn_string)

        try:
                # get a connection, if a connect cannot be made an exception will be raised here
                conn = psycopg2.connect(conn_string)
                # conn.cursor will return a cursor object, you can use this cursor to perform queries
                cursor = conn.cursor()
                #print "Connected !!!\n"
                print "Feed into DB...\n"
                print "Year: "+str(year)+"Day: "+str(day)+"Zone: "+str(zone)+"Count: "+str(count)+"Mean: "+str(mean)+"St.dev: "+str(stdev)+"Sum: "+str(summ)+"\n"

                cursor.execute(inquery,(year,day,zone,count,mean,stdev,summ,))
                conn.commit()
                
                print "Sucessfully Inserted ..."
        except:
                # Get the most recent exception
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                # Exit the script and print an error telling what happened.
                print("Database connection failed !!:-: \n %s" % (exceptionValue))

        finally:
            
                conn.close()
                del cursor
                del conn
            
        
if __name__=="__main__":
    ObjRpyDbHandler=RpyDbHandler("postgres","eastweb1","db_EastWeb","localhost")
    ObjRpyDbHandler.Transpose("select year,day,zone,count,mean,stdev from tbl_eta limit 1500","D:/Demo/test.csv")
##    ObjRpyDbHandler.InDB(1999,1,1,1,1,1,"INSERT INTO tbl_eta(year,day,zone,count,mean,stdev) VALUES(%s,%s,%s,%s,%s,%s)")
    
