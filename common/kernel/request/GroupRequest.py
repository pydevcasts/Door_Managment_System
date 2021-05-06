from common.kernel.request.Request import Request


class GroupRequest(Request):

    CREATE = "C"
    RENAME = "R"
    UPDATE = "U"
    DELETE = "D"

    #########################################################################################
    def __init__(self, action, group=None, name=None, serial=None):
        Request.__init__(self, Request.GROUP)
        self.action = action
        if group is not None:
            self.group = group
        if name is not None:
            self.name = name
        if serial is not None:
            self.serial = serial

    #########################################################################################
    @staticmethod
    def create(name, serial):
        return GroupRequest(GroupRequest.CREATE, name=name, serial=serial)

    #########################################################################################
    @staticmethod
    def update(group, serial):
        return GroupRequest(GroupRequest.UPDATE, group=group, serial=serial)

    #########################################################################################
    @staticmethod
    def rename(group, name):
        return GroupRequest(GroupRequest.RENAME, group=group, name=name)

    #########################################################################################
    @staticmethod
    def delete(group):
        return GroupRequest(GroupRequest.DELETE, group=group)
