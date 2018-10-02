import sys
from sqlalchemy import create_engine
import sqlite3
import re
import pandas as pd
import numpy as np
import pickle

import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.ensemble import AdaBoostClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from sklearn.metrics import classification_report, accuracy_score



def load_data(database_filepath):
    
    # read data
    ## (local) engine = sqlite3.connect(database_filepath)
    ## (local) df = pd.read_sql('SELECT * FROM DisasterResponse', engine)
    engine = create_engine('sqlite:///' + database_filepath)
    df = pd.read_sql_table('DisasterResponse', engine)
    
    # endogenous variable will be drived from messages  
    X = df['message']

    # exogenous variable is the dataframe of 36 categories
    cat = df.columns[-36:]
    Y = df[cat]

    # category names
    category_names = []
    for val in np.unique(Y.values):
        category_names.append("class_" + str(val))
    
    return X, Y, category_names


def tokenize(text):
    stop_words = stopwords.words('english')
    lemmatizer = WordNetLemmatizer()

    # normalizing text
    normalizer = re.sub(r'[^a-zA-Z0-9]', ' ', text.lower())

    # splitting text into tokens
    token = word_tokenize(normalizer)

    # lemmatize and remove stop words
    clean_token = [lemmatizer.lemmatize(word) for word in token if word not in stop_words]
    return clean_token


def build_model():
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize, lowercase=True, min_df=10)),
        ('tfidf', TfidfTransformer(smooth_idf=False)),
        ('clf', MultiOutputClassifier(AdaBoostClassifier()))
        ])

    return pipeline


def evaluate_model(model, X_test, Y_test, category_names):
    y_pred = model.predict(X_test)
    
    # classification report
    print(classification_report(Y_test.iloc[:,0], y_pred[:,0],
                                target_names=category_names,
                                digits=2))
    # average accuracy score
    score = []
    for i in range(36):
        score.append(accuracy_score(Y_test.iloc[:,i], y_pred[:,i]))
    print("Average accuracy_socore: {:.4f}".format(np.mean(score)))



def save_model(model, model_filepath):
    with open(model_filepath,"wb") as pkl_file:
        pickle.dump(model, pkl_file)
    pkl_file.close()


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()