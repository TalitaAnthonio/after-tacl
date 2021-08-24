

import json
import bz2
import os
import pickle

path_to_file = './bigrams_singles_to_get_revised_context.json'
path_to_file_out = './bigrams_singles_to_get_revised_context_article.json'


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
        data[filename] = file_in_dict_format
    return data


def get_left_timestamp(res, upper_part, all_indexes):
    upper_part = list(reversed(upper_part))
    index_of_first_timestamp = 0
    for line_nr in upper_part:
        if "Timestamp" in res[line_nr]:
            index_of_first_timestamp = all_indexes.index(line_nr)
            break
    return index_of_first_timestamp


def get_right_timestamp(res, lower_part, all_indexes):
    index_of_first_timestamp = 0
    for line_nr in lower_part:
        if "Timestamp" in res[line_nr]:
            index_of_first_timestamp = all_indexes.index(line_nr)
            break
    return index_of_first_timestamp


def main():
    print("read file")
    # Read file here (format = a dict {key: {elements_from_wikihow} })

    with open(path_to_file, 'r') as json_in:
        wikihow_dataset = json.load(json_in)

    # contains all the files in dict format
    files_in_dict_format = get_file_to_dict_format()

    with open("files_in_dict_format_filtered_train_set.pickle", "rb") as pickle_in:
        files_in_dict_format = pickle.load(pickle_in)

    """
    #print("save to file ....")
    #with open("files_in_dict_format_revised_context.pickle", "wb") as pickle_in:
    #    pickle.dump(files_in_dict_format, pickle_in)
    collection_with_articles = {}
    counter = 0
    for key, value in wikihow_dataset.items():
        counter += 1
        print(
            "Fake Processing Bar {0}/{1}".format(counter, len(wikihow_dataset)))
        # get base_article
        # get the line number where the base sentence is
        # previously: line_number_for_source = wikihow_dataset[key]["Base_Nr"]
        line_number_for_source = wikihow_dataset[key]["Target_Line_Nr"]
        filename = "{0}.bz2".format(wikihow_dataset[key]["Filename"])

        # make a list of the linenrs starting from the base sentence
        line_nrs_in_article = [line_nr for line_nr,
                               value in files_in_dict_format[filename].items()]
        # find the index of the base_line_nr
        index_of_base_line_nr = line_nrs_in_article.index(
            line_number_for_source)

        # excluding the sentence itself.
        from_base_to_top = line_nrs_in_article[:index_of_base_line_nr]
        from_base_to_bottom = line_nrs_in_article[index_of_base_line_nr+1:]
        top_index = get_left_timestamp(
            files_in_dict_format[filename], from_base_to_top, line_nrs_in_article)
        lower_index = get_right_timestamp(
            files_in_dict_format[filename], from_base_to_bottom, line_nrs_in_article)

        # exclude the base sentence
        article_dict = {}
        article_indexes_left = line_nrs_in_article[top_index:index_of_base_line_nr]
        current_line = files_in_dict_format[filename][line_nrs_in_article[index_of_base_line_nr]]

        article_dict["left_context"] = [
            files_in_dict_format[filename][line_nr] for line_nr in article_indexes_left]
        article_dict["current_line"] = [current_line]

        article_indexes_right = line_nrs_in_article[index_of_base_line_nr +
                                                    1:lower_index+1]
        if article_indexes_right:
            article_dict["right_context"] = [
                files_in_dict_format[filename][line_nr] for line_nr in article_indexes_right]
        else:
            article_indexes_right = line_nrs_in_article[index_of_base_line_nr+1:]
            article_dict["right_context"] = [
                files_in_dict_format[filename][line_nr] for line_nr in article_indexes_right]

        collection_with_articles[key] = wikihow_dataset[key]
        collection_with_articles[key].update({"Revised_Article": article_dict})

    with open(path_to_file_out, 'w') as json_out:
        json.dump(collection_with_articles, json_out)

    """
main()
