

#################################################
#################################################
class BaseData:

    #############################################
    def __init__(self, key, text):
        self.key = key
        self.text = text

    #############################################
    def __str__(self):
        from Lang import lget
        return lget(self.text)


#################################################
#################################################
class BaseDataList:
    """basedatalist"""

    #############################################
    def __init__(self, d=None):
        self.list = []
        self.load(d)

    #############################################
    def __len__(self):
        return len(self.list)

    #############################################
    def __getitem__(self, key):
        return self.list[key]

    #############################################
    def __iter__(self):
        return iter(self.list)

    #############################################
    def load(self, d):
        if d is None:
            return
        for key, text in d.items():
            baseData = BaseData(key, text)
            self.add(baseData)

    #############################################
    def list(self):
        return self.list

    #############################################
    def add(self, basaData):
        self.list.append(basaData)

    #############################################
    def find(self, key):
        for baseData in self.list:
            if baseData.key == key:
                return baseData
        return None
        """دیکشنری  کلاس و بیار بریز توی 
        self.list
        و بعد ایتریبلش کن 
        و بعد کلید اون لیست برابر با ازگوان 
        find 
        بود بیا اون لیست و که حلقشو خواستیم بگیریم و نشون بده
        
        """