from datetime import datetime
from elasticsearch import Elasticsearch
from pprint import pprint
import requests
import time
import json
#from app.core.job import Worker

from app.elastic.configs.index_configs import index_configs
from app.config import config

index_confs = index_configs()

def wait_for_elastic():
    url = config.elastic_url + '_cat/health'
    while True:
        try:
            res = requests.get(url)
            return
        except Exception as e:
            print(f'Elastic cannot be reached at {url}, retrying in 1 second')
            time.sleep(1)


class SearchIndex:
    instance = None
    def __init__(self, elastic_url=config.elastic_url,
                    index_name=config.elastic_index,
                    ssl=False,
                    check_certs=False,
                    certs="",
                    delete_old_index=False,
                    index_config='prefix'):
        if delete_old_index or not SearchIndex.instance:
            SearchIndex.instance = SearchIndex.__SearchIndex(elastic_url,
                index_name,
                ssl,
                check_certs,
                certs,
                index_config)
        else:
            SearchIndex.instance.elastic_url = elastic_url
            SearchIndex.instance.index_name = index_name
            SearchIndex.instance.ssl = ssl
            SearchIndex.instance.check_certs = check_certs
            SearchIndex.instance.certs = certs
    
    def __getattr__(self, name):
        return getattr(self.instance, name)

    class __SearchIndex:
        def __init__(self,
                    elastic_url,
                    index_name,
                    ssl,
                    check_certs,
                    certs,
                    index_config):
            self.connection = Elasticsearch([elastic_url])
            self.index_name = index_name
            self.certs = certs
            self.ssl = ssl
            self.index_config = index_config
            self.index = self.connection.indices.create(
                index=index_name,
                body=index_confs[self.index_config], 
                ignore=400)

        def is_connected(self, host, port):
            if self.connection != host + ":" + port:
                return False
            else:
                return True

        def put(self, doc, id):
            doc = json.dumps(doc.reprJSON(), cls=Encoder)
            res = self.connection.index(index=self.index_name, id=id, body=doc, doc_type="_doc")
            return res

        def get(self, id):
            self.connection.get(index=self.index_name, id=id, doc_type="_doc")
        
        def get_con(self):
            return self.connection

        def search(self, search_term):
            search_param = {"query": {
                "match": {
                    "text":  {
                        "query": search_term, 
                        "operator": "and"
                    }
                }
            }}
            response = self.connection.search(index=self.index_name, body=search_param, doc_type="_doc")
            return response
        
        def refresh(self):
            self.connection.indices.refresh(index=self.index_name)


class Document:
    def __init__(self, asr_result, path_to_audio="to-do.mp3"):
        self.results = []
        for part in asr_result["parts"]:
            for word_result in part["result"]:
                res = AsrInnerResult(
                    word_result["conf"], word_result["start"], word_result["end"], word_result["word"])
                self.results.append(res)
        self.text = asr_result["text"]
        self.path_to_audio = path_to_audio
        self.created_at = datetime.now()
       


    def reprJSON(self):        
        return dict(results=[result.reprJSON() for result in self.results],
                    text=self.text,
                    path_to_audio=self.path_to_audio,
                    created_at=self.created_at
                    )


class AsrInnerResult():
    def __init__(self, conf, start, end, word):
        self.conf = conf
        self.start = start
        self.end = end
        self.word = word

    def reprJSON(self):
        return dict(conf=self.conf,
                    start=self.start,
                    end=self.end,
                    word=self.word
                    )


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.__str__()
        elif hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)


if __name__ == "__main__":
    # asr_result = {"result": [{
    #     "conf": 0.49457,
    #     "end": 2.34,
    #     "start": 1.35,
    #     "word": "hello"},
    #     {
    #     "conf": 0.9,
    #     "end": 2.3,
    #     "start": 1.4,
    #     "word": "hello"}],
    #     "text": "transcript"}
    asr_result = {'text': ' fünfundzwanzig jahren leipziger geschichte mit perspektiven als waren zum beispiel erinnerung es kommt',
                  'parts': [
                      {'result': [
                          {'conf': 0.983098, 'end': 1.41, 'start': 0.27, 'word': 'fünfundzwanzig'},
                          {'conf': 0.42963, 'end': 2.034147, 'start': 1.41, 'word': 'jahren'},
                          {'conf': 0.956407, 'end': 2.669977, 'start': 2.1, 'word': 'leipziger'},
                          {'conf': 0.997978, 'end': 3.27, 'start': 2.67082, 'word': 'geschichte'},
                          {'conf': 0.674975, 'end': 3.48, 'start': 3.33, 'word': 'mit'},
                          {'conf': 0.998419, 'end': 4.5, 'start': 3.48, 'word': 'perspektiven'},
                          {'conf': 1.0, 'end': 5.5798, 'start': 5.34, 'word': 'als'},
                          {'conf': 0.829022, 'end': 5.97, 'start': 5.58, 'word': 'waren'},
                          {'conf': 1.0, 'end': 6.48, 'start': 6.33, 'word': 'zum'},
                          {'conf': 1.0, 'end': 6.904158, 'start': 6.48, 'word': 'beispiel'},
                          {'conf': 0.678397, 'end': 7.411906, 'start': 6.904158, 'word': 'erinnerung'},
                          {'conf': 0.898544, 'end': 7.92, 'start': 7.74, 'word': 'es'},
                          {'conf': 0.999274, 'end': 8.43, 'start': 7.920014, 'word': 'kommt'}
                      ],
                          'text': 'fünfundzwanzig jahren leipziger geschichte mit perspektiven als waren zum beispiel erinnerung es kommt'}
                  ]}

    path_to_audio = "path/to/audio"
    
    search_index = SearchIndex()
    doc = Document(asr_result, path_to_audio)
    #PUT Document in index
    pprint("INDEX")
    pprint(search_index.put(doc, "1"))
    #SEARCH the Word "transcript" in index
    pprint("SEARCH")
    pprint(search_index.search("leip"))
