'''
Created on Jul 30, 2013

@author: julian Garrido
'''

#from time import localtime
import MySQLdb
import numpy
from astropy.io.votable import parse_single_table
import numpy.ma as ma
import configparser
import os
from numpy import array
import numpy as np


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

    def print_CDS_table(self):
        '''
        Print a CDS table that has been previously loaded.
        '''
        if self.cdstable is None:
            print(" Please load the table first. Nothing to print. ")
            return
        else:
            print(self.cdstable)
    
    def getTableFromDB(self, query, typeColumnsList):
        '''
        Get a table from the AMIGA database
        '''
        # use_unicode=True, charset=...
        connection = MySQLdb.connect(host=self.server, user=self.user, passwd=self.password, db=self.db)
        cursor = connection.cursor()
        cursor.execute(query)
        
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

    def print_AMIGA_table(self):
        '''
        Print an AMIGA table that has been previously loaded.
        '''
        if self.dbtable is None:
            print(" Please load the table first. Nothing to print. ")
            return
        else:
            print(self.dbtable)

    global print_column_diff
    def print_column_diff(cds_column_name,
                          cds_column,
                          amiga_column_name,
                          amiga_column,
                          data_type,
                          tolerance=0):
        '''
        Auxiliary function to print the differences found between two columns:
        * The first one coming from the CDS table
        * The second one coming from the AMIGA table
        '''
        # compare each element in both arrays
        print(('\nDifferences in columns {}@CDS and {}@AMIGA'.format(
              cds_column_name,
              amiga_column_name)))
        print('------------------------------------------')
        print('{:<20} {:<20} {:<20}'.format(
              'Pos',
              cds_column_name + '@CDS',
              amiga_column_name  + '@AMIGA'))
        i = 0
        for e in cds_column:
            # and print the different ones
            if data_type == 'int':

                if (abs(cds_column[i] - amiga_column[i]) + tolerance) > 0:
                    print('{:<20} {:<20} {:<20}'.format(i, cds_column[i], amiga_column[i]))

            elif data_type == 'str':

                if cds_column[i] != amiga_column[i]:
                    print('{:<20} {:<20} {:<20}'.format(i, cds_column[i], amiga_column[i]))

            i += 1

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
            raise Exception('Different number of columns')
        
        message = ""
        
        for i in range(0, len(columnNamesListDB)):

            data1 = self.cdstable.array[ColumnNamesListCDS[i]]
            data2 = self.dbtable[columnNamesListDB[i]]

            if len(data1) != len(data2) :
                message = "There are " + str(len(data1)) + " rows in CDS and " \
                            + str(len(data2)) + " rows in the AMIGA DB."
                raise Exception(message)

            if (data1.dtype != np.dtype(str).type) and (data2.dtype != np.dtype(str).type):

                if not ma.allclose(data1, data2, atol=tol[i]):
                    print_column_diff(ColumnNamesListCDS[i],
                                      data1,
                                      columnNamesListDB[i],
                                      data2,
                                      'int',
                                      tol[i])
                    message += '\nColumns {}@CDS and {}@AMIGA are different (see above).'.format(
                            ColumnNamesListCDS[i],
                            columnNamesListDB[i])

            elif (data1.dtype == np.dtype(str).type) and (data2.dtype == np.dtype(str).type):

                if ((sum(data1 == data2) ) != len(data1)): 
                    print_column_diff(ColumnNamesListCDS[i],
                                      data1,
                                      columnNamesListDB[i],
                                      data2,
                                      'str')
                    message += '\nColumns {}@CDS and {}@AMIGA are different (see above).'.format(
                            ColumnNamesListCDS[i],
                            columnNamesListDB[i])

            elif data1.dtype != np.dtype(str).type :

                newcolumn = numpy.array(list(map(str, data1)))
                if (sum(newcolumn == data2) != len(data1)): 
                    message += ColumnNamesListCDS[i] + ' in cdstable and ' + columnNamesListDB[i] + ' in db are not equal and have different types. ('+ str(sum(data1 != data2)) + ' items).'

            elif data2.dtype != np.dtype(str).type :

                newcolumn = numpy.array(list(map(str, data2)))
                if (sum(data1 == newcolumn) != len(data1)): 
                    message += ColumnNamesListCDS[i] + ' in cdstable and ' + columnNamesListDB[i] + ' in db are not equal and have different types. ('+ str(sum(data1 != data2)) + ' items).'

        if (len(message) > 0) :
            raise Exception(message)
        else:
            return True


