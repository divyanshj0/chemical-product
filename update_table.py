import sqlite3
import streamlit as st
import pandas as pd
# Connect to DB
conn = sqlite3.connect("products_data.db")
cursor = conn.cursor()


def extract_keyword(product_name):
    return product_name.split()[0].upper()


# Fetch all chemical list products
chemical_df = pd.read_sql_query("SELECT * FROM chemicals_list", conn)

# Product dropdown
selected_product = st.selectbox("Select a product from Chemical List", chemical_df['ProductName'])
keyword=extract_keyword(selected_product)
# Get the HSN code of selected product
selected_row = chemical_df[chemical_df['ProductName'] == selected_product].iloc[0]
selected_hsn = selected_row['hsn']
selected_grade=selected_row['grade']

st.write(f"Selected HSN Code: `{selected_hsn}`")
st.write(f"Selected grade: `{selected_grade}`")
selected_hsn_str = int(selected_hsn)

# Fetch from chemicals_list
cursor.execute("SELECT * FROM chemicals_list WHERE ProductName LIKE ? AND grade = ? AND hsn = ? ", (f"%{keyword}%",f"{selected_grade}",selected_hsn_str,))
chem_rows = cursor.fetchall()
chem_matches = pd.DataFrame(chem_rows, columns=[col[0] for col in cursor.description])

# Fetch from loba
cursor.execute("SELECT * FROM loba WHERE ProductName LIKE ? AND grade = ? AND hsn = ? ", (f"%{keyword}%",f"{selected_grade}",selected_hsn_str,))
loba_rows = cursor.fetchall()
loba_matches = pd.DataFrame(loba_rows, columns=[col[0] for col in cursor.description])

st.subheader("Chemical List Products with same HSN")
st.dataframe(chem_matches)

st.subheader("Loba Products with same HSN")
st.dataframe(loba_matches)
if st.button("Update to Final Table (updated_list)"):
    chem_matches['source'] = 'chemicals_list'
    loba_matches['source'] = 'loba'
    combined = pd.concat([chem_matches, loba_matches], ignore_index=True)
    combined = combined[~combined['pkg'].isin(['POR'])]
    combined = combined.dropna(subset=['pkg'])

    # Custom row selection logic
    def select_row(group):
        if len(group) == 1:
            row = group.iloc[0].copy()
            row['old_price'] = float(row['price']) if pd.notnull(row['price']) else None
            row['new_price'] = float(row['price']) if pd.notnull(row['price']) else None
            return row
        else:
            chem_row = group[group['source'] == 'chemicals_list'].iloc[0]
            loba_row = group[group['source'] == 'loba'].iloc[0]
            chem_price = float(chem_row['price']) if pd.notnull(chem_row['price']) else float('inf')
            loba_price = float(loba_row['price']) if pd.notnull(loba_row['price']) else float('inf')
            row = chem_row.copy()
            row['old_price'] = chem_price
            row['new_price'] = min(chem_price, loba_price)
            return row

    # Group and apply logic
    result = combined.groupby(['hsn', 'grade', 'pkg'], as_index=False).apply(select_row)
    result = result.reset_index(drop=True)

    # Drop unnecessary columns
    for col in ['id', 'price', 'source']:
        if col in result.columns:
            result = result.drop(columns=[col])

    # Ensure float type for price columns
    for col in ['old_price', 'new_price']:
        if col in result.columns:
            result[col] = result[col].astype(float)

    # Remove already existing rows
    existing = pd.read_sql_query("SELECT ProductName, pkg FROM updated_list", conn)
    merged = pd.merge(result, existing, on=['ProductName', 'pkg'], how='left', indicator=True)
    new_rows = result[merged['_merge'] == 'left_only']

    cursor.execute("SELECT COUNT(*) FROM updated_list")
    before_count = cursor.fetchone()[0]

    # Append new rows
    if not new_rows.empty:
        new_rows.to_sql("updated_list", conn, if_exists="append", index=False)
    cursor.execute("SELECT COUNT(*) FROM updated_list")
    after_count = cursor.fetchone()[0]
    added_count = after_count - before_count
    st.write(f"Number of products updated: {added_count}")

if st.checkbox("Show Updated List Table"):
    updated_list = pd.read_sql_query("SELECT * FROM updated_list", conn)
    st.dataframe(updated_list)
