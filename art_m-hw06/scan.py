import sys
from pathlib import Path

image_files = list()
video_files = list()
doc_files = list()
audio_files = list()
archives = list()
folders = ["images", "documents", "audio", "video", "archives", "others"]
others = list()
extensions = set()
unknown_extensions = set()

registered_extensions = {
    'JPEG': image_files,
    'PNG': image_files,
    'JPG': image_files,
    'SVG': image_files,
    'AVI': video_files,
    'MP4': video_files,
    'MOV': video_files,
    'MKV': video_files,
    'DOC': doc_files,
    'DOCX': doc_files,
    'TXT': doc_files,
    'PDF': doc_files,
    'XLSX': doc_files,
    'PPTX': doc_files,
    'MP3': audio_files,
    'OGG': audio_files,
    'WAV': audio_files,
    'AMR': audio_files,
    'ZIP': archives,
    'GZ': archives,
    'TAR': archives
}

def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def scan(folder):
    for item in folder.iterdir():
        if item.is_dir() and item.name not in folders:
            if item.name not in registered_extensions.keys():  #('JPEG', 'PNG', 'JPG', 'TXT', 'DOCX', 'ARCHIVE', 'OTHER')
                # folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        if not extension:
            pass
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(extension)
            except KeyError:
                unknown_extensions.add(extension)
                others.append(extension)