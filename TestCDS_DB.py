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
    def test_LISENFELD2011_table1_5(self):
        '''
        It compares table 1 and 5 in the paper of Lisenfeld 2011 with table 1 and 5 in the database (CIG_CO_LISENFELD11). 
        Fields in CIG_CO_LISENFELD11.Table1: cig, DIST, VEL, D25, POS_INCLIN_LOS, MType, IA, log(LB), l_log(LFIR), log(LFIR) and log(LK)
        Fields in CIG_CO_LISENFELD11.Table5: cig: , Det, log(MH2c), log(MH2m), log(MH2e), Tel, BibCode
        Fields in CDS table (table 1 and 5) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/534/A102:
            CIG, Dist, Vel, D25, i, TT, Mi, log(LB), l_log(LFIR), log(LFIR), log(LK), Det, MH2c, MH2e
        
        Therefore, log(MH2m), tel and bibcode are not checked (because they are not in CDS). 
        '''

        print "Test LISENFELD2011_table1_5 \n"
        print " - log(MH2m), tel and bibcode are not checked (because they are not in CDS).\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "CIG_CO_LISENFELD11", self.user, self.password)        
        
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
        Fields in CIG_CO_LISENFELD11.Table1: cig, DIST, VEL, D25, POS_INCLIN_LOS, MType, IA, log(LB), l_log(LFIR), log(LFIR) and log(LK)
        Fields in CIG_CO_LISENFELD11.Table5: cig: , Det, log(MH2c), log(MH2m), log(MH2e), Tel, BibCode
        Fields in CDS table (table 1 and 5) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/534/A102:
            CIG, Dist, Vel, D25, i, TT, Mi, log(LB), l_log(LFIR), log(LFIR), log(LK), Det, MH2c, MH2e
        
        Therefore, log(MH2m), tel and bibcode are not checked.  
        '''
        
        print "Test LISENFELD2011_table4 \n"
        print " - log(MH2m), tel and bibcode are not checked.\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "CIG_CO_LISENFELD11", self.user, self.password)
                
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
        self.diff = diff_DB_CDS("amiga.iaa.es", "CIG_LEON2003", self.user, self.password)
               
        cdsnames = ['CIG', 'n_CIG', 'RA1', 'DE1', 'RAJ2000', 'DEJ2000', 'sig']#, 'K73'
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/411/391/table1&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('n_CIG', 'S1'), ('RA1', 'S11'), ('DE1', 'S11'), ('RAJ2000', 'S11'), ('DEJ2000', 'S11'), ('sig', 'S2')]
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT CIG, n_CIG, RA1, DE1, RAJ2000, DEJ2000, sig FROM `TABLE1`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0.1, -1, -1, -1, -1, -1, -1])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in Leon 2003 (table 1)') 
        

    #SULENTIC 2006
    #SULENTIC2006.TABLE1 is in CDS but not in the DB
    @unittest.skip("skipped to avoid overload")   
    def test_SULENTIC2006_table3(self):
        '''
        It compares table 3 in the paper of Sulentic 2006 with table 3 in the database (CIG_SULENTIC2006.TABLE1). 
        Fields in CIG_SULENTIC2006.TABLE3: 'CIG', 'T', 'u_T', 'Bar', 'I/A'
        Fields in CDS table (table 3) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/449/937:
            More, CIG, T, u_T, Bar, I/A, CIG_data, Simbad, NED, _RA, _DE
        
        Therefore, More, CIG_data, Simbad, NED, _RA, _DE are not checked.  
        '''
        
        print "SULENTIC2006.TABLE1 is in CDS but not in the DB.\n"
        print "Test SULENTIC2006.Table3\n"
        print " - More, CIG_data, Simbad, NED, _RA, _DE are not checked\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "CIG_SULENTIC2006", self.user, self.password)
               
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
        It compares table 4 in the paper of Sulentic 2006 with table 4 in the database (CIG_SULENTIC2006.TABLE4). 
        Fields in CIG_SULENTIC2006.TABLE4: 'CIG', 'MType', 'r_MType'
        Fields in CDS table (table 4) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/449/937:
            More, CIG, MType, r_MType, CIG_data, Simbad, NED, _RA, _DE
        
        Therefore, More, CIG_data, Simbad, NED, _RA, _DE are not checked.  
        '''
        
        print "Test SULENTIC2006.Table4\n"
        print " - More, CIG_data, Simbad, NED, _RA, _DE are not checked\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "CIG_SULENTIC2006", self.user, self.password)
               
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
        It compares table 5 in the paper of Sulentic 2006 with table 5 in the database (CIG_SULENTIC2006.TABLE5). 
        Fields in CIG_SULENTIC2006.TABLE4: 'CIG', 'MTypeO', 'I/AO', 'MTypeP', 'I/AP'
        Fields in CDS table (table 5) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/449/937:
            CIG, MTypeO, I/AO, MTypeP, I/AP
              
        '''
        
        print "Test SULENTIC2006.Table5\n"
        print " - More, CIG_data, Simbad, NED, _RA, _DE are not checked\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "CIG_SULENTIC2006", self.user, self.password)
               
        cdsnames = ['CIG', 'MTypeO', 'I/AO', 'MTypeP', 'I/AP']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/449/937/table5&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('MTypeO', int), ('I/AO', 'S1'), ('MTypeP', int), ('I/AP', 'S1')]
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `CIG`, `MTypeO`, `I/AO`, `MTypeP`, `I/AP` FROM `TABLE5`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0.1, 0.1, -1, 0.1, -1])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in Sulentic 2006 (table 5)')

    @unittest.skip("RADIOCONT_LEON08 is skipped. it has errorsssssssssss")
    def test_RADIOCONT_LEON08_table2(self):
        '''
        It compares table 2 in the paper of RADIOCONT LEON 08 with table 2 in the database (CIG_RADIOCONT_LEON08.TABLE2). 
        Fields in CIG_RADIOCONT_LEON08.TABLE2: 'CIG', 'l_F325', 'F325', 'e_F325', 'r_F325', 'l_P325', 'P325', 'l_F1420', 'F1420', 'e_F1420', 'r_F1420', 'l_P1420', 'P1420', 'l_F4850', 'F4850', 'e_F4850', 'r_F4850', 'l_P4850', 'P4850'
        Fields in CDS table (table 2) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/485/475:
            'CIG', 'l_F325', 'F325', 'e_F325', 'r_F325', 'l_P325', 'P325', 'l_F1420', 'F1420', 'e_F1420', 'r_F1420', 'l_P1420', 'P1420', 'l_F4850', 'F4850', 'e_F4850', 'r_F4850', 'l_P4850', 'P4850', K73, AMIGa, Simbad, NED, _RA, _DE
        
        Therefore K73, AMIGa, Simbad, NED, _RA, _DE columns are not checked
        '''
        
        print "Test CIG_RADIOCONT_LEON08.Table2\n"
        print " - K73, AMIGa, Simbad, NED, _RA, _DE are not checked\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "CIG_RADIOCONT_LEON08", self.user, self.password)
               
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
    def test_AGN_SABATER12_table1(self):
        '''
        It compares table 1 in the paper of AGN Sabater 08 with table 1 in the database (CIG_AGN_SABATER12.TABLE1) 
        Fields in CIG_AGN_SABATER12.TABLE1: 'CIG', 'fks', 'e_fks', 'logLks', 'e_logLks', 'f_logLks', 'logLB', 'MType', 'e_MType' 
        Fields in CDS table (table 1) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/545/A15:
            'CIG', 'fks', 'e_fks', 'logLks', 'e_logLks', 'f_logLks', 'logLB', 'MType', 'e_MType', CIG86, AMIGA, Simbad, NED, LEDA, _RA, _DE 
        
        Therefore CIG86, AMIGA, Simbad, NED, LEDA, _RA, _DE columns are not checked
        '''
        
        print "Test CIG_AGN_SABATER12.Table1\n"
        print " - CIG86, AMIGA, Simbad, NED, LEDA, _RA, _DE are not checked\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "CIG_AGN_SABATER12", self.user, self.password)
               
        cdsnames = ['CIG', 'fks', 'e_fks', 'logLks', 'e_logLks', 'f_logLks', 'logLB', 'MType', 'e_MType']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/545/A15/table1&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('fks', float), ('e_fks', float), ('logLks', float), ('e_logLks', float), 
                ('f_logLks', int), ('logLB', float), ('MType', float), ('e_MType', float)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT CIG, fks, e_fks, logLks, e_logLks, f_logLks, logLB, MType, e_MType FROM `TABLE1`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0.0000000001, 0.0000000001, 0.001, 0.001, 0, 0.001, 0.01, 0.01])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in AGN Sabater 08 (table 1)')
    
    @unittest.skip("skipped to avoid overload")   
    def test_AGN_SABATER12_table2_7(self):
        '''
        It compares table 2 and 7 (nuclear) in the paper of AGN Sabater 08 with table  in the database (CIG_AGN_SABATER12.TABLE2 and TABLE7) 
        Fields in CIG_AGN_SABATER12.TABLE2: 'CIG', Plate, MJD, Fiber, cc, z, e_z, v, e_v, zsp, e_zsp, sigma, e_sigma, Com
        Fields in CIG_AGN_SABATER12.TABLE7: 'CIG', cl.NII, cl.SII, cl.OI, Class, TOType
        Fields in CDS table (table nuclear) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/545/A15:
            'CIG', Plate, MJD, Fiber, cc, z, e_z, v, e_v, zsp, e_zsp, sigma, e_sigma, Com, Sloan, cl.NII, cl.SII, cl.OI, Class, TOType 
        
        Therefore Sloan column is not checked
        '''
        
        print "Test CIG_AGN_SABATER12.Table2 and Table7\n"
        print " - Sloan is not checked\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "CIG_AGN_SABATER12", self.user, self.password)
               
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
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in AGN Sabater 08 (table 2 and 7)')
    
    @unittest.skip("skipped to avoid overload")   
    def test_AGN_SABATER12_table3_6(self):
        '''
        It compares table 3 and 6 (lines) in the paper of AGN Sabater 08 with table  in the database (CIG_AGN_SABATER12.TABLE3 and TABLE6) 
        Fields in CIG_AGN_SABATER12.TABLE3: 'CIG', vshift, vdisp, Anu
        Fields in CIG_AGN_SABATER12.TABLE6: 'CIG', `f_logNIIa`, `l_logNIIa`, `logNIIa`, `e_logNIIa`, `f_logOIIIb`, `l_logOIIIb`, `logOIIIb`, `e_logOIIIb`, `f_logSIIa`, `l_logSIIa`, `logSIIa`, `e_logSIIa`, `f_logOIa`, `l_logOIa`, `logOIa`, `e_logOIa`
        Fields in CDS table (table lines) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/545/A15:
            'CIG', 'vshift', 'vdisp', 'Anu', 'f_logNIIa', 'l_logNIIa', 'logNIIa', 'e_logNIIa', 'f_logOIIIb', 'l_logOIIIb', 'logOIIIb', 'e_logOIIIb', 'f_logSIIa', 'l_logSIIa', 'logSIIa', 'e_logSIIa', 'f_logOIa', 'l_logOIa', 'logOIa', 'e_logOIa' 

        '''
        
        print "Test CIG_AGN_SABATER12.Table3 and Table6\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "CIG_AGN_SABATER12", self.user, self.password)
               
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
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in AGN Sabater 08 (table 3 and 6)')
        
    @unittest.skip("skipped to avoid overload")   
    def test_AGN_SABATER12_table4(self):
        '''
        It compares table 4  in the paper of AGN Sabater 08 with table  in the database (CIG_AGN_SABATER12.TABLE4) 
        Fields in CIG_AGN_SABATER12.TABLE4: 'CIG', Age, Z, Per        
        Fields in CDS table  using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/545/A15:
            'CIG', Age, Z, Per 

        '''
        
        print "Test CIG_AGN_SABATER12.Table4\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "CIG_AGN_SABATER12", self.user, self.password)
               
        cdsnames = ['CIG', 'Age', 'Z', 'Per']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/545/A15/table4&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('Age', float), ('Z', float), ('Per', float)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT CIG, Age, Z, Per  FROM TABLE4"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0.001, 0.0001, 0.00001])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in AGN Sabater 08 (table 4)')

    @unittest.skip("skipped to avoid overload")   
    def test_AGN_SABATER12_table5(self):
        '''
        It compares table 5 in the paper of AGN Sabater 08 with table  in the database (CIG_AGN_SABATER12.TABLE4) 
        Fields in CIG_AGN_SABATER12.TABLE5: `CIG`, `Line`, `l_Flux`, `Flux`, `e_Flux`, `pkInt`, `Width`, `Pos`, `sigma`, `Com`  
        Fields in CDS table (table nuclear) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/545/A15:
            '`CIG`, `Line`, `l_Flux`, `Flux`, `e_Flux`, `pkInt`, `Width`, `Pos`, `sigma`, `Com`

        '''
        
        print "Test CIG_AGN_SABATER12.Table5\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "CIG_AGN_SABATER12", self.user, self.password)
               
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
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in AGN Sabater 08 (table 5)')
        
    @unittest.skip("skipped to avoid overload")   
    def test_AGN_SABATER12_tablea1(self):
        '''
        It compares table A1 in the paper of AGN Sabater 08 with table  in the database (CIG_AGN_SABATER12.TABLEA1) 
        Fields in CIG_AGN_SABATER12.TABLEA1: `CIG`, `ObjId`, `umag`, `gmag`, `rmag`, `imag`, `zmag`, `Com`
        Fields in CDS table (table nuclear) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/545/A15:
            '`CIG`, `ObjId`, `umag`, `gmag`, `rmag`, `imag`, `zmag`, `Com`

        '''
        
        print "Test CIG_AGN_SABATER12.Tablea1\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "CIG_AGN_SABATER12", self.user, self.password)
               
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
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in AGN Sabater 08 (table A1)')

    @unittest.skip("skipped to avoid overload")   
    def test_AGN_SABATER12_tablea2(self):
        '''
        It compares table A2 in the paper of AGN Sabater 08 with table  in the database (CIG_AGN_SABATER12.TABLEA2) 
        Fields in CIG_AGN_SABATER12.TABLEA2: `CIG`, MType, BMAG
        Fields in CDS table (table nuclear) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/545/A15:
            `CIG`, MType, BMAG

        '''
        
        print "Test CIG_AGN_SABATER12.Tablea2\n"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "CIG_AGN_SABATER12", self.user, self.password)
               
        cdsnames = ['CIG', 'MType', 'BMAG']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/545/A15/tablea2&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[('CIG',int), ('MType', float), ('BMAG', float)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT `CIG`, MType, BMAG FROM `TABLEA2`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([0, 0.01, 0.0001])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in AGN Sabater 08 (table A2)')
        

    @unittest.skip("skipped to avoid overload")   
    def test_AGN_SABATER12_tablea3(self):
        '''
        It compares table A3 in the paper of AGN Sabater 08 with table  in the database (CIG_AGN_SABATER12.TABLEA3) 
        Fields in CIG_AGN_SABATER12.TABLEA2: HCG, MType, BMAG
        Fields in CDS table (table nuclear) using this url: http://vizier.u-strasbg.fr/viz-bin/votable/-A?-source=J/A+A/545/A15:
             HCG, MType, BMAG, Class, SimbadName, _RA, _DE
             Therefore Class, SimbadName, _RA, _DE columns are not checked
        '''
        
        print "Test CIG_AGN_SABATER12.Tablea3\n"
        print "Class, SimbadName, _RA, _DE columns are not checked"
        
        self.diff = diff_DB_CDS("amiga.iaa.es", "CIG_AGN_SABATER12", self.user, self.password)
               
        cdsnames = ['HCG', 'MType', 'BMAG']
        url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=J/A%2bA/545/A15/tablea3&-out.max=unlimited"
        self.diff.getTableFromCDS(url)
    
        
        dtypes=[ ('HCG', 'S5'), ('MType', float), ('BMAG', float)]
        
        
        dbnames =[pair[0] for pair in dtypes]        
        query = "SELECT HCG, MType, BMAG FROM `TABLEA3`"
        self.diff.getTableFromDB(query, dtypes)      
        
        tolerance = numpy.array([-1, 0.01, 0.0001])
        
        
        self.assertTrue( self.diff.compareTables(dbnames, cdsnames, tolerance), 'There is a mismatch in AGN Sabater 08 (table A3)')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_LISENFELD2011']
    unittest.main()
