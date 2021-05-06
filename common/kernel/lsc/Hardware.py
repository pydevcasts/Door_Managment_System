#######################################################
def getRaspberrySystemSerial():
    serial = '000000000'
    f = open('/proc/cpuinfo', 'r')
    for line in f:
        if line[0:6] == 'Serial':
            serial = line[10:26]
            break
    f.close()

    return serial


#######################################################
def getWindowsSystemSerial():
    import wmi
    c = wmi.WMI()
    for s in c.Win32_Processor():
        return s.ProcessorId.strip()


#######################################################
def getSystemSerial():
    try:
        return getRaspberrySystemSerial()
    except:
        pass

    try:
        return getWindowsSystemSerial()
    except:
        pass

    return "ERROR000000000"


#######################################################
def getRaspberryStorageSerial():
    f = open('/sys/block/mmcblk0/device/cid', 'r')
    for line in f:
        serial = line[:len(line) - 1]
        break
    f.close()
    return serial


#######################################################
def getWindowsStorageSerial():
    import wmi
    c = wmi.WMI()
    for pm in c.Win32_PhysicalMedia():
        return pm.SerialNumber.strip()


#######################################################
def getStorageSerial():
    try:
        return getRaspberryStorageSerial()
    except:
        ""

    try:
        return getWindowsStorageSerial()
    except:
        ""

    return "ERROR000000000000000000000000000"


#######################################################
def getIdentificationCode():
    return getSystemSerial() + "#" + getStorageSerial()
