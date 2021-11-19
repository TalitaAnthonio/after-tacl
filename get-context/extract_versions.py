

import json
import bz2
import os
import pickle
import pdb 

SUBSET = "../test-set/test_set_all_info_filtered_predictions.json"
ARTICLES_IN_DICT_FORMAT = './files_in_dict_format_filtered_test_set.pickle'
FILEOUT = "filtered_set_test_articles.json"

with open(SUBSET, "r") as json_in: 
     subset = json.load(json_in)

with open(ARTICLES_IN_DICT_FORMAT, "rb") as pickle_in: 
     articles_in_dict_format = pickle.load(pickle_in)



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


    collection_with_articles = {}
    counter = 0 
    for key, _ in subset.items():
        counter +=1 
        print(counter)
        
        line_number_for_base = subset[key]["BaseNr"]
     

        filename = subset[key]["filename"].strip(".txt")

        if filename in articles_in_dict_format.keys(): 
        # make a list of the lines starting from the base sentence 
        
            line_nrs_in_article = [line_nr for line_nr, value in articles_in_dict_format[filename].items()]
            

            # find the index of the base_line_nr
            index_of_base_line_nr = line_nrs_in_article.index(line_number_for_base)

            
            # get the index of the timestamps 
                    
            from_base_to_top = line_nrs_in_article[:index_of_base_line_nr]
            from_base_to_bottom = line_nrs_in_article[index_of_base_line_nr+1:]
            top_index = get_left_timestamp(
                articles_in_dict_format[filename], from_base_to_top, line_nrs_in_article)
            lower_index = get_right_timestamp(
                articles_in_dict_format[filename], from_base_to_bottom, line_nrs_in_article)
            
            # collect the article in a dictionary
            article_dict = {}
            # get text from base sentence to timestamp (left)
            article_indexes_left = line_nrs_in_article[top_index:index_of_base_line_nr]
            left_context = [articles_in_dict_format[filename][line_nr] for line_nr in article_indexes_left]
            
        
            # get the text that is on the line of the base sentence 

            current_line = articles_in_dict_format[filename][line_nrs_in_article[index_of_base_line_nr]]

            article_dict["left_context"] = [articles_in_dict_format[filename][line_nr] for line_nr in article_indexes_left]
            article_dict["current_line"] = [current_line]

            article_indexes_right = line_nrs_in_article[index_of_base_line_nr +
                                                        1:lower_index+1]

            if article_indexes_right:
                article_dict["right_context"] = [
                    articles_in_dict_format[filename][line_nr] for line_nr in article_indexes_right]
            else:
                article_indexes_right = line_nrs_in_article[index_of_base_line_nr+1:]
                article_dict["right_context"] = [
                    articles_in_dict_format[filename][line_nr] for line_nr in article_indexes_right]

            collection_with_articles[key] = subset[key]
            collection_with_articles[key].update({"BaseArticle": article_dict})
            collection_with_articles[key].update(subset[key])
        

        with open(FILEOUT, 'w') as json_out:
            json.dump(collection_with_articles, json_out)


main()