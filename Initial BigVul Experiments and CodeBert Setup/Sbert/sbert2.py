from sentence_transformers import SentenceTransformer, util
import descriptions_with_ids
import csv

def main():
  model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
  # Two lists of sentences
  sentences1 = descriptions_with_ids.mitre_descriptions # This is reference to the list of dictionaries object in descriptions.py
  '''['The cat sits outside',
                'The cat sits inside',
                'The new movie is so great']'''
                
  list_of_dictionaries = get_palm_descriptions()

  #Compute embedding for both lists
  for row in range(len(sentences1)):
    embedding = model.encode(sentences1[row]['description'], convert_to_tensor=True)
    sentences1[row]['embedding'] = embedding
    
  for dictionary in range(len(list_of_dictionaries)): # dictionary variable is the index number of list
    embedding = model.encode(list_of_dictionaries[dictionary]['Palm_Description'], convert_to_tensor=True)
    list_of_dictionaries[dictionary]['embedding'] = embedding

  # Compute cosine-similarities and compare each entry in list_of_dictionary with sentences1
  with open('copilot_result.csv', 'w', newline='') as f:
    fieldnames = ['Cwe', 'Folder', 'Palm_Description', 'Id_of_description_1', 'Description_from_cwe_website1', 'Score1', 'Id_of_description_2', 'Description_from_cwe_website2', 'Score2', 'Id_of_description_3', 'Description_from_cwe_website3', 'Score3', 'Id_of_description_4', 'Description_from_cwe_website4', 'Score4', 'Id_of_description_5', 'Description_from_cwe_website5', 'Score5']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    
    for x in range(len(list_of_dictionaries)):
      needed_list_of_dictionaries = []
      for y in range(len(sentences1)):
        cosine_score = util.cos_sim(list_of_dictionaries[x]['embedding'], sentences1[y]['embedding'])
        #print("{} \t\t {} \t\t Score: {:.4f}".format(list_of_dictionaries[x]['Palm_Description'], sentences1[y], cosine_score[0][0]))
        value = cosine_score[0][0].item()
        record = {
          'Cwe': list_of_dictionaries[x]['Cwe'],
          'Folder': list_of_dictionaries[x]['Folder'],
          'Palm_Description': list_of_dictionaries[x]['Palm_Description'],
          'Description_from_cwe_website': sentences1[y]['description'],
          'Cwe_id_of_description_from_cwe_website': sentences1[y]['id'],
          'Score': "{:.4f}".format(value)
        }
        
        needed_list_of_dictionaries.append(record)
    
    
      # Sort needed_list_of_dictionaries and and top 5 record as 1 entry in csv file
      sorted_list = sorted(needed_list_of_dictionaries, key=lambda dic: dic['Score'], reverse=True)
      
      # Get the 
      #sorted_list = sorted_list[:5]
      
      data = {
        'Cwe': sorted_list[0]['Cwe'], 'Folder': sorted_list[0]['Folder'], 'Palm_Description': sorted_list[0]['Palm_Description'], 
        'Id_of_description_1': sorted_list[0]['Cwe_id_of_description_from_cwe_website'], 'Description_from_cwe_website1': sorted_list[0]['Description_from_cwe_website'], 'Score1': sorted_list[0]['Score'], 
        'Id_of_description_2': sorted_list[1]['Cwe_id_of_description_from_cwe_website'], 'Description_from_cwe_website2': sorted_list[1]['Description_from_cwe_website'], 'Score2': sorted_list[1]['Score'], 
        'Id_of_description_3': sorted_list[2]['Cwe_id_of_description_from_cwe_website'], 'Description_from_cwe_website3': sorted_list[2]['Description_from_cwe_website'], 'Score3': sorted_list[2]['Score'], 
        'Id_of_description_4': sorted_list[3]['Cwe_id_of_description_from_cwe_website'], 'Description_from_cwe_website4': sorted_list[3]['Description_from_cwe_website'], 'Score4': sorted_list[3]['Score'], 
        'Id_of_description_5': sorted_list[4]['Cwe_id_of_description_from_cwe_website'], 'Description_from_cwe_website5': sorted_list[4]['Description_from_cwe_website'], 'Score5': sorted_list[4]['Score']
      }
      
      for i, j in enumerate(sorted_list):
        data['Id_of_description_' + str(i+1)] = sorted_list[i]['Cwe_id_of_description_from_cwe_website']
        data['Description_from_cwe_website']
        
        
      writer.writerow(data)
      

    
def min():
  get_palm_descriptions()
  
def get_palm_descriptions():
  data = []
  file_name = 'method_descriptions_copilot.csv'
  with open(file_name, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
      data.append(row)
    
  return data
  
if __name__ == '__main__':
  main()
  