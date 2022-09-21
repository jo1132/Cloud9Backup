import boto3
import pandas as pd
import urllib.request
import time

# S3 Client
s3 = boto3.client('s3')
bucket_name = 'ai-item-image'
Ori_folder_name = 'Ori_Images'
Det_folder_name = 'Images'

# read cvs
PATH = '/home/ec2-user/environment/image_save/'
csv_path = '/home/ec2-user/environment/image_save/marketkurly_Crawling3.csv'
img_df = pd.read_csv(csv_path)
img_df.columns = ['Image_ID', 'Item_Name', 'Ori_img_URL', 'Detail_img_URL']

# for each row
for i in range(len(img_df)):
    # get Image
    ori_url = img_df.iloc[i]['Ori_img_URL']
    det_url = img_df.iloc[i]['Detail_img_URL']
    
    ori_save_path = PATH + Ori_folder_name + '/' + str(i) + ".jpg"
    det_save_path = PATH + Det_folder_name +'/' + str(i) + ".jpg"
    
    urllib.request.urlretrieve(ori_url, ori_save_path)
    urllib.request.urlretrieve(det_url, det_save_path)
    
    
    # Upload Image to S3
    s3.upload_file(ori_save_path, bucket_name, Ori_folder_name + '/' + str(i) + ".jpg")
    s3.upload_file(det_save_path, bucket_name, Det_folder_name +'/' + str(i) + ".jpg")
    
    # maybe sleep 1 sec
    time.sleep(1)
