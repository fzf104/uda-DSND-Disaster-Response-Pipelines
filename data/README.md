# Data Process

Data Process is to execute ETL pipeline. 

## 1. Input

- disaster_message.csv
- disaster_categories.csv

## 2. Output

- DisasterResponse.db with table  DisasterResponse


## 3. Process
message is a file including texts which are recorded to predict disaster categories whose dataframe is stored in categories. Categories datum are dummy variable that should be seperated from docstrings. Finally, cleaned data is stored in SQL database.


## 4. Execute

Type:
<pre>
	
	python process_data.py 'disaster_messages.csv' 'disaster_categories.csv' 'DisasterResponse.db'

</pre>