
import pandas as pd
import pymysql
# read cvs
PATH = '/home/ec2-user/environment/Custommer/'
csv_path = PATH+'total_Custommer.csv'
img_df = pd.read_csv(csv_path, index_col='Unnamed: 0')
img_df.columns = ['Items', 'Custommer_ID', 'Custommer_Name', 'allergy']
img_df.drop(['allergy'], axis=1)

def str_list_to_list(x):
    return (', ').join([item[1:-1] for item in x[1:-1].split(', ')])
    
img_df['Items'] = img_df['Items'].apply(str_list_to_list)



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
sql_create_option = []
for k, v in rds_config.rds_keys.items():
    sql_create_option.append(k+' '+v[1])
sql_create_option = (', ').join(sql_create_option)
print('init table :',sql_create_option )
with conn.cursor() as cur:
    cur.execute("create table if not exists "+table_name+" ("+sql_create_option+")")
    conn.commit()
print('init table successed')

    
# Item INSERT

data_keys = (', ').join(img_df.columns.tolist()[:3])
print([img_df.iloc[0][keyword] for keyword in img_df.columns.tolist()])

error_list = []
for i in range(len(img_df)):
    A, B, C , _= tuple(img_df.iloc[i][keyword] for keyword in img_df.columns.tolist())
    data_vals = '\'{}\', {}, \'{}\''.format(A, B, C)
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

