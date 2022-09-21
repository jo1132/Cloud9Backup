#config file containing credentials for RDS MySQL instance
# for test
import os
rds_endpoint = os.environ['RDS_ENDPOINT']
db_username = os.environ['USERNAME']
db_password = os.environ['PASSWORD']
db_name = os.environ['DB_NAME']
table_name = os.environ['TABLE_NAME']

rds_keys={
    'Item_id': ['', 'varchar(200)'],
    #'Item_URL': ['', 'varchar(200)'],
    'Item_key': ['',  'varchar(200) PRIMARY KEY'],
    '계란': ['0', 'boolean default 0'],
    '우유': ['0', 'boolean default 0'],
    '땅콩': ['0', 'boolean default 0'],
    '견과류': ['0', 'boolean default 0'],
    '밀': ['0', 'boolean default 0'],
    '갑각류': ['0', 'boolean default 0'],
    '대두': ['0', 'boolean default 0'],
    '메밀': ['0', 'boolean default 0'],
    '쇠고기': ['0', 'boolean default 0'],
    '돼지고기': ['0', 'boolean default 0'],
    '닭고기': ['0', 'boolean default 0'],
    '생선': ['0', 'boolean default 0'],
    '과일': ['0', 'boolean default 0'],
    'Nutrition': ['', 'varchar(1000)'],
    'Ingredient' : ['', 'varchar(2000)']
}
