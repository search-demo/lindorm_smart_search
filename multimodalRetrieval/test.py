import re
import json
from src.lindorm import Lindorm
from src.prompt import VL_PROMPT, REWRITE_SUMMARY_PROMPT

def safe_json_loads(s):
    try:
        return json.loads(s)
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}")
        return None

def parse_markdown_json(s):
    """
    从形如 ```json{...}``` 的字符串中提取并解析 JSON
    """
    if not isinstance(s, str):
        raise TypeError("Input must be a string")

    # 移除首尾空白后匹配
    s = s.strip()
    pattern = r'^```(?:json)?\s*\n?(.*?)\n?\s*```$'
    match = re.search(pattern, s, re.DOTALL | re.IGNORECASE)

    if not match:
        raise ValueError("Cannot find valid JSON in code block")

    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON content: {e}")

def embedding_test(input_type, content: str):
    res = lindorm.lindormAI.embedding(input_type=input_type, content=content, model="qwen3-vl-embedding")
    print(res)

def vl_test(image_url: str):
    res = lindorm.lindormAI.vl_picture_withdraw(img_url=image_url, model="qwen3-vl-plus", prompt=VL_PROMPT)
    print(f"#{res}#")
    res_json = safe_json_loads(res)
    print(res_json)

def rerank_test(text: str, chunks: list):
    res = lindorm.lindormAI.rerank_text(text=text, chunks=chunks, model="qwen3-rerank", top_n=5)
    print(res)

def rewrite_test(text: str):
    res = lindorm.lindormAI.rewrite_text(text=text, model="qwen-max", prompt=REWRITE_SUMMARY_PROMPT)
    print(res)

def get_test(id: str):
    res = lindorm.lindormSearch.get_doc( id)
    img_desc = res.get('_source').get('img_desc')
    print(img_desc)

if __name__ == '__main__':
    lindorm = Lindorm("multimodal_retrieval_index")
    url = "https://graphoss-cnshenzhen.oss-cn-shenzhen.aliyuncs.com/zhaozhen/dataset/Flickr30k-CN-valid/1163438830.jpg"
    text = """
    这张照片展示了一个户外儿童戏水的场景。画面中只有一个孩子，看起来大约5到8岁，是男孩。他正坐在一个充气游泳池里，身体微微后仰，双腿抬起，脚丫溅起水花，似乎刚从旁边的黄色塑料滑梯滑下或正在玩耍。他上身赤裸，下身穿着一条蓝色带花纹的泳裤，没有戴帽子、眼镜或其他配饰。场景位于一个庭院或后院，背景有茂密的绿色植物，旁边是一个黄色和米色相间的塑料滑梯，游泳池内还有粉色和绿色的充气玩具以及一块彩色图案的漂浮垫。由于画面中只有一个人，因此不存在人物之间的互动。重要物体包括黄色滑梯、蓝色充气游泳池、多个彩色充气玩具和漂浮垫。
    """
    # rewrite_test( text)
    get_test("2")
    # embedding_test("image", url)
    # embedding_test("text", "自动化无人车间")
    # vl_test(url)
    # query = "汽车"
    # lists = ["特斯拉", "摩拜", "飞机", "高铁", "小鹏", "汉兰达"]
    # rerank_test(query, lists)