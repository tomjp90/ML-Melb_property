import pandas as pd

################################## ADDITIONAL WORK FOR DEMO DAY ###########################################
# -------------------- MELB AVG FOR PROPERTY TYPE FOR 2016-2018---------------------------
# read in CSV and to find the average values for property type

# def melb_avg(type_lower):

#       avg_type = pd.read_csv("data/type_averages.csv")                 
#       # loop through rows
#       for index, row in avg_type.iterrows():
#             # find row that matches property type                         
#             if (type_lower == row["Type"]):
#                   # save all averages
#                   avg_rooms = row["Rooms"]
#                   avg_price = row["Price"]
#                   avg_bathroom = row["Bathroom"]
#                   avg_car = row["Car"]
#                   avg_landsize = row["Landsize"]
      
#       return(avg_rooms, avg_price, avg_bathroom, avg_car, avg_landsize)

# -------------------- CRIME AND DISTANCE FOR SUBURB AVERAGED FOR 2016-2018  ---------------------------
# read in csv file and find distance and crime based on suburb that is scraped    
        
def distance_crime(suburb_lower): 

      suburb_c_t = pd.read_csv("data/suburb_crime_distance_avincrease.csv")                  
      #loop through rows
      for index, row in suburb_c_t.iterrows():
            # find row that matches scrapes suburb    
            if (suburb_lower == row["Suburb"]):
                  # store row values                              
                  distance = row["Distance"]                             
                  crime  = row["Crime"]
                  avg_increase = row["Average_increase"]

      return(distance, crime, avg_increase)