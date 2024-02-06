from elements import SourceNode, InterimNode, SinkNode

import time
def extract():
    print("Started Extracting")
    for i in range(10):
        yield i
        time.sleep(0.1)

def transform(record):
    return "#" + str(record)
    
source = SourceNode.SourceNode(extract())

transf = InterimNode.InterimNode(transform, source.output)

for e in transf.output:
    print(e)

for e in transf.output:
    print(e)
