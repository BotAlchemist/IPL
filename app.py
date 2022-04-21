# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 22:49:32 2022

@author: Sumit
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title="IPL")
st.set_option('deprecation.showPyplotGlobalUse', False)



st.sidebar.header("IPL Analysis")
st.sidebar.text("Developed by Sumit Srivastava")
st.sidebar.text("sumvast@gmail.com")


df_match= pd.read_csv('IPL Matches 2008-2020.csv')
df_match['date'] = pd.to_datetime(df_match['date'])
df_match['Year']= df_match['date'].dt.year

time_frame = st.slider( 'Select time frame (years)', min(df_match['date'].dt.year), max(df_match['date'].dt.year), (min(df_match['date'].dt.year), max(df_match['date'].dt.year)))
df_match= df_match[df_match['Year']>= time_frame[0] ]
df_match= df_match[df_match['Year']<= time_frame[1]]


menu = st.sidebar.selectbox("", ['Overview', 'Team analysis'])
if menu == 'Overview':
    user_option= st.sidebar.selectbox(" ", ['Number of wins', 'City played', 'Stadium played'])
    
    if user_option == 'Number of wins':
        df_team_win= df_match['winner'].value_counts().to_frame(name="# wins")
        fig = plt.figure(figsize = (9, 6))
        plt.barh(df_team_win.index, df_team_win['# wins'])
        plt.xlabel("Number of Wins")
        plt.ylabel("Teams")    
        plt.title("No. of wins by each Team")
        for index, value in enumerate(df_team_win['# wins']):
            plt.text(value, index, str(value))
        st.pyplot(fig)
    
    elif user_option == 'City played':
        df_city= df_match['city'].value_counts().to_frame(name="# match")
        fig = plt.figure(figsize = (9, 7))
        plt.barh(df_city.index, df_city['# match'])
        plt.xlabel("Number of Matches")
        plt.ylabel("City")    
        plt.title("No. of matches played in each City")
        for index, value in enumerate(df_city['# match']):
            plt.text(value, index, str(value))
        st.pyplot(fig)    
    
    
    elif user_option == 'Stadium played':
        df_stadium= df_match['venue'].value_counts().to_frame(name="# match")
        fig = plt.figure(figsize = (9, 7))
        plt.barh(df_stadium.index, df_stadium['# match'])
        plt.xlabel("Number of Matches")
        plt.ylabel("Stadium")    
        plt.title("No. of matches played in each Stadium")
        for index, value in enumerate(df_stadium['# match']):
            plt.text(value, index, str(value))
        st.pyplot(fig)

