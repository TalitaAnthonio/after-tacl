
import json
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.translate.bleu_score import sentence_bleu
from progress.bar import Bar
import re
import argparse
import pdb
from pprint import pprint
import spacy


tagger = spacy.load("en_core_web_sm")

def normalize_punkt(text):
    """replace unicode punctuation by ascii"""
    text = re.sub('[\u2010\u2043]', '-', text)  # hyphen
    text = re.sub('[\u2018\u2019]', "'", text)  # single quotes
    text = re.sub('[\u201c\u201d]', '"', text)  # double quotes
    return text


def format_new(string): 
    line = normalize_punkt(string)
    line = re.sub(r'<.*?>', r'', string)
    line = re.sub(r'\[\[Image:.*?\]\]', r'', line)
    line = line.lstrip('-*\\0123456789. ')
    line = re.sub(r'\[ \[[^\[]*?\|(.*?)\] \]', r'\1', line)

    # apply to deal with isues caused by my sentence splitter 
    line = re.sub(r' .$', r'.', line )
    line = re.sub(r' ,', r',', line)
    return line 


def tokenize_with_spacy(list_with_string_sentences):
    return [token.text for token in tagger(list_with_string_sentences)]


def remove_html_tags(line):
    """Remove html tags from a string"""
    # remove HTML tags
    line = re.sub(r"<[^>]*>", "", line)

    # remove images
    line = re.sub(r"\[\[Image:[^]]*]]", "", line)
    line = re.sub(r"\[\[[^|]*\|([^]]*)]]", "", line) 
    line = re.sub(r"__[A-Z]+__", "", line)

    return line 

def sentence_splitter(document, sent=False):
    """
      Sentence splitter to deal with bullet items in texts.

    """
    # Tokenize per 'sub sentence list' instead of joining (to keep markdown headers separated)
    if not document:
        return []

    if len(document) == 1:
        tokenized_doc = sent_tokenize(remove_html_tags(' '.join(document)))
    else:
        tokenized_doc = [' '.join(sent_tokenize(
            remove_html_tags(elem))) for elem in document]

    if len(tokenized_doc) == 1 or not tokenized_doc:
        return tokenized_doc
    else:
        sentences = iter(tokenized_doc)
        # Flatten sentences: (https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists)
        # sentences = (
        #    sentence for sub_sentences in unflattened_sentences for sentence in sub_sentences)

        # currently because base_tokenized has
        # ''2 . Be patient -> space between bullet point
        pattern = re.compile(r"^[0-9]+\s+\.$")
        merged_item_sents = []

        sentence = next(sentences)
        while sentence:
            if re.match(pattern, sentence):
                try:
                    next_sentence = next(sentences)
                except StopIteration:
                    break
                merged = f"{sentence} {next_sentence}"
                merged_item_sents.append(merged)
            else:
                merged_item_sents.append(sentence)

            try:
                sentence = next(sentences)
            except StopIteration:
                sentence = False
                break
        return merged_item_sents


def sentence_splitter_new(document, use_sent=False): 
    if use_sent: 
        tokenized_doc_current = sent_tokenize(remove_html_tags(' '.join(document)))
        return tokenized_doc_current
    else: 
        tokenized_doc = []
        for elem in document: 
            if elem.startswith('##'):
               tokenized_doc.append(elem)
            elif len(elem) == 1: 
                tokenized_doc.append(elem)
            else: 
                tokenized_sent = sent_tokenize(remove_html_tags(elem))
                tokenized_doc += tokenized_sent
        return tokenized_doc


