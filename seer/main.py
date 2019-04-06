from typing import List

import os
import subprocess

import botocore
import boto3


BUCKET_NAME: str = 'ocry-czl'

"""Returns an iterator through all the items in a S3 bucket.
"""
def bucket_items(bucket: str):
    client: botocore.client = boto3.client('s3')
    paginator = client.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket):
        if page['KeyCount'] > 0:
            for item in page['Contents']:
                yield item

if __name__ == '__main__':
    for item in bucket_items('ocry-czl'):
        key: str = item['Key']
        if not key.endswith('.pdf'):
            continue
        pdf_name: str = key.split('/')[-1]
        no_extension_name: str = pdf_name[:-len('.pdf')]
        tiff_name: str = no_extension_name + '.tiff'
        txt_name: str = no_extension_name + '.txt'
        boto3.resource('s3').Bucket(BUCKET_NAME).download_file(key, pdf_name)
        subprocess.Popen([
            'convert',
            '-density', '96',
            '-depth', '8',
            '-quality', '85',
            pdf_name,
            tiff_name
        ], stdout=subprocess.PIPE).wait()
        subprocess.Popen([
            'tesseract',
            tiff_name,
            no_extension_name,
            '-l', 'ron'
        ]).wait()
        boto3.resource('s3').meta.client.upload_file(
            txt_name, 
            BUCKET_NAME, 
            'txt/' + txt_name)
        os.remove(pdf_name)
        os.remove(tiff_name)
        os.remove(txt_name)
