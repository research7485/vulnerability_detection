import csv


import xml.etree.ElementTree as ET



def main():
    data = read_cwe('copilot_score_99_10.csv')
    
    with open('xxx.csv', 'w') as f:
        
        writer = csv.DictWriter(f, fieldnames=['CWE', 'Folder', 'Vulnerable', 'relation-with-Top-3', '#relevant-top-3', 'relations', 'similar-id-1', 'similar-id-2', 'similar-id-3', 'similar-id-4', 'similar-id-5', 'similar-id-6', 'similar-id-7', 'similar-id-8', 'similar-id-9', 'similar-id-10']) 
        writer.writeheader()
        # Now find relations 
        print(data[0])
        for row in data:
            print(row['cwe'][0])    # ground truth
            _, id = row['cwe'][0].split('-')
            
            #print(row['folder'][0])
            record = {'CWE': id,
                      'Folder': row['folder'],
                      'Vulnerable': row['Vulnerable'][0]}
            count_good_relations = 0
            last_col = ''
            for x in range(10):
                
                record[f'similar-id-{int(x) + 1}'] = row[f'{int(x) + 1}']
                
                # Skip empty cells
                if row[f'{int(x) + 1}'] == '':
                    continue
                
                a = child_and_father(id, row[f'{int(x) + 1}'])
                b = sibling(id, row[f'{int(x) + 1}'])
                
                if id == row[f'{int(x) + 1}']:
                    count_good_relations += 1
                    if len(last_col) == 0:
                        last_col = 'Same weakness'
                    else:
                        last_col = last_col + ', Same weakness'
                                                
                elif a is not None:
                    count_good_relations += 1
                    if len(last_col) == 0:
                        last_col = a
                    else:
                        last_col = last_col + f', {a}'
                        
                elif b is not None:
                    count_good_relations += 1
                    if len(last_col) == 0:
                        last_col = b
                    else:
                        last_col = last_col + f', {b}'
                 
            # Fill in last 3 columns       
            if count_good_relations > 0:
                record['relation-with-Top-3'] = 'Yes'
                record['#relevant-top-3'] = count_good_relations
            else:
                record['relation-with-Top-3'] = 'No'
                record['#relevant-top-3'] = 0
            
            record['relations'] = last_col
            
            writer.writerow(record)
                
            #print(last_col)
            
        
    #print(child_and_father('200', '1258'))
    #print(sibling('1273', '1258'))
        
    
def read_cwe(filename):
    data = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        
        for x in reader:
            row = {}
            row['cwe'] = str(x['Cwe']),
            row['folder'] =  x['Folder']
            row['Vulnerable'] = x['Vulnerable'],
            row['1'] = x['Id_of_description_1']
            row['2'] = x['Id_of_description_2']
            row['3'] = x['Id_of_description_3']
            row['4'] = x['Id_of_description_4']
            row['5'] = x['Id_of_description_5']
            row['6'] = x['Id_of_description_6']
            row['7'] = x['Id_of_description_7']
            row['8'] = x['Id_of_description_8']
            row['9'] = x['Id_of_description_9']
            row['10'] = x['Id_of_description_10']
            data.append(row)
            
    return data     
        
def child_and_father(lhs, rhs):
    '''
    Return all relationships especially child amd father relationship or else none (does not return sibling relationship)
    '''
    
    # Load the XML content from the file
    xml_file = "1000.xml"

    # Parse the XML content
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Define the namespace
    namespace = {'ns': 'http://cwe.mitre.org/cwe-7'}

    # Find all <Weakness> elements
    weaknesses = root.findall('.//ns:Weakness', namespaces=namespace)

    # Iterate through each <Weakness> element and extract the required information
    for weakness in weaknesses:
        weakness_id = weakness.get('ID')
        
        if lhs == weakness_id:

            related_weaknesses = weakness.findall('.//ns:Related_Weakness', namespaces=namespace)
            for related_weakness in related_weaknesses:
                related_weakness_id = related_weakness.get('CWE_ID')
                relation = related_weakness.get('Nature')
                view_id = related_weakness.get('View_ID')

                if view_id == '1000' and rhs == related_weakness_id:
                    return f'{lhs} {relation} {rhs}'
                
        if rhs == weakness_id:
            related_weaknesses = weakness.findall('.//ns:Related_Weakness', namespaces=namespace)
            for related_weakness in related_weaknesses:
                related_weakness_id = related_weakness.get('CWE_ID')
                relation = related_weakness.get('Nature')
                view_id = related_weakness.get('View_ID')

                if view_id == '1000' and lhs == related_weakness_id:
                    return f'{rhs} {relation} {lhs}'
                
    return None
    
    
def sibling(lhs, rhs):
    #get parents of lhs
    parents_lhs = parent_finder(lhs)
    parents_rhs = parent_finder(rhs)
    
    for parent in parents_lhs:
        if parent in parents_rhs:
            return f'{lhs} and {rhs} are siblings'
    
def parent_finder(id):
    
    parents = []
    # Load the XML content from the file
    xml_file = "1000.xml"

    # Parse the XML content
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Define the namespace
    namespace = {'ns': 'http://cwe.mitre.org/cwe-7'}

    # Find all <Weakness> elements
    weaknesses = root.findall('.//ns:Weakness', namespaces=namespace)

    # Iterate through each <Weakness> element and extract the required information
    for weakness in weaknesses:
        weakness_id = weakness.get('ID')
        
        if id == weakness_id:

            related_weaknesses = weakness.findall('.//ns:Related_Weakness', namespaces=namespace)
            for related_weakness in related_weaknesses:
                related_weakness_id = related_weakness.get('CWE_ID')
                relation = related_weakness.get('Nature')
                view_id = related_weakness.get('View_ID')

                if view_id == '1000' and relation == 'ChildOf':
                    parents.append(related_weakness_id)
                
    return parents

            
# Not used      
def reference():
    
    xxx = set()
    # Load the XML content from the file
    xml_file = "1000.xml"

    # Parse the XML content
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Define the namespace
    namespace = {'ns': 'http://cwe.mitre.org/cwe-7'}

    # Find all <Weakness> elements
    weaknesses = root.findall('.//ns:Weakness', namespaces=namespace)

    # Iterate through each <Weakness> element and extract the required information
    for weakness in weaknesses:
        weakness_id = weakness.get('ID')
        print("Weakness ID:", weakness_id)

        related_weaknesses = weakness.findall('.//ns:Related_Weakness', namespaces=namespace)
        for related_weakness in related_weaknesses:
            related_weakness_id = related_weakness.get('CWE_ID')
            relation = related_weakness.get('Nature')
            view_id = related_weakness.get('View_ID')
            print("Related Weakness ID:", related_weakness_id)
            print("Relation:", relation)
            print('View_id =', view_id)
            if view_id == '1000':
                xxx.add(relation)
        print("\n")
        
    print(xxx)
    
    
if __name__ == '__main__':
    main()