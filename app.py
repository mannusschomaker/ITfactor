import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Loading data
@st.cache_data
def load_data():
    results_df = pd.read_csv('firm_data/results.csv')  # replace with path to your data
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
    plt.title(selected_firm)
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
    all_rechtsgebieden = results_df.columns[6:]

    # Create a dropdown to select firm
    firms = np.sort(results_df['Firm'].unique().tolist())
    selected_firm = "Van Doorne N.V."
    selected_firm = st.selectbox('Select a firm:', firms)

    # Get data for the selected firm
    firm_data = results_df[results_df['Firm'] == selected_firm].iloc[0]
    
    # For spider plot
    rechtsgebieden_data = firm_data[all_rechtsgebieden]
    rechtsgebieden_data = rechtsgebieden_data[rechtsgebieden_data > 0]
    rechtsgebieden_data = rechtsgebieden_data.drop('Niet bekend', errors='ignore')
    rechtsgebieden_data = rechtsgebieden_data.astype(int)
    rechtsgebieden_data = rechtsgebieden_data.nlargest(10)

    # Select the 'Beëdigingsdatum' categories
    beedigings_cats = ['Num_Beëdigingsdatum_Old_10', 'Num_Beëdigingsdatum_Old_6', 'Num_Beëdigingsdatum_Old_3', 'Num_Beëdigingsdatum_Young_3']

    # Get data for these categories
    beedigings_data = firm_data[beedigings_cats]
    beedigings_data['Num_Beëdigingsdatum_Old_6'] = beedigings_data['Num_Beëdigingsdatum_Old_6'] - beedigings_data['Num_Beëdigingsdatum_Old_10']
    beedigings_data['Num_Beëdigingsdatum_Old_3'] = beedigings_data['Num_Beëdigingsdatum_Old_3'] - beedigings_data['Num_Beëdigingsdatum_Old_6']

    # Draw plots
    st.pyplot(create_spider_plot(firm_data, rechtsgebieden_data,selected_firm))
    st.pyplot(create_bar_plot(firm_data, beedigings_data,selected_firm,beedigings_cats))

if __name__ == "__main__":
    main()
