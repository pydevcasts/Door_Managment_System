class CRC:
    """datalist hexadecimal and octal
      منطق crc 
            اینه که 2 تا از بایت ها که بین کنترل باکس و 
            
            و رزبری هستش چک میشن بین رزبری و کنترل باکس
            فرضا میگیم 15 بایت از رزبری به کنترل باکس بره 
            15 میشه طول ارایه و
            و 128 میشه یک بیت 
            و خود 15 میشه بیت دوم 
            و 13 تا دیگه میمونه که 2 تا از این بایتا میاد چک میشن که مقدار فرضا جمعشون برابر هم 
            باشه اینجوری بین کنترل باکس و رزبری 
            انالیز میشه
        
    """
    def __init__(self):
        pass

    def createCRC(self, dataList):
        if dataList is None:
            return None

        if len(dataList) < 2:
            return None

        if len(dataList) < dataList[1]:
            return None

        result = int(0)

        for i in range(0, dataList[1]):
            if i == 2 or i == 3:
                continue

            data = dataList[i]
            result = (result >> 8) | (result << 8)
            result ^= data
            result ^= (result & 0xff) >> 4
            result ^= (result << 8) << 4
            result ^= ((result & 0xff) << 4) << 1
            result &= 0xffff

        return int(result)

    def putCRC(self, dataList):

        crc = self.createCRC(dataList)
        if crc is None:
            return

        dataList[3] = crc & 0xFF
        dataList[2] = (crc >> 8) & 0xFF

    def checkCRC(self, dataList):
        crc = self.createCRC(dataList)
        if crc is None:
            return None

        return crc == (dataList[2] * 256 + dataList[3])


############################################################
############################################################
############################################################
crc = CRC()
