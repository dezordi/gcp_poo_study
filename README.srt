google cloud computing - Object Oriented Programming - Python study
=========


The general idea is to retrieve sra data via BigQuery by specifying a taxonomic group, or using a list file with different taxonomic groups, and if necessary, saving the data to Storage.


=====
First Steps
=====

**Set enviroment**

.. code:: bash
    
    conda env create -f gcp_poo_study.yml -n <enviroment_name>
    conda activate <enviroment_name>
    
**Set Google authentication
- Follow this guide: https://cloud.google.com/docs/authentication/getting-started

=====
Usage
=====


**Get help**

.. code:: bash
    
    python main_bq.py --help

**To recovery sra of specific family

.. code:: bash

    python main_bq.py -tx Coronaviridae


**To recovery sra of a specific list of organisms

.. code:: bash

    python main_bq.py -so specific_organism_file_example.txt

**To recovery sra of a specific list of organisms and from one or more specific library sources**

.. code:: bash

    python main_bq.py -so specific_organism_file_example.txt -ke TRANSCRIPTOMIC 'TRANSCRIPTOMIC SINGLE CELL' METATRANSCRIPTOMIC

**To store the results on gcp Store**

.. code:: bash

    python main_bq.py -so specific_organism_file_example.txt -bn <bucket_name>

==========
Disclaimer
==========
- Feel free to commit changes that make the code more efficient or cleaner.
- This repository will be constantly updated.