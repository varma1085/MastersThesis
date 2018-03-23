import json
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
from pprint import pprint
import os

class StanfordNLP:
    def __init__(self):
        self.server = ServerProxy(JsonRpc20(),
                                  TransportTcpIp(addr=("127.0.0.1", 8080), limit=50550000, timeout = 20000.0))
    
    def parse(self, text):
        return json.loads(self.server.parse(text))

nlp = StanfordNLP()

in_file = open("file.txt", "rt") # open file lorem.txt for reading text data
contents = in_file.read()         # read the entire file into a string variable
in_file.close()                   # close the file
print(contents)  		          # print contents

result = nlp.parse(contents)
pprint(result)

filename ="chiruNLPout.txt"
pathc = os.path.join(filename)
with open(pathc, 'w',) as f:
    counter=str(result)
    f.write(counter)


from nltk.tree import Tree
tree = Tree.fromstring(result['sentences'][0]['parsetree'])
pprint(tree)

