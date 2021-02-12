import argparse
from bigquery_sra_by_tax import TaxBigQuery2CSV, OrganismsBigQuery2CSV
from data_to_storage import Data2Storage

#Passing arguments
parser = argparse.ArgumentParser(description = 'This script makes a bigquery search against nih-sra-datastore. You need:\n- Google Cloud Credentials\n - A project on bigquery ',formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-tx", "--tax_name", help="Tax name, e.g. Escherichia, Bacteria, Coronaviridae", default = None)
parser.add_argument("-ke","--librarysource",help="If you want, you can choose a specific experiment, e.g.: GENOMIC, TRANSCRIPTOMIC, etc. Default will return all experiments", default = None, choices=["GENOMIC SINGLE CELL","TRANSCRIPTOMIC","METAGENOMIC","VIRAL RNA","TRANSCRIPTOMIC SINGLE CELL","METATRANSCRIPTOMIC","GENOMIC","OTHER","SYNTHETIC"], nargs='+')
parser.add_argument("-so","--specific_organisms",help="Sometimes some studies attribute an incorrect taxa in the tax_name field. In this way, you can pass a file list with the name of specific organisms inside the tax_name. The file should be formated with one name per line", default = None)
parser.add_argument("-bn","--bucket_name",help="if you want to store your results into gcp store, pass a bucket name ", default = None)
#Storing argument on variables
args = parser.parse_args()
tax_name = args.tax_name
librarysource = args.librarysource
specific_organisms = args.specific_organisms
bucket_name = args.bucket_name
#Call main function
if __name__ == '__main__':
    if tax_name != None:
        run_tax_big_query_to_csv = TaxBigQuery2CSV(tax_name,librarysource)
        run_tax_big_query_to_csv.get_sra_table_by_tax_name()
    if specific_organisms != None:
        run_organisms_big_query_to_csv = OrganismsBigQuery2CSV(specific_organisms ,librarysource)
        run_organisms_big_query_to_csv.get_sra_table_by_organisms()
    if bucket_name != None:
        run_storage = Data2Storage('main_bq_output.csv',bucket_name)
        run_storage.check_or_create_bucket()
        run_storage.upload_file_to_bucket()