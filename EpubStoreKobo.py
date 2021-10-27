
import os, sys, glob, subprocess
from common import process_new_file
from configloader import config


def process():
    before_files = glob.glob(os.path.join(config["KOBO_OUTPUT_DIR"], "*.epub"))
    print("Books already downloaded: %d" % (len(before_files)))
    if config["KOBO_PREVENT_CONSOLE_OUTPUT"]:
        print("Retrieving books...")
    kobodl()
    after_files = glob.glob(os.path.join(config["KOBO_OUTPUT_DIR"], "*.epub"))
    new_files = [x for x in after_files if x not in before_files]
    if len(new_files) == 0:
        print("No new books available")
        return
    print("New books: %d" % (len(new_files)))
    print()

    for file in new_files:
        print("Downloaded new book: %s" % file)
        process_new_file(file, "Kobo")
        print()


def kobodl():
    out = subprocess.DEVNULL if config["KOBO_PREVENT_CONSOLE_OUTPUT"] else subprocess.STDOUT
    subprocess.call(
        config["KOBODL_COMMAND"] + [
            "book", "get", "--get-all",
            "--output-dir", config["KOBO_OUTPUT_DIR"]
        ],
        stdout=out,
        stderr=out
    )
