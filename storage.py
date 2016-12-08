from google.cloud import storage

class Storage:

    def __init__(self, bucket_name):
        self.storage_client = storage.Client()
        self.bucket_name = bucket_name
        

    def upload_blob(self, content, destination_name):
        bucket = self.storage_client.get_bucket(self.bucket_name)
        blob = bucket.blob(destination_name)
        blob.upload_from_string(content, "text/plain")
