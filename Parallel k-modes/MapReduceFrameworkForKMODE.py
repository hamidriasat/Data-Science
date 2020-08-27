import json
import os



class MapReduce:
    def __init__(self):
        self.intermediate = {}
        self.result = []

    def emit_intermediate(self, key, value):
        self.intermediate.setdefault(key, [])
        self.intermediate[key].append(value)

    def emit(self, value):
        self.result.append(value) 

    def execute(self, data, mapper, reducer):
        for file in data:
            for line in open(data[file],encoding='utf-8-sig'):
            # record = json.loads(line)
            # mapper(record)
                mapper(line)

        # for line in data:
        #     mapper(line)

        os.remove("centriods.txt")
        for key in self.intermediate:
            reducer(key, self.intermediate[key])

        #jenc = json.JSONEncoder(encoding='latin-1')
        jenc = json.JSONEncoder()
        for item in self.result:
            print(jenc.encode(item))
