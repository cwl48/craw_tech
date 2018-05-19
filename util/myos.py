import platform


def is_linux():
    sysstr = platform.system()
    print(sysstr)
    return sysstr == "Linux"
