import logging
import os
import subprocess
from pathlib import Path

from craft_parts.utils import file_utils

logger = logging.getLogger(__name__)


def download_slices(stage_slices, slices_dir):

    os.makedirs(slices_dir, exist_ok=True)
    for slice_ in stage_slices:
        logger.debug("Downloading chisel slice %s", slice_)
        chisel_bin = "chisel"
        slice_download_cmd = [chisel_bin, "cut", "--root", str(slices_dir), slice_]
        try:
            subprocess.run(
                slice_download_cmd,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError as err:
            raise


def install_slices(download_path: Path, install_path: Path):
    """Installs previously downloaded slices"""
    file_utils.link_or_copy_tree(download_path.as_posix(), install_path.as_posix())
