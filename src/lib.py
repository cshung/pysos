import pykd

# This file is meant for storing code that are shared across the commands

def getNumberFromExpression(expression):
    command = "?? (uint64)(%s)" % expression
    return pykd.dbgCommand(command).split()[1]

def getAddressFromExpression(expression):
    command = "?? (uint64_t*)(%s)" % expression
    return pykd.dbgCommand(command).split()[3]

def getVTable(address):
    return pykd.dbgCommand("dqs %s L1" % address).split()[2]