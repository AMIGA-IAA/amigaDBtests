'''
Created on Jul 30, 2013

@author: julian Garrido
'''

#from time import localtime
import MySQLdb
import numpy
from astropy.io.votable import parse_single_table
import numpy.ma as ma


class diff_DB_CDS(object):
    '''
    This class is able to download a votable from CDS and compare it with a table in a database
    '''

    def __init__(self, server, db, user, password):
        '''
        Constructor
        '''
        self.password = password
        self.server = server
        self.user = user
        self.db = db
        
    def getTableFromCDS(self, url):
        '''
        It retrieves a votable from CDS. 
        example: "url=http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/534/A102"
        '''
        self.url_cds = url
        self.cdstable = parse_single_table(url)
    
    def getTableFromDB(self, query, typeColumnsList):
        connection = MySQLdb.connect(host=self.server, user=self.user, passwd=self.password, db=self.db ) #,use_unicode=True,  charset = ...
        cursor = connection.cursor()
        cursor.execute(query)
        
        #This method doesn't work if there are Nulls in the DB. --> None in the python array
        #self.dbtable = numpy.fromiter(cursor, typeColumnsList)
        
        #Build the numpy array
        #results = cursor.fetchall()
        #results = list(results)
        #for index_r, row in enumerate(results):
        #    newrow = list(row)
        #    for index_c, col in enumerate(newrow) :
        #        if col is None :
        #            newrow[index_c]=numpy.nan
        #    results[index_r] = tuple(newrow)
        #    #if changes :
        #    #    results results[index_r]
        
        values = cursor.fetchall()
        ncols = len(values[0])
        nrows = len(values)
        
        arr = ma.zeros(nrows, dtype=typeColumnsList)
        
        for i, row in enumerate(values):
            for j, cell in enumerate(values[i]):
                if values[i][j] is None:
                    arr.mask[i][j] = True
                else:
                    arr.data[i][j] = cell
        
        self.dbtable = arr
        
        connection.close()
        
    def compareTables(self, columnNamesListDB, ColumnNamesListCDS, tol):
        '''
        Call getTaleFromDB and getTAbleFromCds before calling this method. 
        This method receive a list of names for the dbtable and a list of names for the cdstable.
        also an array of tolerance with an element for each column. If the column is not numeric,
        the value would be ignored. 
        If two columns contain numbers it checks if the difference is 0. with the absolute tolerance
        that is provided as input
        If two columns contain strings it checks if they are equal.
        If two columns have different types, it transform them two strings and checks if they are equal.
        Remark: string types must be provided as static strings e.g. S3 is valid but not str 
        Return True if all the columns are equal.
        Restriction: Columns to be compared must be in the same position in both lists.
        '''
        if len(columnNamesListDB) != len(ColumnNamesListCDS):
            raise Exception, 'Different number of columns'
        
        message = ""
        
        for i in range(0, len(columnNamesListDB)):
            data1 = self.cdstable.array[ColumnNamesListCDS[i]]
            data2 = self.dbtable[columnNamesListDB[i]]
            print "column: " + str(i)
            if not numpy.issubdtype(data1.dtype, str) and not numpy.issubdtype(data2.dtype, str):
                #data2_ma = ma.masked_array(data2, mask=numpy.isnan(data2).tolist())
                if not ma.allclose(data1, data2, atol=tol[i]) :
                    same = ma.allclose(data1, data2, atol=tol[i])
                    difference = [(x,y) for x,y,z in zip(data1, data2, same) if z == False]
                    message += ColumnNamesListCDS[i] + ' in CDStable and ' + columnNamesListDB[i] + ' in db are not equal.'  + str(difference) + '\n'
            elif numpy.issubdtype(data1.dtype, str) and numpy.issubdtype(data2.dtype, str):
                if ((sum(data1 == data2) ) != len(data1)): 
                    same = data1==data2
                    difference = [(x,y) for x,y,z in zip(data1, data2, same) if z == False]
                    message += ColumnNamesListCDS[i] + ' in CDStable and ' + columnNamesListDB[i] + ' in db are not equal ('+ str(sum(data1 != data2)) + ' items): ' + str(difference) + '\n'
                    #print data1[0], data2[0], data1[0]==data2[0] 
            elif not numpy.issubdtype(data1.dtype, str) :
                newcolumn = numpy.array(map(str, data1))
                if (sum(newcolumn == data2) != len(data1)): 
                    message += ColumnNamesListCDS[i] + ' in cdstable and ' + columnNamesListDB[i] + ' in db are not equal and have different types. ('+ str(sum(data1 != data2)) + ' items).'
            elif not numpy.issubdtype(data2.dtype, str) :
                newcolumn = numpy.array(map(str, data2))
                if (sum(data1 == newcolumn) != len(data1)): 
                    message += ColumnNamesListCDS[i] + ' in cdstable and ' + columnNamesListDB[i] + ' in db are not equal and have different types. ('+ str(sum(data1 != data2)) + ' items).'
        if(len(message) > 0) :
            #print "Errors: " + message
            raise Exception, message
        else:
            return True


