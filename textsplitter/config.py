import environs

env = environs.Env()
env.read_env("env")


class Config:
    # vector search
    SEARCH_HOST = env.str("SEARCH_HOST", 'ld-2zescxxxxx-proxy-search-pub.lindorm.aliyuncs.com')
    SEARCH_PORT = env.str("SEARCH_PORT", '30070')
    AI_HOST = env.str("AI_HOST", 'ld-2zescxxxxxx-proxy-ai-pub.lindorm.aliyuncs.com')
    AI_PORT = env.str("AI_PORT", '9002')
    LD_USER = env.str("LD_USER", 'root')
    LD_PASSWORD = env.str("LD_PASSWORD", '*********')
    SEARCH_TOP_K = env.str("SEARCH_TOP_K", "30")

    # row storage (MySQL)
    ROW_HOST = env.str("ROW_HOST", 'ld-2zescxxxxx-proxy-row-pub.lindorm.aliyuncs.com')
    ROW_PORT = env.str("ROW_PORT", '3306')

    LOAD_FILE_PATH = "data/cmrc2018_train.json"
