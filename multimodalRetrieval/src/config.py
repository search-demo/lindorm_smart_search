import environs

env = environs.Env()
env.read_env("env")


class Config:
    # vector search
    SEARCH_LINK = env.str("SEARCH_LINK", 'ld-2zescxxxxx-proxy-search-pub.lindorm.aliyuncs.com:30070')
    AI_LINK = env.str("AI_LINK", 'ld-2zescxxxxxx-proxy-ai-pub.lindorm.aliyuncs.com:9002')
    LD_USER = env.str("LD_USER", 'root')
    LD_PASSWORD = env.str("LD_PASSWORD", '*********')
    SEARCH_TOP_K = env.str("SEARCH_TOP_K", "30")