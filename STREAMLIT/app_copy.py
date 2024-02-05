import streamlit as st
import pandas as pd


def load_data():
    overall_df = pd.read_csv('https://github.com/nlewism/Gaming_Project/blob/Sam_branch/data/cleaned/players_for_eda/overall_kills_wons_final.csv?raw=true',index_col=0)
    wlratio_df = pd.read_csv('https://github.com/nlewism/Gaming_Project/blob/Sam_branch/data/cleaned/players_for_eda/headshots_wlratio_revives_final.csv?raw=true',index_col=0)
    kdratio_df = pd.read_csv('https://github.com/nlewism/Gaming_Project/blob/Sam_branch/data/cleaned/players_for_eda/deaths_assists_kd_final.csv?raw=true',index_col=0)

    return overall_df,wlratio_df,kdratio_df


st.title('FPS Game and Specialist Recommender')
overall_df,wlratio_df,kdratio_df = load_data()
overall_df
wlratio_df
kdratio_df
st.header("Please enter your player Stats")
st.text('Use this button to find your player stats.')

url = 'https://tracker.gg/'
st.markdown(f'''
<a href={url}><button style="background-color:GreenYellow;">Tracker Network: Find your stats for your favorite games</button></a>
''',
unsafe_allow_html=True)
gamer_tag = st.text_input('What is your gamertag?')
user_kills = st.number_input("Kills",min_value=0, value=58205)
user_deaths = st.number_input("Deaths",min_value=0, value=34470)

user_kd_selection = st.radio("Do you have K/D Ratio or need the calculation?", 
                             ["K/D Ratio Available", "Need Calculation","Either Kills or Death is not Available"])

if user_kd_selection == 'K/D Ratio Available':
    user_kd = st.number_input("K/D Ratio",min_value=0.0, value=3.28)
elif user_kd_selection == 'Need Calculation':
    user_kd = (user_kills/user_deaths)*100
else:
    user_kd = 0

user_matches_won = st.number_input("Matches Won",min_value=0, value=5821)

user_assists = st.number_input("Assists",min_value=0, value=16600)


user_headshots = st.number_input("Headshots",min_value=0, value=41593)
user_revives = st.number_input("Revives",min_value=0, value=4717)
user_wlratio = st.number_input("Win Loss Ratio",min_value=0.0, value=64.67)

user_specialty = st.radio("Do you have a specialty preference?", 
                             ["ASSAULT", "RECON","SUPPORT","ENGINEER","NONE"])

user_submit = st.button("Get your recommendation!")


if user_submit:

    to_predict = pd.DataFrame({'KILLS':user_kills,'MATCHES_WON': user_matches_won,
                               'DEATHS':user_deaths,'ASSISTS':user_assists,'K/D':user_kd,
                               'HEADSHOTS':user_headshots,'REVIVES':user_revives,
                               'WLRATIO':user_wlratio},index=[gamer_tag])
    to_predict

#
#    # Make predictions using the loaded model
#    prediction = loaded_model.predict(user_data)
#    
#    if prediction[0] == 1:
#        prediction_text = "At Risk"
#    else:
#        prediction_text = "Not At Risk"
#    
#    st.subheader("Prediction Result:")
#    st.write("Based on the provided information, you are", prediction_text, "of having a stroke.")