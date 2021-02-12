from google.cloud import storage

client = storage.Client()    

class Data2Storage():
    def __init__(self, filename, bucket_name):
        self.filename = filename
        self.bucket_name = bucket_name

    def check_or_create_bucket(self):
        global BUCKET
        BUCKET = client.bucket(self.bucket_name)
        if BUCKET.exists():
            BUCKET = client.get_bucket(self.bucket_name)
        else:
            bucket_name = self.bucket_name
            BUCKET = client.create_bucket(bucket_name)

    def upload_file_to_bucket(self):
        filename = self.filename
        blob = BUCKET.blob(self.filename)
        blob.upload_from_filename(self.filename)