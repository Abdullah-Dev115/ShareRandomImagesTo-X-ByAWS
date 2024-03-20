import random
import tweepy
import boto3

# Enter your Twitter (X) API tokens below
bearer_token = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
consumer_key = 'XXXXXXXXXXXXXXXXXXXXXXXXX'# API Key
consumer_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXX' # API Secret Token
access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXX'

# Enter your AWS credentials and S3 bucket name
aws_access_key_id = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
aws_secret_access_key = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
s3_bucket_name = 'XXXXXXXXXXXXXXXXXXXXXXXXX'

# Initialize AWS S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

# Initialize Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

client = tweepy.Client(
    bearer_token,
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    wait_on_rate_limit=True,
)

def fetch_random_image_from_s3():
    # List objects in the S3 Bucket
    response = s3_client.list_objects_v2(Bucket=s3_bucket_name)

    if 'Contents' in response:
        # Extract filenames
        keys = [obj['Key'] for obj in response['Contents']]

        # Choose random image (S3 Bucket Object)
        random_key = random.choice(keys)

        # Download the object to a temporary file
        temp_file_path = '/tmp/' + random_key
        s3_client.download_file(s3_bucket_name, random_key, temp_file_path)

        return temp_file_path

def post_image():
    image_path = fetch_random_image_from_s3()
    if image_path:
        media = api.media_upload(image_path)
        return media.media_id_string
    else:
        return None

# Do not change this variable name
def lambda_handler(event, context):
    text_in_the_post = ""
    media_id = post_image()
    if media_id:
        client.create_tweet(text=text_in_the_post, media_ids=[media_id])
        print(f"""
-----------------------------------------------------------------------
The Post has been sent!
Media ID : {media_id}
-----------------------------------------------------------------------
        """)

# Define lambda handler (don't change this!)
lambda_handler.lambda_handler = lambda_handler
