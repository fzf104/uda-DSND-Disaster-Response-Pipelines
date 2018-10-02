# DisasterResponse Project

## 1. Project about
This is a project from Udacity which is about to setup piplines and to publish visulizaiont on web. Five main skills are used in:
  - I/O
  - natural language processing
  - supervised machine learning with multioutputclassifier
  - sklearn piplines and feature improvement
  - publish on web by flask
  
 ## 2. File description
 
<pre>
 - app
 | - template
 | |- master.html  # main page of web app
 | |- go.html  # classification result page of web app
 | - run.py  # Flask file that runs app

 - data
 |- disaster_categories.csv  # data to process 
 |- disaster_messages.csv  # data to process
 |- process_data.py
 |- InsertDatabaseName.db   # database to save clean data to

 - models
 |- train_classifier.py
 |- classifier.pkl  # saved model 

 - README.md
 - ETL Pipeline Preparation.html 
 - ETL Pipeline Preparation.ipynb # ETL data processing
 - ML Pipeline Preparation.html
 - ML Pipeline Preparation.ipynb # Modeling 
 </pre>

## 3. How to Run?
### 3.1 process_data.py
<pre>
> cd data
> python process_data.py disaster_messages.csv disaster_categories.csv DisasterResponse.db
</pre>

### 3.2 train_classifier.py
<pre>
> cd models
> python train_classifier.py ../data/DisasterResponse.db classifier.pkl
</pre>

### 3.3 run.py
under udacity workspace environment, type：
<pre>
evn | grep WORK
</pre>
get spaceid and spacedomain
![image](https://s3.cn-north-1.amazonaws.com.cn/u-img/8090fa27-82d0-4a02-8cf0-1d60cfe87c97)

in the new brower window, type:
<pre>
https://SPACEID-3001.SPACEDOMAIN
</pre>
replace the spaceid and spacedomain. Then,

<pre>
> cd app
> python run.py
</pre>

refresh the webpage.


