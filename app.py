import streamlit as st
import pandas as pd

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
    st.title('Kalkulator cen pokoi')
    
    base_price_input = st.text_input('Wprowadź cenę bazową:', '')
    
    if base_price_input:
        try:
            base_price = float(base_price_input.replace(',', '.'))
            
            if base_price <= 0:
                st.error('Cena bazowa musi być większa niż 0')
            else:
                df = calculate_prices(base_price)
                
                st.dataframe(
                    df,
                    column_config={
                        "Typ pokoju": st.column_config.TextColumn("Typ pokoju"),
                        "Cena bezzwrotna": st.column_config.NumberColumn(
                            "Cena bezzwrotna",
                            format="%.0f PLN"
                        ),
                        "Cena zwrotna": st.column_config.NumberColumn(
                            "Cena zwrotna",
                            format="%.0f PLN"
                        )
                    },
                    hide_index=True
                )
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Pobierz jako CSV",
                    csv,
                    "ceny_pokoi.csv",
                    "text/csv",
                    key='download-csv'
                )
                
        except ValueError:
            st.error('Nieprawidłowy format ceny. Wprowadź liczbę.')

if __name__ == '__main__':
    main()
