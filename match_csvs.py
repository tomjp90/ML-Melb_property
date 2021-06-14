import pandas as pd

# -------------------- MELB AVG FOR PROPERTY TYPE FOR 2016-2018---------------------------
# read in CSV and to find the average values for property type

def melb_avg(type_lower):

      avg_type = pd.read_csv("data/type_averages.csv")      

      if (type_lower == "h"):
            type_lower = "h"
      elif (type_lower == "v"):
            type_lower = "h"

      # If townhouse/unit or flat -----------------------                       
      if (type_lower == "a"):
            type_lower = 'u'
      elif (type_lower == "u"):
            type_lower =  "u"                 
      elif (type_lower == "n"):
            type_lower = "u"                     
      elif (type_lower == "f"):
            type_lower = "u"  

      # If Townhouse -----------------------------------
      if (type_lower == "t"):
            type_lower = "t"
                           
      # loop through rows
      for index, row in avg_type.iterrows():
            # find row that matches property type                         
            if (type_lower == row["Type"]):

                  avg_rooms = row["Rooms"]
                  avg_price = row["Price"]
                  avg_bathroom = row["Bathroom"]
                  avg_car = row["Car"]
                  avg_landsize = row["Landsize"]
      
      return(avg_rooms, avg_price, avg_bathroom, avg_car, avg_landsize)

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

# --------------------------- FIND SUBURBS FROM DISTANCE TO CBD  ----------------------------------
def suburbs_by_dist(dist):

      suburbs_distance = pd.read_csv("data/suburb_crime_distance_avincrease.csv")     
      suburbs = [] 
      avg_inc = []         
      # loop through rows
      for index, row in suburbs_distance.iterrows():
            max_dist = dist + 1
            min_dist = dist - 1             

            distance = row["Distance"]        
            sub = row["Suburb"].upper()            
            inc = row["Average_increase"]


            if distance >= min_dist and distance <= max_dist:

                  suburbs.append(sub)
                  avg_inc.append(inc)

      #average all suburbs avg inc
      len_inc = len(avg_inc)
      temp = 0
      for inc in avg_inc:
            temp +=  float(inc)

      avg_inc_dist = round(temp/len_inc, 4)
      print(f"================= THE INC {avg_inc_dist}")
      data = {"suburbs" : suburbs,
                  "avg_inc_dist" : avg_inc_dist}

      return data