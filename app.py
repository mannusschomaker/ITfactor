import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.spatial.distance as distance

# Loading data
@st.cache_data
def load_data():
    results_df = pd.read_csv('results.csv')  # replace with path to your data
    return results_df

# Function to create spider plot
def create_spider_plot(firm_data, rechtsgebieden_data,selected_firm):
    labels = np.array(rechtsgebieden_data.index)
    stats = rechtsgebieden_data.values

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    stats = np.concatenate((stats,[stats[0]]))  # closed
    angles = np.concatenate((angles,[angles[0]]))  # closed
    labels = np.concatenate((labels,[labels[0]]))  # closed

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, stats, color='red', alpha=0.25)
    ax.set_yticklabels([])
    ax.set_thetagrids(np.degrees(angles), labels)
    plt.title(selected_firm, y=0.5)
    return fig

# Function to create bar plot
def create_bar_plot(firm_data, beedigings_data,selected_firm,beedigings_cats):
    fig, ax = plt.subplots()
    beedigings_data.plot(kind='bar', color='skyblue', ax=ax)
    plt.title(f'Beëdigingsdatum categories for {selected_firm}')
    plt.ylabel('Count')
    plt.xlabel('Beëdigingsdatum category')
    plt.xticks(range(len(beedigings_cats)), ['> 10 years ago', '6-10 years ago', '3-6 years ago', '< 3 years ago'])
    return fig

# Main part of the app
def main():
    # Load the data
    results_df = load_data()
    

    # Create a dropdown to select firm
    firms = np.sort(results_df['Firm'].unique().tolist())
    selected_firm = "Van Doorne N.V."
    selected_firm = st.selectbox('Select a firm:', firms)
    all_rechtsgebieden = results_df.columns[6:] 




    # Get data for the selected firm
    firm_data = results_df[results_df['Firm'] == selected_firm].iloc[0]
    distances = results_df.apply(lambda row: distance.euclidean(row[6:], firm_data[6:]), axis=1)
    
    # For spider plot
    rechtsgebieden_data = firm_data[all_rechtsgebieden]
    rechtsgebieden_data = rechtsgebieden_data[rechtsgebieden_data > 0]
    rechtsgebieden_data = rechtsgebieden_data.drop('Niet bekend', errors='ignore')
    rechtsgebieden_data = rechtsgebieden_data.astype(float)
    rechtsgebieden_data = rechtsgebieden_data.nlargest(10)

    # Select the 'Beëdigingsdatum' categories
    beedigings_cats = ['Num_Beëdigingsdatum_Old_10', 'Num_Beëdigingsdatum_Old_6', 'Num_Beëdigingsdatum_Old_3', 'Num_Beëdigingsdatum_Young_3']

    # Get data for these categories
    beedigings_data = firm_data[beedigings_cats]
    beedigings_data['Num_Beëdigingsdatum_Old_6'] = beedigings_data['Num_Beëdigingsdatum_Old_6'] - beedigings_data['Num_Beëdigingsdatum_Old_10']
    beedigings_data['Num_Beëdigingsdatum_Old_3'] = beedigings_data['Num_Beëdigingsdatum_Old_3'] - beedigings_data['Num_Beëdigingsdatum_Old_6']

    st.markdown('De spiderplot, ook wel een radardiagram genoemd, is een waardevolle visuele weergave om de juridische expertise van een gekozen advocatenkantoor te ontcijferen. Het illustreert het aantal advocaten per rechtsgebied binnen het betreffende kantoor. Met de nadruk op de tien meest beoefende rechtsgebieden, toont de spiderplot effectief hoe de expertise van het kantoor zich verspreidt over deze verschillende rechtsgebieden. Door de verdeling van deze gebieden te observeren, kunnen we de veelzijdigheid van het kantoor of juist hun specialisatiegebieden bepalen.')
    # Draw plots
    st.pyplot(create_spider_plot(firm_data, rechtsgebieden_data,selected_firm))
    st.markdown('Verder kan er op dezelfde wijze naar de senioriteit van de advocaten binnen het geselecteerde kantoor worden gekeken. De advocaten zijn onderverdeeld in vier categorieën gebaseerd op hun beëdigingsdatum: 0-3 jaar, 3-6 jaar, 6-10 jaar en langer dan 10 jaar. De verdeling van deze categorieën verschaft inzicht in de ervaringsniveaus binnen het kantoor. Een grotere hoeveelheid advocaten met een langere beëdigingsdatum kan bijvoorbeeld duiden op een kantoor met meer ervaring en stabiliteit.')
    st.pyplot(create_bar_plot(firm_data, beedigings_data,selected_firm,beedigings_cats))
    st.markdown('Tenslotte wordt de data van de spiderplot genormaliseerd met behulp van de min-max normalisatie. Deze techniek transformeert de initiële ruwe data naar een gestandaardiseerd bereik, wat het mogelijk maakt om advocatenkantoren op een eerlijke wijze met elkaar te vergelijken. Met de genormaliseerde data, kan vervolgens Kullback–Leibler divergence worden berekend om de meest vergelijkbare kantoren te identificeren. Hierdoor kunnen kantoren op een objectieve manier worden vergeleken, ongeacht hun omvang of het aantal beoefende rechtsgebieden.')
    similar_firms = distances.nsmallest(10)
    row = results_df.loc[similar_firms.index[1]]
    # For spider plot
    rechtsgebieden_data = row[all_rechtsgebieden]
    rechtsgebieden_data = rechtsgebieden_data[rechtsgebieden_data > 0]
    rechtsgebieden_data = rechtsgebieden_data.drop('Niet bekend', errors='ignore')
    rechtsgebieden_data = rechtsgebieden_data.astype(float)
    rechtsgebieden_data = rechtsgebieden_data.nlargest(10)

    st.pyplot(create_spider_plot(firm_data, rechtsgebieden_data,row['Firm']))

    row = results_df.loc[similar_firms.index[2]]
    # For spider plot
    rechtsgebieden_data = row[all_rechtsgebieden]
    rechtsgebieden_data = rechtsgebieden_data[rechtsgebieden_data > 0]
    rechtsgebieden_data = rechtsgebieden_data.drop('Niet bekend', errors='ignore')
    rechtsgebieden_data = rechtsgebieden_data.astype(float)
    rechtsgebieden_data = rechtsgebieden_data.nlargest(10)

    st.pyplot(create_spider_plot(firm_data, rechtsgebieden_data,row['Firm']))

    row = results_df.loc[similar_firms.index[3]]
    
    # For spider plot
    rechtsgebieden_data = row[all_rechtsgebieden]
    rechtsgebieden_data = rechtsgebieden_data[rechtsgebieden_data > 0]
    rechtsgebieden_data = rechtsgebieden_data.drop('Niet bekend', errors='ignore')
    rechtsgebieden_data = rechtsgebieden_data.astype(float)
    rechtsgebieden_data = rechtsgebieden_data.nlargest(10)

    st.pyplot(create_spider_plot(firm_data, rechtsgebieden_data,row['Firm']))

if __name__ == "__main__":
    main()
