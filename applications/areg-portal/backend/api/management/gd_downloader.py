import os

from google_drive_downloader import GoogleDriveDownloader
import logging


class GDDownloader:

    def __init__(self, file_id, dest):
        self.file_id = file_id
        self.dest = dest

    def get_filename(self):
        return os.path.join(self.dest, 'tmp_download.zip')

    def download(self):
        if not os.path.exists(self.dest):
            os.makedirs(self.dest)
            logging.info("Downloading %s to %s.", self.file_id, self.get_filename())
            GoogleDriveDownloader.download_file_from_google_drive(file_id=self.file_id,
                                                                  dest_path=self.get_filename(),
                                                                  unzip=True)
            logging.info("Download completed.")
            self.clean()
        else:
            logging.info('%s download skipped: file already present', self.dest)

    def clean(self):
        os.remove(self.get_filename())
