#!/usr/local/bin/python3

from EpubStoreKobo import process as kobo_process
from EpubStoreJnc import process as jnc_process
from common import process_new_file
from configloader import config
		
def main():
	if config["USE_KOBO"]:
		print()
		print("### KOBO ###")
		print()
		kobo_process()
	if config["USE_JNC"]:
		print()
		print("### JNC ###")
		print()
		jnc_process()

if __name__ == "__main__":
	#process_new_file("/Users/Nosgoroth/Dropbox (Personal)/reading/_epub/Kobo/Sankakuhead - Himouto! Umaru-chan Vol. 1.epub", 'asd')
	main()

