import json
import boto3
import re


BUCKET_NAME = 'smtp-reacredence-forward'
word_list = ['Subject: Test*']
pattern = '(?:% s)' % '|'.join(word_list)
word1=str('Content-Type:'+' '+'text/plain')
pattern1=re.compile(word1)
a= []

def download_email(key):
    try:
        print("{} function has been called".format("download_email()"))
        s3_source = boto3.client('s3')
        save_key=key.split('/', 1)[-1]
        s3_source.download_file(BUCKET_NAME,key,'/tmp/'+save_key)
        match_subject(save_key)
    except Exception as e:
        print(e)
        
def match_subject(key):
    try:
        print("{} function has been called".format("match_subject()"))
        index=0
        f=open('/tmp/'+key, 'r')
        for line in f:
            index+=1
            if re.match(pattern,line):
                print("Matched Line is: ",line)
                get_message(key,index)
        f.close()
    except Exception as e:
        print(e)

def get_message(key,index):
    try:
        idx=0
        print("{} function has been called".format("get_message()"))
        f=open('/tmp/'+key, 'r')
        for i,line in enumerate(f):
            idx+=1
            if i > index:
                # print(line)
                if re.match(pattern1,line):
                    extract_message(key,idx)
        f.close()
    except Exception as e:
        print(e)
        
def extract_message(key,idx):
    try:
        print("{} function has been called".format("extract_message()"))
        f=open('/tmp/'+key, 'r')
        for i,line in enumerate(f):
            if i > idx:
                if line != "\n":
                    if line.startswith('--'):
                        break
                    else:
                        a.append(line)
        f.close()
    except Exception as e:
        print(e)
        
def convert_to_string(a):
    try:
        print("{} function has been called".format("convert_to_string()"))
        str1 = "" 
        for ele in a: 
            str1 += ele
        print("Message is: ",str1)
        # post_message(str1)
    except Exception as e:
        print(e)
        
def post_message(message):
    try:
        print("{} function has been called".format("post_message()"))
        url = 'https://chat.googleapis.com/v1/spaces/AA/messages/'
        bot_message = {
            'text' : message
        }
        message_headers = {'Content-Type': 'application/json; charset=UTF-8'}
        http_obj = Http()
        response = http_obj.request(
            uri=url,
            method='POST',
            headers=message_headers,
            body=dumps(bot_message),
        )
        print(response)
    except Exception as e:
        print(e)
    
def lambda_handler(event, context):
    try:
        print(event)
        key = event['Records'][0]['s3']['object']['key']
        print(key)
        download_email(key)
        convert_to_string(a)
    except Exception as e:
        print(e)

