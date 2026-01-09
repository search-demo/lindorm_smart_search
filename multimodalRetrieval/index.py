# -*- coding: utf-8 -*-

def get_index_body(dim):
    return {
        "settings": {
            "index": {
                "number_of_shards": 2,
                "knn": True,
                "knn.offline.construction": True,
                "origin.vector_source_only_includes.enabled": True
            }
        },
        "mappings": {
            "_source": {
                "excludes": ["embedding"]
            },
            "properties": {
                "embedding": {
                    "type": "knn_vector",
                    "dimension": dim,
                    "data_type": "float",
                    "method": {
                        "engine": "lvector",
                        "name": "ivfpq",
                        "space_type": "cosinesimil",
                        "parameters": {
                            "m": dim,
                            "nlist": 20,
                            "centroids_use_hnsw": True,
                            "centroids_hnsw_m": 48,
                            "centroids_hnsw_ef_construct": 500,
                            "centroids_hnsw_ef_search": 200
                        }
                    }
                },
                "create_time": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss||yyyy/MM/dd HH:mm:ss||iso8601||epoch_millis||epoch_second"
                },
                "url": {
                    "type": "keyword"
                },
                "img_desc": {
                    "type": "text"
                }
            }
        }
    }
