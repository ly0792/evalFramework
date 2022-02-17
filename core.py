import json
import pandas as pd
import pickle

try:
    input_file = open("predictions2.jsonl", 'r')
    dictionary_list = pickle.load(input_file)
    for d in dictionary_list:
        print(d)
    input_file.close()

except:
    print('error occurred!')

input_file2 = open("preds_gtt_out.jsonl")
json_content2 = json.load(input_file2)

print('test')
