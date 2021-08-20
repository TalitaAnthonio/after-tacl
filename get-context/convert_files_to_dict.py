# Puts all the files in a dictionary format. 
# "id_of_the_article": {line_nr: "the text on the line"}

import json
import bz2
import os
import pickle

def get_file_to_dict_format(directory='filenames'):
    """
      Param: 
        directory: name of the directory with the bz2 files 
      Returns: 
        Dict where {"filename": complete file with line nrs}

    """
    data = {}
    counter = 0
    for filename in os.listdir(directory):
        counter += 1
        print(
            "Processing filename {0}/{1}".format(counter, len(os.listdir(directory))))
        path = "./{0}/{1}".format(directory, filename)
        with bz2.open(path, "rt") as bz_file:
            file_in_dict_format = {}
            for counter, line in enumerate(bz_file, 1):
                if line != '\n':
                    file_in_dict_format[counter] = line.strip('\n').strip()
        data[filename.strip(".txt.bz2")] = file_in_dict_format
    return data


def main():
    print("read files") 
    files_in_dict_format = get_file_to_dict_format()

    with open("files_in_dict_format_filtered_train_set.pickle", "wb") as pickle_out:
        files_in_dict_format = pickle.dump(files_in_dict_format, pickle_out)

main()