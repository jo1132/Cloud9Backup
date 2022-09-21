#config file containing credentials for RDS MySQL instance
# for test
import os
rds_endpoint = 'rds_endpoint'
db_username = 'db_username'
db_password = 'db_password'
db_name = 'db_name'
table_name = 'table_name'

rds_keys={
    'Items': ['', 'varchar(1000) not null'],
    'Custommer_ID': [0, 'int not null'],
    'Custommer_Name': ['', 'varchar(50) not null']
}