elif menu == 'Team analysis':
    col1, col2, col3, col4= st.beta_columns(4)
    i_team_list= df_match['team2'].unique()
    i_team= st.sidebar.selectbox('Select Team', i_team_list)
    
    #________________________________________________________________________ Pie chart for win vs loss ______________________________
    no_of_wins= len(df_match[df_match['winner']== i_team])
    no_of_losses= (len(df_match[(df_match['team1']==i_team) | (df_match['team2']==i_team)])) - (len(df_match[df_match['winner']== i_team]))
    explode = (0.1, 0) 
    fig1, ax1 = plt.subplots()
    ax1.pie([no_of_wins, no_of_losses], explode=explode, labels=['Wins', 'Losses'], autopct='%1.1f%%',startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(i_team)
    col1.pyplot(fig1)
    
       
    
    #_________________________________________________ Pie chart for toss win % ____________________________________
    no_of_toss_wins= len(df_match[df_match['toss_winner']== i_team])
    no_of_tosses= (len(df_match[(df_match['team1']==i_team) | (df_match['team2']==i_team)])) 
    no_of_toss_losses= no_of_tosses- no_of_toss_wins
    explode = (0.1, 0) 
    fig1, ax1 = plt.subplots()
    ax1.pie([no_of_toss_wins, no_of_toss_losses], explode=explode, labels=['Wins', 'Losses'], autopct='%1.1f%%',startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(i_team + ' Toss Win %')
    col2.pyplot(fig1)
    
    #_____________________________________________ Pie chart for bat / field first preference ______________
    df_team= df_match[df_match['toss_winner']== i_team]
    team_bat = df_team['toss_decision'].value_counts()['bat']
    team_bowl= df_team['toss_decision'].value_counts()['field']
    explode = (0.1, 0) 
    fig1, ax1 = plt.subplots()
    ax1.pie([team_bat, team_bowl], explode=explode, labels=['Bat', 'Field'], autopct='%1.1f%%',startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(i_team + ' Bat/Field first preference after winning toss')
    col3.pyplot(fig1)
    
    #_____________________________________ Pie chart for Win % after winning toss __________________________________
    df_team= df_match[df_match['toss_winner']== i_team]
    df_team_win = df_team[df_team['winner']==i_team]
    team_win_toss= len(df_team_win)
    team_loss_toss= len(df_team) - len(df_team_win)
    explode = (0.1, 0) 
    fig1, ax1 = plt.subplots()
    ax1.pie([team_win_toss, team_loss_toss], explode=explode, labels=['Win', 'Loss'], autopct='%1.1f%%',startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(i_team + ' % win after winning toss')
    col4.pyplot(fig1)
    
    
    col1, col2= st.beta_columns(2)
    #_____________________________________________________________ Line chart for % wins across years __________________________________________
    team_hist=[]
    for i_year in df_match['Year'].unique():
        df_team_year= df_match[df_match['Year']==i_year]
        no_of_wins= len(df_team_year[df_team_year['winner']== i_team])
        no_of_losses= (len(df_team_year[(df_team_year['team1']==i_team) | (df_team_year['team2']==i_team)])) - (len(df_team_year[df_team_year['winner']== i_team]))
        try:
            win_percentage= (no_of_wins/(no_of_wins + no_of_losses))*100
            team_hist.append([i_year,win_percentage ])
        except:
            team_hist.append([i_year,0 ])
    
    df_team_hist= pd.DataFrame(team_hist, columns= ['Year', 'Win %']).set_index('Year')
    df_team_hist['Win %'] = df_team_hist['Win %'].round()

    fig = plt.figure(figsize = (8, 6))
    plt.plot( df_team_hist.index, df_team_hist['Win %']) 
    plt.axhline(y=50, color='r', linestyle='-')
    plt.xlabel("Year")
    plt.ylabel("Win percentage")    
    plt.title("Win % across years")     
    col1.pyplot(fig)
    
    
    # _______________________________ Bar chart showing straong/weak opponents ____________________________________
    select_opponent= col2.selectbox( "", ['Strong opponents', 'Weak opponents'])
    if select_opponent== 'Weak opponents':
        df_team_win = df_match[df_match['winner']== i_team]
        weak_teams_list=[]
        for index, row in df_team_win.iterrows():
            #print(row['team1'], row['team2'])
            match_between= [row['team1'], row['team2']]
            match_between.remove(i_team)
            weak_team= match_between
            weak_teams_list.append(  weak_team  )
            
        s_weak_team= pd.DataFrame(weak_teams_list).value_counts()
        df_weak_team= s_weak_team.to_frame()
        df_weak_team = df_weak_team.rename(columns= {0: 'Count'})
        df_weak_team= df_weak_team.reset_index()
        df_weak_team.columns = ['Team', 'Count']
        df_weak_team= df_weak_team.set_index('Team')
        
        
        
        fig = plt.figure(figsize = (9, 8))
        plt.barh(df_weak_team.index, df_weak_team['Count'])
        plt.xlabel("Number of Wins")
        plt.ylabel("Teams")    
        plt.title( i_team +  ": Weak opponents")
        for index, value in enumerate(df_weak_team['Count']):
            plt.text(value, index, str(value))
        col2.pyplot(fig)
        
    elif select_opponent== 'Strong opponents':
        df_team_played= df_match[(df_match['team1']==i_team) | (df_match['team2']==i_team)] 
        df_team_loss= df_team_played[df_team_played['winner']!= i_team]
        df_team_loss['winner'].value_counts()
        s_strong_team= df_team_loss['winner'].value_counts()
        df_strong_team= s_strong_team.to_frame()
        df_strong_team = df_strong_team.rename(columns= {0: 'Count'})
        df_strong_team= df_strong_team.reset_index()
        df_strong_team.columns = ['Team', 'Count']
        df_strong_team= df_strong_team.set_index('Team')
        
        fig = plt.figure(figsize = (9, 8))
        plt.barh(df_strong_team.index, df_strong_team['Count'])
        plt.xlabel("Number of Losses")
        plt.ylabel("Teams")    
        plt.title( i_team +  ": Strong opponents")
        for index, value in enumerate(df_strong_team['Count']):
            plt.text(value, index, str(value))
        col2.pyplot(fig)
    
        




 