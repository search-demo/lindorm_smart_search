# -*- coding: utf-8 -*-
import json
import random

import requests
from opensearchpy import OpenSearch

from src.config import Config


class Lindorm:
    def __init__(self, index_name: str):
        self.random = random.Random(0)
        self.index_name = index_name
        self.lindormSearch = self.LindormSearch(self)
        self.lindormAI = self.LindormAI(self)

    def index_check(self, clear_index: bool, index_body: dict):
        if self.lindormSearch.detect():
            print('连接成功')
        else:
            print('连接失败')
            raise Exception("连接失败")

        if self.lindormSearch.get_index():
            if clear_index:
                print("索引已存在, 删除索引,重新导入数据")
                self.lindormSearch.drop_index()
                self.lindormSearch.create_search_index(index_body)
                print('索引创建成功')
        else:
            self.lindormSearch.create_search_index(index_body)
            print('索引创建成功')

    class LindormSearch:
        def __init__(self, parent):
            self.parent = parent
            self.index_name = self.parent.index_name
            self.search_host = Config.SEARCH_LINK.split(":")[0]
            self.search_port = Config.SEARCH_LINK.split(":")[1]
            try:
                self.client = OpenSearch(
                    hosts=[{"host": self.search_host, "port": self.search_port}],
                    http_auth=(Config.LD_USER, Config.LD_PASSWORD),
                    http_compress=False,
                    use_ssl=False,
                    pool_maxsize=128,
                    timeout=120
                )
            except Exception as e:
                print("Connection search error", e)

        def get_ingest_pipeline(self, pipeline_name: str):
            try:
                return self.client.ingest.get_pipeline(pipeline_name)
            except Exception as e:
                if e.status_code == 404:
                    print("pipeline not found")
                    return None
                else:
                    raise e

        def create_ingest_pipeline(self, pipeline_name: str, body):
            try:
                return self.client.ingest.put_pipeline(pipeline_name, body)
            except Exception as e:
                if e.status_code == 409:
                    print("pipeline already exists")
                    return None
                else:
                    raise e

        def get_search_pipeline(self, pipeline_name: str):
            try:
                return self.client.search_pipeline.get(pipeline_name)
            except Exception as e:
                if e.status_code == 404:
                    print("pipeline not found")
                    return None
                else:
                    raise e

        def create_search_pipeline(self, pipeline_name: str, body):
            try:
                return self.client.search_pipeline.put(pipeline_name, body)
            except Exception as e:
                if e.status_code == 409:
                    print("pipeline already exists")
                    return None
                else:
                    raise e

        def detect(self):
            try:
                self.client.cat.indices()
                return True
            except Exception as e:
                print("Connection search error", e)
                return False

        # 创建搜索索引,包含图片向量列
        def create_search_index(self, body):
            return self.client.indices.create(index=self.index_name, body=body, timeout=60)

        def drop_index(self):
            return self.client.indices.delete(index=self.index_name, timeout=60)

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

        def build_index(self, vector_column: str):
            body = {
                "indexName": self.index_name,
                "fieldName": vector_column,
                "removeOldIndex": "true"
            }
            return self.client.transport.perform_request(
                method="POST",
                url='/_plugins/_vector/index/build',
                body=body,
                timeout=60,
            )

        def query_index_build_states(self, vector_column: str):
            build_query = {
                "indexName": self.index_name,
                "fieldName": vector_column,
                "taskIds": "[]"
            }

            return self.client.transport.perform_request(
                method='GET',
                url='/_plugins/_vector/index/tasks',
                body=build_query,
                timeout=60,
            )

        def write_doc(self, element: dict, docId: str = None):
            return self.client.index(index=self.index_name, body=element, id=docId)

        def update_doc(self, element: dict, docId: str = None):
            body = {
                "doc": element
            }
            return self.client.update(index=self.index_name, id=docId, body=body)

        def get_doc(self, docId: str):
            try:
                return self.client.get(index=self.index_name, id=docId, _source=True)
            except Exception as e:
                if e.status_code == 404:
                    return None
                else:
                    raise e

        def delete_doc(self, docId: str):
            return self.client.delete(index=self.index_name, id=docId)

        def __search__(self, body):
            response = self.client.search(index=self.index_name, body=body)
            return response.get('hits').get('hits')

        def search(self, body):
            return self.__search__(body)

        def knn_search(self, embedding: list, embedding_column, source: bool = True, min_score: float = 0.0,
                       top_k: int = 0):
            top_k = Config.SEARCH_TOP_K if top_k == 0 else top_k
            body = {
                "_source": source,
                "query": {
                    "knn": {
                        embedding_column: {
                            "vector": embedding,
                            "k": top_k
                        }
                    }
                },
                "size": top_k,
                "ext": {"lvector": {"min_score": str(min_score)}}
            }
            return self.__search__(body)

        def rrf_search(self, desc, desc_column, embedding: list, embedding_column, source: bool = True,
                       factor: float = 0.5, min_score: float = 0.0, top_k: int = 0):
            top_k = Config.SEARCH_TOP_K if top_k == 0 else top_k
            query = {
                "_source": source,
                "size": top_k,
                "query": {
                    "knn": {
                        embedding_column: {
                            "vector": embedding,
                            "filter": {
                                "match": {
                                    desc_column: desc
                                }
                            },
                            "k": top_k
                        }
                    }
                },
                "ext": {"lvector": {
                    "min_score": str(min_score),
                    "hybrid_search_type": "filter_rrf",
                    "rrf_rank_constant": "60",
                    "rrf_knn_weight_factor": str(factor)
                }}
            }
            return self.__search__(query)

        def rrf_search_with_filter(self, desc, desc_column, embedding: list, embedding_column,
                                   conditions: dict, source: bool = True, factor: float = 0.5,
                                   min_score: float = 0.0, top_k: int = 0):
            top_k = Config.SEARCH_TOP_K if top_k == 0 else top_k
            query = {
                "_source": source,
                "size": top_k,
                "query": {
                    "knn": {
                        embedding_column: {
                            "vector": embedding,
                            "filter": {
                                "bool": {
                                    "must": [
                                        {
                                            "bool": {
                                                "must": [{
                                                    "match": {
                                                        desc_column: {
                                                            "query": desc
                                                        }
                                                    }
                                                }]
                                            }
                                        },
                                        conditions
                                    ]
                                }
                            },
                            "k": top_k
                        }
                    }
                },
                "ext": {"lvector": {
                    "filter_type": "efficient_filter",
                    "min_score": str(min_score),
                    "hybrid_search_type": "filter_rrf",
                    "rrf_rank_constant": "60",
                    "rrf_knn_weight_factor": str(factor)
                }}
            }
            return self.__search__(query)

        def full_text_search(self, text, desc_column, source: bool = True, top_k: int = 0):
            top_k = Config.SEARCH_TOP_K if top_k == 0 else top_k
            query = {
                "_source": source,
                "size": top_k,
                "query": {
                    "match": {
                        desc_column: text
                    }
                }
            }
            return self.__search__(query)

        def filter_search(self, body, source, top_k: int = 0):
            top_k = Config.SEARCH_TOP_K if top_k == 0 else top_k
            query = {
                "_source": source,
                "size": top_k,
                "query": body
            }
            return self.__search__(query)

    class LindormAI:
        def __init__(self, parent):
            self.parent = parent
            self.ai_host = Config.AI_LINK.split(":")[0]
            self.ai_port = Config.AI_LINK.split(":")[1]
            self.headers = {"x-ld-ak": Config.LD_USER,
                            "x-ld-sk": Config.LD_PASSWORD}

        def post_model_request(self, url: str, body: dict):
            # print(f"url {url}, body {body}, headers {self.headers}")
            result = requests.post(url=url, json=body, headers=self.headers)
            # 确保请求成功
            result.raise_for_status()
            return result.json()

        def embedding(self, input_type: str, content: str, model: str):
            url = f"http://{self.ai_host}:{self.ai_port}/dashscope/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding"
            body = {
                "input": {
                    "contents": [
                        {
                            input_type: content
                        }
                    ]
                },
                "model": model
            }
            return self.post_model_request(url, body)['output']['embeddings'][0]['embedding']

        def vl_picture_withdraw(self, img_url: str, model: str, prompt: str):
            url = f"http://{self.ai_host}:{self.ai_port}/dashscope/compatible-mode/v1/chat/completions"
            body = {
                "messages": [
                    {
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": img_url,
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ],
                        "role": "user"
                    }
                ],
                "model": model
            }
            return self.post_model_request(url, body)['choices'][0]['message']['content']

        def rerank_text(self, text: str, chunks: list, model: str, top_n: int):
            url = f"http://{self.ai_host}:{self.ai_port}/dashscope/compatible-api/v1/reranks"
            body = {
                "query": text,
                "documents": chunks,
                "top_n": top_n,
                "model": model
            }
            return self.post_model_request(url, body)['results']

        def rewrite_text(self, text: str, model: str, prompt: str):
            url = f"http://{self.ai_host}:{self.ai_port}/dashscope/compatible-mode/v1/chat/completions"
            body = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": prompt
                    },
                    {
                        "role": "user",
                        "content": text
                    }]
                # "response_format": {"type": "json_object"}
            }
            return self.post_model_request(url, body)['choices'][0]['message']['content']
