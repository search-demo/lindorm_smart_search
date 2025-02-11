import environs

env = environs.Env()
env.read_env("env")


class Config:
    # AI
    AI_HOST = env.str("AI_HOST", '')
    AI_PORT = env.str("AI_PORT", '9002')

    # Row_Table
    ROW_HOST = env.str("ROW_HOST", '')
    ROW_PORT = env.str("ROW_PORT", '33060')

    # vector search
    SEARCH_HOST = env.str("SEARCH_HOST", '')
    SEARCH_PORT = env.str("SEARCH_PORT", '30070')

    LD_USER = env.str("LD_USER", 'root')
    LD_PASSWORD = env.str("LD_PASSWORD", '')

    LOAD_FILE_PATH = env.str("LOAD_FILE_PATH", "")

    SEARCH_TOP_K = env.str("SEARCH_TOP_K", "5")

    DASHSCOPE_API_KEY = env.str("DASHSCOPE_API_KEY", "")

    LD_VL_MODEL = env.str("LD_VL_MODEL", "bge_visual0")
    LD_TEXT_MODEL = env.str("LD_TEXT_MODEL", "bge_m3_model")


