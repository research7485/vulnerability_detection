from sentence_transformers import SentenceTransformer, util
import descriptions
import csv

def main():
  model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
  # Two lists of sentences
  sentences1 = descriptions.descriptions # This is reference to the list object in descriptions.py
  '''['The cat sits outside',
                'The cat sits inside',
                'The new movie is so great']'''
                
  list_of_dictionaries = get_palm_descriptions()

  #Compute embedding for both lists
  embeddings1 = model.encode(sentences1, convert_to_tensor=True)
  for dictionary in range(len(list_of_dictionaries)): # dictionary variable is the index number of list
    embedding = model.encode(list_of_dictionaries[dictionary]['Palm_Description'], convert_to_tensor=True)
    list_of_dictionaries[dictionary]['embedding'] = embedding

  # Compute cosine-similarities and compare each entry in list_of_dictionary with sentences1
  with open('result.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['Cwe', 'Folder', 'Palm_Description', 'Description_from_cwe_website1', 'Score1', 'Description_from_cwe_website2', 'Score2', 'Description_from_cwe_website3', 'Score3', 'Description_from_cwe_website4', 'Score4', 'Description_from_cwe_website5', 'Score5'])
    writer.writeheader()
    
    for x in range(len(list_of_dictionaries)):
      needed_list_of_dictionaries = []
      for y in range(len(sentences1)):
        cosine_score = util.cos_sim(list_of_dictionaries[x]['embedding'], embeddings1[y])
        #print("{} \t\t {} \t\t Score: {:.4f}".format(list_of_dictionaries[x]['Palm_Description'], sentences1[y], cosine_score[0][0]))
        value = cosine_score[0][0].item()
        record = {
          'Cwe': list_of_dictionaries[x]['Cwe'],
          'Folder': list_of_dictionaries[x]['Folder'],
          'Palm_Description': list_of_dictionaries[x]['Palm_Description'],
          'Description_from_cwe_website': sentences1[y],
          'Score': "{:.4f}".format(value)
        }
        
        needed_list_of_dictionaries.append(record)
    
    
      # Sort needed_list_of_dictionaries and and top 5 record as 1 entry in csv file
      sorted_list = sorted(needed_list_of_dictionaries, key=lambda dic: dic['Score'], reverse=True)
      sorted_list = sorted_list[:5]
      
      data = {
        'Cwe': sorted_list[0]['Cwe'], 'Folder': sorted_list[0]['Folder'], 'Palm_Description': sorted_list[0]['Palm_Description'], 
        'Description_from_cwe_website1': sorted_list[0]['Description_from_cwe_website'], 'Score1': sorted_list[0]['Score'], 
        'Description_from_cwe_website2': sorted_list[1]['Description_from_cwe_website'], 'Score2': sorted_list[1]['Score'], 
        'Description_from_cwe_website3': sorted_list[2]['Description_from_cwe_website'], 'Score3': sorted_list[2]['Score'], 
        'Description_from_cwe_website4': sorted_list[3]['Description_from_cwe_website'], 'Score4': sorted_list[3]['Score'], 
        'Description_from_cwe_website5': sorted_list[4]['Description_from_cwe_website'], 'Score5': sorted_list[4]['Score']
      }
      writer.writerow(data)
      

    
      
  
  '''
  #Compute cosine-similarities
  cosine_scores = util.cos_sim(embeddings1, embeddings2)
  npArr = cosine_scores.cpu().detach().numpy()
  #print(npArr)

  #Output the pairs with their score
  for i in range(len(sentences1)):
      for j in range(len(sentences2)):  # You should loop through both lists to access all pairs
          print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[i], sentences2[j], cosine_scores[i][j]))'''

  '''f= open('outputEmbeddingReport.txt','w')
  for i in range(len(npArr)):
    for j in range(len(npArr)):
      f.write(str(npArr[i][j])+" ")
    f.write("\n")
  f.close()'''
def min():
  get_palm_descriptions()
  
def get_palm_descriptions():
  data = []
  file_name = 'method_descriptions.csv'
  with open(file_name, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
      data.append(row)
    
  return data
  
if __name__ == '__main__':
  main()
  