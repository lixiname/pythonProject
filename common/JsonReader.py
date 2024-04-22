import json
import os

def read_model_config(path):
    with open(path, 'r') as f:
        data = json.load(f)
    return data


class LogRuntimeJson:
    """
         任务运行日志
    """
    def __init__(self,modelName,part_file_name,saveLogFlage=True):

        folderPath=os.path.join(os.getcwd(), "result", "runtime",modelName)
        catalogFloderExist('output', folderPath)
        self.logSavePath =os.path.join(folderPath,part_file_name+'.txt')
        self.saveLog=saveLogFlage
    def logJson(self,logDict):
        """
        @param logDict:
        """
        if self.saveLog:
            content=json.dumps(logDict, ensure_ascii=False, indent=1)
            with open(self.logSavePath,'w') as f:
                f.write(content)



def catalogFloderExist(pathTypeInputOrOutput,specificTaskDataPath):
    """
    用于判断目录是否存在并创建不存在的目录结构

    Args:
        pathTypeInputOrOutput: 描述将要传入的路径是输入还是输出路径，传入类型未字符串，有两种取值:input或output
        specificTaskDataPath: 传入的是将要打开的路径，该路径的值为文件夹目录且只可传入文件夹目录

    Returns:
        传入的目录存在返回true。不存在创建该目录并且返回false

    """
    #if os.path.isdir(specificTaskDataPath):

    #else:
       # print("error not dir ")
      #  return False

    path = specificTaskDataPath
    if not os.path.exists(path):
        os.makedirs(path)
        return False
    else:
        return True