# Fetal_Health_ML_Flow

Steps in mlflow:

1.ML code

2.Create new env--mlflow

3. install mlflow

4.run the ML code with parameter values which generates mlruns and artifacts, and every run creates a new model.

---create a new file along with the newly created files-(mlproject) with details of this project:

***********
name: tutorial

conda_env: conda.yaml

entry_points:
  main:
    parameters:
      ne: int
      md: int
    command: "python fh_main.py {ne} {md}"
*********
--python main.py <argument1> <argument2> (To run from command prompt in vs code )
or
--mlflow run <github link with same main.py,datasets,readme,conda.yaml,and project file(mlproject)>  <argument>
*************
5.	mlflow ui
Follow the link to open a browser that tracks each run model and the given values and parameters.
*************

  # MLFLOW REGISTRY

1. Create a db in mysql .
2. Add this step inside main():

mlflow.set_tracking_uri("http://localhost:8001")

3. run this code in mlflow env to connect a sql server with mlflow to store the model details (from mlflow environment)
************
mlflow server --backend-store-uri mysql+pymysql://root:Sachin.1234@localhost/Fetal_Health_tracking --default-artifact-root file:"C:\Users\sachi\OneDrive\Documents\Reflections Infos\Project\ML_Flow\mlruns" -h 0.0.0.0 -p 8001
**************
4. Install sqlalchemy

5. Run the file from another python  terminal

6. Check the ui to track and also make sure details are being stored in the mysql db-----db-tables-register_models.(Here, everytime u run the code, registered_model_name="random_forest_Classifier" , so every run will keep updating the value in it.)

7. In the UI, the model is registered in the given name, you can open it and select the model into staging or production.
(Best model- production, 2nd best- staging)


SECOND STAGE:

1. Completed ML code.
2. Updated ml code with mlflow components
3. Created a new database fetal_heath in mysql
4. Open a new server with diff port number: 8001
5. Run code from cmd with diff parameters and track the models and compare 
6. Put the best performing model into production
7. For every model run, a run id is created.
8. The best model’s run id is selected and deployed to a new server with port number 1234.
***********
9. mlflow models serve -m C:\Users\gokul\Downloads\ML_flow\mlruns\0\<runid>\artifacts\model -h localhost -p 1234 
*************

10. Run the curl command in mlflow cmd with json values for every X feature.
curl -X POST http://localhost:1234/invocations -H "Content-Type: application/json; format=pandas-split" -d '{"columns":["baseline value","accelerations","fetal_movement","uterine_contractions","light_decelerations","severe_decelerations","prolongued_decelerations","abnormal_short_term_variability","mean_value_of_short_term_variability","percentage_of_time_with_abnormal_long_term_variability","mean_value_of_long_term_variability","histogram_width","histogram_min","histogram_max","histogram_number_of_peaks","histogram_number_of_zeroes","histogram_mode","histogram_mean","histogram_median","histogram_variance","histogram_tendency"],"data":[[-0.0308843924,-0.3048812642,0.0111303507,-0.4639189423,0.0373494708,-0.0574756037,-0.268754303,-0.0576028598,-0.2636191598,-0.5353612764,1.2817610857,-0.037125459,0.0480660349,-0.001415823,0.3160034467,-0.4584438153,0.0945189102,0.0249817554,-0.0062441596,-0.338550661,-0.5245255285],,[-0.8440140307,-0.8223883043,-0.1817755637,1.5731722894,2.064710531,-0.0574756037,-0.268754303,0.8732374625,0.4158566943,-0.5353612764,-1.2595924328,0.0399032259,-0.8655387782,-1.3392112661,0.3160034467,-0.4584438153,-0.4550176524,-1.1937537856,-0.9050779201,0.3517991427,1.1129800127]]}'
************
11.
import requests
host = 'localhost'
port = '1234'
url = f'http://{host}:{port}/invocations'
headers = {'Content-Type': 'application/json',}
#test_data is a Pandas dataframe with data for testing the ML model
#http_data = test_data.to_json(orient='split')
r = requests.post(url=url, headers=headers, data=http_data)
print(f'Predictions: {r.text}')


This is the code for predicting values in python directly.
(You can add it to the main.py code if u need to check.)

  
  
  
  
  
  
  
  
  
  
  .
  .
  .

