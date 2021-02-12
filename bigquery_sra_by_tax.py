import pandas_gbq
import google.auth, argparse
from google.cloud import bigquery
from google.cloud import bigquery_storage

def gb_to_csv(sql,project_id):
    df = pandas_gbq.read_gbq(sql, project_id=project_id)
    df.columns = ["experiment",
                "sra", 
                "platform",
                "librarysource",
                "assay_type",
                "organism",
                "collection_date_sam",
                "geo_loc_name_country_calc",
                "geo_loc_name_country_continent_calc",
                "geo_loc_name_sam"
                ]
    df.to_csv('main_bq_output.csv', index=False, header=True, sep=',')

credentials, your_project_id = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
bqclient = bigquery.Client(credentials=credentials, project=your_project_id,)
bqstorageclient = bigquery_storage.BigQueryReadClient(credentials=credentials)

class TaxBigQuery2CSV():
    def __init__(self, tax_name, librarysource):
        self.tax_name = tax_name
        self.librarysource = librarysource

    
    def get_sra_table_by_tax_name(self,project_id=your_project_id):
        if self.librarysource == None:
            sql = f"""
            SELECT m.experiment, m.acc, m.platform, m.librarysource, m.assay_type, m.organism, m.collection_date_sam , m.geo_loc_name_country_calc, m.geo_loc_name_country_continent_calc, m.geo_loc_name_sam 
            FROM `nih-sra-datastore.sra.metadata` m, `nih-sra-datastore.sra_tax_analysis_tool.tax_analysis` tax
            WHERE m.acc = tax.acc
            and tax.name = '{self.tax_name}'
            and m.consent = 'public'
            """
            gb_to_csv(sql=sql,project_id=project_id)
        else:
            if len(self.librarysource) > 1:
                sql = f"""
                SELECT m.experiment, m.acc, m.platform, m.librarysource, m.assay_type, m.organism, m.collection_date_sam , m.geo_loc_name_country_calc, m.geo_loc_name_country_continent_calc, m.geo_loc_name_sam 
                FROM `nih-sra-datastore.sra.metadata` m, `nih-sra-datastore.sra_tax_analysis_tool.tax_analysis` tax
                WHERE m.acc = tax.acc
                and tax.name = '{self.tax_name}'
                and m.librarysource	 in {tuple(self.librarysource)}
                and m.consent = 'public'
                """
                gb_to_csv(sql=sql,project_id=project_id)
            else:
                sql = f"""
                SELECT m.experiment, m.acc, m.platform, m.librarysource, m.assay_type, m.organism, m.collection_date_sam , m.geo_loc_name_country_calc, m.geo_loc_name_country_continent_calc, m.geo_loc_name_sam 
                FROM `nih-sra-datastore.sra.metadata` m, `nih-sra-datastore.sra_tax_analysis_tool.tax_analysis` tax
                WHERE m.acc = tax.acc
                and tax.name = '{self.tax_name}'
                and m.librarysource	 = '{self.librarysource[0]}'
                and m.consent = 'public'
                """
                gb_to_csv(sql=sql,project_id=project_id)

class OrganismsBigQuery2CSV():
    def __init__(self, specific_organisms, librarysource):
        self.specific_organisms = specific_organisms
        self.librarysource = librarysource
        specific_organisms_file = open(self.specific_organisms,'r')
        specific_organisms_file_content = specific_organisms_file.read()
        global specific_organisms_list 
        specific_organisms_list = specific_organisms_file_content.split('\n')

    def get_sra_table_by_organisms(self,project_id=your_project_id):
        if self.librarysource == None:
            sql = f"""
            SELECT experiment, acc, platform, librarysource, assay_type, organism, collection_date_sam , geo_loc_name_country_calc, geo_loc_name_country_continent_calc, geo_loc_name_sam 
            FROM `nih-sra-datastore.sra.metadata`
            WHERE organism in {tuple(specific_organisms_list[:-1])}
            and consent = 'public'
            """
            gb_to_csv(sql=sql,project_id=project_id)
        else:
            if len(self.librarysource) > 1:
                sql = f"""
                SELECT experiment, acc, platform, librarysource, assay_type, organism, collection_date_sam , geo_loc_name_country_calc, geo_loc_name_country_continent_calc, geo_loc_name_sam 
                FROM `nih-sra-datastore.sra.metadata`
                WHERE organism in {tuple(specific_organisms_list[:-1])}
                and librarysource in {tuple(self.librarysource)}
                and consent = 'public'
                """
                gb_to_csv(sql=sql,project_id=project_id)
            else:
                sql = f"""
                SELECT experiment, acc, platform, librarysource, assay_type, organism, collection_date_sam , geo_loc_name_country_calc, geo_loc_name_country_continent_calc, geo_loc_name_sam 
                FROM `nih-sra-datastore.sra.metadata`
                WHERE organism in {tuple(specific_organisms_list[:-1])}
                and librarysource = '{self.librarysource[0]}'
                and consent = 'public'
                """
                gb_to_csv(sql=sql,project_id=project_id)