import pandas as pd
import streamlit as st
from scipy.spatial.distance import cdist

@st.cache_data

def load_player_data():
    overall_df = pd.read_csv('https://github.com/nlewism/Gaming_Project/blob/Sam_branch/data/cleaned/players_for_eda/overall_kills_wons_final.csv?raw=true',index_col=0)
    wlratio_df = pd.read_csv('https://github.com/nlewism/Gaming_Project/blob/Sam_branch/data/cleaned/players_for_eda/headshots_wlratio_revives_final.csv?raw=true',index_col=0)
    kdratio_df = pd.read_csv('https://github.com/nlewism/Gaming_Project/blob/Sam_branch/data/cleaned/players_for_eda/deaths_assists_kd_final.csv?raw=true',index_col=0)

    return overall_df,wlratio_df,kdratio_df

def load_player_specialists_data():
    overall_player_specialists = pd.read_csv('https://github.com/nlewism/Gaming_Project/blob/Sam_branch/data/cleaned/players_for_eda/overall_specialist.csv?raw=true',index_col=0)
    wlratio_player_specialists = pd.read_csv('https://github.com/nlewism/Gaming_Project/blob/Sam_branch/data/cleaned/players_for_eda/wlratio_specialist.csv?raw=true',index_col=0)
    kdratio_player_specialists = pd.read_csv('https://github.com/nlewism/Gaming_Project/blob/Sam_branch/data/cleaned/players_for_eda/kdratio_specialist.csv?raw=true',index_col=0)
    specialty_mapping = pd.read_csv('https://github.com/nlewism/Gaming_Project/blob/Sam_branch/data/cleaned/specialty_mapping_df.csv?raw=true',index_col=0)
    return overall_player_specialists,wlratio_player_specialists,kdratio_player_specialists, specialty_mapping

def load_character_data():
    df_apex = pd.read_csv('https://github.com/nlewism/Gaming_Project/blob/Sam_branch/data/cleaned/game_specialists/apex_legends_final.csv?raw=true',index_col=0)
    df_rainbow = pd.read_csv('https://github.com/nlewism/Gaming_Project/blob/Sam_branch/data/cleaned/game_specialists/r6_operators_final.csv?raw=true',index_col=0)
    df_battlefield = pd.read_csv('https://github.com/nlewism/Gaming_Project/blob/Sam_branch/data/cleaned/game_specialists/bf2042_specialists_final.csv?raw=true',index_col=0)
    df_overwatch = pd.read_csv('https://github.com/nlewism/Gaming_Project/blob/Sam_branch/data/cleaned/game_specialists/overwatch_heroes_final.csv?raw=true',index_col=0)

    return df_apex,df_rainbow,df_battlefield,df_overwatch


def overall_recommendation(overall_df, overall_specialist, scaler,user_kills,user_matches_won,specialty_mapping,user_specialty,name):
    df_recommender = overall_df[['Kills','Matches_Won']]
    xscaled = scaler.fit_transform(df_recommender)
    to_predict = pd.DataFrame({'Kills': user_kills, 'Matches_Won': user_matches_won}, index=['You'])
    to_predict_scaled = scaler.transform(to_predict)

    result_df = pd.DataFrame(cdist(xscaled, to_predict_scaled), index=overall_df['name'], columns=['Distance']).sort_values('Distance').head()
    
    to_predict['name']=name
    closest_player_for_display = result_df.merge(overall_df, on='name')
    closest_player_for_display = pd.concat([to_predict,closest_player_for_display])
    closest_player_for_display = closest_player_for_display[['name','Kills', 'Matches_Won']]
    
    closest_player = result_df.index

    overall_recommended_game = overall_df[overall_df['name'].isin(closest_player)]['Game'].unique()
    overall_recommended_character = overall_specialist.loc[overall_specialist.index.isin(closest_player), 'variable'].unique()

    if user_specialty != 'NONE':
        
        recommended_characters_with_specialty = specialty_mapping[specialty_mapping['Character'].isin(overall_recommended_character)]
        overall_filtered_characters = recommended_characters_with_specialty[recommended_characters_with_specialty['Specialty'] == user_specialty]['Character'].tolist()
    else:
        
        overall_filtered_characters = overall_recommended_character

    return overall_recommended_game, overall_filtered_characters, closest_player_for_display

