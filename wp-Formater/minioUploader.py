# coding=utf-8
from minio import Minio
from minio.error import InvalidResponseError
from minio.commonconfig import Tags
import os
import time
import configparser
import hashlib

def toBoolean(str):
    if "true" == str.lower():
        return True
    else:
        return False

def getFileMD5(file_path):
    with open(file_path, 'rb') as fp:
        data = fp.read()
    return hashlib.md5(data).hexdigest()

def getExternName(str):
    if '.' in str:
        return str.split('.')[-1]
    else:
        return ""

def minioGetObjectNameList(client, bucket):
    objectNameList = []
    if not client.bucket_exists(bucket):
        print("Bucket: {} not exists".format(bucket))
    else:
        objectList = client.list_objects(bucket)
        for object in objectList:
            objectNameList.append(object.object_name)
    return objectNameList

def uploadImage(clientObj, image_path, label):
    client = clientObj[0]
    url = clientObj[1]
    bucket = clientObj[2]
    try:
        if not client.bucket_exists(bucket):
            print("Bucket: {} not exists".format(bucket))
            return None
        image_name = os.path.split(image_path)[-1]
        minio_image_name = getFileMD5(image_path) + "." + getExternName(image_name)
        if minio_image_name in minioGetObjectNameList(client, bucket):
            print("File: {} already existed, skipped".format(minio_image_name))
        else:
            print(client.fput_object(bucket, minio_image_name, image_path))
        tags = client.get_object_tags(bucket, minio_image_name)
        tags[label] = time.strftime("%Y-%m-%d",time.localtime(time.time()))
        client.set_object_tags(bucket, minio_image_name, tags)
        print("image tags: {}".format(tags))
        return url + "/" + bucket + "/" + minio_image_name
    except InvalidResponseError as err:
        print(err)
        return None
    except FileNotFoundError as err:
        print(err)
        return None

def loadMinioClient(config_path):
    con = configparser.ConfigParser()
    con.read(config_path, encoding='utf-8')
    sections = con.sections()
    if 'minio' not in sections:
        print('No config!')
        exit(1)

    items = dict(con.items('minio'))
    secure = toBoolean(items['secure'])
    endpoint = items['host']
    bucket = items['bucket_name']
    url = endpoint
    if secure :
        url = 'https://' + url
    else :
        url = 'http://' + url
    return (Minio(   endpoint = items['host'],
                    access_key = items['access_key'],
                    secret_key = items['secret_key'],
                    secure = toBoolean(items['secure'])), url, bucket)
    