if __name__ == '__main__':
    
    diff = diff_DB_CDS("amiga.iaa.es", "CIG_CO_LISENFELD11", "amiga", "")
    
    cdsnames = ['CIG', 'Dist', 'Vel','D25','i','TT','Mi','log(LB)','l_log(LFIR)','log(LFIR)','log(LK)','Det','MH2c','MH2e']
    url="http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/534/A102"
    diff.getTableFromCDS(url)
    
        
    #dtypes=[('cig',int), ('DIST', int), ('VEL', int), ('D25', float), ('POS_INCL_LOS', float), ('MType', int), ('IA', int), ('log(LB)', float), ('l_log(LFIR)', str), ('log(LFIR)', float), ('log(LK)', float), ('Det', int), ('log(MH2c)', float), ('log(MH2m)', float), ('log(MH2e)', float), ('Tel', int), ('BibCode', int)]
    dtypes=[('cig',int), ('DIST', int), ('VEL', int), ('D25', float), ('POS_INCL_LOS', float), ('MType', int), ('IA', int), ('log(LB)', float), ('l_log(LFIR)', 'S2'), ('log(LFIR)', float), ('log(LK)', float), ('Det', int), ('log(MH2c)', float),  ('log(MH2e)', float)]
    #I have to remove ('log(MH2m)', float), tel y bibcode, from the query because the cds doesn't return these columns: , t5.`log(MH2m)`
    dbnames =[pair[0] for pair in dtypes]
    #query = "select t1.cig, t1.dist, t1.vel, t1.d25, t1.pos_incl_los, t1.mtype, t1.ia, t1.`log(LB)`, t1.`l_log(lfir)`, t1.`log(lfir)`, t1.`log(LK)`, t5.Det, t5.`log(MH2c)`, t5.`log(MH2m)`, t5.`log(MH2e)`, t5.Tel, t5.BibCode from TABLE1 as t1, TABLE5 as t5 WHERE t1.cig = t5.cig"
    query = "select t1.cig, t1.dist, t1.vel, t1.d25, t1.pos_incl_los, t1.mtype, t1.ia, t1.`log(LB)`, t1.`l_log(lfir)`, t1.`log(lfir)`, t1.`log(LK)`, t5.Det, t5.`log(MH2c)`, t5.`log(MH2e)` from TABLE1 as t1, TABLE5 as t5 WHERE t1.cig = t5.cig"
    diff.getTableFromDB(query, dtypes)
    
    
    tolerance = numpy.array([0.0001, 0.0001, 0.0001, 0.001, 0.0001, 0.0001, 0.0001, 0.001, 0, 0.001, 0.001, 0.0001, 0.001, 0.001 ])
    
    
    #Check why l_log(LFIR) is not equal in both tables: the answer is that one contains spaces and the other nothing.
    #print (diff.cdstable.array['l_log(LFIR)'])
    #print (diff.dbtable['l_log(LFIR)'])    
    #same  = diff.cdstable.array['l_log(LFIR)']==diff.dbtable['l_log(LFIR)']
    #cig_diff = diff.cdstable.array['CIG']-diff.dbtable['cig']
    #[(z,x,y) for x,y,z,k in zip(list(diff.cdstable.array['l_log(LFIR)']), diff.dbtable['l_log(LFIR)'], diff.dbtable['cig'], same) if k == False]
    
    #print dbnames
    diff.compareTables(dbnames, cdsnames, tolerance)

