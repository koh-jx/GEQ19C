import boto3

BUCKET_NAME = 'insert s3 bucket name here'
KEY = "userdict.pickle"

def s3_client():
    s3 = boto3.client('s3')
    """ :type : boto3.s3"""
    return s3

# pickle file already saved
def upload_userdict():
    s3_resource = boto3.resource('s3')
    s3_resource.Object(BUCKET_NAME, KEY).put(Body=open(KEY, 'rb'))

# saves pickle file to userdict.pickle
def read_userdict_from_bucket():
    s3 = boto3.resource('s3')
    with open(KEY, 'wb') as data:
        s3.Bucket(BUCKET_NAME).download_fileobj(KEY, data)