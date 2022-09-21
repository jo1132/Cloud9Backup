#config file containing credentials for RDS MySQL instance
# for test
import os

rds_endpoint = os.environ['RDS_ENDPOINT']
db_username = os.environ['USERNAME']
db_password = os.environ['PASSWORD']
db_name = os.environ['DB_NAME']
table_name = os.environ['TABLE_NAME']
