import os
import json
import pandas as pd
import rds_connect

class NUTIRITION:
  allergys_keyword = []
  allergy_dict =  {}
  ingredient_list = []
  nutrition_keyword = []
  nutrition_list = []
  box = []
  def __init__(self):
    self.allergys_keyword = [['계란', '난류', '알류'], ['우유'], ['땅콩'], ['견과류','호두', '잣'], ['밀'], ['갑각류', '새우', '게', '조개류'], ['대두'], ['메밀'], ['쇠고기'], ['돼지고기', '돼지 고기'], ['닭고기'],['생선', '고등어'], ['과일', '복숭아']]
    self.allergy_dict =  {i[0]:'0' for i in self.allergys_keyword}
    self.ingredient_list = []
    self.nutrition_keyword = set(['영양정보', '영양 정보'])
    self.nutrition_list = []
    self.box = []

  def Nutrition_Processing(self, word_list):
    for word in word_list[1:]:
      if '%' in word:
        item_list = word.split('%')
        for item in item_list:
          item = item.strip()
          if item:
             self.nutrition_list.append(item+'%')
      else:
        self.nutrition_list.append(word)

  def Check_Word(self, labels, boxes):
    for idx, label in enumerate(labels):
      label = label.strip()
      label = label.replace(',', '|')

      for i, keys in enumerate(self.allergys_keyword):
        for key in keys:
          if key in label:
            print(key, label)
            self.allergy_dict[keys[0]] = '1'
            self.box.append(boxes[i])

      if(label in self.nutrition_keyword):
        print('in')
        self.Nutrition_Processing(labels[idx:-2])
        break

      else:
        self.ingredient_list.append(label)


def handler(event, context):
    datas = event['responsePayload']['body']
    key = event['responsePayload']['key']
    bucket = event['responsePayload']['bucket']
    print(key, bucket)

    df = pd.DataFrame(columns=['description', 'box', 'height'])
    for data in datas:
        description = data['description']
        box = data['box']
        height = box[0]/20 + box[1]
        df.loc[len(df.index)]=[description, box, height]

    sorted_df = df.sort_values(by='height')
    show_labels = sorted_df.description.tolist()
    boxes = sorted_df.box.tolist()
    process = NUTIRITION()
    process.Check_Word(show_labels, boxes)

    print('fix and Deployed by CodePipeline')
    try:
        rds_connect.Insert_RDS(process, key, bucket)
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }
    except:
        return{
            'statusCode': 400,
            'body': json.dumps('ERROR!')
        }
