import boto3
import boto3.session
from botocore.exceptions import ClientError
import xmltodict
import json
from dotenv import load_dotenv
import os

load_dotenv('awskeys.env')

ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_ACCESS_KEY')

os.environ['AWS_ACCESS_KEY_ID'] = ACCESS_KEY
os.environ['AWS_SECRET_ACCESS_KEY'] = SECRET_KEY

environments = {
            "live": {
                "endpoint": "https://mturk-requester.us-east-1.amazonaws.com",
                "preview": "https://www.mturk.com/mturk/preview",
                "manage": "https://requester.mturk.com/mturk/manageHITs",
                "reward": "0.00"
            },
            "sandbox": {
                "endpoint": "https://mturk-requester-sandbox.us-east-1.amazonaws.com",
                "preview": "https://workersandbox.mturk.com/mturk/preview",
                "manage": "https://requestersandbox.mturk.com/mturk/manageHITs",
                "reward": "0.00"
            },
    }

def create_hit(
        title = 'Sample HIT', 
        desc = 'This is a dummy HIT for testing purposes.',
        region = 'us-east-1',
        create_in_live = 'False'
        ):
    
    create_hits_in_live = create_in_live
    mturk_environment = environments["live"] if create_hits_in_live else environments["sandbox"]
    endpoint_url = mturk_environment['endpoint']
    sandbox_endpoint = "https://mturk-requester-sandbox.us-east-1.amazonaws.com"

    client = boto3.client(
        'mturk',
        endpoint_url=sandbox_endpoint,
        region_name=region,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )

    user_balance = client.get_account_balance()
    # In Sandbox this always returns $10,000. In live, it will be your acutal balance.
    print("Your account balance is {}".format(user_balance['AvailableBalance']))


    question_sample = open("mturkquestion.xml", "r").read()

    try:
        # creating a hit
        response = client.create_hit(
            Title=title,
            Description=desc,
            MaxAssignments=1,
            Reward=mturk_environment['reward'],
            AssignmentDurationInSeconds=3600,
            LifetimeInSeconds=86400,
            Question=question_sample
        )
        
        # Extract the HIT ID from the response
        hit_id = response['HIT']['HITId']
        print(f"HIT created successfully with HIT ID: {hit_id}")
        

        print ("\nYou can work the HIT here:")
        hit_type_id = response['HIT']['HITTypeId']
        workerlink = mturk_environment['preview'] + "?groupId={}".format(hit_type_id)
        print(workerlink)

        print("\nAnd see results here:")
        print(mturk_environment['manage'])
        
        return hit_id, workerlink
    
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None
    
    # Test that you can connect to the API by checking your account balance


def get_current_hits(check_for_live=False, region='us-east-1'):
    mturk_environment = environments["live"] if check_for_live else environments["sandbox"]
    endpoint_url = mturk_environment['endpoint']

    client = boto3.client(
        'mturk',
        endpoint_url=endpoint_url,
        region_name=region,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )
    hits = client.list_hits()
    if len(hits)>0:
        print("List of HITs:")
        for hit in hits['HITs']:
            print(f"HIT ID: {hit['HITId']}, Title: {hit['Title']}")
    else:
        print('No HITs previously present.')

# if __name__=='__main__':
#     hits = client.list_hits()

#     if len(hits)>0:
#         print("List of HITs:")
#         for hit in hits['HITs']:
#             print(f"HIT ID: {hit['HITId']}, Title: {hit['Title']}")
#     else:
#         print('No HITs previously present.')

#     # Call the function to create a HIT
#     hit_id = create_hit()

#     print(hit_id)

# create_hit()