from joblib import dump, load
import xgboost


#---------------------- LOAD MODELS   -----------------------------------
MODEL_PATH = "model/models/model.joblib"

def load_model():

      return load(MODEL_PATH)

# no landsize model
MODEL_PATH_NL = "model/models/model_without_landsize.joblib"

def load_model_NL():
      
      return load(MODEL_PATH_NL)

# no crime model
MODEL_PATH_NC = "model/models/model_no_crime.joblib"

def load_model_NC():
      
      return load(MODEL_PATH_NC)




      

#-------------------- PREDICTION FUNCTIONS -----------------------------
def predict_value(X):

      model = load_model()
      prediction = model.predict(X)                 

      return prediction


def predict_value_NL(X):

      model = load_model_NL()
      prediction = model.predict(X)                 

      return prediction

