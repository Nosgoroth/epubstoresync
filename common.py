
import os, subprocess
from pushover import pushover
from configloader import config

def process_new_file(file, storeName):
    fn = os.path.basename(file)
    dirname = os.path.dirname(file)
    basefn, _ = os.path.splitext(fn)

    print("Newly downloaded file: %s" % basefn)

    cwd = os.getcwd()
    os.chdir(dirname)

    try:
        if "USE_SEND_TO_KINDLE" in config and config["USE_SEND_TO_KINDLE"]:
            fsize = os.stat(fn).st_size
            if fsize < config["KINDLE_MAX_FSIZE"]:
                print("Sending to kindle: %s" % basefn)
                
                cmd = config["SEND_TO_KINDLE_COMMAND"] + [fn]
                
                if "SEND_TO_KINDLE_LOGFILE" in config and config["SEND_TO_KINDLE_LOGFILE"]:
                    with open(config["SEND_TO_KINDLE_LOGFILE"], 'a') as logfile:
                        subprocess.call(cmd, stdout=logfile, stderr=logfile)
                else:
                    subprocess.call(cmd)
                
                pushover("[ESSYNC:%s] Sent to Kindle new epub: %s" % (storeName, basefn))
            else:
                pushover("[ESSYNC:%s] Downloaded large epub: %s" % (storeName, basefn))
        else:
            pushover("[ESSYNC:%s] Downloaded epub: %s" % (storeName, basefn))
    except:
        os.chdir(cwd)
        raise

    os.chdir(cwd)
