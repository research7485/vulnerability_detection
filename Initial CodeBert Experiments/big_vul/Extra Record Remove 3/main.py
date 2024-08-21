import csv 

fieldnames = []
data_codebert = []
with open('codebert_big_vul_ranked_90_T10.csv', 'r') as f:
    writer = csv.DictReader(f)
    fieldnames = writer.fieldnames
    for row in writer:
        data_codebert.append(row)
        
        
data_sbert = []
with open('codebert_big_vul_ranked_top_3.csv', 'r') as f:
    writer = csv.DictReader(f)
    for row in writer:
        data_sbert.append(row)
        
print(len(data_codebert))
print(len(data_sbert))

count = 0
with open('codebert_big_vul_ranked_90_T10_fixed.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for record in data_codebert:
        
        # Check if the record was in sbert file or not
        found = False
        for dic in data_sbert:
            if record['Index'] == dic['Index']:
                found = True
                break
            
        if found:
            count += 1
            writer.writerow(record) 
            
print(count)