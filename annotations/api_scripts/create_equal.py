import boto3
import time
import json
import configparser
import logging
import os
import sys
    
import amt_api

SCRIPTDIR = os.path.abspath(os.path.dirname(sys.argv[0]))


def make_qualification(mturk, questionqual_xml):
    with open(os.path.join(SCRIPTDIR, questionqual_xml), 'r') as myfile:
        question=myfile.read()
    with open(os.path.join(SCRIPTDIR, './answerqual.xml'), 'r') as myfile:
        answer=myfile.read()
        
    print(question)
    print(answer)
        
    response = mturk.create_qualification_type(
        Name='QualificationTest',
        Keywords='qualification test',
        Description='Please do this simplified version of our HITs before participating.',
        QualificationTypeStatus='Active',
        Test=question,
        AnswerKey=answer,
        TestDurationInSeconds=300,
    )
    print(response)
    
    del response['QualificationType']['CreationTime']
    
    with open("protectionqual.json", 'w') as outfile:
        json.dump(response, outfile)
        
    return True

def update_qualification(mturk, qualtypeID, questionqual_xml):
    with open(os.path.join(SCRIPTDIR, questionqual_xml), 'r') as myfile:
        question=myfile.read()
    with open(os.path.join(SCRIPTDIR, './answerqual.xml'), 'r') as myfile:
        answer=myfile.read()
        
    print(question)
    print(answer)
        
    response = mturk.update_qualification_type(
        QualificationTypeId=qualtypeID,
        Description='Please do this simplified version of our HITs before participating.',
        QualificationTypeStatus='Active',
        Test=question,
        AnswerKey=answer,
        TestDurationInSeconds=300,
    )
    print(response)
    del response['QualificationType']['CreationTime']
    
    with open("protectionqual.json", 'w') as outfile:
        json.dump(response, outfile)
        
    return True

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Please give a me a config file as argument")
        sys.exit()
    else:
        configfile = sys.argv[1]

    data_path = os.path.dirname(configfile)

    log_dir = os.path.join(data_path, "logs")
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    moment = time.strftime("%Y-%b-%d_%H_%M_%S", time.localtime())
    logging.basicConfig(filename=os.path.join(log_dir, moment+'.log'),level=logging.INFO)


    CONFIG = configparser.ConfigParser()
    CONFIG.read(configfile)
    print(CONFIG)
    logging.info("config file: "+configfile)
    questionqual_xml = './questionqual_round1.xml'

    MTURK = amt_api.connect_mturk(CONFIG)
    
    if "QualificationTest" in CONFIG["qualification"]:
        sys.stdout.write("Config contains qualification protection (id %s). Updating qualification..." % (CONFIG["qualification"]["QualificationTest"]))
        logging.info("Updating qualification:")
        logging.info(CONFIG["qualification"]["QualificationTest"])
        update_qualification(MTURK, CONFIG["qualification"]["QualificationTest"], questionqual_xml)
        print("Qualification {0} updated.".format(CONFIG["qualification"]["QualificationTest"]))
    else:
        make_qualification(MTURK, questionqual_xml)
        print("Qualification created.")
    
