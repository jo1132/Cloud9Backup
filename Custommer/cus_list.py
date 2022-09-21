
import pandas as pd
import pymysql
# read cvs
PATH = '/home/ec2-user/environment/Custommer/'
csv_path = PATH+'total_Custommer.csv'
img_df = pd.read_csv(csv_path, index_col='Unnamed: 0')
img_df.columns = ['Items', 'Custommer_ID', 'Custommer_Name', 'Allergy_List']

def str_list_to_list(x):
    return (', ').join([item[1:-1] for item in x[1:-1].split(', ')])
    
cus_list = pd.DataFrame(columns=['Custommer_ID', 'Custommer_Name'])
cus_list['Custommer_ID'] = img_df['Custommer_ID']
cus_list['Custommer_Name'] = img_df['Custommer_Name']
cus_list = cus_list.sort_values(['Custommer_ID'])
cus_list = cus_list.drop_duplicates()



# add Allergy
def get_allergy(x):
    import random
    allergy_list = ['계란', '우유', '땅콩', '견과류', '밀', '갑각류', '대두', '메밀', '쇠고기', '돼지고기', '닭고기', '생선']
    return (', ').join([random.choice(allergy_list) for i in range(random.randrange(0, 4))])

cus_list['Allergy_List'] = cus_list['Custommer_ID'].apply(get_allergy)

################################################################################
import rds_config
rds_endpoint  = rds_config.rds_endpoint
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
table_name = 'Custommer_list'


# Connect to RDS
try:
    conn = pymysql.connect(host=rds_endpoint, user=name, passwd=password, db=db_name, connect_timeout=5)
    print('connected')
except pymysql.MySQLError as e:
    print(e)

print("SUCCESS: Connection to RDS MySQL instance succeeded")


#Init Table

### CREATE TABLE

sql_create_option = 'Custommer_ID int not null PRIMARY KEY, Custommer_Name varchar(50) not null, Allergy_List varchar(50)'
print('init table :',sql_create_option )
with conn.cursor() as cur:
    cur.execute("create table if not exists "+table_name+" ("+sql_create_option+")")
    conn.commit()
print('init table successed')

    
# Item INSERT

data_keys = (', ').join(cus_list.columns.tolist())

error_list = []
print(len(cus_list))

for i in range(len(cus_list)):
    A, B, C = tuple(cus_list.iloc[i][keyword] for keyword in cus_list.columns.tolist())
    data_vals = '{}, \'{}\', \'{}\''.format(A, B, C)
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
