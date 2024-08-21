import sys
import csv 

data = []
with open(sys.argv[1], 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
      data.append(row)

print(data[0])
   
TP = 0
TN = 0
FP = 0
FN = 0
Extra_FN = 0
Weak = 0
Safe = 0
  
for dic in data:
    if dic['Vulnerable'] == '1':
        Weak += 1
    else:
        Safe += 1
    
    if dic['TP'] == 'Yes':
        TP += 1
        continue
    
    elif dic['TN'] == 'Yes':
        TN += 1
        continue
    
    elif dic['FP'] == 'Yes':
        FP += 1
        continue
    
    elif dic['FN'] == 'Yes':
        FN += 1
        continue
        
    elif dic['Extra FN'] == 'Yes':
        Extra_FN += 1
        continue
        
        
        
print(f"Weak: {Weak}") 
print(f'Safe: {Safe}')
print(f'TP = {TP}')
print(f'TN = {TN}')
print(f'FP = {FP}')
print(f'FN = {FN}')
print(f'Extra FN = {Extra_FN}')

