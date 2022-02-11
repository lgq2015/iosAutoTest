if __name__ == '__main__':
    android_test = False
    ios_test = True

    if android_test is True:
        pass
    if ios_test is True:
        from test.ios_test.IosRunCase import RunCase
        from utils.BaseDevicesInfo import get_devices_serial_list

        runner = RunCase()
        runner.run(get_devices_serial_list())
