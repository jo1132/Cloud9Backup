def dict_to_query(dic):
    keys, vals = [], []

    for key, val in dic.items():
        if(val):
            keys.append(key)
            vals.append('\"'+str(val)+('\"')) 

    return ((', ').join(keys), (', ').join(vals))


def Insert_RDS(text_data, ITEM_KEY, bucket):
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

    # dict_keys(['Item_id', 'Item_URL', 'Item_key', '계란', '우유', '땅콩', '견과류', '밀', '갑각류', '대두', '메밀', '육류', '생선', '과일', 'Nutirition', 'Ingredient']
    item_dict = {k:v[0] for k, v in rds_config.rds_keys.items()}

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
        sql_create_option = []
        for k, v in rds_config.rds_keys.items():
            sql_create_option.append(k+' '+v[1])
        sql_create_option = (', ').join(sql_create_option)
        print('init table :',sql_create_option )
        with conn.cursor() as cur:
            cur.execute("create table if not exists "+table_name+" ( "+sql_create_option+" )")
            conn.commit()
        print('init table successed')
    except pymysql.MySQLError as e:
        logger.error("ERROR: Init Table Error")
        logger.error(e)
        sys.exit(2)


    #Set Item_ID
    item_dict['Item_id'] = ITEM_KEY.split('/')[-1]
    item_dict['Item_key'] = item_dict['Item_id'].split('.')[0]

    '''
    #Init ROW
    data_keys, data_vals = dict_to_query(item_dict)
    try:
        with conn.cursor() as cur:
            cur.execute('insert into '+table_name+' ('+data_keys+') values('+data_vals+') WHERE NOT EXIST (SELECT Item_id FROM '+table_name+' WHERE Item_id = '+item_dict['Item_id']+';')
            conn.commit()
        print("Added items from RDS MySQL table")

    except:
        logger.error("ERROR: Init Row Error")
        sys.exit(3)
    '''

    # Item INSERT
    ## fit text_data to item_dict
    for k, v in text_data.allergy_dict.items():
        item_dict[k] = v
    
    item_dict['Nutrition'] = ('|').join(text_data.nutrition_list)
    item_dict['Ingredient'] = ('|').join(text_data.ingredient_list)
    print(item_dict)
    
    data_keys, data_vals = dict_to_query(item_dict)
    print('insert into '+table_name+' ('+data_keys+') values('+data_vals+')')

    try:
        with conn.cursor() as cur:
            cur.execute('insert into '+table_name+' ('+data_keys+') values('+data_vals+')')
            conn.commit()
        print("Added items from RDS MySQL table")
    
    except pymysql.err.InternalError as e:
    	code, msg = e.args
    	logger.error("ERROR: Insert Fail. Code:",code," message:", msg)
    	sys.exit(2)
