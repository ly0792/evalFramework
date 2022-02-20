import json
import pandas as pd


longqa_input = []

# Insert your data from LongQA prediction
with open("predictions2.jsonl") as f:
    for line in f:
        longqa_input.append(json.loads(line))

# Insert your data from gtt prediction
gtt_input = open("preds_gtt_out.jsonl")
gtt_input_json = json.load(gtt_input)

# Converting the inputs into dataframe, split the prediction and gold into 2 dataframe
longqa_df = pd.DataFrame(longqa_input)
gtt_df = pd.DataFrame.from_dict(gtt_input_json, orient='index')
gtt_df_pred = pd.DataFrame.from_dict(gtt_df['pred_templates'])
gtt_df_gold = pd.DataFrame.from_dict(gtt_df['gold_templates'])


# function to flatten the pred and gold dataframe
def flatten_input_df(dataFrame, colName):
    
    result = [] 
    col_names = ["incident_type", "PerpInd", "PerpOrg", "Target", "Victim", "Weapon"]
    for Index, row in dataFrame.iterrows():
        row_result = {}
        for c in col_names:
            value = [item[c] for item in row[colName]]
            if (len(value) == 0):
                continue
            if isinstance(value[0], list):
    
                result_list = []
                for item in row[colName]:
                    result_list.extend(item[c])
                row_result[c] = result_list
    
    
            elif isinstance(value[0],str):
                row_result[c] = ", ".join([item[c] for item in row[colName]])
        result.append(row_result)

    result_test = pd.DataFrame(result)
    result_test = result_test.drop(columns=['incident_type'])
    return result_test

gtt_df_gold_flatten = flatten_input_df(gtt_df_gold, 'gold_templates')
gtt_df_pred_flatten = flatten_input_df(gtt_df_pred, 'pred_templates')

# Preparing the final dataframe to merge all the data together
final_df = pd.DataFrame( dtype='object')
col_name = ["PerpInd", "PerpOrg", "Target", "Victim", "Weapon"]

for Index, row in longqa_df.iterrows():
    row_result = {}
    for c in col_name:

        row_result['docid'] = longqa_df.iloc[Index]['docid']
        row_result['field'] = c
        test = gtt_df_gold_flatten.iloc[Index]
        row_result['gold'] = gtt_df_gold_flatten.iloc[Index][c]
        row_result['gtt'] = gtt_df_pred_flatten.iloc[Index][c]
        row_result['long_qa'] = longqa_df.iloc[Index][c]

        final_df = final_df.append(row_result,ignore_index=True)  
            
                
        

