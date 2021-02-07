import boto3

BUCKET_NAME = 'koh-jx-s3-nusebucket'
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


# OTHER USEFUL FUNCTIONS

# # returns the unread pickle file
# def read_userdict_from_bucket():
#     object_key = 'userdict'
#     result = s3_client().get_object(Bucket = BUCKET_NAME, Key = object_key)
#     return result["Body"]


# if __name__ == '__main__':
    # create_bucket(BUCKET_NAME)
    # create_bucket_policy()
    # version_bucket_files()





# def create_bucket(bucket_name):
#     return s3_client().create_bucket(
#         Bucket=bucket_name,
#         CreateBucketConfiguration={'LocationConstraint': 'ap-southeast-1'}
#     )

# def create_bucket_policy():
#     bucket_policy = {
#         "Version": "2012-10-17",
#         "Statement": [
#             {
#                 "Sid": "AddPerm",
#                 "Effect": "Allow",
#                 "Principal": "*",
#                 "Action": ["s3:*"],
#                 "Resource": ["arn:aws:s3:::koh-jx-s3-nusebucket/*"]
#             }
#         ]
#     }

#     policy_string = json.dumps(bucket_policy)

#     return s3_client().put_bucket_policy(
#         Bucket = BUCKET_NAME,
#         Policy = policy_string
#     ) 


#Enable versioning of files; just do once
# To upload a new version, upload small file
# def version_bucket_files():
#     s3_client().put_bucket_versioning(
#         Bucket = BUCKET_NAME,
#         VersioningConfiguration = {
#             'Status': 'Enabled'
#         }
#     )


# def get_bucket_policy():
#     return s3_client().get_bucket_policy(Bucket=BUCKET_NAME)


# def list_buckets():
#     return s3_client().list_buckets()

# def get_bucket_encryption():
#     return s3_client().get_bucket_encryption(Bucket = BUCKET_NAME)