# foto/storages/backends/firebase.py

from django.core.files.storage import Storage
import firebase_admin
from firebase_admin import storage as fb_storage

class FirebaseStorage(Storage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bucket = fb_storage.bucket()

    def _save(self, name, content):
        blob = self.bucket.blob(name)
        blob.upload_from_file(content)
        return name

    def url(self, name):
        blob = self.bucket.blob(name)
        return blob.generate_signed_url(version='v4', expiration=3600, method='GET')

    def exists(self, name):
        blob = self.bucket.blob(name)
        return blob.exists()
