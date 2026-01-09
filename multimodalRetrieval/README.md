## 概述

* 多模态检索样demo，结合 Lindorm 与百炼共同实现图文多模态检索

<img src="data/架构图.png" alt="架构图" style="width:50%; height:auto;" />


* demo 功能概述
  * 图片一键入库
    * qwen-vl 模型图片内容识别，生成描述
    * qwen-plus 对描述再进行优化改写，提升检索效果
    * 图片进行 embedding，生成向量值
    * 图片描述、图片向量、其他标签共同写入 Lindorm 实例
  * 图片检索
    * 以图搜图
    * 以文搜图
  
* 依赖模型
  * qwen2.5-vl-embedding  多模态 embedding 模型
  * qwen-plus             文本生成模型,优化图片描述
  * qwen3-vl-plus         图片理解大模型
  * qwen3-rerank          召回按照语义精排模型

## 前提条件
* Lindorm 实例文档了解 [文档](https://help.aliyun.com/zh/lindorm/)
* python3.11 环境
* 安装依赖包: pip install -r requirements.txt
* 开通引擎: 向量引擎、搜索引擎、AI 引擎
* 内置打通百炼平台，无需额外申请百炼 api_key
* 示例数据集包含一个CSV文件 flickr30k-valid-test.csv,内容有 id、url、create_time
  * 说明：本文使用的样例数据集来自开源 flickr30k 数据集


## 操作流程

### 步骤一: 配置索引和模型
* 配置依赖的 4 个模型
* 配置测试索引名称
* 强制清库为 True 时，索引会先清空，再创建索引

<img src="data/配置模型和索引.png" alt="配置" style="width:50%; height:auto;" />

* 创建索引，不存在自动创建，存在的话结合 force_clear 参数控制是否清空索引

<img src="data/创建索引.png" alt="创建索引" style="width:50%; height:auto;" />


### 步骤二: 导入数据
* 选择样例 flickr30k-valid-test.csv 进行导入

<img src="data/导入数据.png" alt="导数据" style="width:50%; height:auto;" />

### 步骤三: 构建磁盘索引
* 构建磁盘索引是一次性，后续新增数据不用再次导入

<img src="data/构建磁盘索引.png" alt="构建磁盘索引" style="width:50%; height:auto;" />

### 步骤四: 多模态检索

* 以文搜图
* 输入需要检索的文本信息，检索相应的图片

<img src="data/以文搜图1.png" alt="以文搜图" style="width:50%; height:auto;" />
<img src="data/以文搜图2.png" alt="以文搜图" style="width:50%; height:auto;" />

* 以图搜图
* 上传本地图片，检索相应的图片

<img src="data/以图搜图.png" alt="以图搜图" style="width:50%; height:auto;" />