def correct_sentence_splitter(sentence_splitted_par, use_current=True): 
    """
        Input: list of sentences 
    """
    if use_current: 
        new_list = []
        sentence_splitted_par_iter = iter(range(len(sentence_splitted_par)))
        for sent_index in sentence_splitted_par_iter: 
            #print(sentence_splitted_par[sent_index])
            # check if there is a single element in the list of form '<num>.'
            # if this is the case, concatenate that element with the next element in sentence_splitted_par. 
            if re.match(r"^[0-9]+.$", sentence_splitted_par[sent_index]) or re.match(r"^[0-9] +.$", sentence_splitted_par[sent_index]):
               # the "if" "else" deal with this annoying case ("INDEX  2562")
               if sent_index != len(sentence_splitted_par)-1:
                    if len(sentence_splitted_par[sent_index]) == 3: 
                        merged_sent = "{0}{1}".format(sentence_splitted_par[sent_index][:-1], sentence_splitted_par[sent_index][-1]) + ' ' +  sentence_splitted_par[sent_index+1]
                     
                        new_list.append(merged_sent)
                        next(sentence_splitted_par_iter)
                    else: 
                        merged_sent = sentence_splitted_par[sent_index] + ' ' +  sentence_splitted_par[sent_index+1]
                        new_list.append(merged_sent)
                        next(sentence_splitted_par_iter)
                
               else: 
                    new_list += sentence_splitted_par[sent_index:]
            else: 
                new_list.append(sentence_splitted_par[sent_index])
               
        return new_list
    else: 
        new_list = []
        sentence_splitted_par_iter = iter(range(len(sentence_splitted_par)))
        for sent_index in sentence_splitted_par_iter: 
            #print(sentence_splitted_par[sent_index])
            # check if there is a single element in the list of form '<num>.'
            # if this is the case, concatenate that element with the next element in sentence_splitted_par. 
            if re.match(r"^[0-9]+.$", sentence_splitted_par[sent_index]):
               # the "if" "else" deal with this annoying case ("INDEX  2562")
               if sent_index != len(sentence_splitted_par)-1:
                    merged_sent = sentence_splitted_par[sent_index] + ' ' +  sentence_splitted_par[sent_index+1]
                    new_list.append(merged_sent)
                    next(sentence_splitted_par_iter)
               else: 
                    new_list += sentence_splitted_par[sent_index:]
            else: 
                new_list.append(sentence_splitted_par[sent_index])
               
        return new_list

class SentenceSplitter: 

    def __init__(self, use_sent=False): 
        self.use_sent = use_sent 
    
    def tokenize(self, document): 
        tokenized_text = sentence_splitter_new(document, self.use_sent)
        # if use_current = true, then use the sentence 
        corrected_tokenized_text = correct_sentence_splitter(tokenized_text, self.use_sent)
        return corrected_tokenized_text 


def check_if_sentence_in_context(context, sent): 


    formatted_sents_in_context = [format_new(sent) for sent in context]
    try: 
        index_of_sent = formatted_sents_in_context.index(sent)
        return index_of_sent   
    except ValueError: 
        return []


def get_matching_sent_context(context, sent):
    """
        Use this function to get closest match to a source_line or target_line in a paragraph.
        Tokenized: whether the input sent should be tokenized or not (nesecarry when the sent is a string.)
        use_sent_from_context: if true, then the matched sent will be taken in the final representation.

        Context: the tokenized current_line 
    """
    bleu_scores = []
    sents_in_article = []


    index_of_sentence_in_context = check_if_sentence_in_context(context, sent) 
    if index_of_sentence_in_context != []:
        # then do something with the index 
    
        return {

            "before_sent": context[:index_of_sentence_in_context],
            "current": [context[index_of_sentence_in_context]],
            "after_sent": context[index_of_sentence_in_context+1:], 
            "match_found": "yes", 
            "index_of_sentence_in_context": index_of_sentence_in_context
        }

    else:  
        for tokenized_sentence in context:
            # print(tokenized_sentence)
            #reference = [word_tokenize(elem)]
            # the reference is the tokenized sentence here

            tokenized_sentence = tokenize_with_spacy(tokenized_sentence)
            score = sentence_bleu(tokenized_sentence, sent)
            

            bleu_scores.append(score)
            sents_in_article.append(tokenized_sentence)
        index_of_max_bleu = bleu_scores.index(max(bleu_scores))
        matched_sent = sents_in_article[index_of_max_bleu]

        # current might have items to the left or right already.
        left_items = context[:index_of_max_bleu]
        current = context[index_of_max_bleu]
        right_items = context[index_of_max_bleu+1:]

        if re.match(r"^[0-9]+.$", ' '.join(matched_sent)):
            matched_sent = current + right_items[1]
            right_items = right_items[1:]

        return {

            "before_sent": left_items,
            "current": [' '.join(matched_sent)],
            "after_sent": right_items, 
            "match_found": "no", 
            "index_of_sentence_in_context": index_of_max_bleu
        }

def correct_splitter(context): 

    # correct the problem with remaining *.
    formatted = []
    for i in range(len(context)): 
        formatted = context 
        if context[i].startswith('#'): 
            pattern = re.findall(r"[0-9]+.$", context[i])
            if pattern != [] and i != len(context)-1: 
            # remove the number from the line 
                formatted[i] = re.sub(r'[0-9]+.$', r'', context[i])
                formatted[i+1] = " ".join(pattern) + " " + context[i+1]
                if i < len(context): 
                    i += 1 

        else: 
            formatted.append(context[i])
    
    
    # fix the remaining problem with the stars 
    context_new = []
    for sent in formatted: 
    
        if " * " in sent: 
            sent = sent.replace(" *", "\n*")
            context_new.extend(sent.split("\n"))
            
        else: 
            context_new.append(sent)

    return context_new



if __name__ == "__main__":
    pass
