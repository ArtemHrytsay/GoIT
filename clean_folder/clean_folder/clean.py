import re
import sys
import shutil
from pathlib import Path


UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()

def normalize(name: str) -> str:
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', '_', new_name)
    return f"{new_name}.{'.'.join(extension)}"



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



def handle_file(path, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize(path.name))

def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = normalize(path.name.replace(".zip", ''))

    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass

def main(folder_path):
    print(folder_path)
    scan.scan(folder_path)

    for file in image_files:
        handle_file(file, folder_path, 'images')

    for file in audio_files:
        handle_file(file, folder_path, "audio")

    for file in video_files:
        handle_file(file, folder_path, "video")

    for file in doc_files:
        handle_file(file, folder_path, "documents")

    for file in others:
        handle_file(file, folder_path, "others")

    for file in archives:
        handle_archive(file, folder_path, "archives")

    remove_empty_folders(folder_path)



if __name__ == '__main__':
    path = sys.argv[1]
    print(f'Start in {path}')

    folder = Path(path)
    main(folder.resolve())