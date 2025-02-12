## 介绍
- 多模态检索样例工程，提供以图搜图、以文搜图功能
- 提供图片去重入库功能

## 数据导入
    - 数据源 102flowers: https://www.robots.ox.ac.uk/~vgg/data/flowers/102/index.html
    - PictureImoprt.ipynb

## 模型介绍
- 采用 lindorm 多模态检索模型
    - bge_visual0: 图片向量化
    - bge_m3_model: 文本向量化

## 多模态检索
- MultiModalRetrieval.ipynb

### 以图搜图
- 通过本地图片搜索图片

### 以文搜图
- 通过文本搜索图片

### 图片去重入库
- ImageDeduplication.ipynb
- 通过以图搜图，提供图片自动去重功能，相似度 >= 阈值的图片不导入，并返回相似照片
