'''
Created on Sep 30, 2013

@author: Julian Garrido
'''
import unittest
from diffTables import diff_DB_CDS
import numpy
import ConfigParser
import os


class TestAMIGAdb(unittest.TestCase):
    '''
    This class tests the consistency between amiga database and CDS
    It needs to access to a database. The access information should be 
    in  ~/.amigaDB.cfg' or ./amigaDB.cfg' For example:
    [amigaDB]
    useramiga = *****
    passamiga = *****
    '''

    @classmethod
    def setUpClass(self):
        try :
            config = ConfigParser.RawConfigParser(allow_no_value=True)
          
            config.read(['amigaDB.cfg', os.path.expanduser('~/.amigaDB.cfg')])
            
            user = config.get("AMIGADB", "useramiga")
            password = config.get("AMIGADB", "passamiga")
            self.diff = diff_DB_CDS("amiga.iaa.es", "CIG_CO_LISENFELD11", user, password)
            
        except (ConfigParser.NoOptionError, ConfigParser.NoOptionError, ConfigParser.Error):
            message = "Problems with the configuration options to access the DB"
            print message
            self.fail(message)

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_LISENFELD2011_table1_5(self):
        '''
        It compares table 1 and 5 in the paper of Lisenfeld 2011 with table 1 and 5 in the database (CIG_CO_LISENFELD11). 
        Fields in CIG_CO_LISENFELD11.Table1: cig, DIST, VEL, D25, POS_INCLIN_LOS, MType, IA, log(LB), l_log(LFIR), log(LFIR) and log(LK)
        Fields in CIG_CO_LISENFELD11.Table5: cig: , Det, log(MH2c), log(MH2m), log(MH2e), Tel, BibCode
        Fields in CDS table (table 1 and 5) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/534/A102:
            CIG, Dist, Vel, D25, i, TT, Mi, log(LB), l_log(LFIR), log(LFIR), log(LK), Det, MH2c, MH2e
        
        Therefore, log(MH2m), tel and bibcode are not checked (because they are not in CDS). 
        '''
        
        
        cdsnames = ['CIG', 'Dist', 'Vel','D25','i','TT','Mi','log(LB)','l_log(LFIR)','log(LFIR)','log(LK)','Det','MH2c','MH2e']
        url="http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/534/A102"
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/534/A102/table15&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
        
            
        #dtypes=[('cig',int), ('DIST', int), ('VEL', int), ('D25', float), ('POS_INCL_LOS', float), ('MType', int), ('IA', int), ('log(LB)', float), ('l_log(LFIR)', str), ('log(LFIR)', float), ('log(LK)', float), ('Det', int), ('log(MH2c)', float), ('log(MH2m)', float), ('log(MH2e)', float), ('Tel', int), ('BibCode', int)]
        #query = "select t1.cig, t1.dist, t1.vel, t1.d25, t1.pos_incl_los, t1.mtype, t1.ia, t1.`log(LB)`, t1.`l_log(lfir)`, t1.`log(lfir)`, t1.`log(LK)`, t5.Det, t5.`log(MH2c)`, t5.`log(MH2m)`, t5.`log(MH2e)`, t5.Tel, t5.BibCode from TABLE1 as t1, TABLE5 as t5 WHERE t1.cig = t5.cig"
        #I have to remove ('log(MH2m)', float), tel y bibcode, from the query because cds doesn't return these columns: , t5.`log(MH2m)`
        
        dtypes=[('cig',int), ('DIST', int), ('VEL', int), ('D25', float), ('POS_INCL_LOS', float), ('MType', int), ('IA', int), ('log(LB)', float), ('l_log(LFIR)', 'S2'), ('log(LFIR)', float), ('log(LK)', float), ('Det', int), ('log(MH2c)', float),  ('log(MH2e)', float)]
        dbnames =[pair[0] for pair in dtypes]        
        query = "select t1.cig, t1.dist, t1.vel, t1.d25, t1.pos_incl_los, t1.mtype, t1.ia, t1.`log(LB)`, t1.`l_log(lfir)`, t1.`log(lfir)`, t1.`log(LK)`, t5.Det, t5.`log(MH2c)`, t5.`log(MH2e)` from TABLE1 as t1, TABLE5 as t5 WHERE t1.cig = t5.cig"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0.0001, 0.0001, 0.0001, 0.001, 0.0001, 0.0001, 0.0001, 0.001, 0, 0.001, 0.001, 0.0001, 0.001, 0.001 ])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in Lisenfeld 2011 (table 1 and 5)') 


    
    def test_LISENFELD2011_table4(self):
        '''
        It compares table 4 in the paper of Lisenfeld 2011 with table 1 and 5 in the database (CIG_CO_LISENFELD11). 
        Fields in CIG_CO_LISENFELD11.Table1: cig, DIST, VEL, D25, POS_INCLIN_LOS, MType, IA, log(LB), l_log(LFIR), log(LFIR) and log(LK)
        Fields in CIG_CO_LISENFELD11.Table5: cig: , Det, log(MH2c), log(MH2m), log(MH2e), Tel, BibCode
        Fields in CDS table (table 1 and 5) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/534/A102:
            CIG, Dist, Vel, D25, i, TT, Mi, log(LB), l_log(LFIR), log(LFIR), log(LK), Det, MH2c, MH2e
        
        Therefore, log(MH2m), tel and bibcode are not checked.  
        '''
        
        
        cdsnames = ['CIG', 'u_CIG', 'oRA','oDE','rms','l_ICO','ICO','e_ICO','VCO','WCO','Tel']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/534/A102/table4&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
        
            
        dtypes=[('cig',int), ('u_CIG', 'S2'), ('oRA', int), ('oDE', int), ('rms', float), ('l_ICO', 'S2'), ('ICO', float), ('e_ICO', float), ('VCO', int), ('WCO', int), ('Tel', int)]
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `cig`, `u_CIG`, `oRA`, `oDE`, `rms`, `l_ICO`, `ICO`, `e_ICO`, `VCO`, `WCO`, `Tel` FROM `TABLE4`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0.1, -1, 0.1, 0.1, 0.001, -1, 0.001, 0.001, 0.1, 0.1, 0.1 ])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in Lisenfeld 2011 (table 4)') 



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_LISENFELD2011']
    unittest.main()