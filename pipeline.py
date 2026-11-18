import pandas as pd
from solution import add_virtual_column

def parse_number(s: pd.Series) -> pd.Series:
    cleaned = (s.astype('string')
                 .str.replace(r'[\s\u00a0]', '', regex=True)
                 .str.replace(',', '.', regex=False))
    return pd.to_numeric(cleaned, errors='coerce')

def run_pipeline():

    raw_df = pd.read_csv('sales.csv', sep=',', dtype=str, encoding='utf-8-sig')
    raw_df.columns = raw_df.columns.str.strip()

    # ------------------------------------------------------------------------------------------------------------------
    # Odfiltrowanie wierszy technicznych, duplikatów
    is_not_technical_row = ~raw_df['Order ID'].str.strip().str.upper().isin(['ORDER ID', 'TOTAL'])
    is_not_duplicate = ~raw_df.duplicated()

    stats = { 'technical': int((~is_not_technical_row).sum()), 'duplicates': int((~is_not_duplicate).sum())}

    temp_df = raw_df[is_not_technical_row & is_not_duplicate].copy()

    # Standardize region names to clean the data for calculations.
    temp_df['region'] = temp_df['Region'].str.strip().str.title()
    # Replace commas with dots, remove spaces, and convert to numeric format
    temp_df['unit_price'] = parse_number(temp_df['Unit Price'])
    temp_df['quantity'] = parse_number(temp_df['Quantity'])
    # ... and filling missing values with 0.0.
    temp_df['discount'] = parse_number(temp_df['Discount']).fillna(0.0)

    # Filtering out rows where 'Unit Price' is NaN
    is_valid_price = temp_df['unit_price'].notna()

    # Keep only rows where Quantity >
    is_positive_qty = temp_df['quantity'] > 0

    clean_df = temp_df[is_valid_price & is_positive_qty].copy()

    stats['bad_price_only'] = int((~is_valid_price & is_positive_qty).sum())
    stats['bad_qty_only'] = int((is_valid_price & ~is_positive_qty).sum())
    stats['both_bad'] = int((~is_valid_price & ~is_positive_qty).sum())

    #-------------------------------------------------------------------------------------------------------------------
    # We only pass columns with correct names to ensure the function does not reject
    # the DataFrame due to columns like 'Order ID' or 'Order Date', which contain spaces.
    # revenue: quantity * unit_price - discount
    calc_df = add_virtual_column(clean_df[['region', 'quantity', 'unit_price', 'discount']],
                              "quantity * unit_price - discount", "revenue")


    # agregation
    revenue_by_region = (
        calc_df.groupby('region', as_index=False)['revenue']
        .sum()
        .rename(columns={'revenue': 'total_revenue'})
        .sort_values(by='total_revenue', ascending=False)
    )

    revenue_by_region['total_revenue'] = revenue_by_region['total_revenue'].round(2)

    revenue_by_region.to_csv('revenue_by_region.csv', index=False)
    print(stats)
    print(f"Procesed {len(clean_df)} out of {len(raw_df)} rows")


if __name__ == '__main__':
    run_pipeline()