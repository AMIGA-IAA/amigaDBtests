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
            
            self.user = config.get("rootAMIGA", "user")
            self.password = config.get("rootAMIGA", "passw")
            
        except (ConfigParser.NoOptionError, ConfigParser.NoOptionError, ConfigParser.Error):
            message = "Problems with the configuration options to access the DB"
            print message
            self.fail(message)

    def setUp(self):
        pass


    def tearDown(self):
        pass



    @unittest.skip("skipped to avoid overload")      
    def test_SM_SIZE_FERNANDEZ13_table1(self):
        '''
        It compares table 1 in the paper of sm size with table 1 in the database (PAPERS_SM_SIZE_FERNANDEZ13.TABLE1) 
        Fields in PAPERS_SM_SIZE_FERNANDEZ13.TABLE1:  
          `CIG`, `MType`, `gmag`, `e_gmag`, `rmag`, `e_rmag`, `imag`, `e_imag`, `Ksmag`, `e_Ksmag`, `logM(0.7)`, 
          `e_logM(0.7)`, `R50(0.7)`, `e_R50(0.7)`, `nsersic`, `e_nsersic`, `Re(0.7)`, `e_Re(0.7)`, `b/a`, `logM(0.75)`, 
          `e_logM(0.75)`, `R50(0.75)`, `e_R50(0.75)`, `Re(0.75)`, `e_Re(0.75)`
        Fields in CDS table (table 1) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/545/A15:
          'CIG', 'MType', 'gmag', 'rmag',  'imag', 'Ksmag', 'logM(0.7)', 
          'n', 'Re(0.7)', 'b/a', 'logM(0.75)',  'Re(0.75)'
        Therefore  columns some columns are not checked. 
        These are in the DB and not in CDS: `e_gmag`, `e_rmag`, `e_imag`,`e_Ksmag`, `e_logM(0.7)`, `e_nsersic`,  `R50(0.7)`, `e_R50(0.7)`, `e_Re(0.7)`, 
        `e_logM(0.75)`, `R50(0.75)`, `e_R50(0.75)`,  `e_Re(0.75)`
        These are in CDS and not in the DB: CIG86, AMIGA, Simbad, NED, LEDA, _RA, _DE
        '''
        
        print "Test PAPERS_SM_SIZE_FERNANDEZ13.Table1\n"
        print " - are not checked\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_SM_SIZE_FERNANDEZ13", self.user, self.password)
               
        cdsnames = ['CIG', 'MType', 'gmag', 'rmag',  'imag', 'Ksmag', 'logM(0.7)', 
          'n', 'Re(0.7)', 'b/a', 'logM(0.75)',  'Re(0.75)' ]
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/MNRAS/434/325/table1&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('MType', int), ('gmag', float), ('rmag', float), ('imag', float), 
                ('Ksmag', float), ('logM(0.7)', float), ('nsersic', float), ('Re(0.7)', float),  
                ('b/a', float), ('logM(0.75)', float), ('Re(0.75)', float)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `CIG`, `MType`, `gmag`, `rmag`, `imag`,  `Ksmag`, `logM(0.7)`,  `nsersic`, `Re(0.7)`, `b/a`, `logM(0.75)`, `Re(0.75)`  FROM `TABLE1`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0, 0.001, 0.001, 0.001, 
                                                    0.001, 0.001, 0.01, 0.01, 
                                                    0.001, 0.01, 0.01])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in SM size Fernandez 13 (table 1)')
    


    @unittest.skip("skipped to avoid overload")      
    def test_AGN_SABATER12_table1(self):
        '''
        It compares table 1 in the paper of AGN Sabater 12 with table 1 in the database (PAPERS_AGN_SABATER12.TABLE1) 
        Fields in PAPERS_AGN_SABATER12.TABLE1: 'CIG', 'fks', 'e_fks', 'logLks', 'e_logLks', 'f_logLks', 'logLB', 'MType', 'e_MType' 
        Fields in CDS table (table 1) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/545/A15:
            'CIG', 'fks', 'e_fks', 'logLks', 'e_logLks', 'f_logLks', 'logLB', 'MType', 'e_MType', CIG86, AMIGA, Simbad, NED, LEDA, _RA, _DE 
        
        Therefore CIG86, AMIGA, Simbad, NED, LEDA, _RA, _DE columns are not checked. 
        TODAS ESTAS COLUMNAS DAN IGUAL
        '''
        
        print "Test PAPERS_AGN_SABATER12.Table1\n"
        print " - CIG86, AMIGA, Simbad, NED, LEDA, _RA, _DE are not checked\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_AGN_SABATER12", self.user, self.password)
               
        cdsnames = ['CIG', 'fks', 'e_fks', 'logLks', 'e_logLks', 'f_logLks', 'logLB', 'MType', 'e_MType']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/545/A15/table1&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('fks', float), ('e_fks', float), ('logLks', float), ('e_logLks', float), 
                ('f_logLks', int), ('logLB', float), ('MType', float), ('e_MType', float)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT CIG, fks, e_fks, logLks, e_logLks, f_logLks, logLB, MType, e_MType FROM `TABLE1`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0.0000000001, 0.0000000001, 0.001, 0.001, 0, 0.001, 0.01, 0.01])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in AGN Sabater 12 (table 1)')
    
    @unittest.skip("skipped to avoid overload")   
    def test_AGN_SABATER12_table2_7(self):
        '''
        It compares table 2 and 7 (nuclear) in the paper of AGN Sabater 12 with table  in the database (PAPERS_AGN_SABATER12.TABLE2 and TABLE7) 
        Fields in PAPERS_AGN_SABATER12.TABLE2: 'CIG', Plate, MJD, Fiber, cc, z, e_z, v, e_v, zsp, e_zsp, sigma, e_sigma, Com
        Fields in PAPERS_AGN_SABATER12.TABLE7: 'CIG', cl.NII, cl.SII, cl.OI, Class, TOType
        Fields in CDS table (table nuclear) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/545/A15:
            'CIG', Plate, MJD, Fiber, cc, z, e_z, v, e_v, zsp, e_zsp, sigma, e_sigma, Com, Sloan, cl.NII, cl.SII, cl.OI, Class, TOType 
        
        Therefore Sloan column is not checked
        '''
        
        print "Test PAPERS_AGN_SABATER12.Table2 and Table7\n"
        print " - Sloan is not checked\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_AGN_SABATER12", self.user, self.password)
               
        cdsnames = ['CIG', 'Plate', 'MJD', 'Fiber', 'cc', 'z', 'e_z', 'v', 'e_v', 'zsp', 'e_zsp', 'sigma', 'e_sigma', 'Com', 'cl.NII', 'cl.SII', 'cl.OI', 'Class', 'TOType']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/545/A15/nuclear&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('Plate', int), ('MJD', int), ('Fiber', int), ('cc', int), 
                ('z', float), ('e_z', float), ('v', int), ('e_v', int), ('zsp', float), 
                ('e_zsp', float), ('sigma', float), ('e_sigma', float), ('Com', 'S2'), 
                ('cl.NII', 'S9'), ('cl.SII', 'S5'), ('cl.OI', 'S5'), ('Class', 'S9'), ('TOType', 'S5')]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT t2.CIG,  Plate, MJD, Fiber, cc, z, e_z, v, e_v, zsp, e_zsp, sigma, e_sigma, Com, `cl.NII`, `cl.SII`, `cl.OI`, `Class`, `TOType` FROM `TABLE7` as t7, TABLE2 as t2 where t2.CIG = t7.CIG"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0, 0, 0, 0, 
                                 0.0000001, 0.0000001, 0, 0, 0.0000001,
                                 0.0000001, 0.01, 0.01, -1,
                                 -1, -1, -1, -1, -1])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in AGN Sabater 12 (table 2 and 7)')
    
    @unittest.skip("skipped to avoid overload")   
    def test_AGN_SABATER12_table3_6(self):
        '''
        It compares table 3 and 6 (lines) in the paper of AGN Sabater 12 with table  in the database (PAPERS_AGN_SABATER12.TABLE3 and TABLE6) 
        Fields in PAPERS_AGN_SABATER12.TABLE3: 'CIG', vshift, vdisp, Anu
        Fields in PAPERS_AGN_SABATER12.TABLE6: 'CIG', `f_logNIIa`, `l_logNIIa`, `logNIIa`, `e_logNIIa`, `f_logOIIIb`, `l_logOIIIb`, `logOIIIb`, `e_logOIIIb`, `f_logSIIa`, `l_logSIIa`, `logSIIa`, `e_logSIIa`, `f_logOIa`, `l_logOIa`, `logOIa`, `e_logOIa`
        Fields in CDS table (table lines) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/545/A15:
            'CIG', 'vshift', 'vdisp', 'Anu', 'f_logNIIa', 'l_logNIIa', 'logNIIa', 'e_logNIIa', 'f_logOIIIb', 'l_logOIIIb', 'logOIIIb', 'e_logOIIIb', 'f_logSIIa', 'l_logSIIa', 'logSIIa', 'e_logSIIa', 'f_logOIa', 'l_logOIa', 'logOIa', 'e_logOIa' 

        '''
        
        print "Test PAPERS_AGN_SABATER12.Table3 and Table6\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_AGN_SABATER12", self.user, self.password)
               
        cdsnames = ['CIG', 'vshift', 'vdisp', 'Anu', 'f_logNIIa', 'l_logNIIa', 'logNIIa', 'e_logNIIa', 'f_logOIIIb', 'l_logOIIIb', 'logOIIIb', 'e_logOIIIb', 'f_logSIIa', 'l_logSIIa', 'logSIIa', 'e_logSIIa', 'f_logOIa', 'l_logOIa', 'logOIa', 'e_logOIa']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/545/A15/lines&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('vshift', float), ('vdisp', float), ('Anu', float),  
                ('f_logNIIa', int), ('l_logNIIa', int), ('logNIIa', float), ('e_logNIIa', float), 
                ('f_logOIIIb', int), ('l_logOIIIb', int), ('ogOIIIb', float), ('e_logOIIIb', float), 
                ('f_logSIIa', int), ('l_logSIIa', int), ('logSIIa', float), ('e_logSIIa', float),
                ('f_logOIa', int), ('l_logOIa', int), ('logOIa', float), ('e_logOIa', float)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT t3.CIG, vshift, vdisp, Anu,`f_logNIIa`, `l_logNIIa`, `logNIIa`, `e_logNIIa`, `f_logOIIIb`, `l_logOIIIb`, `logOIIIb`, `e_logOIIIb`, `f_logSIIa`, `l_logSIIa`, `logSIIa`, `e_logSIIa`, `f_logOIa`, `l_logOIa`, `logOIa`, `e_logOIa` FROM TABLE6 as t6, TABLE3 as t3 WHERE t3.CIG = t6.CIG"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0.001, 0.001, 0.00001, 
                                 0, 0, 0.00001, 0.00001,
                                 0, 0, 0.00001, 0.00001,
                                 0, 0, 0.00001, 0.00001,
                                 0, 0, 0.00001, 0.00001])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in AGN Sabater 12 (table 3 and 6)')
        
    @unittest.skip("skipped to avoid overload")   
    def test_AGN_SABATER12_table4(self):
        '''
        It compares table 4  in the paper of AGN Sabater 12 with table  in the database (PAPERS_AGN_SABATER12.TABLE4) 
        Fields in PAPERS_AGN_SABATER12.TABLE4: 'CIG', Age, Z, Per        
        Fields in CDS table  using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/545/A15:
            'CIG', Age, Z, Per 

        '''
        
        print "Test PAPERS_AGN_SABATER12.Table4\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_AGN_SABATER12", self.user, self.password)
               
        cdsnames = ['CIG', 'Age', 'Z', 'Per']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/545/A15/table4&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('Age', float), ('Z', float), ('Per', float)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT CIG, Age, Z, Per  FROM TABLE4"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0.001, 0.0001, 0.00001])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in AGN Sabater 12 (table 4)')

    @unittest.skip("skipped to avoid overload")   
    def test_AGN_SABATER12_table5(self):
        '''
        It compares table 5 in the paper of AGN Sabater 12 with table  in the database (PAPERS_AGN_SABATER12.TABLE4) 
        Fields in PAPERS_AGN_SABATER12.TABLE5: `CIG`, `Line`, `l_Flux`, `Flux`, `e_Flux`, `pkInt`, `Width`, `Pos`, `sigma`, `Com`  
        Fields in CDS table using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/545/A15:
            '`CIG`, `Line`, `l_Flux`, `Flux`, `e_Flux`, `pkInt`, `Width`, `Pos`, `sigma`, `Com`

        '''
        
        print "Test PAPERS_AGN_SABATER12.Table5\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_AGN_SABATER12", self.user, self.password)
               
        cdsnames = ['CIG', 'Line', 'l_Flux', 'Flux', 'e_Flux', 'pkInt', 'Width', 'Pos', 'sigma', 'Com']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/545/A15/table5&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('Line', int), ('l_Flux', int), ('Flux', float), ('e_Flux', float),
                ('pkInt', float), ('Width', float), ('Pos', float), ('sigma', float), ('Com', int)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `CIG`, `Line`, `l_Flux`, `Flux`, `e_Flux`, `pkInt`, `Width`, `Pos`, `sigma`, `Com`  FROM TABLE5"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0, 0, 0.01, 0.01, 
                                 0.00001, 0.00001, 0.001, 0.00001, 0])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in AGN Sabater 12 (table 5)')
        
    @unittest.skip("skipped to avoid overload")   
    def test_AGN_SABATER12_tablea1(self):
        '''
        It compares table A1 in the paper of AGN Sabater 12 with table  in the database (PAPERS_AGN_SABATER12.TABLEA1) 
        Fields in PAPERS_AGN_SABATER12.TABLEA1: `CIG`, `ObjId`, `umag`, `gmag`, `rmag`, `imag`, `zmag`, `Com`
        Fields in CDS table using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/545/A15:
            '`CIG`, `ObjId`, `umag`, `gmag`, `rmag`, `imag`, `zmag`, `Com`

        '''
        
        print "Test PAPERS_AGN_SABATER12.Tablea1\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_AGN_SABATER12", self.user, self.password)
               
        cdsnames = ['CIG', 'ObjId', 'umag', 'gmag', 'rmag', 'imag', 'zmag', 'Com']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/545/A15/tablea1&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('ObjId', 'S18'), ('umag', float), ('gmag', float), ('rmag', float),
                ('imag', float), ('zmag', float), ('Com', int)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `CIG`, `ObjId`, `umag`, `gmag`, `rmag`, `imag`, `zmag`, `Com` FROM `TABLEA1`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, -1, 0.001, 0.001, 0.001, 
                                 0.001, 0.001, 0])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in AGN Sabater 12 (table A1)')

    @unittest.skip("skipped to avoid overload")   
    def test_AGN_SABATER12_tablea2(self):
        '''
        It compares table A2 in the paper of AGN Sabater 12 with table  in the database (PAPERS_AGN_SABATER12.TABLEA2) 
        Fields in PAPERS_AGN_SABATER12.TABLEA2: `CIG`, MType, BMAG
        Fields in CDS table using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/545/A15:
            `CIG`, MType, BMAG

        '''
        
        print "Test PAPERS_AGN_SABATER12.Tablea2\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_AGN_SABATER12", self.user, self.password)
               
        cdsnames = ['CIG', 'MType', 'BMAG']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/545/A15/tablea2&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('MType', float), ('BMAG', float)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `CIG`, MType, BMAG FROM `TABLEA2`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0.01, 0.0001])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in AGN Sabater 12 (table A2)')
        

    @unittest.skip("skipped to avoid overload")   
    def test_AGN_SABATER12_tablea3(self):
        '''
        It compares table A3 in the paper of AGN Sabater 12 with table  in the database (PAPERS_AGN_SABATER12.TABLEA3) 
        Fields in PAPERS_AGN_SABATER12.TABLEA2: HCG, MType, BMAG
        Fields in CDS table using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/545/A15:
             HCG, MType, BMAG, Class, SimbadName, _RA, _DE
             Therefore Class, SimbadName, _RA, _DE columns are not checked
        '''
        
        print "Test PAPERS_AGN_SABATER12.Tablea3\n"
        print "Class, SimbadName, _RA, _DE columns are not checked"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_AGN_SABATER12", self.user, self.password)
               
        cdsnames = ['HCG', 'MType', 'BMAG']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/545/A15/tablea3&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[ ('HCG', 'S5'), ('MType', float), ('BMAG', float)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT HCG, MType, BMAG FROM `TABLEA3`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([-1, 0.01, 0.0001])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in AGN Sabater 12 (table A3)')    
        
    

    @unittest.skip("skipped to avoid overload")      
    def test_COLOR_FERNANDEZ12_table1(self):
        '''
        It compares table 1 in the paper of sm size with table 1 in the database (PAPERS_COLOR_FERNANDEZ12.TABLE1) 
        Fields in PAPERS_COLOR_FERNANDEZ12.TABLE1:  
          `CIG`, `VELOC_HC`, `E_VELOC_HC`, `r_Vhel`, `DIST`, `MType`, `e_MType`, `OptAssym`, `r_MType`, `Bmag`, `e_Bmag`, 
          `Ag`, `Ai`, `Ak`, `Bmag_corr`, `LogLB`, `MajAxis`, `MinAxis`, `MajAxis_p`, `MinAxis_p`, `Inc`, `Studied`
        Fields in CDS table (table 1) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/545/A15:
          'CIG', 'HV', 'Dist',  'TT',   'Bmag',  'Bmagc' , 'logLB',   'amaj', 'bmin', 'amajp', 'bminp', 'i', 'St'
        Therefore  columns some columns are not checked. 
        These are in the DB and not in CDS:  `E_VELOC_HC`, `e_MType`, `OptAssym`, `r_MType`,  `e_Bmag`, `Ag`, `Ai`, `Ak`,
        These are in CDS and not in the DB:  CIG86, AMIGA, Simbad, NED, LEDA, _RA, _DE
        '''

        
        print "Test PAPERS_COLOR_FERNANDEZ12.Table1\n"
        print " - are not checked\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_COLOR_FERNANDEZ12", self.user, self.password)
               
        cdsnames = ['CIG', 'HV', 'Dist',  'TT',   'Bmag',  'Bmagc' , 'logLB',   'amaj', 'bmin', 'amajp', 'bminp', 'i', 'St' ]
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/540/A47/table1&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('VELOC_HC', float), ('DIST', float), ('Mtype',  float),  ('Bmag', float), ('Bmag_corr', float), 
                ('LogLB', float), ('MajAxis', float), ('MinAxis', float), ('MajAxis_p', float),  
                ('MinAxis_p', float), ('Inc', float), ('Studied', int)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `CIG`, `VELOC_HC`, `DIST`, `MType`, `Bmag`, `Bmag_corr`, `LogLB`, `MajAxis`, `MinAxis`, `MajAxis_p`, `MinAxis_p`, `Inc`, `Studied`  FROM `TABLE1`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0.0001, 0.0001, 0.0001, 0.0001, 
                                                    0.0001, 0.0001, 0.0001, 0.0001, 
                                                    0.0001, 0.0001, 0.0001, 0])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in Color Fernandez 12 (table 1)')


    @unittest.skip("skipped to avoid overload")      
    def test_COLOR_FERNANDEZ12_table2(self):
        '''
        It compares table 2 in the paper of sm size with table 2 in the database (PAPERS_COLOR_FERNANDEZ12.TABLE2) 
        Fields in PAPERS_COLOR_FERNANDEZ12.TABLE2:  
          `cig`, `gmag`, `gmagExt`, `Kcorr_g`, `gMag_abs`, `rmag`, `rmagExt`, `Kcorr_r`, `rMag_abs`, `Ai(g-r)`, `g-r`
        Fields in CDS table (table 2) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/545/A15:
          'CIG', `gmag`, `gAg`, `gKcorr`, `gMAG`, `rmag`, `rAg`, `rKcorr`, `rMAG`, `Ai(g-r)`, `g-r`
        Therefore  columns some columns are not checked. 
        These are in the DB and not in CDS:  ---
        These are in CDS and not in the DB:  ---
        '''

        
        print "Test PAPERS_COLOR_FERNANDEZ12.Table2\n"
        print " - are not checked\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_COLOR_FERNANDEZ12", self.user, self.password)
               
        cdsnames = ['CIG', 'gmag', 'gAg', 'gKcorr', 'gMAG', 'rmag', 'rAg', 'rKcorr', 'rMAG', 'Ai(g-r)', 'g-r']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/540/A47/table2&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('cig',int), ('gmag', float), ('gmagExt', float), ('Kcorr_g',  float),  ('gMag_abs', float), ('rmag', float), 
                ('rmagExt', float), ('Kcorr_r', float), ('rMag_abs', float), ('Ai(g-r)', float),  ('g-r', float)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `cig`, `gmag`, `gmagExt`, `Kcorr_g`, `gMag_abs`, `rmag`, `rmagExt`, `Kcorr_r`, `rMag_abs`, `Ai(g-r)`, `g-r` FROM `TABLE2`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0.0001, 0.0001, 0.0001, 0.0001, 
                                                    0.0001, 0.0001, 0.0001, 0.0001, 
                                                    0.0001, 0.0001])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in Color Fernandez 12 (table 2)')

    @unittest.skip("skipped to avoid overload")      
    def test_HI_ESPADA11_table1(self):
        '''
        It compares table 1 in the paper of sm size with table 1 in the database (PAPERS_HI_ESPADA11.TABLE1) 
        Fields in PAPERS_HI_ESPADA11.TABLE1:  
          `cig`, `Class`, `AFR`, `e_AFR`, `e1`, `e2`
        Fields in CDS table (table 1) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/532/A117:
          'CIG', 'Class', 'AFR', 'e_AFR', 'e1', 'e2' AMIGA, Simbad, NED, LEDA, _RA, _DE, CIG_DATA
        Therefore  columns some columns are not checked. 
        These are in the DB and not in CDS:  
        These are in CDS and not in the DB:  AMIGA, Simbad, NED, LEDA, _RA, _DE, CIG_DATA
        '''

        
        print "Test PAPERS_HI_ESPADA11.Table1\n"
        print " - are not checked\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_HI_ESPADA11", self.user, self.password)
               
        cdsnames = ['CIG', 'Class', 'AFR', 'e_AFR', 'e1', 'e2']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/532/A117/table1&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('cig',int), ('Class', float), ('AFR', float), ('e_AFR',  float),  ('e1', float), ('e2', float), 
                ('LogLB', float), ('MajAxis', float), ('MinAxis', float), ('MajAxis_p', float),  
                ('MinAxis_p', float), ('Inc', float), ('Studied', int)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `cig`, `Class`, `AFR`, `e_AFR`, `e1`, `e2` FROM `TABLE1`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0, 0.0001, 0.0001, 0.0001, 0.0001])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in HI_ESPADA11 (table 1)')


    @unittest.skip("skipped to avoid overload")   
    def test_LISENFELD2011_table1_5(self):
        '''
        It compares table 1 and 5 in the paper of Lisenfeld 2011 with table 1 and 5 in the database (CIG_CO_LISENFELD11). 
        Fields in CIG_CO_LISENFELD11.Table1: cig, DIST, VEL, D25, POS_INCLIN_LOS, MType, IA, log(LB), l_log(LFIR), log(LFIR) and log(LK)
        Fields in CIG_CO_LISENFELD11.Table5: cig: , Det, log(MH2c), log(MH2m), log(MH2e), Tel, BibCode
        Fields in CDS table (table 1 and 5) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/534/A102:
            CIG, Dist, Vel, D25, i, TT, Mi, log(LB), l_log(LFIR), log(LFIR), log(LK), Det, MH2c, MH2e, Simbad, NED, LEDA, AMIGA, _RA, _DE
        
        Therefore, log(MH2m), tel and bibcode are not checked (because they are not in CDS). 
        Therefore,  Simbad, NED, LEDA, AMIGA, _RA, _DE, V are not checked because they are not in the BD
        '''

        print "Test LISENFELD2011_table1_5 \n"
        print " - log(MH2m), tel and bibcode are not checked (because they are not in CDS).\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_CO_LISENFELD11", self.user, self.password)        
        
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


    @unittest.skip("skipped to avoid overload")   
    def test_LISENFELD2011_table4(self):
        '''
        It compares table 4 in the paper of Lisenfeld 2011 with table 1 and 5 in the database (CIG_CO_LISENFELD11). 
        Fields in CIG_CO_LISENFELD11.Table4: `cig`, `u_CIG`, `oRA`, `oDE`, `rms`, `l_ICO`, `ICO`, `e_ICO`, `VCO`, `WCO`, `Tel`
        Fields in CDS table (table 4) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/534/A102:
            'CIG', 'u_CIG', 'oRA','oDE','rms','l_ICO','ICO','e_ICO','VCO','WCO','Tel'
        
        '''
        
        print "Test LISENFELD2011_table4 \n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_CO_LISENFELD11", self.user, self.password)
                
        cdsnames = ['CIG', 'u_CIG', 'oRA','oDE','rms','l_ICO','ICO','e_ICO','VCO','WCO','Tel']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/534/A102/table4&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
        
            
        dtypes=[('cig',int), ('u_CIG', 'S2'), ('oRA', int), ('oDE', int), ('rms', float), ('l_ICO', 'S2'), ('ICO', float), ('e_ICO', float), ('VCO', int), ('WCO', int), ('Tel', int)]
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `cig`, `u_CIG`, `oRA`, `oDE`, `rms`, `l_ICO`, `ICO`, `e_ICO`, `VCO`, `WCO`, `Tel` FROM `TABLE4`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0.1, -1, 0.1, 0.1, 0.001, -1, 0.001, 0.001, 0.1, 0.1, 0.1 ])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in Lisenfeld 2011 (table 4)') 


    @unittest.skip("skipped to avoid overload")      
    def test_FOURIER_DURBALA09_table1(self):
        '''
        It compares table 1 in the paper of sm size with table 1 in the database (PAPERS_FOURIER_DURBALA09.TABLE1) 
        Fields in PAPERS_FOURIER_DURBALA09.TABLE1:  
          `cig`, `PA`, `method`, `Qg`, `e_Qg`, `Qb`, `e_Qb`, `Qs`, `e_Qs`, `A2b`, `A4b`, `A6b`, `lbar`, `r(Qb)`
        Fields in CDS table (table 1) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/mnras/397/1756:
         'CIG',  'PA', 'met', 'Qg', 'e_Qg', 'Qb', 'e_Qb', 'Qs', 'e_Qs', 'A2b', 'A4b', 'A6b', 'lbar', 'r(Qb)'
        Therefore  columns some columns are not checked. 
        These are in the DB and not in CDS: 
        These are in CDS and not in the DB: CIG86, AMIGA, Simbad, NED, LEDA, _RA, _DE
        '''

        
        print "Test PAPERS_FOURIER_DURBALA09.Table1\n"
        print " - are not checked\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_FOURIER_DURBALA09", self.user, self.password)
               
        cdsnames = ['CIG',  'PA', 'met', 'Qg', 'e_Qg', 'Qb', 'e_Qb', 'Qs', 'e_Qs', 'A2b', 'A4b', 'A6b', 'lbar', 'r(Qb)']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/mnras/397/1756/table1&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('PA', int), ('method', 'S3'), ('Qg',  float),  ('e_Qg', float), ('Qb', float), 
                ('e_Qb', float), ('Qs', float), ('e_Qs', float), ('A2b', float),  
                ('A4b', float), ('A6b', float), ('lbar', float), ('r(Qb)', float)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `cig`, `PA`, `method`, `Qg`, `e_Qg`, `Qb`, `e_Qb`, `Qs`, `e_Qs`, `A2b`, `A4b`, `A6b`, `lbar`, `r(Qb)` FROM `TABLE1`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0, -1, 0.0001, 0.0001,  0.0001,
                                                    0.0001, 0.0001, 0.0001, 0.0001, 
                                                    0.0001, 0.0001, 0.01, 0.01])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in FOURIER_DURBALA09 (table 1)')



    @unittest.skip("skipped to avoid overload")      
    def test_PHOT_DURBALA08_table1_2_4_9(self):
        '''
        It compares table 1,2,4,9 in the paper of sm size with table 1,2,4,9 in the database (PAPERS_PHOT_DURBALA08.TABLE1) 
        Fields in PAPERS_PHOT_DURBALA08.TABLE1:  
          `cig`, `UGC_NGCname`, `RAh`, `RAm`, `RAs`, `DE-`, `DEd`, `DEm`, `DEs`, `Vr`, `Inc`, `MType_old`, `MType_rev` 
          t2.`(g-i)`, t2.`iMag`, t2.`a_i25`, t2.`a_g25`, 
          t4.`B/T`, t4.`D/T`, t4.`Bar/T`, t4.`B/D`, t4.`r_e`, t4.`mu_e`, t4.`n_b`, t4.`h_r`, t4.`mu_0`, t4.`l_bar`, t4.`n_bar`,
          t9.`C`, t9.`A`, t9.`S`
        Fields in CDS table (table 1) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/mnras/390/881:
         'CIG',  RAJ2000, DEJ2000, Vr, Inc, MTrev, g-i, iMAG, ai25, ag25, B/T, D/T, Bar/T, B/D, re, mue, nb, hr, mu0, lbar, nbar, C, A,S
        Therefore  columns some columns are not checked. 
        These are in the DB and not in CDS: UGC_NGCname`, `MType_old`, `RAh`, `RAm`, `RAs`, `DE-`, `DEd`, `DEm`, `DEs`,
        These are in CDS and not in the DB: RAJ2000, DEJ2000, AMIGA, Simbad, NED, LEDA, _RA, _DE
        '''

        
        print "Test PAPERS_PHOT_DURBALA08.Table1,2,4,9\n"
        print " - are not checked\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_PHOT_DURBALA08", self.user, self.password)
               
        cdsnames = ['CIG',  'Vr', 'Inc', 'MTrev', 'g-i', 'iMAG', 'ai25', 'ag25', 'B/T', 'D/T', 'Bar/T', 'B/D', 're', 'mue', 'nb', 'hr', 'mu0', 'lbar', 'nbar', 'C', 'A','S']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/MNRAS/390/881/catalog&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('Vr', int), ('Inc', int), ('MType_rev',  'S15'),  ('(g-i)', float), 
                ('iMag', float),  ('a_i25', float), ('a_g25', float), ('B/T', float), ('D/T', float),  
                ('Bar/T', float), ('B/D', float), ('r_e', float), ('mu_e', float),  ('n_b', float),  
                 ('h_r', float), ('mu_0', float), ('l_bar', float), ('n_bar', float),  ('C', float) , 
                ('A', float), ('S', float)]
        
        dbnames =[pair[0] for pair in dtypes]        
        #query = "SELECT t1.`cig`, t1.`Vr`, t1.`Inc`, t1.`MType_rev`, t2.`(g-i)`, t2.`iMag`, t2.`a_i25`, t2.`a_g25`, t4.`B/T`, t4.`D/T`, t4.`Bar/T`, t4.`B/D`, t4.`r_e`, t4.`mu_e`, t4.`n_b`, t4.`h_r`, t4.`mu_0`, t4.`l_bar`, t4.`n_bar`, t9.`C`, t9.`A`, t9.`S` FROM `TABLE1` as t1, TABLE2 as t2, TABLE4 as t4, TABLE9 as t9 where t1.cig = t2.cig AND t1.cig = t4.cig AND t1.cig=t9.cig" 
        query = "SELECT t1.`cig`, t1.`Vr`, t1.`Inc`, t1.`MType_rev`, t2.`(g-i)`, t2.`iMag`, t2.`a_i25`, t2.`a_g25`, t4.`B/T`, t4.`D/T`, t4.`Bar/T`, t4.`B/D`, t4.`r_e`, t4.`mu_e`, t4.`n_b`, t4.`h_r`, t4.`mu_0`, t4.`l_bar`, t4.`n_bar`, t9.`C`, t9.`A`, t9.`S` FROM `TABLE1` as t1 LEFT JOIN (TABLE2 as t2, TABLE4 as t4, TABLE9 as t9) ON (t1.cig = t2.cig AND t1.cig = t4.cig AND t1.cig=t9.cig)" 
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0, 0,-1, 0.001, 
                                                   0.001, 0.01, 0.01, 0.0001, 0.0001, 
                                                   0.0001 , 0.0001, 0.001, 0.001, 0.001, 
                                                   0.001, 0.001, 0.001, 0.001, 0.001, 
                                                   0.001, 0.001])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in PHOT_DURBALA08 (table 1,2,4,9)')





    @unittest.skip("skipped to avoid overload")   
    def test_RADIOFIR_SABATER08_table1(self):
        '''
        It compares table 1 in the paper of RadioFIR Sabater 08 with table in the database (PAPERS_RADIOFIR_SABATER08.TABLE1) 
        Fields in PAPERS_RADIOFIR_SABATER08.TABLE1: `CIG`, `Type1`, `Type2`, `Type3`
        Fields in CDS table  using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/486/73:
             `CIG`, `Type1`, `Type2`, `Type3`, Link1, AMIGA, NED, Simbad, _RA, _DE
             Therefore: Link1, AMIGA, NED, Simbad, _RA, _DE columns are not checked
        '''
        
        print "Test PAPERS_RADIOFIR_SABATER08.Table1\n"
        print "Link1, AMIGA, NED, Simbad, _RA, _DE columns are not checked"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_RADIOFIR_SABATER08", self.user, self.password)
               
        cdsnames = ['CIG', 'Type1', 'Type2', 'Type3']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/486/73/table1&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[ ('CIG', int), ('Type1', 'S11'), ('Type2', 'S6'),  ('Type3', 'S5')]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `CIG`, `Type1`, `Type2`, `Type3` FROM `TABLE1`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, -1, -1,  -1])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in RADIOFIR Sabater 08 (table 1)')

    @unittest.skip("skipped to avoid overload")   
    def test_RADIOFIR_SABATER08_table2(self):
        '''
        It compares table 2 in the paper of RadioFIR Sabater 08 with table in the database (PAPERS_RADIOFIR_SABATER08.TABLE2) 
        Fields in PAPERS_RADIOFIR_SABATER08.TABLE2: `CIG`, `Sample`, `logLFIR`, `l_logLFIR`, `logL1.4GHz`, `MType`, `Excess
        Fields in CDS table  using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/486/73:
             `CIG`, `Sample`, `logLFIR`, `l_logLFIR`, `logL1.4GHz`, `MType`, `Excess`, Link5, AMIGA, NED, Simbad, _RA, _DE
             Therefore: Link5, AMIGA, NED, Simbad, _RA, _DE columns are not checked
        '''
        
        print "Test PAPERS_RADIOFIR_SABATER08.Table2\n"
        print "Link5, AMIGA, NED, Simbad, _RA, _DE columns are not checked"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_RADIOFIR_SABATER08", self.user, self.password)
               
        cdsnames = ['CIG', 'Sample', 'logLFIR', 'l_logLFIR', 'logL1.4GHz', 'MType', 'Excess']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/486/73/table2&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[ ('CIG', int), ('Sample', 'S1'), ('logLFIR', float),  ('l_logLFIR', int), 
                ('logL1.4GHz', float),  ('MType', 'S4'),  ('Excess', float)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `CIG`, `Sample`, `logLFIR`, `l_logLFIR`, `logL1.4GHz`, `MType`, `Excess` FROM `TABLE2`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, -1, 0.001,  0,  0.001,  -1,  0.01])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in RADIOFIR Sabater 08 (table 2)')

    @unittest.skip("skipped to avoid overload")   
    def test_RADIOFIR_SABATER08_table4(self):
        '''
        It compares table 4 in the paper of RadioFIR Sabater 08 with table in the database (PAPERS_RADIOFIR_SABATER08.TABLE4) 
        Fields in PAPERS_RADIOFIR_SABATER08.TABLE4: `CIG`,  `NVSS`, `FIRST`, `Dist`
        Fields in CDS table  using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/486/73:
             `CIG`, `NVSS`, `FIRST`, `Dist`, Link9, AMIGA, NED, Simbad, _RA, _DE 
             Therefore: Link9, AMIGA, NED, Simbad, _RA, _DE columns are not checked
        '''
        
        print "Test PAPERS_RADIOFIR_SABATER08.Table4\n"
        print "Link9, AMIGA, NED, Simbad, _RA, _DE columns are not checked"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_RADIOFIR_SABATER08", self.user, self.password)
               
        cdsnames = ['CIG', 'NVSS', 'FIRST', 'Dist']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/486/73/table4&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[ ('CIG', int), ('NVSS', float), ('FIRST', float),  ('Dist', float)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `CIG`, `NVSS`, `FIRST`, `Dist` FROM `TABLE4`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0.01,   0.001,   0.01])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in RADIOFIR Sabater 08 (table 4)')

    @unittest.skip("skipped to avoid overload")   
    def test_RADIOFIR_SABATER08_table5(self):
        '''
        It compares table 5 in the paper of RadioFIR Sabater 08 with table in the database (PAPERS_RADIOFIR_SABATER08.TABLE5) 
        Fields in PAPERS_RADIOFIR_SABATER08.TABLE5: `CIG`,  `Sample`, `S25um`, `l_S25um`, `S60um`, `l_S60um`, `Type`
        Fields in CDS table  using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/486/73:
             `CIG`, `Sample`, `S25um`, `l_S25um`, `S60um`, `l_S60um`, `Type`,  Link13, AMIGA, NED, Simbad, _RA, _DE
             Therefore: Link13, AMIGA, NED, Simbad, _RA, _DE columns are not checked
        '''
        
        print "Test PAPERS_RADIOFIR_SABATER08.Table5\n"
        print "Link13, AMIGA, NED, Simbad, _RA, _DE columns are not checked"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_RADIOFIR_SABATER08", self.user, self.password)
               
        cdsnames = ['CIG', 'Sample', 'S25um', 'l_S25um', 'S60um', 'l_S60um', 'Type']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/486/73/table5&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[ ('CIG', int), ('Sample', 'S1'), ('S25um', float),  ('l_S25um', int), 
                        ('S60um', float), ('l_S60um', int),  ('Type', 'S6')]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `CIG`, `Sample`, `S25um`, `l_S25um`, `S60um`, `l_S60um`, `Type` FROM `TABLE5`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, -1,  0.001,  0,   0.001,   0,  -1])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in RADIOFIR Sabater 08 (table 5)')


    @unittest.skip("skipped to avoid overload")   
    def test_RADIOFIR_SABATER08_table6(self):
        '''
        It compares table 6  in the paper of RadioFIR Sabater 08 with table in the database (PAPERS_RADIOFIR_SABATER08.TABLE6) 
        Fields in PAPERS_RADIOFIR_SABATER08.TABLE6: `CIG`, `RAJ2000`, `DEJ2000`, `Type1`, `Type2`, `F3`, `F5`, `Sample`
        Fields in CDS table  using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/486/73:
             `CIG`, `RAJ2000`, `DEJ2000`, `Type1`, `Type2`, `F3`, `F5`, `Sample`, Link17, AMIGA, NED, Simbad, _RA, _DE
             Therefore: Link17, AMIGA, NED, Simbad, _RA, _DE columns are not checked
        '''
        
        print "Test PAPERS_RADIOFIR_SABATER08.Table6\n"
        print "Link17, AMIGA, NED, Simbad, _RA, _DE columns are not checked"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_RADIOFIR_SABATER08", self.user, self.password)
               
        cdsnames = ['CIG', 'RAJ2000', 'DEJ2000', 'Type1', 'Type2', 'F3', 'F5', 'Sample']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/486/73/table6&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[ ('CIG', int), ('RAJ2000', 'S11'), ('DEJ2000', 'S11'),  ('Type1', 'S5'), 
                        ('Type2', 'S6'),  ('F3', int), ('F5', int),  ('Sample', int)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `CIG`, `RAJ2000`, `DEJ2000`, `Type1`, `Type2`, `F3`, `F5`, `Sample` FROM `TABLE6`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, -1, -1,  -1,  -1,  0,  0,  0])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in RADIOFIR Sabater 08 (table 6)')



    @unittest.skip("RADIOCONT_LEON08 is skipped. it has errorsssssssssss")
    def test_RADIOCONT_LEON08_table2(self):
        '''
        It compares table 2 in the paper of RADIOCONT LEON 08 with table 2 in the database (PAPERS_RADIOCONT_LEON08.TABLE2). 
        Fields in PAPERS_RADIOCONT_LEON08.TABLE2: 'CIG', 'l_F325', 'F325', 'e_F325', 'r_F325', 'l_P325', 'P325', 'l_F1420', 'F1420', 'e_F1420', 'r_F1420', 'l_P1420', 'P1420', 'l_F4850', 'F4850', 'e_F4850', 'r_F4850', 'l_P4850', 'P4850'
        Fields in CDS table (table 2) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/485/475:
            'CIG', 'l_F325', 'F325', 'e_F325', 'r_F325', 'l_P325', 'P325', 'l_F1420', 'F1420', 'e_F1420', 'r_F1420', 'l_P1420', 'P1420', 'l_F4850', 'F4850', 'e_F4850', 'r_F4850', 'l_P4850', 'P4850', K73, AMIGa, Simbad, NED, _RA, _DE
        
        Therefore K73, AMIGA, Simbad, NED, _RA, _DE columns are not checked
        '''
        
        print "Test PAPERS_RADIOCONT_LEON08.Table2\n"
        print " - K73, AMIGA, Simbad, NED, _RA, _DE are not checked\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_RADIOCONT_LEON08", self.user, self.password)
               
        cdsnames = ['CIG', 'l_F325', 'F325', 'e_F325', 'r_F325', 'l_P325', 'P325', 'l_F1420', 'F1420', 'e_F1420', 'r_F1420', 'l_P1420', 'P1420', 'l_F4850', 'F4850', 'e_F4850', 'r_F4850', 'l_P4850', 'P4850']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/485/475/table2&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('l_F325', 'S1'), ('F325', float), ('e_F325', float), ('r_F325', int), ('l_P325', 'S1'), ('P325', float), 
                ('l_F1420', 'S1'), ('F1420', float), ('e_F1420', float), ('r_F1420', int), ('l_P1420', 'S1'), ('P1420', float), 
                ('l_F4850', 'S1'), ('F4850', float), ('e_F4850', float), ('r_F4850', int), ('l_P4850', 'S1'), ('P4850', float)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT CIG, l_F325, F325, e_F325, r_F325, l_P325, P325, l_F1420, F1420, e_F1420, r_F1420, l_P1420, P1420, l_F4850, F4850, e_F4850, r_F4850, l_P4850, P4850 FROM `TABLE2`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, -1, 0.001, 0.001, 0, -1, 0.0001, -1, 0.001, 0.001, 0, -1, 0.0001, -1, 0.001, 0.001, 0, -1, 0.0001])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in RADIOCONT LEON 2008 (table 2)')



    @unittest.skip("skipped to avoid overload")   
    def test_ISOLATATION_VERLEY07b_table3(self):
        '''
        It compares table 3 in the paper of ISOLATATION_VERLEY07b with table in the database (PAPERS_ISOLATATION_VERLEY07b.TABLE3) 
        Fields in PAPERS_ISOLATATION_VERLEY07b.TABLE3: `cig`, `NName`, `RAdeg`, `DEdeg`, `Area`, `Emag`, `Dist`, `D25`, `Flg1`, `Flg2`, `Vel`, `Ref`, BIB
        Fields in CDS table  using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/470/505:
             `CIG`, `NName`, `RAJ2000`, `DEJ2000`, `Area`, `Emag`, `Dist`, `D25`, `Flg1`, `Flg2`, `Vel`, `Ref`, Source, Simad, Ned
             Therefore: BIB, Source, Simad, Ned columns are not checked
        '''
        
        print "Test PAPERS_ISOLATATION_VERLEY07b.Table3\n"
        print "BIB, Source, Simad, Ned columns are not checked"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_ISOLATION_VERLEY07b", self.user, self.password)
               
        cdsnames = ['CIG', 'NName', 'RAJ2000', 'DEJ2000', 'Area', 'Emag', 'Dist', 'D25', 'Flg1', 'Flg2', 'Vel', 'Ref']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/470/505/table3&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[ ('cig', int), ('NName', int), ('RAdeg', float),  ('DEdeg', float), 
                        ('Area', float),  ('Emag', float), ('Dist', float),  ('D25', float), 
                        ('Flg1', int),  ('Flg2', int), ('Vel', int),  ('Ref', int)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `cig`, `NName`, `RAdeg`, `DEdeg`, `Area`, `Emag`, `Dist`, `D25`, `Flg1`, `Flg2`, `Vel`, `Ref` FROM `TABLE3`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0,  0.000001,  0.000001,  0.0001,  0.0001,  0.01,  0.01,  0,  0,  0,  0])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in ISOLATION Verley 07b (table 3)')


    @unittest.skip("skipped to avoid overload")   
    def test_FIR_LISENFELD07_table2(self):
        '''
        It compares table 2 in the paper of FIR_LISENFELD07 with table in the database (PAPERS_FIR_LISENFELD07.TABLE2) 
        Fields in PAPERS_FIR_LISENFELD07.TABLE2: `cig`, `l_F12um`, `F12um`, `e_F12um`, `n_F12um`, `f_F12um`, `l_F25um`, 
        `F25um`, `e_F25um`, `n_F25um`, `f_F25um`, `l_F60um`, `F60um`, `e_F60um`, `n_F60um`, `f_F60um`, `l_F100um`, 
        `F100um`, `e_F100um`, `n_F100um`, `f_F100um`
        Fields in CDS table  using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/462/507:
             `CIG`,  `l_F12um`, `F12um`, `e_F12um`, `n_F12um`, `f_F12um`, `l_F25um`, 
        `F25um`, `e_F25um`, `n_F25um`, `f_F25um`, `l_F60um`, `F60um`, `e_F60um`, `n_F60um`, `f_F60um`, `l_F100um`, 
        `F100um`, `e_F100um`, `n_F100um`, `f_F100um`, CIG_data, IRAS
             Therefore: CIG_data, IRAS  columns are not checked
        '''
        
        print "Test PAPERS_FIR_LISENFELD07.Table3\n"
        
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_FIR_LISENFELD07", self.user, self.password)
               
        cdsnames = ['CIG',  'l_F12um', 'F12um', 'e_F12um', 'n_F12um', 'f_F12um', 'l_F25um', 
                            'F25um', 'e_F25um', 'n_F25um', 'f_F25um', 'l_F60um', 'F60um', 'e_F60um', 'n_F60um', 
                            'f_F60um', 'l_F100um', 'F100um', 'e_F100um', 'n_F100um', 'f_F100um']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/462/507/table2&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[ ('cig', int), ('l_F12um', 'S1'), ('F12um', float),  ('e_F12um', float), ('n_F12um', int), ('f_F12um', 'S1'), 
                        ('l_F25um', 'S1'), ('F25um', float),  ('e_F25um', float), ('n_F25um', int), ('f_F25um', 'S1'), 
                        ('l_F60um', 'S1'), ('F60um', float),  ('e_F60um', float), ('n_F60um', int), ('f_F60um', 'S1'), 
                        ('l_F100um', 'S1'), ('F100um', float),  ('e_F100um', float), ('n_F100um', int), ('f_F100um', 'S1') ]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `cig`, `l_F12um`, `F12um`, `e_F12um`, `n_F12um`, `f_F12um`, `l_F25um`, `F25um`, `e_F25um`, `n_F25um`, `f_F25um`, `l_F60um`, `F60um`, `e_F60um`, `n_F60um`, `f_F60um`, `l_F100um`, `F100um`, `e_F100um`, `n_F100um`, `f_F100um` FROM `TABLE2`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0,  -1, 0.0001,  0.0001,  0,  -1, 
                                                    -1, 0.0001,  0.0001,  0,  -1, 
                                                    -1, 0.0001,  0.0001,  0,  -1, 
                                                    -1, 0.0001,  0.0001,  0,  -1])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in FIR_LISENFELD07 (table 2)')



    @unittest.skip("skipped to avoid overload")   
    def test_FIR_LISENFELD07_table3(self):
        '''
        It compares table 3 in the paper of FIR_LISENFELD07 with table in the database (PAPERS_FIR_LISENFELD07.TABLE3) 
        Fields in PAPERS_FIR_LISENFELD07.TABLE3: `cig`, `Dist`, `l_logLFIR`, `logLFIR`, `logLB`
        Fields in CDS table  using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/462/507:
             `CIG`, `Dist`, `l_logLFIR`, `logLFIR`, `logLB`, CIG_data, Simbad, NED, _RA, _DE
             Therefore: , CIG_data, Simbad, NED, _RA, _DE columns are not checked
        '''
        
        print "Test PAPERS_FIR_LISENFELD07.Table3\n"
        
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_FIR_LISENFELD07", self.user, self.password)
               
        cdsnames = ['CIG', 'Dist', 'l_logLFIR', 'logLFIR', 'logLB']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/462/507/table3&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[ ('cig', int), ('Dist', float), ('l_logLFIR', 'S1'),  ('logLFIR', float), 
                        ('logLB', float)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `cig`, `Dist`, `l_logLFIR`, `logLFIR`, `logLB` FROM `TABLE3`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0.01,  -1,  0.001,  0.001])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in FIR_LISENFELD07 (table 3)')

        

    #SULENTIC 2006
    #SULENTIC2006.TABLE1 is in CDS but not in the DB
    @unittest.skip("skipped to avoid overload")   
    def test_SULENTIC2006_table3(self):
        '''
        It compares table 3 in the paper of Sulentic 2006 with table 3 in the database (PAPERS_MORPHO_SULENTIC06.TABLE3). 
        Fields in PAPERS_MORPHO_SULENTIC06.TABLE3: 'CIG', 'T', 'u_T', 'Bar', 'I/A'
        Fields in CDS table (table 3) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/449/937:
            More, CIG, T, u_T, Bar, I/A, CIG_data, Simbad, NED, _RA, _DE
        
        Therefore, More, CIG_data, Simbad, NED, _RA, _DE are not checked.  
        '''
        
        print "SULENTIC2006.TABLE1 is in CDS but not in the DB.\n"
        print "Test SULENTIC2006.Table3\n"
        print " - More, CIG_data, Simbad, NED, _RA, _DE are not checked\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_MORPHO_SULENTIC06", self.user, self.password)
               
        cdsnames = ['CIG', 'T', 'u_T', 'Bar', 'I/A']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/449/937/table3&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('T', int), ('u_T', 'S1'), ('Bar', 'S1'), ('I/A', 'S1')]
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `CIG`, `T`, `u_T`, `Bar`, `I/A` FROM `TABLE3`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0.1, 0,1, -1, -1, -1])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in Sulentic 2006 (table 3)') 
    
    @unittest.skip("skipped to avoid overload")   
    def test_SULENTIC2006_table4(self):
        '''
        It compares table 4 in the paper of Sulentic 2006 with table 4 in the database (PAPERS_MORPHO_SULENTIC06.TABLE4). 
        Fields inPAPERS_MORPHO_SULENTIC06.TABLE4: 'CIG', 'MType', 'r_MType'
        Fields in CDS table (table 4) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/449/937:
            More, CIG, MType, r_MType, CIG_data, Simbad, NED, _RA, _DE
        
        Therefore, More, CIG_data, Simbad, NED, _RA, _DE are not checked.  
        '''
        
        print "Test SULENTIC2006.Table4\n"
        print " - More, CIG_data, Simbad, NED, _RA, _DE are not checked\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_MORPHO_SULENTIC06", self.user, self.password)
               
        cdsnames = ['CIG', 'MType', 'r_MType']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/449/937/table4&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('MType', 'S13'), ('r_MType', int)]
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `CIG`, `MType`, `r_MType` FROM `TABLE4`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0.1, -1, 0.1])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in Sulentic 2006 (table 4)')
     
    @unittest.skip("skipped to avoid overload")   
    def test_SULENTIC2006_table5(self):
        '''
        It compares table 5 in the paper of Sulentic 2006 with table 5 in the database (PAPERS_MORPHO_SULENTIC06.TABLE5). 
        Fields in PAPERS_MORPHO_SULENTIC06.TABLE4: 'CIG', 'MTypeO', 'I/AO', 'MTypeP', 'I/AP'
        Fields in CDS table (table 5) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/449/937:
            CIG, MTypeO, I/AO, MTypeP, I/AP
              
        '''
        
        print "Test SULENTIC2006.Table5\n"
        print " - More, CIG_data, Simbad, NED, _RA, _DE are not checked\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_MORPHO_SULENTIC06", self.user, self.password)
               
        cdsnames = ['CIG', 'MTypeO', 'I/AO', 'MTypeP', 'I/AP']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/449/937/table5&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('MTypeO', int), ('I/AO', 'S1'), ('MTypeP', int), ('I/AP', 'S1')]
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `CIG`, `MTypeO`, `I/AO`, `MTypeP`, `I/AP` FROM `TABLE5`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0.1, 0.1, -1, 0.1, -1])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in Sulentic 2006 (table 5)')


    @unittest.skip("skipped to avoid overload")   
    def test_LB_VERDESM05_table1(self):
        '''
        It compares table 1 in the paper of LB_VERDESM05 with table 1 in the database (CIG_LB_VERDESM05.TABLE1). 
        Fields in CIG_LB_VERDESM05.TABLE1: `cig`, `Vr`, `Vr3K`, `r_Vr`
        Fields in CDS table (table 1 ) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/436/443:
            CIG, `Vr`, `Vr3K`, `r_Vr`, CIG_data
        
        Therefore, CIG_data is not checked.  
        '''
 
        print "Test LB_VERDESM05_table1\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_LB_VERDESM05", self.user, self.password)
               
        cdsnames = ['CIG', 'Vr', 'Vr3K', 'r_Vr']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/436/443/table1&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('cig',int), ('Vr', int), ('Vr3K', int), ('r_Vr', int)]
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `cig`, `Vr`, `Vr3K`, `r_Vr` FROM `TABLE1`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0, 0, 0])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in LB_VERDESM05 (table 1)') 

    @unittest.skip("skipped to avoid overload")   
    def test_LB_VERDESM05_table2(self):
        '''
        It compares table 2 in the paper of LB_VERDESM05 with table 2 in the database (CIG_LB_VERDESM05.TABLE1). 
        Fields in CIG_LB_VERDESM05.TABLE1:`cig`, `Dist`, `r_Dist`
        Fields in CDS table (table 2 ) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/436/443:
            CIG, `Dist`, `r_Dist`, CIG_data
        
        Therefore, CIG_data is not checked.  
        '''
 
        print "Test LB_VERDESM05_table2\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_LB_VERDESM05", self.user, self.password)
               
        cdsnames = ['CIG', 'Dist', 'r_Dist']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/436/443/table2&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('cig',int), ('Dist', float), ('r_Dist', int)]
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `cig`, `Dist`, `r_Dist` FROM `TABLE2`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0.01, 0])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in LB_VERDESM05 (table 2)') 


    @unittest.skip("skipped to avoid overload")   
    def test_LB_VERDESM05_table3(self):
        '''
        It compares table 3 in the paper of LB_VERDESM05 with table 3 in the database (CIG_LB_VERDESM05.TABLE3). 
        Fields in CIG_LB_VERDESM05.TABLE1: `cig`, `Bmag`, `Bmagcor`, `LB`
        Fields in CDS table (table 3 ) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/436/443:
            CIG, `Bmag`, `Bmagcor`, `LB`, CIG_data, Simbad, NED, _RA, _DE
        
        Therefore,  CIG_data, Simbad, NED, _RA, _DE are not checked.  
        '''
 
        print "Test LB_VERDESM05_table3\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_LB_VERDESM05", self.user, self.password)
               
        cdsnames = ['CIG', 'Bmag', 'Bmagcor', 'LB']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/436/443/table3&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('cig',int), ('Bmag', float), ('Bmagcor', float), ('LB', float)]
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `cig`, `Bmag`, `Bmagcor`, `LB` FROM `TABLE3`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0.001, 0.001, 0.001])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in LB_VERDESM05 (table 3)') 


    #@unittest.skip("skipped to avoid overload")   
    def test_LB_VERDESM05_refs(self):
        '''
        It compares refs in the paper of LB_VERDESM05 with refs in the database (CIG_LB_VERDESM05.refs). 
        Fields in CIG_LB_VERDESM05.refs: `Ref`, `BibCode`, `Author`, `n_REFS`
        Fields in CDS table (table refs) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/436/443:
            Ref, BibCode, Aut, Com
        '''
 
        print "Test LB_VERDESM05_refs\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_LB_VERDESM05", self.user, self.password)
               
        cdsnames = ['Ref', 'BibCode', 'Aut', 'Com']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/436/443/refs&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('Ref',int), ('BibCode', 'S19'), ('Author', 'S23'), ('n_REFS', 'S99')]
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `Ref`, `BibCode`, `Author`, `n_REFS` FROM `REFS`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, -1, -1, -1])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in LB_VERDESM05 (table refs)') 


    @unittest.skip("skipped to avoid overload")   
    def test_LEON2003_table1(self):
        '''
        It compares table 1 in the paper of Leon 2003 with table 1 in the database (CIG_LEON2003.TABLE1). 
        Fields in CIG_LEON2003.TABLE1: CIG, n_CIG, RA1, DE1, RAJ2000, DEJ2000, sig
        Fields in CDS table (table 1 and 5) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/411/391:
            CIG, n_CIG, RA1, DE1, RAJ2000, DEJ2000, sig, K73
        
        Therefore, K73 is not checked.  
        '''
 
        print "Test LEON2003_table1\n"
        print " - K73 is not checked.\n"
        self.diff = diff_DB_CDS("amiga.iaa.es", "PAPERS_POS_LEON03", self.user, self.password)
               
        cdsnames = ['CIG', 'n_CIG', 'RA1', 'DE1', 'RAJ2000', 'DEJ2000', 'sig']#, 'K73'
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/411/391/table1&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('n_CIG', 'S1'), ('RA1', 'S11'), ('DE1', 'S11'), ('RAJ2000', 'S11'), ('DEJ2000', 'S11'), ('sig', 'S2')]
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT CIG, n_CIG, RA1, DE1, RAJ2000, DEJ2000, sig FROM `TABLE1`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0.1, -1, -1, -1, -1, -1, -1])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in Leon 2003 (table 1)') 
 


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_LISENFELD2011']
    unittest.main()
