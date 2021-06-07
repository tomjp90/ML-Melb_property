from flask import Flask, render_template, redirect, jsonify, request
import scrape
from match_csvs import distance_crime
from model.persist import load_model, load_model_NL, predict_value, predict_value_NL
import requests
from flask import Flask, redirect, url_for, request
import numpy as np
import pandas as pd
from joblib import dump, load
import xgboost


app = Flask(__name__)


# Home route ----------------------------------------------------------------------------------------
@app.route("/")
def home():
      #return index html from home route    
      return render_template("index_template.html")
# predict route ----------------------------------------------------------------------------------------

# Crime source route----------------------------------------------------------------------------------------
@app.route("/source_crime")
def source_crime():
      #return index html from home route    
      return render_template("inner-page_source_crime_template.html", name="default")

# Kaggle source route----------------------------------------------------------------------------------------
@app.route("/source_kaggle")
def source_kaggle():
      #return index html from home route    
      return render_template("inner-page_source_kaggle_template.html", name="default")

# Team route----------------------------------------------------------------------------------------
@app.route("/team")
def team():
      #return index html from home route    
      return render_template("inner-page_team_template.html", name="default")

# Trends route----------------------------------------------------------------------------------------
@app.route("/trends")
def trends():
      #return index html from home route    
      return render_template("inner-page_trends_template.html", name="default")
      
