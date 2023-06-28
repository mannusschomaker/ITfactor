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

# Function to create pie chart
def create_pie_chart(beedigings_data, selected_firm, beedigings_cats):
    fig, ax = plt.subplots()
    #colors
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
    explode = (0.05,0.05,0.05,0.05)
    beedigings_data.plot(kind='pie', colors = colors, labels=['> 10 years ago', '6-10 years ago', '3-6 years ago', '< 3 years ago'], ax=ax,startangle=90, pctdistance=0.85, explode = explode)
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    plt.title(f'Beëdigingsdatum categories for {selected_firm}')
    plt.ylabel('')
    # plt.legend(title="Categories", loc="upper right",ncol=4)
    ax.axis('equal')  
    plt.tight_layout()
    return fig




# Main part of the app
def main():
    # Load the data
    results_df = load_data()
    

    # Create a dropdown to select firm
    firms = np.sort(results_df['Firm'].unique().tolist())
    # selected_firm = "Van Doorne N.V."
    selected_firm = st.selectbox('Select a firm:', firms)
    all_rechtsgebieden = results_df.columns[6:] 




    # Get data for the selected firm
    firm_data = results_df[results_df['Firm'] == selected_firm].iloc[0]
    
    
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
    st.pyplot(create_pie_chart(beedigings_data,selected_firm,beedigings_cats))
    st.markdown('Tenslotte wordt de data van de spiderplot genormaliseerd met behulp van de min-max normalisatie. Deze techniek transformeert de initiële ruwe data naar een gestandaardiseerd bereik, wat het mogelijk maakt om advocatenkantoren op een eerlijke wijze met elkaar te vergelijken. Met de genormaliseerde data, kan vervolgens de KL divergence worden berekend om de meest vergelijkbare kantoren te identificeren. Hierdoor kunnen kantoren op een objectieve manier worden vergeleken, ongeacht hun omvang of het aantal beoefende rechtsgebieden.')
    
    results_df["Number_of_Lawyers"] = results_df["Number_of_Lawyers"].astype(int)
    min_laywers = results_df["Number_of_Lawyers"].min()
    max_laywers = results_df["Number_of_Lawyers"].max() 
        
    # st.markdown(values)
    values = st.slider(
        'Select a range of values',
        int(min_laywers), int(max_laywers), (int(min_laywers), int(max_laywers)))
    # filtered_df = results_df[(results_df["Number_of_Lawyers"] >= values[0]) & (results_df["Number_of_Lawyers"] <= values[0])].copy()
    # st.markdown(str(filtered_df.shape[0])+" kantoren voldoen aan de criteria")
    # if filtered_df.shape[0] < 1:
    #     return

    if values:
        results_df = results_df[results_df["Number_of_Lawyers"].between(values[0], values[1])]    
    distances = results_df.apply(lambda row: distance.euclidean(row[6:], firm_data[6:]), axis=1)
    if results_df.shape[0] > 4:
        number_of_firms = 4
        similar_firms = distances.nsmallest(number_of_firms)
    else:
        number_of_firms = results_df.shape[0]
        similar_firms = distances.nsmallest(number_of_firms)
    
    for i in range(number_of_firms):
        if i == 0:
            st.markdown(f"De meest vergelijkbare kantoren met {selected_firm} zijn:")
            continue

        row = results_df.loc[similar_firms.index[i]]
        # For spider plot
        rechtsgebieden_data = row[all_rechtsgebieden]
        rechtsgebieden_data = rechtsgebieden_data[rechtsgebieden_data > 0]
        rechtsgebieden_data = rechtsgebieden_data.drop('Niet bekend', errors='ignore')
        rechtsgebieden_data = rechtsgebieden_data.astype(float)
        rechtsgebieden_data = rechtsgebieden_data.nlargest(10)

        st.pyplot(create_spider_plot(firm_data, rechtsgebieden_data,row['Firm']))
        st.markdown(f"De Euclidische afstand tussen {selected_firm} en {row['Firm']} is {similar_firms.iloc[i]}")    
st.markdown('KL divergentie is een maat voor hoe een waarschijnlijkheidsverdeling afwijkt van een tweede, verwachte waarschijnlijkheidsverdeling. In tegenstelling tot Euclidische afstand is KL divergentie niet symmetrisch, wat betekent dat KL(P||Q) niet gelijk is aan KL(Q||P). Deze maat wordt gebruikt in velden als informatietheorie en machine learning om de "afstand" tussen twee waarschijnlijkheidsverdelingen te meten. De KL divergentie van twee discrete waarschijnlijkheidsverdelingen P en Q is gegeven door: ∑ P(i) log(P(i)/Q(i)) voor alle i De Kullback-Leibler divergentie heeft zijn wortels in de informatietheorie en geeft vaak relevantere resultaten bij het vergelijken van waarschijnlijkheden. Dus, de belangrijkste verschillen zijn:Euclidische afstand is symmetrisch (de afstand van A naar B is hetzelfde als van B naar A), terwijl KL divergentie dat niet is. Euclidische afstand is een maat voor daadwerkelijke afstand in ruimte, terwijl KL divergentie een maat is voor het verschil tussen twee waarschijnlijkheidsverdelingen. KL divergentie is een toepasselijker maat bij het omgaan met waarschijnlijkheden omdat het rekening houdt met de onzekerheid van gebeurtenissen, terwijl Euclidische afstand dat niet doet. In de context van het vergelijken van rechtsgebieden tussen verschillende kantoren, kan KL divergentie relevanter zijn dan de Euclidische afstand omdat het rekening houdt met de "verdeling" van de rechtsgebieden. Als een kantoor bijvoorbeeld een bepaald rechtsgebied domineert en een ander kantoor dat niet doet, dan zal de KL divergentie dit verschil in verdeling herkennen, terwijl de Euclidische afstand dat niet noodzakelijkerwijs doet. Het geeft dus een dieper inzicht in de overeenkomsten en verschillen tussen de specialiteiten van verschillende kantoren.')

if __name__ == "__main__":
    main()
