import os
import json
import sys
from struct import pack
import urllib.parse
import boto3

import pandas as pd
import pymysql
import numpy as np
#import rds_config
import rds_connect
cus_id = 9
rds_endpoint  = 'rds_endpoint'
name = 'name'
password = 'password'
db_name = 'db_name'

  
def text_cleaning(text):
    text_list = []
    for item in text.split(', '):
        item = item.strip('[')
        item = item.strip(']')
        item = item.strip('\'')
        text_list.append(item)
    return text_list
    
    
def get_Orderlist(conn, table_name, cus_id):
  sql="select Items from "+table_name+" where Custommer_ID="+str(cus_id)
  result_list = pd.read_sql_query(sql,conn).values

  text = []
  for result in result_list:
    text += text_cleaning(result[0])

  # Drop duplicate
  text = set(text)
  return (', ').join(list(text))


def get_Allergy_list(conn, table_name, cus_id):
  sql="select Allergy_List from "+table_name+" where Custommer_ID="+str(cus_id)
  result_list = pd.read_sql_query(sql,conn).values
  
  print(result_list)
  result_list = sum(result_list, [])
  
  if(result_list):
    return result_list
  else:
    return []
      
def get_Item_df(conn, table_name):
  sql="select * from "+table_name
  result = pd.read_sql_query(sql,conn)
  result['Ingredient'] = result['Ingredient'].apply(lambda x: x.replace('|', ', '))
  return result

def get_Data_Count(df):
  from sklearn.feature_extraction.text import TfidfVectorizer
  vect = TfidfVectorizer()
  return vect.fit_transform(df['items'])
  
def get_Cosine_Similarity(matrix):
  from sklearn.metrics.pairwise import cosine_similarity
  item_custommer_similarity = cosine_similarity(matrix, matrix)
  item_custommer_similarity = item_custommer_similarity.argsort()[:, ::-1]
  return item_custommer_similarity[0]
  
  
#def handler(event, context):
conn = pymysql.connect(host=rds_endpoint, user=name, passwd=password, db=db_name, connect_timeout=5)

# Get Order items
Order_items = get_Orderlist(conn, 'Order_Table', cus_id)

Item_df = get_Item_df(conn, 'Item')

dump = pd.DataFrame(data=[[-1, Order_items]], columns=['Item_key', 'Ingredient'])
cus_item_df = pd.concat([dump, Item_df])
cus_item_df = pd.concat([cus_item_df['Item_key'], cus_item_df['Ingredient']], axis=1)
cus_item_df.columns=['Item_key', 'items']

item_custommer_matrix = get_Data_Count(cus_item_df)

item_custommer_sorted = get_Cosine_Similarity(item_custommer_matrix)
allergy_list = get_Allergy_list(conn, 'Custommer_list', cus_id)

len_Item = len(Item_df)
point_list = [0]*len_Item

for point, item in enumerate(item_custommer_sorted[1:]):
  item -= 1

  point_list[item] = len_Item - point
  
  for allergy in allergy_list:
    print(item, allergy_list)
    if int(Item_df.iloc[item][allergy]):
      point_list[item] = 0

Item_df['point'] = point_list
print(Item_df.sort_values(by='point', ascending=False))
recommand_list = Item_df.sort_values(by='point', ascending=False)['Item_key'].tolist()
if len(recommand_list) > 100:
  recommand_list = recommand_list[:100]
conn.close()

rds_connect.Insert_RDS(cus_id, '\"' + (', ').join(recommand_list) + '\"')