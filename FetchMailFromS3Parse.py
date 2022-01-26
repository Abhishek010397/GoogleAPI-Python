import json
import boto3
import re


BUCKET_NAME = 's3-Bucket-name'
word = str('Subject'+':'+' '+'Test')
pattern = re.compile(word)
first_word = str('<div'+' '+'dir'+'='+'"ltr">')
TAG_RE = re.compile(r'<[^>]+>')


def download_email(key):
    try:
        s3_source = boto3.client('s3')
        save_key = key.split('/', 1)[-1]
        s3_source.download_file(BUCKET_NAME, key, '/tmp/'+save_key)
        match_subject(save_key)
    except Exception as e:
        print(e)


def match_subject(key):
    try:
        index = 0
        f = open('/tmp/'+key, 'r')
        for line in f:
            index += 1
            if re.match(pattern, line):
                print("Matched Line is: ", line)
                get_message(key, index)
        f.close()
    except Exception as e:
        print(e)


def get_message(key, index):
    try:
        f = open('/tmp/'+key, 'r')
        for i, line in enumerate(f):
            print(line)
            if i > index:
                if line.startswith(first_word):
                    #Parsing ALL HTML Objects and Producing the clear body of the message
                    pure_message = TAG_RE.sub('', line)
                    print(pure_message)
        f.close()
    except Exception as e:
        print(e)


def lambda_handler(event, context):
    print(event)
    key = event['Records'][0]['s3']['object']['key']
    print(key)
    download_email(key)
