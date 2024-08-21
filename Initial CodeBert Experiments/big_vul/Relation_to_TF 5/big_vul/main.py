import sys
import csv 

data_not_ground = []
with open('input/codebert_bigvul_relation_98_top_10.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
      data_not_ground.append(row)
      
    
    

with open('output/big_vul_relation_with_98_T10.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['Index', 'CWE', 'Vulnerable', 'relation-with-Top-3', '#relevant-top-3', 'relations', 'TP', 'TN', 'FP', 'FN', 'Extra FN', 'similar-id-1', 'similar-id-2', 'similar-id-3'])
    writer.writeheader()
    for x in data_not_ground:
        record = {'Index': x['Index'],
                  'CWE': x['CWE'],
                  'Vulnerable': x['Vulnerable'],
                'relation-with-Top-3': x['relation-with-Top-3'],
                '#relevant-top-3': x['#relevant-top-3'],
                'relations': x['relations'],
                'similar-id-1': x['similar-id-1'],
                'similar-id-2': x['similar-id-2'],
                'similar-id-3': x['similar-id-3'],
                'TP': '',
                'TN': '',
                'FP': '',
                'FN': '',
                'Extra FN': ''}
            
        
        #print(x['#relevant-top-3'], y['top_choice_vulnerable'])
                    
        if int(x['#relevant-top-3']) > 0 and x['Vulnerable'] == '1': #Something return by sbert (at least cwe must be related to original cwe) and actually vulnerable
            record['TP'] = 'Yes'
            
        elif x['similar-id-1'] != '' and x['Vulnerable'] == '0':  #Something return by sbert and actually not vulnerable
            record['FP'] = 'Yes'
            
        elif (x['similar-id-1'] == '' and  x['Vulnerable'] == '1'): # Nothing return by sbert and actually vulnerable
            record['FN'] = 'Yes'
            
        elif x['similar-id-1'] == '' and x['Vulnerable'] == '0':    #Nothing return by sbert and actually not vulnerable
            record['TN'] = 'Yes'
        
        elif (x['similar-id-1'] != '' and int(x['#relevant-top-3']) == 0 and x['Vulnerable'] == '1'):
            record['Extra FN'] = 'Yes'
                    
        writer.writerow(record) 