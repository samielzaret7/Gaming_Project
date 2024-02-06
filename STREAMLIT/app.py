import streamlit as st
from backend import load_player_data,load_player_specialists_data,overall_recommendation,wl_ratio_recommendation,kd_ratio_recommendation, load_character_data, image_width_func
from sklearn.preprocessing import StandardScaler


def main():
    st.title('FPS Game and Specialist Recommender')
    st.header("Please enter your player Stats")
    st.text('Use this button to find your player stats.')

    url = 'https://tracker.gg/'
    st.markdown(f'''
    <a href={url}><button style="background-color:#33B3A6;">Tracker Network: Find your stats for your favorite games</button></a>
    ''',
    unsafe_allow_html=True)


    name = st.text_input('What is your gamertag?')
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

    overall_df,wlratio_df,kdratio_df = load_player_data()
    overall_player_specialists,wlratio_player_specialists,kdratio_player_specialists, specialty_mapping = load_player_specialists_data()
    df_apex,df_rainbow,df_battlefield,df_overwatch = load_character_data()

    game_dataframes = {
            'Apex': df_apex,
            'Rainbow': df_rainbow,
            'BF2042': df_battlefield,
            'Overwatch': df_overwatch
        }

    if user_submit:
        scaler = StandardScaler()

        # Overall Recommendation
        overall_recommended_game, overall_filtered_characters, closest_player_for_display = overall_recommendation(overall_df, overall_player_specialists, scaler,user_kills,user_matches_won,specialty_mapping,user_specialty,name)

        overall_character_details = {}  

        for game in overall_recommended_game:

            image_width = image_width_func(game)
            game_characters_df = game_dataframes.get(game)

        if game_characters_df is not None:
            recommended_characters_details = game_characters_df[game_characters_df['Character'].isin(overall_filtered_characters)][['Character', 'Picture Link', 'Reference Link']]
            overall_character_details[game] = recommended_characters_details.to_dict(orient='records')

        if not recommended_characters_details.empty:
            st.write("---")
            st.subheader(f'Based on your Kills and Matches Won, the Recommended Characters for {game} are:')

            num_columns = 2
            num_rows = (len(recommended_characters_details) + num_columns - 1) // num_columns

            for i in range(0, len(recommended_characters_details), num_columns):
                col1, col2 = st.columns(2)

                character1 = recommended_characters_details.iloc[i]

                markdown_str1 = f"<div style='text-align: center;'><a href='{character1['Reference Link']}' target='_blank'><img src='{character1['Picture Link']}' alt='{character1['Character']}' width={image_width}/></a></div>\n<div style='text-align: center;'>{character1['Character']}</div>"
                col1.markdown(markdown_str1, unsafe_allow_html=True)

                if i + 1 < len(recommended_characters_details):
                    character2 = recommended_characters_details.iloc[i + 1]
                    col1.write("")
                    markdown_str2 = f"<div style='text-align: center;'><a href='{character2['Reference Link']}' target='_blank'><img src='{character2['Picture Link']}' alt='{character2['Character']}' width={image_width}/></a></div>\n<div style='text-align: center;'>{character2['Character']}</div>"
                    col2.markdown(markdown_str2, unsafe_allow_html=True)

            with st.expander("Closest Players to You"):
                st.dataframe(closest_player_for_display)



        # WLRatio Recommendation
        wl_ratio_recommended_game, wl_ratio_filtered_characters, closest_player_for_display = wl_ratio_recommendation(wlratio_df, wlratio_player_specialists, scaler, user_kills, user_matches_won, user_headshots, user_revives, user_wlratio,specialty_mapping,user_specialty,name)

        wl_ratio_character_details = {}  
    
        for game in wl_ratio_recommended_game:

            image_width = image_width_func(game)
            game_characters_df = game_dataframes.get(game)

            if game_characters_df is not None:

                recommended_characters_details = game_characters_df[game_characters_df['Character'].isin(wl_ratio_filtered_characters)][['Character', 'Picture Link', 'Reference Link']]
                wl_ratio_character_details[game] = recommended_characters_details.to_dict(orient='records')

        if not recommended_characters_details.empty:

            st.write("---")
            st.subheader(f'Based on your Headshots, Revives, and Win/Loss Ratio the Recommended Characters for {game} are:')

            num_columns = 2
            num_rows = (len(recommended_characters_details) + num_columns - 1) // num_columns

            for i in range(0, len(recommended_characters_details), num_columns):

                col1, col2 = st.columns(2)

                character1 = recommended_characters_details.iloc[i]

                markdown_str1 = f"<div style='text-align: center;'><a href='{character1['Reference Link']}' target='_blank'><img src='{character1['Picture Link']}' alt='{character1['Character']}' width={image_width}/></a></div>\n<div style='text-align: center;'>{character1['Character']}</div>"
                col1.markdown(markdown_str1, unsafe_allow_html=True)

                if i + 1 < len(recommended_characters_details):

                    col1.write("")

                    character2 = recommended_characters_details.iloc[i + 1]

                    markdown_str2 = f"<div style='text-align: center;'><a href='{character2['Reference Link']}' target='_blank'><img src='{character2['Picture Link']}' alt='{character2['Character']}' width={image_width}/></a></div>\n<div style='text-align: center;'>{character2['Character']}</div>"
                    col2.markdown(markdown_str2, unsafe_allow_html=True)

            with st.expander("Closest Players to You"):
                st.dataframe(closest_player_for_display)


        # KDRatio Recommendation
        kd_ratio_recommended_game, kd_ratio_filtered_characters, closest_player_for_display = kd_ratio_recommendation(kdratio_df, kdratio_player_specialists, scaler, user_kills, user_matches_won, user_deaths,user_assists,user_kd,specialty_mapping,user_specialty,name)

        kd_ratio_character_details = {}  
    
        for game in kd_ratio_recommended_game:

            image_width = image_width_func(game)
            game_characters_df = game_dataframes.get(game)

            if game_characters_df is not None:

                recommended_characters_details = game_characters_df[game_characters_df['Character'].isin(kd_ratio_filtered_characters)][['Character', 'Picture Link', 'Reference Link']]
                kd_ratio_character_details[game] = recommended_characters_details.to_dict(orient='records')

    

        if not recommended_characters_details.empty:

            st.write("---")
            st.subheader(f'Based on your Deaths, Assists, and K/D the Recommended Characters for {game} are:')

            num_columns = 2
            num_rows = (len(recommended_characters_details) + num_columns - 1) // num_columns

            for i in range(0, len(recommended_characters_details), num_columns):

                col1, col2 = st.columns(2)

                character1 = recommended_characters_details.iloc[i]

                markdown_str1 = f"<div style='text-align: center;'><a href='{character1['Reference Link']}' target='_blank'><img src='{character1['Picture Link']}' alt='{character1['Character']}' width={image_width}/></a></div>\n<div style='text-align: center;'>{character1['Character']}</div>"
                col1.markdown(markdown_str1, unsafe_allow_html=True)



                if i + 1 < len(recommended_characters_details):

                    col1.write("")
                    character2 = recommended_characters_details.iloc[i + 1]

                    markdown_str2 = f"<div style='text-align: center;'><a href='{character2['Reference Link']}' target='_blank'><img src='{character2['Picture Link']}' alt='{character2['Character']}' width={image_width}/></a></div>\n<div style='text-align: center;'>{character2['Character']}</div>"
                    col2.markdown(markdown_str2, unsafe_allow_html=True)

            with st.expander("Closest Players to You"):
                st.dataframe(closest_player_for_display)

 
if __name__ == '__main__':
    main()

