import uiautomator2 as u2
import os
import re


# 获取手机UUID
def get_devices_serial_list():
    device_serial_list = []
    # 手机设备的序列号
    adb_devices = os.popen('adb devices').readlines()
    adb_devices.pop()
    rm1 = 'Active code page: 65001\n'
    rm2 = 'List of devices attached\n'
    if rm1 in adb_devices:
        adb_devices.remove(rm1)
    if rm2 in adb_devices:
        adb_devices.remove(rm2)
    # print(adb_devices)
    for device in adb_devices:
        device_serial = re.findall(r'(^[0-9a-zA-Z:.]*)', device)[0]
        device_serial_list.append(device_serial)
    # device_serial_list = ['22932a78f00d7ece']
    print(device_serial_list)
    if len(device_serial_list) == 0:
        raise Exception("没有获取到设备列表")
    return device_serial_list


def get_ios_devices_list():
    device_serial_list = []
    adb_devices = os.popen('tidevice list').readlines()
    print(adb_devices)
    rm1 = 'Active code page: 65001\n'
    if rm1 in adb_devices:
        adb_devices.remove(rm1)
    rm2 = 'List of apple devices attached\n'
    if rm2 in adb_devices:
        adb_devices.remove(rm2)
    rm3 = '\x1b[0m'
    if rm3 in adb_devices:
        adb_devices.remove(rm3)
    for device in adb_devices:
        device_serial = device.split(" ")[0]
        device_serial_list.append(device_serial)
    print(device_serial_list)
    if len(device_serial_list) == 0:
        raise Exception("没有获取到设备列表")
    return device_serial_list


# 获取软件版本
def get_app_version(package, device):
    if package is None:
        raise Exception("包名不能传空")
    # version_list = []
    appinfo = os.popen('adb shell -s %s "dumpsys package %s| grep versionName"' % (device, package)).readlines()
    if len(appinfo) == 0:
        return None
    for version in appinfo:
        version = re.findall(r'\d.*', version)[0]
        break
        # version_list.append(version)
    return version


# 配置手机IP
def get_devices_ip_list():
    device_ip_list = ["192.168.1.103"]
    return device_ip_list


# 获取手机信息
def get_device_info(device):
    driver = u2.connect(f'{device}')
    result = driver.device_info
    # print(result)
    return result


# 通过adb获取手机系统版本
def get_android_version(device):
    android_version = os.popen('adb -s %s shell getprop ro.build.version.release' % device).readline()
    if len(android_version) == 0:
        raise Exception("没有获取到手机系统版本")
    version = re.findall(r'\d*', android_version)[0]
    # print(version)
    return version


# 通过tidevice获取手机系统版本
def get_ios_info(device):
    ios_info = os.popen('tidevice --udid %s info' % device).readlines()
    # print(ios_info)
    rm = 'Active code page: 65001\n'
    if rm in ios_info:
        ios_info.remove(rm)
    rm = '\x1b[0m'
    if rm in ios_info:
        ios_info.remove(rm)
    new_list = {}
    for text in ios_info:
        kk, vv = text.strip("\n").split(":", 1)
        new_list[kk] = vv.strip()

    return new_list


# 通过adb获取手机系统api版本
def get_api_version(device):
    android_version = os.popen('adb -s %s shell getprop ro.build.version.sdk' % device).readline()
    if len(android_version) == 0:
        raise Exception("没有获取到手机系统api版本")
    version = re.findall(r'\d*', android_version)[0]
    # print(version)
    return version


# 获取手机分辨率
def get_device_pix(device):
    driver = u2.connect(f'{device}')
    pix = driver.device_info['display']
    print(pix)
    return pix


# 获取手机电池信息
def get_device_battery(device):
    driver = u2.connect(f'{device}')
    battery = driver.device_info['battery']
    print(battery)
    return battery


if __name__ == '__main__':
    devices = get_devices_serial_list()
    for i in devices:
        print(get_android_version(i))
        print(get_api_version(i))
        print(get_device_info(i))
    # print(get_app_version("com.google.android.webview"))
'''
{'udid': '22932a78f00d7ece-b2:bb:62:e8:87:52-SM-G9650', 'version': '10', 'serial': '22932a78f00d7ece', 
'brand': 'samsung', 'model': 'SM-G9650', 'hwaddr': 'b2:bb:62:e8:87:52', 'sdk': 29, 'agentVersion': '0.10.0', 
'display': {'width': 1440, 'height': 2960}, 
'battery': {'acPowered': False, 'usbPowered': True, 'wirelessPowered': False, 'status': 2, 'health': 2, 'present': True, 'level': 13, 'scale': 100, 'voltage': 3827, 'temperature': 232, 'technology': 'Li-ion'}, 
'memory': {'total': 5713076, 'around': '5 GB'}, 
'cpu': {'cores': 8, 'hardware': 'Qualcomm Technologies, Inc SDM845'}, 
'arch': '', 'owner': None, 'presenceChangedAt': '0001-01-01T00:00:00Z', 'usingBeganAt': '0001-01-01T00:00:00Z', 'product': None, 'provider': None}
'''
