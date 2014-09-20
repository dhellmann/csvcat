csvcat - Concatenate comma separated value files.
----------------------------------------

csvcat reads one or more comma separated value text file (a CSV file)
and outputs some or all of the data in the same format.  It includes
options for limiting and reordering the columns in the output, as well
as skipping repeated headers.

Installation
---------

The simplest way to install is using 'easy_install':

    $ easy_install csvcat

If you have already downloaded the source and unpacked it, you can
also install by running:

    $ sudo python setup.py install
 

Usage
-----

Run 'csvcat --help' for a complete description of all options,
including examples of how to use the program in various modes.


Examples
-------

The inputs to ''csvcat'' are any number of CSV files, and the output
is CSV data printed to standard output.  The examples listed below
assume two simple CSV files.

      $ cat testdata1.csv
      "Title 1","Title 2","Title 3"
      1,"a",08/18/07
      2,"b",08/19/07
      3,"c",08/20/07

      $ cat testdata2.csv
      Title 1,Title 2,Title 3
      40,D,08/21/07
      50,E,08/22/07
      60,F,08/23/07

When given no options, 'csvcat' simply prints the contents of an input
file to standard output.

       $ csvcat testdata1.csv
       Title 1,Title 2,Title 3
       1,a,08/18/07
       2,b,08/19/07
        3,c,08/20/07

To select which columns should be included in the output, use the
''--columns'' option.  Columns are identified by their number,
beginning with ''0''.  Column numbers can be listed in any order, so
it is possible to reorder the columns of the input data, if needed.

    $ csvcat --columns 2,0 testdata1.csv
    Title 3,Title 1
    08/18/07,1
    08/19/07,2
    08/20/07,3

Different output formats can be selected by using the '--dialect'
option.  There are only two dialects available by default, but the the
'csv' module API supports registering additional dialects.

    $ csvcat --dialect excel-tab testdata1.csv
    Title 1 Title 2 Title 3
    1       a       08/18/07
    2       b       08/19/07
    3       c       08/20/07

To merge multiple files, only including a single set of headers, use
the '--skip-headers' option:

     csvcat --skip-headers --columns 2,0 testdata1.csv testdata2.csv
    Title 3,Title 1
    08/18/07,1
    08/19/07,2
    08/20/07,3
    08/21/07,40
    08/22/07,50
    08/23/07,60
