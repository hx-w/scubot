from os import path
import nonebot
import sys
sys.path.append('/var/lib/scubot')

try:
    import config
except:
    import nonebot.default_config as config

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'plugins'),
        'plugins'
    )
    nonebot.run()