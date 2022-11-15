import pykd
from lib import getNumberFromExpression
from lib import getAddressFromExpression

head = getAddressFromExpression("&(coreclr!green_head)")
tail = getAddressFromExpression("&(coreclr!green_tail)")

def getNextSuspendedGreenThread(pSuspendedGreenThread):
    return getAddressFromExpression("((coreclr!SuspendedGreenThread*)%s)->next" % pSuspendedGreenThread)

def getPrevStackList(pStackList):
    return getAddressFromExpression("((coreclr!GreenThreadStackList*)%s)->prev" % pStackList)

def getNextStackList(pStackList):
    return getAddressFromExpression("((coreclr!GreenThreadStackList*)%s)->next" % pStackList)

suspendedGreenThread = getNextSuspendedGreenThread(head)

while suspendedGreenThread != tail:
    threadObject = getAddressFromExpression("((coreclr!SuspendedGreenThread*)%s)->pGreenThread->m_ExposedObject->unused" % suspendedGreenThread)
    threadId = getNumberFromExpression("((coreclr!SuspendedGreenThread*)%s)->pGreenThread->m_ThreadId" % suspendedGreenThread)
    currentStackPointer = getAddressFromExpression("((coreclr!SuspendedGreenThread*)%s)->currentStackPointer" % suspendedGreenThread)
    print("Green Thread #%s" % threadId)
    print("  Managed object        : %s" % threadObject)
    print("  Current stack pointer : %s" % currentStackPointer)
    print("  Stack Ranges")

    stackList = getAddressFromExpression("((coreclr!SuspendedGreenThread*)%s)->currentThreadStackSegment" % suspendedGreenThread)
    
    while True:
        prev = getPrevStackList(stackList)
        if prev == "0x00000000`00000000":
            break
        stackList = prev
    
    while stackList != "0x00000000`00000000":
        stackBase = getAddressFromExpression("((coreclr!GreenThreadStackList*)%s)->stackRange.stackBase" % stackList)
        stackLimit = getAddressFromExpression("((coreclr!GreenThreadStackList*)%s)->stackRange.stackLimit" % stackList)
        print("    [%s, %s)" % (stackBase, stackLimit))
        stackList = getNextStackList(stackList)

    suspendedGreenThread = getNextSuspendedGreenThread(suspendedGreenThread)