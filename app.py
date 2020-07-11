# Importing essential libraries
from flask import Flask, render_template, request
import pickle
import numpy as np

# Load the Random Forest CLassifier model
filename = 'first-innings-score-ipl-model.pkl'
regressor = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    temp_array = list()
    
    if request.method == 'POST':
        
        batting_team = request.form['batting-team']
        if batting_team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif batting_team == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif batting_team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif batting_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif batting_team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif batting_team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif batting_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif batting_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]
            
            
        bowling_team = request.form['bowling-team']
        if bowling_team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0]
        elif bowling_team == 'Delhi Daredevils':
            temp_array = temp_array + [0,1,0,0,0,0,0,0]
        elif bowling_team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,1,0,0,0,0,0]
        elif bowling_team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,1,0,0,0,0]
        elif bowling_team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,1,0,0,0]
        elif bowling_team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,1,0,0]
        elif bowling_team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,1,0]
        elif bowling_team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,1]
        
        venue = request.form['venue']
        if venue == 'M Chinnaswamy Stadium':
            temp_array = temp_array + [1,0,0,0,0,0,0,0,0,0,0,0,0]
        elif venue == 'Punjab Cricket Association Stadium, Mohali': 
            temp_array = temp_array + [0,1,0,0,0,0,0,0,0,0,0,0,0]
        elif venue == 'MA Chidambaram Stadium, Chepauk':
            temp_array = temp_array + [0,0,1,0,0,0,0,0,0,0,0,0,0]
        elif venue =='Feroz Shah Kotla':
            temp_array = temp_array + [0,0,0,1,0,0,0,0,0,0,0,0,0]
        elif venue == 'Eden Gardens':
            temp_array = temp_array + [0,0,0,0,1,0,0,0,0,0,0,0,0]
        elif venue == 'Wankhede Stadium':
            temp_array = temp_array + [0,0,0,0,0,1,0,0,0,0,0,0,0]
        elif venue == 'Himachal Pradesh Cricket Association Stadium':
            temp_array = temp_array + [0,0,0,0,0,0,1,0,0,0,0,0,0]
        elif venue =='Rajiv Gandhi International Stadium, Uppal':
            temp_array = temp_array + [0,0,0,0,0,0,0,1,0,0,0,0,0]
        elif venue=='Shaheed Veer Narayan Singh International Stadium':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,1,0,0,0,0]
        elif venue =='JSCA International Stadium Complex':  
             temp_array = temp_array + [0,0,0,0,0,0,0,0,0,1,0,0,0]
        elif venue == 'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,1,0,0]
        elif venue == 'Punjab Cricket Association IS Bindra Stadium, Mohali':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,0,1,0]
        elif venue == 'Holkar Cricket Stadium':    
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,0,0,0,1]
        
        overs = float(request.form['overs'])
        runs = int(request.form['runs'])
        wickets = int(request.form['wickets'])
        runs_in_prev_5 = int(request.form['runs_in_prev_5'])
        wickets_in_prev_5 = int(request.form['wickets_in_prev_5'])
        striker = int(request.form['striker'])
        non_striker = int(request.form['non-striker'])
        
        temp_array = temp_array + [overs, runs, wickets, runs_in_prev_5, wickets_in_prev_5,striker, non_striker]
        
        data = np.array([temp_array])
        my_prediction = int(regressor.predict(data)[0])
              
        return render_template('result.html', lower_limit = my_prediction-10, upper_limit = my_prediction+5)



if __name__ == '__main__':
	app.run(debug=True)