import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json
from pymongo import MongoClient

i = 0
client = MongoClient('localhost',27017)
db=client.comment
collection=db.comment
collection2=db.after

def sentiment_classify(data):
    access_token=''
    http=urllib3.PoolManager()
    url='https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token='+access_token
    params={'text':data}
    #进行json转换的时候，encode编码格式不指定也不会出错
    encoded_data = json.dumps(params).encode('GBK')
    try:
        request=http.request('POST',
                              url,
                              body=encoded_data,
                              headers={'Content-Type':'application/json'})
        result = str(request.data,'GBK')
        result = json.loads(result)
        return result['items'][0]['sentiment']
    except Exception as e:
        if result.get('error_code') == 18:
            print("error:qps limit",i, e, data, result)
            time.sleep(0.2)
            return sentiment_classify(data)

def data_processing():
    collection2.remove()

    for item in collection.find():
        global i
        i+=1
        comment = item.get('content')
        sentiment = sentiment_classify(comment)
        collection2.insert({'comment': comment,'sentiment':sentiment})
data_processing()

