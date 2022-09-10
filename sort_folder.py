from pathlib import Path
from string import punctuation as punct
import os
import shutil
import sys


CYRILLIC_SYMBOLS = " абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = (
    "_", "a", "b", "v", "g", "d", "e", "e", "j", "z",
    "i", "j", "k", "l", "m", "n", "o", "p", "r", "s",
    "t", "u", "f", "h", "ts", "ch", "sh", "sch", "",
    "y", "", "e", "yu", "ya", "je", "i", "ji", "g"
)
IGNORE_FOLDERS = ("image", "video", "documents", "audio", "archives")
TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


EXTENSIONS = {
    "image": ['JPEG', 'PNG', 'JPG', 'SVG'],
    "video": ['AVI', 'MP4', 'MOV', 'MKV'],
    "documents": ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'PPT'],
    "audio": ['MP3', 'OGG', 'WAV', 'AMR'],
    "archives": ['ZIP', 'GZ', 'TAR']
}


# func which return new_filename path
def normalize(main_path, file_name):
    name, ext = file_name.stem, file_name.suffix
    name = name.translate(TRANS)
    for ch in name:
        if ch in punct:
            name = name.replace(ch, "_")

    new_filename = f"{name}{ext}"
    return main_path.joinpath(new_filename)


def sort_folder(main_path):
    # create an files iterator
    all_files = main_path.iterdir()

    for item in all_files:

        # rename file
        file = normalize(main_path, item)
        if not os.path.exists(file):
            os.rename(item, file)

        # find a key (which folder we will create) by suffix
        for key, value in EXTENSIONS.items():

            # check if our file is file
            if file.is_file:

                # find what type file is
                if file.suffix[1:].upper() in value:

                    # find a path where will be a new folder
                    new_folder_path = main_path.joinpath(key)

                    # if folder is not exist - create it
                    if not os.path.exists(new_folder_path):
                        os.makedirs(new_folder_path)

                    # create a new path where file will be after moving
                    file_newpath = new_folder_path.joinpath(
                        file.name)

                    # if file is archive - unpack him in the separate folder with the same name(except ext)
                    if key == "archives":
                        extract_folder_path = new_folder_path.joinpath(
                            file.stem)

                        # if folder is not exist - create it
                        if not os.path.exists(extract_folder_path):
                            os.makedirs(extract_folder_path)

                        # unpack archive
                        shutil.unpack_archive(
                            file, extract_folder_path)

                    # move file
                    shutil.move(file, file_newpath)

            # check if file is folder whith is not in IGRONE_FOLDERS
            if file.is_dir() and file.name not in IGNORE_FOLDERS:

                # if folder is empty - delete him
                if not os.listdir(file):
                    shutil.rmtree(file)

                # if not empty - recursively call our function again
                else:
                    sort_folder(file)


def main():
    if len(sys.argv) < 2:
        print('Enter path to folder which should be cleaned')
        exit()

    BASE_DIR = Path(sys.argv[1])

    if not (os.path.exists(BASE_DIR) and Path(BASE_DIR).is_dir()):
        print('Path incorrect')
        exit()

    sort_folder(BASE_DIR)


if __name__ == '__main__':
    exit(main())
