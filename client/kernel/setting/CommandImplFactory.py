from Globals import logger


class CommandImplFactory:

    #############################################################
    def __init__(self):
        self.map = {}

    #############################################################
    def register(self, commandImpl):
        model, version = commandImpl.getModelVersion()

        if self.map.get(model, None) is None:
            self.map[model] = {}

        modelMap = self.map[model]
        if modelMap.get(version, None) is None:
            modelMap[version] = {}

        modelMap[version][commandImpl.getParameterCode()] = commandImpl

    #############################################################
    def getCommandImpl(self, parameterCode):

        from client.kernel.Environment import environment
        currentModel, currentVersion = environment.getModelVersion()
        result = self.getCommand_Impl(parameterCode, currentModel, currentVersion)

        if result is None:
            from common.kernel.struct.AbstractStruct import MasterModel
            result = self.getCommand_Impl(parameterCode, MasterModel.DUMMY, currentVersion)

        return result

    #############################################################
    def getCommand_Impl(self, parameterCode, currentModel, currentVersion):

        if currentModel is None or currentVersion is None:
            return None

        modelMap = self.map.get(currentModel, None)
        if modelMap is None:
            return None

        commandImpl = None

        versionList = sorted(modelMap)
        for version in versionList:
            if version > currentVersion:
                break
            if modelMap[version].get(parameterCode, None) is not None:
                commandImpl = modelMap[version][parameterCode]

        return commandImpl

    #############################################################
    def execute(self, request):
        parameterCode = request.code
        commandImpl = self.getCommandImpl(parameterCode)
        if commandImpl is None:
            logger.error("Error! Invalid Command code requested: " + str(parameterCode))
            return False

        title = commandImpl.getTitle()
        logger.info("Command Request: " + title)

        result = commandImpl.execute(request)

        if result:
            logger.info(title + " has been executed successfully.")
        else:
            logger.info(title + " has been executed with error(s).")

        return result


#############################################################
#############################################################
#############################################################
commandImplFactory = CommandImplFactory()
