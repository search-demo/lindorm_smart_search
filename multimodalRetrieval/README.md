## 介绍
- 多模态检索样例工程，提供以图搜图、以文搜图功能
- 提供图片去重入库功能
- 结合qwen-vl-max-latest大模型对图片进行识别，再利用lindorm的图片文本融合检索来实现多模态检索


## 模型介绍
- 采用 lindorm 多模态检索模型
    - bge_visual0: 图片向量化
    - bge_m3_model: 文本向量化
- qwen-vl-max-latest 通义千问图片识别模型

## jupyter 服务演示
- LindormMultiModalSearch.ipynb 纯 lindorm 多模态检索
- LindormQwenVlMultiModalSearch.ipynb lindorm + qwen-vl 融合检索
