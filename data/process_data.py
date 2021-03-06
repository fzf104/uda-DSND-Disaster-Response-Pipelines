import sys
import pandas as pd
from sqlalchemy import create_engine


def load_data(messages_filepath, categories_filepath):
    """
    load message and categories files, 
    merged them anad return dataframe .

    """
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath) 
    df = pd.merge(messages, categories, on="id")
    return df
             
def clean_data(df):
    """
    extract column names and values from texts for categories,
    convert values of categories to be numeric, 
    make sure all categories values here are dummy variable,
    then return the clean data.

    """
    

    # split the column of categories into 36 categories accordingly
    categories = df['categories'].str.split(";", expand=True)
    # set the column name as the first row without labels
    row = categories.loc[0,:]
    categories.columns = row.apply(lambda x: x.split('-')[0])
    
    # extract lables from the cells and turn them to be numeric
    for col in categories:
        categories[col] = categories[col].str.split('-').str[-1]
        categories[col] = pd.to_numeric(categories[col])
        categories[col] = categories[col].apply(lambda x: 1 if x>1 else x)

    # del the column of categories and concat the df of categories
    df.drop('categories', axis=1, inplace=True)
    df = pd.concat([df, categories], axis=1)
    
    # drop duplicates
    df.drop_duplicates(inplace=True)
    return df

def save_data(df, database_filename):
    """
    save dataframe to database

    """


    engine = create_engine('sqlite:///' + database_filename)
    df.to_sql('DisasterResponse', engine, if_exists='replace', index=False) 


def main():
    """
    This function is to combine all steps of process data in order including:
    1. load_data
    2. clean_data
    3. save_data

    Make sure 3 arguments will be inputed from command line properly, 
    if not return the instruction.  

    """
    


    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()