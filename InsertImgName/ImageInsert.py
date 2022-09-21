def get_price():
    import random
    return round(random.randrange(1, 100000), -1)
    

import pandas as pd
import pymysql
# read cvs
PATH = '/home/ec2-user/environment/InsertImgName/'
csv_path = '/home/ec2-user/environment/image_save/marketkurly_Crawling3.csv'

img_df = pd.read_csv(csv_path)
img_df.columns = ['Image_ID', 'Item_Name', 'Ori_img_URL', 'Detail_img_URL']

print(img_df.head())

################################################################################
import rds_config
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

print("SUCCESS: Connection to RDS MySQL instance succeeded")
print(len(img_df))



#Init Table

### CREATE TABLE
sql_create_option = 'Image_ID int PRIMARY KEY, Item_Name varchar(1000) NOT NULL, Item_Price int NOT NULL, Image varchar(50), Info_Image varchar(50)'
print('init table :',sql_create_option )
with conn.cursor() as cur:
    cur.execute("create table if not exists "+table_name+" ("+sql_create_option+")")
    conn.commit()
print('init table successed')

    

# Item INSERT

data_keys = 'Image_ID, Item_Name, Item_Price, Image, Info_Image'
print([img_df.iloc[0][keyword] for keyword in img_df.columns.tolist()[:2]])


error_list = []
for i in range(len(img_df)):
    A, B, _ , _= tuple(img_df.iloc[i][keyword] for keyword in img_df.columns.tolist())
    A = str(A)
    B = B.replace('\'', '')
    C = get_price()
    D = 'https://img-cf.kogoon.me/product/' + A + '.jpg'
    E = 'https://img-cf.kogoon.me/product_info/' + A + '.jpg'
    data_vals = '{}, \'{}\', {}, \'{}\', \'{}\''.format(A, B, C, D, E)
    print('insert into '+table_name+' ('+data_keys+') values('+data_vals+')')

    try:
        with conn.cursor() as cur:
            cur.execute('insert into '+table_name+' ('+data_keys+') values('+data_vals+')')
            conn.commit()
        print("Added items from RDS MySQL table")
    
    except pymysql.err.InternalError as e:
    	print(e)
    	error_list.append(i)

print(error_list)
