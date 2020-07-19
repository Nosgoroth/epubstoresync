# Readme

## Setup

Uses [this fork of kobo-book-downloader](https://github.com/subdavis/kobo-book-downloader).

To setup:

```sh
kobodl user add
```

## Usage

Just run:

```sh
python3 epubstoresync.py
```

It'll download new books and automatically send to kindle if within size limit. If not, you can open the ebook in Calibre's `ebook-edit.app` and run `Tools > Compress images losslessly` with a lossy compression.
