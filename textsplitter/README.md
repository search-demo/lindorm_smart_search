# 智搜说明文档

## 环境准备

1. python环境：

已安装Python环境，要求安装Python 3.10及以上版本。

2. jupyter服务安装

请参考： https://help.aliyun.com/document_detail/2865243.html 文档中的安装逻辑

3. 依赖安装

 pip3 install -r requirements.txt 

4. 启动jupyter

可以使用 jupyter notebook 启动，这样会使用 ~/.jupyter/jupyter_notebook_config.py 文件中配置的目录

也可以使用，这样能指定特定端口与目录 notebook-dir 请根据实际的目录确定
python3.11 /usr/local/bin/jupyter-notebook --ip 0.0.0.0 --port 9500 --notebook-dir=/data/lindorm_smart_search/textsplitter --allow-root

5. env配置

```
# AI host: ai引擎的访问域名，请确认好使用内网还是外网。
AI_HOST="ld-xxxxx-proxy-ai-vpc.lindorm.aliyuncs.com"
AI_PORT="9002"

# Row host: 宽表引擎的访问域名，请确认好使用内网还是外网，没有使用宽表可不配置
ROW_HOST="ld-xxxxx-proxy-lindorm-vpc.lindorm.aliyuncs.com"
ROW_PORT="33060"

# Search host: 搜索引擎的访问域名，请确认好使用内网还是外网
SEARCH_HOST="ld-xxxxx-proxy-search-vpc.lindorm.aliyuncs.com"
SEARCH_PORT="30070"

# Lindorm user password 
LD_USER="root"
LD_PASSWORD="******"

# lindorm_demo.ipynb  中使用
LOAD_FILE_PATH="data/cmrc2018_train.json"

SEARCH_TOP_K="5"

# 访问通义前问的apikey: 如何获取参考： https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key
DASHSCOPE_API_KEY="sk-xxx"
```

## Demo 说明：
1.  lindorm_demo.ipynb 
使用 宽表 + AI + 搜索 + 向量集成的一站式智搜服务。 对应官方说明文档：https://help.aliyun.com/document_detail/2865243.html
数据有特殊处理，如写入的子表的文本字段，的拼接格式为  title: chunking

2.  lindorm_search_vector_ai_chunking.ipynb
使用 AI + 搜索 + 向量 集成的一站式智搜服务。
数据有特殊处理，如写入的子表的文本字段的拼接格式为  title: chunking

3. lindorm_common_search_vector_ai_chunking.ipynb
使用 AI + 搜索 + 向量 集成的一站式智搜服务可以上传自己的txt文件。








