import boto3
from botocore.exceptions import ClientError

#  boto3 client for mturk
client = boto3.client('mturk', region_name='us-east-1')  

def create_hit():
    try:
        # creating a hit
        response = client.create_hit(
            Title='Sample HIT',
            Description='This is a dummy HIT for testing purposes.',
            MaxAssignments=1,
            Reward={'Amount': '0.50', 'CurrencyCode': 'USD'},
            AssignmentDurationInSeconds=3600,
            LifetimeInSeconds=86400,
            Question="""<?xml version="1.0" encoding="UTF-8"?>
            <QuestionForm xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/QuestionForm.xsd">
                <Question>
                    <QuestionIdentifier>Q1</QuestionIdentifier>
                    <IsRequired>true</IsRequired>
                    <QuestionContent>
                        <Text>
                            <![[Please enter your response here.]]>
                        </Text>
                    </QuestionContent>
                </Question>
            </QuestionForm>"""
        )
        
        # Extract the HIT ID from the response
        hit_id = response['HIT']['HITId']
        print(f"HIT created successfully with HIT ID: {hit_id}")
        
        return hit_id
    
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None

# Call the function to create a HIT
hit_id = create_hit()

if hit_id:
    hits = client.list_hits()
    print("List of HITs:")
    for hit in hits['HITs']:
        print(f"HIT ID: {hit['HITId']}, Title: {hit['Title']}")
