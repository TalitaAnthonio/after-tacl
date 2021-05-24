
# path_to_data = normal json file. 
# example usage: 
# python coreference_stanza.py --FileOut "../data/trigrams_part3.json" --CorefAlgorithm statistical --Port http://localhost:9001
# python run_coreference_parser.py --FileOut "./new.json" --CorefAlgorithm statistical --Port http://localhost:9002
# python run_coreference.py --FileOut "./dev_with_coref_for_fillers.json" --CorefAlgorithm statistical --Port http://localhost:9002


import os
import json 
import pickle 
import nltk 
import argparse 
from nltk.tokenize import sent_tokenize
os.environ["CORENLP_HOME"] = "stanford-corenlp-4.1.0"
import pdb 
from stanza.server import CoreNLPClient, TimeoutException


# ------------------- SET UP ARGPARSE ----------------------
ap = argparse.ArgumentParser(description="Run coreference")
ap.add_argument("--CorefAlgorithm", type=str, default='neural', help="the coreference algorithm that needs to be used: neural, statistical or deterministic")
ap.add_argument("--FileOut", type=str, help="the name of the file to write out")
ap.add_argument("--Port", type=str, help="Port to use")
args = vars(ap.parse_args())
coref_algorithm = args['CorefAlgorithm']
path_to_write_out = args['FileOut']
port_to_use = args['Port']
# ------------------- SET UP ARGPARSE ----------------------

path_to_data =  "coreference_analysis_predictions_dev_set.json" 

class EasyCoreNLP: 
    # client_annotate_text = client.annotate(text)
    # ann = client.annotate(text)
    def __init__(self, client_annotate_text): 
        self.parser_output = client_annotate_text


    @property 
    def sents(self): 
        """
            Returns a list with the sentence parsed sents to test if it doesn't use other sentence splitter. 
            
        """
        sents = []
        for i in range(len(self.parser_output.sentence)): 
            sent_tokens = [elem.word for elem in self.parser_output.sentence[i].token]
            sents.append(sent_tokens)
        return sents 

    @property 
    def coref_dict(self): 
        chains = self.parser_output.corefChain 
        chain_dict=dict()
        for index_chain,chain in enumerate(chains):
            chain_dict[index_chain]={}
            chain_dict[index_chain]['ref']=''
            chain_dict[index_chain]['mentions']=[{'mentionID':mention.mentionID,
                                                'mentionType':mention.mentionType,
                                                'number':mention.number,
                                                'gender':mention.gender,
                                                'animacy':mention.animacy,
                                                'beginIndex':mention.beginIndex,
                                                'endIndex':mention.endIndex,
                                                'headIndex':mention.headIndex,
                                                'sentenceIndex':mention.sentenceIndex,
                                                'position':mention.position,
                                                'ref':'',
                                                'tokenized_sent': '', 
                                                } for mention in chain.mention ]

        counter = 0  
        for k,v in chain_dict.items():
            counter +=1 
            # a list with mentions 
            mentions=v['mentions']
            # mentions: 'mentions': [{'mentionID': 4, 'mentionType': 
            # 'PRONOMINAL', 'number': 'SINGULAR', 'gender': 'MALE', 'animacy': 'ANIMATE', 'beginIndex': 1, 'endIndex': 2, 'headIndex': 1, 'sentenceIndex': 0, 'position': 5, 'ref': ''}
            for mention in mentions:
                # [mention['sentenceIndex']].token[mention['beginIndex']:mention['endIndex']]
                index_of_sentence_with_mention = mention['sentenceIndex']
                # token[mention['beginIndex']:mention['endIndex'] takes the indexes of this range 

                words_list = self.parser_output.sentence[index_of_sentence_with_mention].token[mention['beginIndex']:mention['endIndex']]
                
                mention['tokenized_sent'] = [elem.word for elem in self.parser_output.sentence[index_of_sentence_with_mention].token]  
                mention['ref']=[t.word for t in words_list]
        return chain_dict 


with open(path_to_data, "r") as json_in:
    dataset = json.load(json_in)


def main(): 
    with CoreNLPClient(annotators=['tokenize','ssplit','pos','parse', 'depparse','coref'], timeout=45000, properties={'annotators': 'coref', 'coref.algorithm' : coref_algorithm, 'ssplit.eolonly': True, 'maxCharLength': -1}, memory='4G', lang='en', be_quiet=True) as client:
        print("annotate the text")
        print("use coref algorithm {0}".format(coref_algorithm))

        # for elem in json.lines 
        
        counter = 0 
        total = len(dataset.keys())
        with open(path_to_write_out, "w") as json_out: 
            for key, _ in dataset.items():
                counter += 1
                print("{0} out of {1}".format(counter, total))
                

                # --------------------------------------------
                context = dataset[key]["par"].rstrip('\n')

                coreference_dict_for_fillers = {"id": key}

                for fillerid, _ in dataset[key]["fillers"].items(): 
                    # TODO: add different name for the filler. 

                    text = context + dataset[key]["fillers"][fillerid]["sentence"]
    

                    try: 
                        ann = client.annotate(text)
                        results = EasyCoreNLP(ann)
                        coreference_dict_for_filler= {"coref": results.coref_dict, "sents": results.sents}
                    except Exception as E: 
                        print(E)
                        coreference_dict_for_filler = {"coref": "empty", "sents": "empty"}
                    
                    coreference_dict_for_fillers[fillerid] = coreference_dict_for_filler
                    
                    # next checkpoint: check hoe de dict eruit ziet. 
                    # ----------------------------------------


                json_out.write(json.dumps(coreference_dict_for_fillers, default=str) + '\n')


main()
