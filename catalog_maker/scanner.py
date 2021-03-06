import os
import traceback

from catalog_maker import CONFIG, logging
from catalog_maker.catalog import create_catalog, get_files
from catalog_maker.database import DataBaseHandler

LOGGER = logging.getLogger(__file__)


class Scanner(object):
    def __init__(self, batch, project, force=False):
        self._batch = batch
        self._project = project
        self._force = force

        self._config = CONFIG[f"project:{project}"]

        # scan - error with scanning file/datset
        # write - error when writing to catalog
        self.rh = DataBaseHandler(
            table_name=f"{project.replace('-', '_')}_catalog_results"
        )

    def _id_to_directory(self, dataset_id):
        archive_dir = self._config["archive_dir"]
        return os.path.join(archive_dir, dataset_id.replace(".", "/"))

    def scan(self, dataset_id):
        LOGGER.info(f"Reading {dataset_id}")
        fpaths = get_files(dataset_id)

        for fpath in fpaths:

            if self._force and self.rh.get_result_status(fpath):
                # delete from db to run again
                LOGGER.info(f"Clearing from database: {fpath}")
                self.rh.delete_result(fpath)

            if self.rh.ran_successfully(fpath):
                LOGGER.info(f"Already converted to catalog: {fpath}")
                continue

            elif self.rh.get_result_status(fpath):
                # delete failure from db
                LOGGER.info(f"Clearing from database: {fpath}")
                self.rh.delete_result(fpath)

            LOGGER.info(f"Scanning file: {fpath}")

            try:
                content = create_catalog(self._project, dataset_id, fpath)

            except Exception:
                msg = f"Failed to extract content for: {fpath}"
                self._wrap_exception(fpath, msg, "scan")
                continue

            try:
                self._finalise(fpath, content)
                LOGGER.info(f"Finalised: {fpath}")

            except Exception:
                msg = f"Finalisation failed for: {fpath}"
                self._wrap_exception(fpath, msg, "write")
                continue

    def _finalise(self, fpath, content):
        self.rh.insert_success(fpath, content)
        LOGGER.info(f"Wrote entry for: {fpath}")

    def _wrap_exception(self, fpath, msg, error_type):
        error = f"{msg}:\n{traceback.format_exc()}"
        self.rh.insert_failure(fpath, error_type, error)
        LOGGER.error(f"FAILED TO COMPLETE FOR: {fpath}\n{error}")
