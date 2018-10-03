# Train Classifier

This Process is to set a pipeline in order to build a classifier model. 

## 1. Input

- DisasterResponse.db with table  DisasterResponse  # result from data process
- disaster_categories.csv

## 2. Output

- classifier.pkl # trained model


## 3. Process
1. Extract words from message to count frequency by using nltk and applying TF-IDF.
2. set a multioutputclassifier model by using ensumble model.
3. set a pipeline to combine process 1 and 2.
4. evaluate model by using classifier report method then improve model by using GridSearchCV method.
5. Trained model save in a pickle file


## 4. Execute

Type:
<pre>
	
	python train_classifier.py '../data/DisasterResponse.db' 'classifier.pkl'

</pre>