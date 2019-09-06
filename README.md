amigaDBtests
============

Tests for the amiga databases

How to use it
-------------

There is an `environment.yml` file in the root folder of this repo with a conda environment that you can use to run it.

If you have conda available, the steps are:
```
conda env create -f environment.yml 
conda activate amigaDBtests
```
In addition, you need a `config.cfg` file in the working directory, which looks like:
```
[amiga_db]
host=<database-fqdn>
user=<your-user>
password=<your-password>
database=<db-name>
table=<table-name>
table_columns=<column_name_1,column_name_2>
table_column_types=<type_1,type_2>

[cds_db]
#url="http://vizier.u-strasbg.fr/viz-bin/votable?-source=<your-details-here>"
url=/path/to/your/vizier_votable.vot
table_columns=<column_name_1,column_name_2>
```
Then, you should be able to run the script with:
```
python diffTables.py 1> output.stdout 2> output.stderr
```