if __name__ == '__main__':
#    
#    diff = diff_DB_CDS("amiga.iaa.es", "CIG_CO_LISENFELD11", "amiga", "")
#    
#    cdsnames = ['CIG', 'Dist', 'Vel','D25','i','TT','Mi','log(LB)','l_log(LFIR)','log(LFIR)','log(LK)','Det','MH2c','MH2e']
#    url="http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/534/A102"
#    diff.getTableFromCDS(url)
#    
#        
#    #dtypes=[('cig',int), ('DIST', int), ('VEL', int), ('D25', float), ('POS_INCL_LOS', float), ('MType', int), ('IA', int), ('log(LB)', float), ('l_log(LFIR)', str), ('log(LFIR)', float), ('log(LK)', float), ('Det', int), ('log(MH2c)', float), ('log(MH2m)', float), ('log(MH2e)', float), ('Tel', int), ('BibCode', int)]
#    dtypes=[('cig',int), ('DIST', int), ('VEL', int), ('D25', float), ('POS_INCL_LOS', float), ('MType', int), ('IA', int), ('log(LB)', float), ('l_log(LFIR)', 'S2'), ('log(LFIR)', float), ('log(LK)', float), ('Det', int), ('log(MH2c)', float),  ('log(MH2e)', float)]
#    #I have to remove ('log(MH2m)', float), tel y bibcode, from the query because the cds doesn't return these columns: , t5.`log(MH2m)`
#    dbnames =[pair[0] for pair in dtypes]
#    #query = "select t1.cig, t1.dist, t1.vel, t1.d25, t1.pos_incl_los, t1.mtype, t1.ia, t1.`log(LB)`, t1.`l_log(lfir)`, t1.`log(lfir)`, t1.`log(LK)`, t5.Det, t5.`log(MH2c)`, t5.`log(MH2m)`, t5.`log(MH2e)`, t5.Tel, t5.BibCode from TABLE1 as t1, TABLE5 as t5 WHERE t1.cig = t5.cig"
#    query = "select t1.cig, t1.dist, t1.vel, t1.d25, t1.pos_incl_los, t1.mtype, t1.ia, t1.`log(LB)`, t1.`l_log(lfir)`, t1.`log(lfir)`, t1.`log(LK)`, t5.Det, t5.`log(MH2c)`, t5.`log(MH2e)` from TABLE1 as t1, TABLE5 as t5 WHERE t1.cig = t5.cig"
#    diff.getTableFromDB(query, dtypes)
#    
#    
#    tolerance = numpy.array([0.0001, 0.0001, 0.0001, 0.001, 0.0001, 0.0001, 0.0001, 0.001, 0, 0.001, 0.001, 0.0001, 0.001, 0.001 ])
#    
#    
#    #Check why l_log(LFIR) is not equal in both tables: the answer is that one contains spaces and the other nothing.
#    #print (diff.cdstable.array['l_log(LFIR)'])
#    #print (diff.dbtable['l_log(LFIR)'])    
#    #same  = diff.cdstable.array['l_log(LFIR)']==diff.dbtable['l_log(LFIR)']
#    #cig_diff = diff.cdstable.array['CIG']-diff.dbtable['cig']
#    #[(z,x,y) for x,y,z,k in zip(list(diff.cdstable.array['l_log(LFIR)']), diff.dbtable['l_log(LFIR)'], diff.dbtable['cig'], same) if k == False]
#    
#    #print dbnames
#    diff.compareTables(dbnames, cdsnames, tolerance)
    
    #new case
    config = configparser.RawConfigParser(allow_no_value=True)
    config.read(['config.cfg', os.path.expanduser('~/.config.cfg')])
    amiga_db_user = config.get("amiga_db", "user")
    amiga_db_password = config.get("amiga_db", "password")
    amiga_db_host = config.get("amiga_db", "host")
    amiga_db_database = config.get("amiga_db", "database")
    amiga_db_table = config.get("amiga_db", "table")
    amiga_db_columns = config.get("amiga_db", "table_columns").split(',')
    amiga_db_column_types = config.get("amiga_db", "table_column_types").split(',')
    
    diff = diff_DB_CDS(amiga_db_host,
                       amiga_db_database,
                       amiga_db_user,
                       amiga_db_password)

    cds_db_url = config.get("cds_db", "url")
    cds_db_columns = config.get("cds_db", "table_columns").split(',')
    diff.getTableFromCDS(cds_db_url)

    #diff.print_CDS_table()

    dtypes=list(zip(amiga_db_columns, amiga_db_column_types))
    sql_columns = ""
    for index, value in enumerate(amiga_db_columns):
        if index == len(amiga_db_columns) - 1:
            # last item
            sql_columns += "`{}`".format(value)
        else:
            sql_columns += "`{}`, ".format(value)
    amiga_db_query = "SELECT {} FROM `{}`".format(sql_columns, amiga_db_table)
    diff.getTableFromDB(amiga_db_query, dtypes)

    #diff.print_AMIGA_table()
        
    tolerance = numpy.array([0, 0])
        
    diff.compareTables(amiga_db_columns, cds_db_columns, tolerance)
