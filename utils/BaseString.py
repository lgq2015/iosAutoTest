#!/usr/bin/env python
# -*- encoding: utf-8 -*-


class BaseString:

    def is_contain(self, str1, str2):
        """
        判断预期结果是否和实际结果相同
        :param str1: 预期结果值
        :param str2: 实际结果值
        :return: flag
        """
        # print(str1, str2)
        if str1 in str2:
            flag = True
        else:
            flag = False
        return flag


if __name__ == "__main__":
    cs = BaseString()
    print(cs.is_contain('adb','adbsdf'))
