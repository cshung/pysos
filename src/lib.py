import pykd

# This file is meant for storing code that are shared across the commands

def getAddressFromExpression(expression):
    command = "?? (uint64_t*)(%s)" % expression
    # print(command)
    return pykd.dbgCommand(command).split()[3]

def getVTable(address):
    return pykd.dbgCommand("dqs %s L1" % address).split()[2]