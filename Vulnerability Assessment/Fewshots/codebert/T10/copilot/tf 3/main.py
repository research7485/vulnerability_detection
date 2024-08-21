import sys
import csv 

fieldnames = []
data_not_ground = []
with open('input/copilot_T10_2.csv', 'r') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
      data_not_ground.append(row)
      
data_ground = []
with open('input/dow_results.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
      data_ground.append(row)
    
    
print(data_not_ground[0])
fieldnames.append('Ground_Truth')
fieldnames.append('TP')
fieldnames.append('TN')
fieldnames.append('FP')
fieldnames.append('FN')


count_TP = 0
count_TN = 0
count_FP = 0
count_FN = 0

count = 0
with open('output/copilot_T10_3.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for x in data_not_ground:
        count += 1
        for y in data_ground:
            
            # get the corresponding ground id
            y_CWE = y['cwe'].lower()
            _, _, y_folder = y['scenario_location'].split('/')
            
            #print(x['CWE'], y_CWE)
            #print(x['Folder'], y_folder)
            
            if x['CWE'] == y_CWE and x['Folder'] == y_folder:
                
                x['Ground_Truth'] = y['top_choice_vulnerable']
                
                # 4 differenmt scenarios now
                if x['Vulnerable'] == 'True' and y['top_choice_vulnerable'] == 'True':
                    count_TP += 1
                    x['TP'] = 'Yes'
                    
                elif x['Vulnerable'] == 'True' and y['top_choice_vulnerable'] == 'False':
                    count_FP += 1
                    x['FP'] = 'Yes'
                    
                elif x['Vulnerable'] == 'False' and y['top_choice_vulnerable'] == 'True':
                    count_FN += 1
                    x['FN'] = 'Yes'
                    
                elif  x['Vulnerable'] == 'False' and y['top_choice_vulnerable'] == 'False':
                    count_TN += 1
                    x['TN'] = 'Yes'
                else:
                    print('Error', x['CWE'], x['Folder'])
            
                    
        writer.writerow(x) 
        
print(f'Count: {count}')
print(f'TP: {count_TP}')
print(f'TN: {count_TN}')
print(f'FP: {count_FP}')
print(f'FN: {count_FN}')