# -*- coding: utf-8 -*-
import json
import random
import base64
import requests
from opensearchpy import OpenSearch
from . import Config


class Lindorm:
    def __init__(self):
        self.random = random.Random(0)
        self.top_k = Config.SEARCH_TOP_K
        self.dimension = 1024
        self.headers = {"x-ld-ak": Config.LD_USER,
                        "x-ld-sk": Config.LD_PASSWORD}
        self.index_name = "multimodal_retrieval_flowers"
        try:
            self.client = OpenSearch(
                hosts=[{"host": Config.SEARCH_HOST, "port": Config.SEARCH_PORT}],
                http_auth=(Config.LD_USER, Config.LD_PASSWORD),
                http_compress=False,
                use_ssl=False,
            )
        except Exception as e:
            print("Connection search error", e)

    def post_model_request(self, model: str, data: dict):
        data = json.dumps(data)
        url = 'http://{}:{}/v1/ai/models/{}/infer'.format(Config.AI_HOST, Config.AI_PORT, model)
        try:
            result = requests.post(url, data=data, headers=self.headers, verify=False)
            # 确保请求成功
            result.raise_for_status()
            # print(f'请求成功: {url}, 返回: {result.json()}')
            return 0, result.json()['data'][0]
        except requests.exceptions.Timeout:
            return -1, "请求超时"
        except requests.exceptions.HTTPError as http_err:
            return -1, f"HTTP 错误: {http_err}"
        except requests.exceptions.RequestException as err:
            return -1, f"请求发生错误: {err}"

    def picture_embedding(self, image):
        encoded_str = base64.b64encode(image).decode('utf-8')
        data = {"input": {"images": [encoded_str]}}
        return self.post_model_request(Config.LD_VL_MODEL, data)

    def text_embedding(self, text: str):
        data = {"input": [text]}
        return self.post_model_request(Config.LD_TEXT_MODEL, data)

    # 创建搜索索引,包含图片向量列
    def create_search_index(self):
        body = {
            "settings": {
                "index": {
                    "number_of_shards": 2,
                    "knn": True
                }
            },
            "mappings": {
                "_source": {
                    "excludes": ["image_embedding"]
                },
                "properties": {
                    "image_embedding": {
                        "type": "knn_vector",
                        "dimension": self.dimension,
                        "data_type": "float",
                        "method": {
                            "engine": "lvector",
                            "name": "hnsw",
                            "space_type": "cosinesimil",
                            "parameters": {
                                "m": 24,
                                "ef_construction": 500
                            }
                        }
                    }
                }
            }
        }
        print(self.index_name, self.client.indices.create(self.index_name, body=body, timeout=60))

    def drop_index(self):
        print(self.client.indices.delete(index=self.index_name, timeout=60))

    def get_index(self):
        try:
            return self.client.indices.get(index=self.index_name)
        except Exception as e:
            if e.status_code == 404:
                print("index not found")
                return None
            else:
                raise e

    def index_count(self):
        return self.client.count(index=self.index_name)

    def write_doc(self, url: str, image_embedding: list):
        element = {
            "image_embedding": image_embedding
        }
        return self.client.index(self.index_name, element, id=url)

    def get_doc(self, docId: str):
        return self.client.get(self.index_name, docId)

    def delete_doc(self, docId: str):
        return self.client.delete(self.index_name, docId)

    def knn_search(self, picture_embedding):
        body = {
            "query": {
                "knn": {
                    "image_embedding": {
                        "vector": picture_embedding,
                        "k": self.top_k
                    }
                }
            },
            "size": self.top_k
        }
        response = self.client.search(index=self.index_name, body=body)
        # print('pure knn search, total', response.get('hits').get('total'))
        hits = []
        for hit in response.get('hits').get('hits'):
            # print(hit.get('_id'), hit.get('_score'))
            hits.append({"_id": hit.get('_id'), "_score": hit.get('_score')})
        return hits
