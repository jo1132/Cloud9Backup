import boto3
import pandas as pd
import urllib.request
import time
import pymysql
import os

start = time.time()

'''
### All Crawling Image Upload
'''
# S3 Client
s3 = boto3.client('s3')
bucket_name = 'ai-item-image'
Ori_folder_name = 'Ori_Images'
Det_folder_name = 'Images'

# read cvs
PATH = '/home/ec2-user/environment/Movie/'
csv_path = '/home/ec2-user/environment/Movie/marketkurly_Crawling3.csv'
img_df = pd.read_csv(csv_path)
img_df.columns = ['Image_ID', 'Item_Name', 'Ori_img_URL', 'Detail_img_URL']

print('총 이미지 {}장'.format([len(img_df)]))
print('마지막 이미지 :', img_df.iloc[-1]['Image_ID'])

os.makedirs(PATH+Ori_folder_name, exist_ok=True)
os.makedirs(PATH+Det_folder_name, exist_ok=True)
time.sleep(3)
for i in range(len(img_df)):
    print(i, img_df.iloc[i]['Item_Name'])
'''
start = time.time()
# for each row Update
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
    
    print(i, img_df.iloc[i]['Item_Name'])


'''
### SQL Response
'''
import pymysql
import time
import rds_config

#rds settings
rds_endpoint  = rds_config.rds_endpoint
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
table_name = rds_config.table_name

# Connect to RDS
try:
    conn = pymysql.connect(host=rds_endpoint, user=name, passwd=password, db=db_name, connect_timeout=5)
    print('connected')
except pymysql.MySQLError as e:
    print(e)


# Get columns
query = 'show columns from '+table_name+';' 
with conn.cursor() as cur:
    cur.execute(query)
    conn.commit()
result = cur.fetchall()

columns = {item[0] : 0 for item in result}
col_list = list(columns.keys())


# Select 97.jpg in RDS
while True:
    query = 'SELECT * FROM '+table_name+' WHERE Item_key=96;'
    print(query)
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()

        result = cur.fetchone()
        if not result:
            print('Still Processing...')
            time.sleep(1)
            continue
        for i, data in enumerate(result):
            columns[col_list[i]] = data
        break
    
    except pymysql.err.InternalError as e:
    	print('Still Processing...')
    	time.sleep(1)

for k, v in columns.items():
    print(k+' : '+str(v))
print("Processing time :", round(time.time() - start, 2))
'''