def wl_ratio_recommendation(wlratio_df, wlratio_specialist, scaler, user_kills, user_matches_won, user_headshots, user_revives, user_wlratio,specialty_mapping,user_specialty,name):
    # Recommendation logic for W/L ratio model

    df_recommender = wlratio_df[['Kills','Matches_Won','Headshots','Revives','WLRatio']]
    xscaled = scaler.fit_transform(df_recommender)
    to_predict = pd.DataFrame({'Kills': user_kills, 'Matches_Won': user_matches_won,'Headshots':user_headshots,'Revives':user_revives,'WLRatio':user_wlratio}, index=['You'])
    to_predict_scaled = scaler.transform(to_predict)
    result_df = pd.DataFrame(cdist(xscaled, to_predict_scaled), index=wlratio_df['name'], columns=['Distance']).sort_values('Distance').head()
    
    to_predict['name']=name
    closest_player_for_display = result_df.merge(wlratio_df, on='name')
    closest_player_for_display = pd.concat([to_predict,closest_player_for_display])
    closest_player_for_display = closest_player_for_display[['name','Kills', 'Matches_Won','Headshots','Revives','WLRatio']]
    
    closest_player = result_df.index
    wl_ratio_recommended_game = wlratio_df[wlratio_df['name'].isin(closest_player)]['Game'].unique()
    wl_ratio_recommended_character = wlratio_specialist.loc[wlratio_specialist.index.isin(closest_player),'variable'].unique()

    if user_specialty != 'NONE':
        
        recommended_characters_with_specialty = specialty_mapping[specialty_mapping['Character'].isin(wl_ratio_recommended_character)]
        wl_ratio_filtered_characters = recommended_characters_with_specialty[recommended_characters_with_specialty['Specialty'] == user_specialty]['Character'].tolist()
    else:
        
        wl_ratio_filtered_characters = wl_ratio_recommended_character


    return wl_ratio_recommended_game, wl_ratio_filtered_characters, closest_player_for_display

def kd_ratio_recommendation(kdratio_df, kdratio_specialist, scaler, user_kills, user_matches_won, user_deaths,user_assists,user_kd,specialty_mapping,user_specialty,name):
    # Recommendation logic for KD ratio model
    df_recommender = kdratio_df[['Kills','Matches_Won','Deaths','Assists','K/D']]
    xscaled = scaler.fit_transform(df_recommender)
    to_predict = pd.DataFrame({'Kills': user_kills, 'Matches_Won': user_matches_won,'Deaths':user_deaths,'Assists':user_assists,'K/D':user_kd}, index=['You'])
    to_predict_scaled = scaler.transform(to_predict)
    result_df = pd.DataFrame(cdist(xscaled, to_predict_scaled), index=kdratio_df['name'], columns=['Distance']).sort_values('Distance').head()
    
    to_predict['name']=name
    closest_player_for_display = result_df.merge(kdratio_df, on='name')
    closest_player_for_display = pd.concat([to_predict,closest_player_for_display])
    closest_player_for_display = closest_player_for_display[['name','Kills', 'Matches_Won','Deaths','Assists','K/D']]
    
    closest_player = result_df.index
    kd_ratio_recommended_game = kdratio_df[kdratio_df['name'].isin(closest_player)]['Game'].unique()
    kd_ratio_recommended_character = kdratio_specialist.loc[kdratio_specialist.index.isin(closest_player),'variable'].unique()
    
    if user_specialty != 'NONE':
        
        recommended_characters_with_specialty = specialty_mapping[specialty_mapping['Character'].isin(kd_ratio_recommended_character)]
        kd_ratio_filtered_characters = recommended_characters_with_specialty[recommended_characters_with_specialty['Specialty'] == user_specialty]['Character'].tolist()
    else:
        
        kd_ratio_filtered_characters = kd_ratio_recommended_character


    return kd_ratio_recommended_game, kd_ratio_filtered_characters, closest_player_for_display


def image_width_func(game):
    if game == 'Apex':
        image_width=350
    elif game =='BF2042':
        image_width=300
    else:
        image_width=200

    return image_width
