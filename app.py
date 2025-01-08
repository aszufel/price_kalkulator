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
    # Utworzenie dwóch kolumn
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Wprowadź dane")
        # Dodanie inputu z placeholder
        base_price_input = st.text_input(
            'Cena bazowa:',
            placeholder='np. 100',
            help='Wprowadź cenę bazową (możesz użyć kropki lub przecinka)'
        )
        
        # Dodanie kolorowego przycisku
        calculate_button = st.button('💰 Oblicz ceny', type="primary")
        
        if base_price_input and calculate_button:
            try:
                base_price = float(base_price_input.replace(',', '.'))
                
                if base_price <= 0:
                    st.error('❌ Cena bazowa musi być większa niż 0')
                else:
                    # Dodanie informacji o cenie bazowej
                    st.success(f'✅ Cena bazowa: {base_price:.2f} PLN')
                    
                    # Obliczenie cen
                    df = calculate_prices(base_price)
                    
                    # Wyświetlenie tabeli w prawej kolumnie
                    with col2:
                        st.markdown("### Wyniki")
                        st.dataframe(
                            df,
                            column_config={
                                "Typ pokoju": st.column_config.TextColumn(
                                    "Typ pokoju",
                                    width="medium"
                                ),
                                "Cena bezzwrotna": st.column_config.NumberColumn(
                                    "Cena bezzwrotna",
                                    format="%.0f PLN",
                                    width="small"
                                ),
                                "Cena zwrotna": st.column_config.NumberColumn(
                                    "Cena zwrotna",
                                    format="%.0f PLN",
                                    width="small"
                                )
                            },
                            hide_index=True,
                            use_container_width=True
                        )
                        
                        # Dodanie wykresu porównawczego
                        st.markdown("### Porównanie cen")
                        fig = px.bar(
                            df,
                            x='Typ pokoju',
                            y=['Cena bezzwrotna', 'Cena zwrotna'],
                            barmode='group',
                            title='Porównanie cen bezzwrotnych i zwrotnych',
                            labels={'value': 'Cena (PLN)', 'variable': 'Rodzaj ceny'}
                        )
                        fig.update_layout(xaxis_tickangle=-45)
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Dodanie przycisku do pobrania CSV
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            "📥 Pobierz jako CSV",
                            csv,
                            "ceny_pokoi.csv",
                            "text/csv",
                            key='download-csv'
                        )
                        
                        # Dodanie statystyk
                        st.markdown("### Statystyki")
                        col_stats1, col_stats2, col_stats3 = st.columns(3)
                        with col_stats1:
                            st.metric(
                                "Średnia cena bezzwrotna",
                                f"{df['Cena bezzwrotna'].mean():.0f} PLN"
                            )
                        with col_stats2:
                            st.metric(
                                "Średnia cena zwrotna",
                                f"{df['Cena zwrotna'].mean():.0f} PLN"
                            )
                        with col_stats3:
                            st.metric(
                                "Różnica cen",
                                f"{(df['Cena zwrotna'] - df['Cena bezzwrotna']).mean():.0f} PLN"
                            )
                            
            except ValueError:
                st.error('❌ Nieprawidłowy format ceny. Wprowadź liczbę.')

if __name__ == '__main__':
    main()