# Predict route ----------------------------------------------------------------------------------------
@app.route('/predict', methods=['POST', 'GET'])
def login():
     
      try:
      # when request POST domain listing is sent and updated
            if request.method == 'POST':
                  # save value inputed in form
                  domain_listing = request.form['nm']
                  # run scraping function fro new domain listing url
                  features = scrape.scrape_house_listing(domain_listing)
                  print(f"************** SCRAPED FEATURES:{features}")
                  # ------------------------------ PREDICTION ------------------------------------

                  # Check State only Victoria
                  if (features["state"] == 'VIC'):
                        # ---------------- PROPERTY TYPE CONVERTED -----------
                        
                        # catch all types for apartment/unit/new apartment/flat
                        # and convert to numerical value
                        convert_type = features["ptype"][0]
                        # If House or Villa-------------------------------
                        if (convert_type == "H"):
                              Type_h = 1
                        elif (convert_type == "V"):
                              Type_h = 1
                        else:
                              Type_h = 0

                        # If townhouse/unit or flat -----------------------                       
                        if (convert_type == "A"):
                              Type_u = 1
                        elif (convert_type == "U"):
                              Type_u = 1                  
                        elif (convert_type == "N"):
                              Type_u = 1                     
                        elif (convert_type == "F"):
                              Type_u = 1
                        else:
                              Type_u = 0

                        # If Townhouse -----------------------------------
                        if (convert_type == "T"):
                              Type_t = 1
                        else:
                              Type_t = 0                   
                  

                        ################################## ADDITIONAL WORK FOR DEMO DAY ###########################################
                        # # -------------------- MELB AVG FOR PROPERTY TYPE FOR 2016-2018---------------------------
                        # # read in CSV and to find the average values for property type           
                        # type_lower = features["ptype"][0].lower()                                    
                        # avg_rooms, avg_price, avg_bathroom, avg_car, avg_landsize = melb_avg(type_lower)
                        # # append to features
                        # features["melbourne_avg"].append(round(avg_rooms,2))
                        # features["melbourne_avg"].append(round(avg_price,2))
                        # features["melbourne_avg"].append(round(avg_bathroom,2))
                        # features["melbourne_avg"].append(round(avg_car,2))
                        # features["melbourne_avg"].append(round(avg_landsize,2))

                        # -------------------- CRIME AND DISTANCE FOR SUBURB AVERAGED FOR 2016-2018  ---------------------------
                        # read in csv file and find distance and crime based on suburb that is scraped                    
                                          
                        suburb_lower = features["suburb"].lower()
                        distance, crime, avg_increase = distance_crime(suburb_lower)
                        
                        features["suburb_distance_crime"].append(round(distance,2))
                        features["suburb_distance_crime"].append(round(crime,2))
                        features["suburb_distance_crime"].append(round(avg_increase,2))  

                        # ------------------ PREDICTION VALUES SCALED BY MIN AND MAX VALUES --------------------------
                        # scale all values to predict
                              # manual scaling min and max
                        
                        Crime = (float(features["suburb_distance_crime"][1]) - 0) / (15485 - 0)                  
                        Distance = float(features["suburb_distance_crime"][0]) / (50 - 0)
                        Rooms = (float(features["bedrooms"]) - 1) / (12 - 1)
                        Bathrooms = (float(features["bathrooms"]) - 0 ) / (9 - 0)
                        Cars = (float(features["cars"]) - 0) / (18 - 0)
                        Month = ((float(features["month"]) - 1) - 0) / (11 - 0)
                        Year = (float(features["year"])-2016)/(2024 - 2016)                
                        Type_h = float(Type_h)
                        Type_t = float(Type_t)                     
                        Type_u = float(Type_u)  

                        print(features)
                        # IF LAND SIZE FOUND
                        if (features["landsize"] != "Unknown"): 

                              lands = features["landsize"]
                              print(f"==================THE LANDSIZE '{lands}'")

                              Landsize = (float(features["landsize"]) - 0) / (433014 - 0)

                              #================================ PREDICTION ==============================================
                              #==========================================================================================
                              #create pandas df to predict value with all features scaled
                              # #['Rooms', 'Distance', 'Bathroom', 'Car', 'Landsize', 'Year', 'Month', 'Crime', 'Type_h', 'Type_t', 'Type_u']
                              X = pd.DataFrame([Rooms, Distance, Bathrooms, Cars, Landsize, Year, Month, Crime, Type_h, Type_t, Type_u], 
                                                ['Rooms', 'Distance', 'Bathroom', 'Car', 'Landsize', 'Year', 'Month', 'Crime', 'Type_h', 'Type_t', 'Type_u']).T
                              model = load_model()
                              # run predict function from persist                                      
                              predict = model.predict(X)[0]
                              # format value predicted
                              prediction_formated = f"{predict:,}"

                              # Average % increase for the last 10 year ------------------------------------
                              inc_avg = 1 + (features["suburb_distance_crime"][2])/100
                              #------- PREDICTED VALUE                                                                     
                              #---2021 
                              pred_2021 = round(predict)                                   
                              pred_2021_f = f"{pred_2021:,}" 
                              features["prediction"].append(pred_2021)
                              features["predict_format"].append(pred_2021_f)                                   
                              #---2022 
                              pred_2022 = round(pred_2021 * inc_avg)                                                                      
                              pred_2022_f = f"{pred_2022 :,}"
                              features["future_predict"].append(pred_2022)
                              features["future_predict_format"].append(pred_2022_f)                                       
                              #---2023 
                              pred_2023 = round(pred_2022 * inc_avg)
                              pred_2023_f = f"{pred_2023:,}"  
                              features["future_predict"].append(pred_2023)
                              features["future_predict_format"].append(pred_2023_f)                                     
                              #---2024 
                              pred_2024 = round(pred_2023 * inc_avg)
                              pred_2024_f = f"{pred_2024:,}"
                              features["future_predict"].append(pred_2024)
                              features["future_predict_format"].append(pred_2024_f)      

                              # return prediction if everything scraped and predicted correctly
                              return render_template('inner-page_prediction_template.html', features=features)                

                        #IF NO LANDSIZE FOUND
                        elif (features["landsize"] == 'Unknown'):

                              #================================ PREDICTION ==============================================
                              #==========================================================================================
                              #create pandas df to predict value with all features scaled
                              # #['Rooms', 'Distance', 'Bathroom', 'Car', 'Landsize', 'Year', 'Month', 'Crime', 'Type_h', 'Type_t', 'Type_u']
                              X = pd.DataFrame([Rooms, Distance, Bathrooms, Cars, Year, Month, Crime, Type_h, Type_t, Type_u], 
                                                      ['Rooms', 'Distance', 'Bathroom', 'Car', 'Year', 'Month', 'Crime', 'Type_h', 'Type_t', 'Type_u']).T
                              
                              model = load_model_NL()
                              # run predict function from persist                                      
                              predict = model.predict(X)[0]
                              # format value predicted
                              prediction_formated = f"{predict:,}"

                              # Average % increase for the last 10 year ------------------------------------
                              inc_avg = 1 + (features["suburb_distance_crime"][2])/100
                              #------- PREDICTED VALUE                                                                     
                              #---2021 
                              pred_2021 = round(predict)                                   
                              pred_2021_f = f"{pred_2021:,}" 
                              features["prediction"].append(pred_2021)
                              features["predict_format"].append(pred_2021_f)                                   
                              #---2022 
                              pred_2022 = round(pred_2021 * inc_avg)                                                                      
                              pred_2022_f = f"{pred_2022 :,}"
                              features["future_predict"].append(pred_2022)
                              features["future_predict_format"].append(pred_2022_f)                                       
                              #---2023 
                              pred_2023 = round(pred_2022 * inc_avg)
                              pred_2023_f = f"{pred_2023:,}"  
                              features["future_predict"].append(pred_2023)
                              features["future_predict_format"].append(pred_2023_f)                                     
                              #---2024 
                              pred_2024 = round(pred_2023 * inc_avg)
                              pred_2024_f = f"{pred_2024:,}"
                              features["future_predict"].append(pred_2024)
                              features["future_predict_format"].append(pred_2024_f)   
                              


                              return render_template('inner-page_prediction_NL_template.html', features=features)

                  else:
                        error = "Wrong State! Only Property Listings from Victoria"
                        return render_template('inner-page_prediction_error_template.html', error=error)
                  # else: 
                  #       error = "Cannot find all features to predict!"
                  #       # return error html if all features not scraped
                  #       return render_template('inner-page_prediction_error_template.html', error=error)
            else:
                  # return error html if features is empty
                  return render_template('inner-page_predict_template.html')
      except:
            error = "Invalid URL"
                  # return error html if all features not scraped
            return render_template('inner-page_prediction_error_template.html', error=error)

 

if __name__ == "__main__":
    app.run(debug=True)
