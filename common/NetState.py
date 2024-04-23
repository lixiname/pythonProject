'''
 fole
'''
import json
import os
import torch
#import torchinfo
import cv2

last_memory=0


def getMemoryNowAllocated():
    global last_memory
    last_memory=torch.cuda.memory_allocated()

    return last_memory

def PrintMemoryNowAllocated():
    now_memory=getMemoryNowAllocated()
    content=format(now_memory)
    return content

def getMemoryAllocatedChangedSize():
    last=last_memory
    now_memory=getMemoryNowAllocated()
    return now_memory-last

def PrintMemoryAllocatedChangedSize():
    last=last_memory
    now_memory=getMemoryNowAllocated()
    if now_memory-last>0:
        description='increase '
    else :
        description='decrease '
    content=format(abs(now_memory-last))
    return description+content

def format(memory):
    GB = memory // (1024 * 1024 * 1024)
    middle = (memory % (1024 * 1024 * 1024))
    MB = (middle // (1024 * 1024))
    KB = (middle % (1024 * 1024)) // 1024
    B = memory % 1024
    content = str(GB) + ' GB, ' + str(MB) + ' MB, ' + str(KB) + ' KB, ' + str(B) + ' B.'
    return content


def getMemoryNowReserved(parameters=None):
    content=format(torch.cuda.memory_reserved())
    return content

def printMemoryNowReserved(parameters=None):
    if parameters is not None:
        print(f'-----------------------------------\n{parameters}:')
    print(f'v-memory now Reserved: {getMemoryNowReserved()} ')
    print(f'-----------------------------------')

def getMemoryNowAllocatedPrint():
    print(f'v-memory now allocated: {PrintMemoryNowAllocated()}')

def getMemoryAllocatedChangedSizePrint():
    print(f'v-memory allocated ChangedSize: {PrintMemoryAllocatedChangedSize()}')

def getMemoryAllocatedNowAndChangedSizePrint(parameters=None):
    if parameters is not None:
        print(f'-----------------------------------\n{parameters} :')
    print(f'v-memory allocated ChangedSize: {PrintMemoryAllocatedChangedSize()} ; v-memory now allocated: {PrintMemoryNowAllocated()}')
    print(f'-----------------------------------')

def getMemorySummary():
    print(f'v-memorySummary:\n{torch.cuda.memory_summary()}')
def getSystemInitInformation():
    print(f'opencv version: {cv2.__version__}')
    print(f'torch version: {torch.__version__}')
    print(f'cuda version: {torch.version.cuda}')
    print(f'cuDNN version: {torch.backends.cudnn.version()}')

    print(f'cuda available {torch.cuda.is_available()}')
    print(f'v-memory allocated init {PrintMemoryNowAllocated()}')
    printMemoryNowReserved()
    print(f'device num : {torch.cuda.device_count()}')
    print(f'-----------------------------------\ ')

def getParamtersValue(model):
    print('-----------------------------------')
    print('model各层参数值:')
    print(list(model.parameters()))
    print('-----------------------------------')


def getParamtersStruct(model,size,dtype=torch.float32):
    #torchinfo.summary(models,size,dtypes=[dtype])
    print()

#缺一个类似的错误重定向类去记录错误run的输出








