import pandas as pd
import streamlit as st
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist

@st.cache
def overall_recommendation(overall_df, overall_specialist, scaler, xscaled, user_kills, user_matches_won):

    to_predict = pd.DataFrame({'KILLS': user_kills, 'MATCHES_WON': user_matches_won}, index=['gamer_tag'])
    to_predict_scaled = scaler.transform(to_predict)

    result_df = pd.DataFrame(cdist(xscaled, to_predict_scaled), index=overall_df['NAME'], columns=['Distance']).sort_values('Distance').head()
    closest_player = result_df.index

    recommended_game = overall_df[overall_df['NAME'].isin(closest_player)]['GAME'].unique()
    recommended_character = overall_specialist[overall_specialist['NAME'].isin(closest_player)]['variable'].unique()

    return recommended_game, recommended_character