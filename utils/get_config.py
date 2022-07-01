import configparser

config = configparser.ConfigParser()
config.read('conf.ini')


def GetConfig():
    for i in config:
        for t in i:
            t = str(t)

    return config
