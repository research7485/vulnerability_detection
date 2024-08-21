from sentence_transformers import SentenceTransformer, util
import descriptions_with_ids
import csv
import sys

def main():
  if len(sys.argv) != 3:
    sys.exit('Usage: python3 Executable Method_file Output_File_Name')
  
  model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
  # Two lists of sentences
  sentences1 = descriptions_with_ids.mitre_descriptions # This is reference to the list of dictionaries object in descriptions.py
  '''['The cat sits outside',
                'The cat sits inside',
                'The new movie is so great']'''
                
  list_of_dictionaries = get_palm_descriptions(sys.argv[1])

  #Compute embedding for both lists
  for row in range(len(sentences1)):
    embedding = model.encode(sentences1[row]['description'], convert_to_tensor=True)
    sentences1[row]['embedding'] = embedding
    
  for dictionary in range(len(list_of_dictionaries)): # dictionary variable is the index number of list
    embedding = model.encode(list_of_dictionaries[dictionary]['Palm_Description'], convert_to_tensor=True)
    list_of_dictionaries[dictionary]['embedding'] = embedding


  record_count = 0
  sum_col_1 = 0
  sum_col_2 = 0
  sum_col_3 = 0
  
  # Compute cosine-similarities and compare each entry in list_of_dictionary with sentences1
  with open(sys.argv[2], 'w', newline='') as f:
    fieldnames = ['Cwe', 'Folder', 'Palm_Description', 'Id_of_description_1', 'Description_from_cwe_website_1', 'Score_1', 'Id_of_description_2', 'Description_from_cwe_website_2', 'Score_2', 'Id_of_description_3', 'Description_from_cwe_website_3', 'Score_3', 
                  'Ground_Ranking', 'Ground_Score', 'Ground_ID', 'Ground_Desc']
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
    
    
      # Sort needed_list_of_dictionaries in desc order and and top 5 record as 1 entry in csv file
      sorted_list = sorted(needed_list_of_dictionaries, key=lambda dic: dic['Score'], reverse=True)
      #sorted_list = sorted_list[:5]
      
      data = {
        'Cwe': sorted_list[0]['Cwe'], 'Folder': sorted_list[0]['Folder'], 'Palm_Description': sorted_list[0]['Palm_Description'], 
        # empty initialization
        'Id_of_description_1': '', 'Description_from_cwe_website_1': '', 'Score_1': '',
        'Id_of_description_2': '', 'Description_from_cwe_website_2': '', 'Score_2': '',
        'Id_of_description_3': '', 'Description_from_cwe_website_3': '', 'Score_3': ''
      }
      
      for i, _ in enumerate(sorted_list[:3]):
        if float(sorted_list[i]['Score']) >= 0.3713:
          data['Id_of_description_' + str(i+1)] = sorted_list[i]['Cwe_id_of_description_from_cwe_website']
          data['Description_from_cwe_website_' + str(i+1)] = sorted_list[i]['Description_from_cwe_website']
          data['Score_' + str(i+1)] = sorted_list[i]['Score']
      
      # getting sum of first 3 scores
      sum_col_1 += float(sorted_list[0]['Score'])
      sum_col_2 += float(sorted_list[1]['Score'])
      sum_col_3 += float(sorted_list[2]['Score'])
        
      # Add the ground truth prosition and score
      _, ground_id = sorted_list[0]['Cwe'].split('-')
      for i, dic in enumerate(sorted_list): # For each dictionary
        if dic['Cwe_id_of_description_from_cwe_website'] == ground_id:
          data['Ground_Ranking'] = i + 1
          data['Ground_Score'] = dic['Score']
          data['Ground_ID'] = dic['Cwe_id_of_description_from_cwe_website']
          data['Ground_Desc'] = dic['Description_from_cwe_website']
          
        
      record_count += 1
      writer.writerow(data)
      
  print("Average of first score: {:.4f}".format(sum_col_1/record_count))
  print("Average of second score: {:.4f}".format(sum_col_2/record_count))
  print("Average of third score: {:.4f}".format(sum_col_3/record_count))
      

    
def min():
  get_palm_descriptions()
  
def get_palm_descriptions(method_file):
  data = []
  file_name = method_file#'method_descriptions_copilot.csv'
  with open(file_name, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
      data.append(row)
    
  return data
  
if __name__ == '__main__':
  main()
  