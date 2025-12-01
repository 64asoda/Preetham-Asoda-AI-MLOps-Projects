import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
from src.logger import get_logger
from alibi_detect.cd import KSDrift
from src.feature_store import RedisFeatureStore
from sklearn.preprocessing import StandardScaler
from prometheus_client import start_http_server,Counter,Gauge

logger = get_logger(__name__)

app = Flask(__name__ , template_folder="templates") # Initializing flask app

prediction_count = Counter('prediction_count', "Number of prediction count")
drift_count = Counter('drift_count', 'Number of times drift is detected')

MODEL_PATH = "artifacts/models/xgb_classifier.pkl"
with open (MODEL_PATH, 'rb') as model_file:
    model = pickle.load(model_file)

FEATURE_NAMES= ['CreditScore', 'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard',
'IsActiveMember', 'EstimatedSalary', 'Geography_Germany', 'Geography_Spain']

feature_store = RedisFeatureStore()
scaler = StandardScaler()

def fit_scaler_on_ref_data():
    entity_ids = feature_store.get_all_entity_ids()
    all_features = feature_store.get_batch_features(entity_ids)

    all_features_df = pd.DataFrame.from_dict(all_features, orient='index')[FEATURE_NAMES]

    scaler.fit(all_features_df)
    return scaler.transform(all_features_df)

historica_data = fit_scaler_on_ref_data() #existing data on which model is trained
ksd = KSDrift(x_ref=historica_data, p_val=0.05) #p_val high sensitivity


@app.route('/')
def home():
    return render_template('index.html') #If no prediction is happening

@app.route('/predict', methods=['POST']) #add /predict to index.html so form function will trigger predict function
def predict():
    try:
        data = request.form
        CreditScore = float(data["CreditScore"])
        Gender = int(data["Gender"])
        Age = int(data["Age"])
        Tenure = int(data["Tenure"])
        Balance = float(data["Balance"])
        NumOfProducts = int(data["NumOfProducts"])
        HasCrCard = int(data["HasCrCard"])
        IsActiveMember = int(data["IsActiveMember"])
        EstimatedSalary = float(data["EstimatedSalary"])
        Geography_Germany = int(data["Geography_Germany"])
        Geography_Spain = int(data["Geography_Spain"])

        features = pd.DataFrame([[CreditScore,Gender,Age,Tenure,Balance,NumOfProducts,HasCrCard,
        IsActiveMember,EstimatedSalary,Geography_Germany,Geography_Spain]], columns=FEATURE_NAMES)
        
        # Data Drift Detection
        features_scaled = scaler.transform(features)
        drift =  ksd.predict(features_scaled)
        print('Drift Response : ',drift)

        drift_response = drift.get('data',{})
        is_drift = drift_response.get('is_drift', None)

        if is_drift is not None and is_drift==1:
            print('Drift Detected')
            logger.info('Drift Detected')

            drift_count.inc() #by default increment number is 1

        prediction = model.predict(features)[0]
        prediction_count.inc()
        
        result = "Churn" if prediction==1 else "Stay"

        return render_template('index.html', prediction_text = f"The predicton is : {result}")

    except Exception as e:
        return jsonify({'error' : str(e)})
    
@app.route('/metrics')
def metrics():
    from prometheus_client import generate_latest
    from flask import Response
    #Prometheus cannot understand html, so using text/plain
    return Response(generate_latest(), content_type='text/plain') 
    
if __name__=='__main__':
    start_http_server(8000) #run prometheus before running flask app
    app.run(debug=True,host='0.0.0.0', port=5000)

    








