import pykd
import argparse
from lib import getAddressFromExpression
from lib import getVTable

parser = argparse.ArgumentParser(description='Dumping the frame chain from a thread object')
parser.add_argument('thread', help='The thread object to dump the frame chain')

args=parser.parse_args()

frame = getAddressFromExpression("((coreclr!Thread*)%s)->m_pFrame" % args.thread)

while frame != "0xffffffff`ffffffff":
    print("%s %s" % (frame, getVTable(frame)))
    frame = getAddressFromExpression("((coreclr!Frame*)%s)->m_Next" % frame)
