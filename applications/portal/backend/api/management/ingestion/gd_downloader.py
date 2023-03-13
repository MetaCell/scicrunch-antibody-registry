import os
import gdown
import logging
import zipfile


class GDDownloader:
    def __init__(self, file_id, dest):
        self.file_id = file_id
        self.dest = dest

    def get_filename(self):
        return os.path.join(self.dest, 'tmp_download.zip')

    def download(self, extract=True):
        if not os.path.exists(self.dest):
            os.makedirs(self.dest)
            logging.info("Downloading %s to %s.", self.file_id, self.get_filename())
            gdown.download(id=self.file_id, output=self.get_filename())
            logging.info("Download completed.")
            if extract:
                self.extract()
            return True

        logging.info('%s download skipped: file already present', self.dest)
        return False

    def extract(self):
        with zipfile.ZipFile(self.get_filename(), 'r') as zip_ref:
            zip_ref.extractall(self.dest)
        self.clean()

    def clean(self):
        os.remove(self.get_filename())
