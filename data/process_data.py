# import packages
import sys
import pandas as pd
from sqlalchemy import create_engine
import sqlite3

import argparse

def load_data(messages_path, categories_path, database_filepath):
    """
        load_data is a function to load files of disaster, 
        then clean them and load clean data to SQL database.
        input: 
            - disaster_messages.csv
            - disaster_categories.csv
        output:
            - DisasterResponse.db

    """

    # read in file
    messages = pd.read_csv(messages_path)
    categories = pd.read_csv(categories_path)
    
    ## merge 2 datasets into a dataframe 
    df = pd.merge(messages, categories, on="id")


    # clean data

    ## split the column of categories into 36 categories accordingly
    categories = df['categories'].str.split(";", expand=True)
    ## set the column name as the first row without labels
    row = categories.loc[0,:]
    categories.columns = row.apply(lambda x: x.split('-')[0])

    ## extract lables from the cells and turn them to be numeric
    for col in categories:
        categories[col] = categories[col].str.split('-').str[-1]
        categories[col] = pd.to_numeric(categories[col])

    ## del the column of categories and concat the df of categories
    df.drop('categories', axis=1, inplace=True)
    df = pd.concat([df, categories], axis=1)
    
    ## drop duplicates
    df.drop_duplicates(inplace=True)

    # load to database
    
    ## (local) engine = sqlite3.Connection(database_filepath)
    
    engine = create_engine('sqlite:///InsertDatabaseName.db')
    df.to_sql('DisasterResponse', engine, if_exists='replace', index=False) 

    print("work")   


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath,database_filepath)

        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv' 'disaster_categories.csv '\
              'DisasterResponse.db')

if __name__ == '__main__':
    main()