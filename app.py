import streamlit as st
import pandas as pd
import plotly.express as px

# Konfiguracja strony
st.set_page_config(
    page_title="Kalkulator cen pokoi",
    page_icon="🏨",
    layout="wide"
)

# Tytuł aplikacji
st.markdown("""
# 🏨 Kalkulator cen pokoi
---
""")

def calculate_prices(base_price):
    room_coefficients = {
        "Eco": 0.80,
        "Pokój 2 os z aneksem": 0.85,
        "Pokój 2 os z balkonem": 0.90,
        "Loftowy 1-2 os": 0.90,
        "Loftowy 3-4 os": 0.95,
        "Pokój 2 os z ogrodem": 0.95,
        "Comfort Plus 2 os": 0.95,
        "Comfort Plus z balkonem": 1.00,
        "Spokojna 42,49,53": 1.05,
        "Comfort Plus z ogrodem": 1.05,
        "Superior 1-2 os": 1.10,
        "Superior 3-4 os": 1.15
    }
    
    prices = {
        'Typ pokoju': [],
        'Cena bezzwrotna': [],
        'Cena zwrotna': []
    }
    
    for room_type, coefficient in room_coefficients.items():
        non_refundable = round(base_price * coefficient)
        refundable = round(base_price * (coefficient + 0.15))
        
        prices['Typ pokoju'].append(room_type)
        prices['Cena bezzwrotna'].append(non_refundable)
        prices['Cena zwrotna'].append(refundable)
    
    return pd.DataFrame(prices)

def main():
    # Input w jednej linii na górze
    st.markdown("### Wprowadź dane")
    col_input1, col_input2 = st.columns([2, 1])
    
    with col_input1:
        base_price_input = st.text_input(
            'Cena bazowa:',
            placeholder='np. 100',
            help='Wprowadź cenę bazową (możesz użyć kropki lub przecinka)'
        )
    
    with col_input2:
        calculate_button = st.button('💰 Oblicz ceny', type="primary")
    
    if base_price_input and calculate_button:
        try:
            base_price = float(base_price_input.replace(',', '.'))
            
            if base_price <= 0:
                st.error('❌ Cena bazowa musi być większa niż 0')
            else:
                st.success(f'✅ Cena bazowa: {base_price:.2f} PLN')
                df = calculate_prices(base_price)
                
                # Wyświetlenie tabeli na całej szerokości
                st.markdown("### Wyniki")
                st.dataframe(
                    df,
                    column_config={
                        "Typ pokoju": st.column_config.TextColumn(
                            "Typ pokoju",
                            width=300
                        ),
                        "Cena bezzwrotna": st.column_config.NumberColumn(
                            "Cena bezzwrotna",
                            format="%.0f PLN",
                            width=200
                        ),
                        "Cena zwrotna": st.column_config.NumberColumn(
                            "Cena zwrotna",
                            format="%.0f PLN",
                            width=200
                        )
                    },
                    hide_index=True,
                    height=500  # Stała wysokość tabeli, dostosuj według potrzeb
                )
                
                # Dwie kolumny na wykres i statystyki
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### Porównanie cen")
                    fig = px.bar(
                        df,
                        x='Typ pokoju',
                        y=['Cena bezzwrotna', 'Cena zwrotna'],
                        barmode='group',
                        height=400,
                        labels={'value': 'Cena (PLN)', 'variable': 'Rodzaj ceny'}
                    )
                    fig.update_layout(
                        xaxis_tickangle=-45,
                        margin=dict(l=20, r=20, t=20, b=20)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("### Statystyki")
                    st.metric("Średnia cena bezzwrotna", f"{df['Cena bezzwrotna'].mean():.0f} PLN")
                    st.metric("Średnia cena zwrotna", f"{df['Cena zwrotna'].mean():.0f} PLN")
                    st.metric("Różnica cen", f"{(df['Cena zwrotna'] - df['Cena bezzwrotna']).mean():.0f} PLN")
                    
                    # Przycisk eksportu na dole statystyk
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "📥 Pobierz jako CSV",
                        csv,
                        "ceny_pokoi.csv",
                        "text/csv",
                        key='download-csv'
                    )
                
        except ValueError:
            st.error('❌ Nieprawidłowy format ceny. Wprowadź liczbę.')

if __name__ == '__main__':
    main()
