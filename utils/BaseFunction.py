# 字符串时分秒转换成秒
def str2sec(x):
    h = m = s = 0
    time = x.strip().split(':')
    if len(time) == 1:
        s = time[0]
    if len(time) == 2:
        m, s = time
    if len(time) == 3:
        h, m, s = time
    # print(h, m, s)
    return int(h) * 3600 + int(m) * 60 + int(s)


if __name__ == '__main__':
    print(str2sec('23:06'))
