import google.generativeai as palm
import os
import sys
import csv
import pprint

def main():
    model_id = 'models/text-bison-001'
    palm.configure(api_key=os.environ['google_key'])

    
    for model in palm.list_models():
        pprint.pprint(model) # 🦎🦦🦬🦄

    
        
     

if __name__  == '__main__':
    main()