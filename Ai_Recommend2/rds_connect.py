def dict_to_query(dic):
    keys, vals = [], []

    for key, val in dic.items():
        if(val):
            keys.append(key)
            vals.append('\"'+str(val)+('\"')) 

    return ((', ').join(keys), (', ').join(vals))


def Insert_RDS(cus_id, text_data):
    import json
    import sys
    import logging
    import rds_config
    import pymysql
    import os
    #rds settings
    rds_endpoint  = rds_config.rds_endpoint
    name = rds_config.db_username
    password = rds_config.db_password
    db_name = rds_config.db_name
    table_name = rds_config.table_name

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Connect to RDS
    try:
        conn = pymysql.connect(host=rds_endpoint, user=name, passwd=password, db=db_name, connect_timeout=5)
        print('connected')
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        sys.exit(1)

    logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")


    #Init Table
    try:
        ### CREATE TABLE
        sql_create_option = 'Custommer_ID int PRIMARY KEY, Recommand_list varchar(500)'
        print('init table :',sql_create_option )
        with conn.cursor() as cur:
            cur.execute("create table if not exists "+table_name+" ( "+sql_create_option+" )")
            conn.commit()
        print('init table successed')
    except pymysql.MySQLError as e:
        logger.error("ERROR: Init Table Error")
        logger.error(e)
        sys.exit(2)

    #Item Insert
    data_keys = 'Custommer_ID, Recommand_list'
    data_vals = '\"' + str(cus_id)+'\", '+text_data
    print('insert into '+table_name+' ('+data_keys+') values ('+data_vals+')')

    try:
        with conn.cursor() as cur:
            cur.execute('insert into '+table_name+' ('+data_keys+') values ('+data_vals+')')
            conn.commit()
        print('Item Insert successed')
    except pymysql.MySQLError as e:
        print(e)
        with conn.cursor() as cur:
            print('update '+table_name+' set Recommand_list='+text_data+' where Custommer_ID='+str(cus_id))
            cur.execute('update '+table_name+' set Recommand_list='+text_data+' where Custommer_ID='+str(cus_id))
            conn.commit()
        print('Item Insert successed')
        