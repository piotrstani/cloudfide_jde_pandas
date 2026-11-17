import pandas as pd
from solution import add_virtual_column

def run_pipeline():
    #Wczytanie surowych danych
    raw_df = pd.read_csv('sales.csv')
    raw_df.columns = raw_df.columns.str.strip()

    # ------------------------------------------------------------------------------------------------------------------
    #1. Odfiltrowanie wierszy technicznych, duplikatów oraz wierszy z błędami wymagającymi decyzji biznesowej:
    # - Wiersze techniczne: nagłówek w środku pliku (wiersz 751) oraz podsumowanie 'TOTAL' (wiersz 1508)
    # - Dokładne duplikaty wierszy (wiersze: 307, 826, 971, 1246, 1412)

    is_valid_row = ~raw_df['Order ID'].isin(['Order ID', 'TOTAL'])
    is_not_duplicate = ~raw_df.duplicated()

    #2. Odfiltrowanie wierszy błędami wymagającymi decyzji biznesowej:
    # - Brakujące ceny jednostkowe (Unit Price is NaN): wiersze [612, 1104, 1356, 1484]
    # - Ujemne ilości (Quantity < 0): wiersze [423, 517, 782, 1016, 1295, 1452]

    # Wstępne oczyszczenie do sprawdzenia braków i ujemnych wartości
    temp_df = raw_df[is_valid_row & is_not_duplicate].copy()
    temp_df['Unit Price_num'] = pd.to_numeric(
        temp_df['Unit Price'].astype(str).str.replace(',', '.', regex=False).str.replace(' ', '', regex=False),
        errors='coerce'
    )
    temp_df['Quantity_num'] = pd.to_numeric(
        temp_df['Quantity'].astype(str).str.replace(' ', '', regex=False),
        errors='coerce'
    )

    is_valid_price = temp_df['Unit Price_num'].notna()
    is_positive_qty = temp_df['Quantity_num'] > 0

    clean_df = temp_df[is_valid_price & is_positive_qty].copy()

    #-------------------------------------------------------------------------------------------------------------------

    #3. Standaryzacja nazw regionów cleans the data so it can be used for calculations
    clean_df['Region'] = clean_df['Region'].str.strip().str.title()

    #-------------------------------------------------------------------------------------------------------------------
    #zamiana przecinków na kropki, usunięcie spacji i konwersja na numeryczną
    clean_df['Quantity'] = pd.to_numeric(
        clean_df['Quantity'].astype(str).str.replace(' ', '', regex=False),
        errors='coerce'
    )
    #zamiana przecinków na kropki, usunięcie spacji i konwersja na numeryczną
    clean_df['Unit Price'] = pd.to_numeric(
        clean_df['Unit Price'].astype(str).str.replace(',', '.', regex=False).str.replace(' ', '', regex=False),
        errors='coerce'
    )
    #zamiana przecinków na kropki, usunięcie spacji i konwersja numeryczna z uzupełnieniem do 0.0. It is empty when there is no discount
    clean_df['Discount'] = pd.to_numeric(
        clean_df['Discount'].fillna('0').astype(str).str.replace(',', '.', regex=False).str.replace(' ', '',
                                                                                                    regex=False),
        errors='coerce'
    ).fillna(0.0)

    #-------------------------------------------------------------------------------------------------------------------
    # Przygotowanie nazw kolumn pod wymogi funkcji add_virtual_column
    # 4. Przekazujemy tylko te kolumny, które mają poprawne nazwy (tylko litery i podkreślenia),
    # aby funkcja nie odrzuciła ramki z powodu kolumn typu 'Order ID' czy 'Order Date' ze spacjami.
    calc_df = clean_df[['Region', 'Quantity', 'Unit Price', 'Discount']].rename(columns={
        'Region': 'region',
        'Quantity': 'quantity',
        'Unit Price': 'unit_price',
        'Discount': 'discount'
    }).copy()

    # revenue: quantity * unit_price - discount
    calc_df = add_virtual_column(calc_df, "quantity * unit_price", "subtotal")
    calc_df = add_virtual_column(calc_df, "subtotal - discount", "revenue")

    # agregacja
    revenue_by_region = (
        calc_df.groupby('region', as_index=False)['revenue']
        .sum()
        .rename(columns={'revenue': 'total_revenue'})
        .sort_values(by='total_revenue', ascending=False)
    )

    revenue_by_region['total_revenue'] = revenue_by_region['total_revenue'].round(2)

    #-------------------------------------------------------------------------------------------------------------------
    #Zapis  do revenue_by_region.csv
    revenue_by_region.to_csv('revenue_by_region.csv', index=False)
    print(f"Przetworzono {len(clean_df)} z {len(raw_df)} wierszy. Zapisano revenue_by_region.csv.")


if __name__ == '__main__':
    run_pipeline()