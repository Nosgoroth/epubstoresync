
import os, sys, glob, subprocess
from common import process_new_file
from configloader import config


class EpubStoreKobo():

    @staticmethod
    def process():
        before_files = glob.glob(os.path.join(config["KOBO_OUTPUT_DIR"], "*.epub"))
        print("Files already downloaded: %d" % (len(before_files)))
        EpubStoreKobo.kobodl()
        after_files = glob.glob(os.path.join(config["KOBO_OUTPUT_DIR"], "*.epub"))
        new_files = [x for x in after_files if x not in before_files]
        print("New files: %d" % (len(new_files)))
        for file in new_files:
            process_new_file(file, "Kobo") 

    @staticmethod
    def kobodl():
        subprocess.call(config["KOBODL_COMMAND"] + [
            "book", "get", "--get-all",
            "--output-dir", config["KOBO_OUTPUT_DIR"]
        ])
