# python amt_api.py config 

import boto3 
import configparser
import sys 
import datetime
import pdb 

def connect_mturk(CONFIG):
    region_name = CONFIG['default']['region']
    aws_access_key_id=CONFIG['default']['id']
    aws_secret_access_key = CONFIG['default']['key']
    endpoint_url = CONFIG['default']['sandbox']

    mturk_client = boto3.client(
        'mturk',
        endpoint_url=endpoint_url,
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    sys.stderr.write("Connected")
    return mturk_client


def parse_time(date_string):
    """
        date_string = "2019-04-17 11:41:34+02:00"
         t = parse_time(date_string)
        datetime(2019, 4, 17)
    """
    if isinstance(date_string, datetime.datetime):
        return date_string
    date_string = [int(a) for a in date_string.split()[0].split("-")]
    return datetime.datetime(date_string[0], date_string[1], date_string[2])


def get_all_hits(mturk):
    """
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk.html#MTurk.Client.list_hits
    """
    # hit_responses' fields: NextToken NumResults HITs ResponseMetadata
    all_hit_ids = []
    hit_responses = mturk.list_hits()
    #while True:
    for hit in hit_responses["HITs"]:
        all_hit_ids.append(hit["HITId"])
        hit_next = hit_responses.get('NextToken', None)
        if hit_next is None:
            break 
        else: 
            print('in else')
            print(hit_next)
            hit_responses = mturk.list_hits(NextToken=hit_next)
    print(all_hit_ids)
    return all_hit_ids


def get_assignments(mturk, hitid, statuses):
    """"
        Returns a key 
        [{'AssignmentId': '39RP059MEI9H98SFWSOY5ZGYFKKBM0', 'WorkerId': 'A2TLGGIQBNMK61', 'HITId': '3X2LT8FDHWYSP2QS7G5AYBW89VAW87', 
        'AssignmentStatus': 'Submitted', 'AutoApprovalTime': datetime.datetime(2021, 8, 12, 8, 59, 56, tzinfo=tzlocal()), 
        'AcceptTime': datetime.datetime(2021, 8, 9, 8, 59, 50, tzinfo=tzlocal()), 
        'SubmitTime': datetime.datetime(2021, 8, 9, 8, 59, 56, tzinfo=tzlocal()), 
        'Answer': '<?xml version="1.0" encoding="ASCII"?><QuestionFormAnswers xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2005-10-01/QuestionFormAnswers.xsd"><Answer><QuestionIdentifier>plausibility</QuestionIdentifier><FreeText>4</FreeText></Answer></QuestionFormAnswers>'}]
    """
    aresponse = mturk.list_assignments_for_hit(
                    HITId=hitid)
    if aresponse["NumResults"] < 1:
        print("\nNo assignments yet for HIT %s." % (str(hitid)))
        return []
    
    anext = aresponse['NextToken']
    assignments = aresponse['Assignments']

    print("\nget Hit",hitid)

    while anext:
        nresponse = mturk.list_assignments_for_hit(
                    HITId=hitid,NextToken=anext,AssignmentStatuses=statuses)
        print(nresponse.keys())
        nextassign = nresponse['Assignments']
        assignments += nextassign

        if 'NextToken' in nresponse:
            anext = nresponse['NextToken']
        else:
            anext = None
            
    return assignments

if __name__ == '__main__': 
    CONFIG = configparser.ConfigParser()
    CONFIG.read(sys.argv[1])


    # connect to amazon 
    client = connect_mturk(CONFIG)

    print(client.get_account_balance()['AvailableBalance'])
    hit_ids = get_all_hits(client)
    for hit_id in hit_ids: 
        assignments = get_assignments(client, hit_id, ["Submitted"])
        assert len(assignments) == 1 or len(assignments) == 0 
        assignment_with_parsed_time = {}

        if assignments != []: 
            for key, _ in assignments[0].items(): 
                print(assignments[0])
                assignment_with_parsed_time[key] = assignments[0][key]
                assignment_with_parsed_time["AutoApprovalTime"] = parse_time(assignments[0]["AutoApprovalTime"]) 

            print(assignment_with_parsed_time)

