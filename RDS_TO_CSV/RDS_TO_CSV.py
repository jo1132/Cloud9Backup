import pandas as pd
import pymysql
import rds_config

rds_endpoint  = rds_config.rds_endpoint
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
table_name = rds_config.table_name
    
conn = pymysql.connect(host=rds_endpoint, user=name, passwd=password, db=db_name, connect_timeout=5)

query = 'SELECT * FROM '+table_name

df = pd.read_sql_query(query, conn)
df.to_csv('/home/ec2-user/environment/RDS_TO_CSV/Custommer_list.csv', index=False)