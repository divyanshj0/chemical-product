# Chemical Product Data Consolidation Platform  

An interactive **Streamlit + SQLite** platform for managing and consolidating chemical product catalogs.  
The app allows users to select products, cross-check across multiple datasets, clean inconsistencies, and update a unified product table for further use.  

---

## 🚀 Features  
- **Product Selection** – pick a chemical product from the database.  
- **Metadata Extraction** – automatically fetches HSN codes and grades.  
- **Cross-Database Matching** – compares products across `chemicals_list` and `loba`.  
- **Data Cleaning & Merging** –  
  - Combines multiple datasets.  
  - Removes duplicates and invalid entries (e.g., `POR` packages).  
  - Updates a consolidated table `updated_list`.  
- **Interactive Dashboard** – Streamlit interface for browsing, comparing, and updating records in real time.  

---

## 🛠 Tech Stack  
- **Frontend:** Streamlit  
- **Backend:** Python (Pandas, SQLite3)  
- **Database:** SQLite (`products_data.db`)  

---

## ⚙️ Setup Instructions  

### 1. Clone the repository  
```bash
git clone https://github.com/your-username/chemical-data-consolidation.git
cd chemical-data-consolidation
```

### 2. Create and activate a virtual environment (recommended)  
```bash
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Mac/Linux
```

### 3. Install dependencies  
```bash
python -m pip install -r requirements.txt
```

### 4. Run the Streamlit app  
```bash
streamlit run update_table.py
```

---

## 📂 Project Structure  
```
update_table.py      # Main Streamlit app
products_data.db     # SQLite database (preloaded tables: chemicals_list, loba, updated_list)
requirements.txt     # Python dependencies
README.md            # Project documentation
```

---

## 📊 How It Works  
1. Choose a product from the dropdown list (`chemicals_list`).  
2. The app fetches its HSN code and grade.  
3. Matching products from both `chemicals_list` and `loba` are displayed.  
4. Click **Update to Final Table** → cleans + merges data → saves to `updated_list`.  

---

## ✅ Example Use Case  
- A company with multiple supplier catalogs can quickly identify duplicates, standardize product metadata, and maintain a clean **single source of truth** for chemical product data.  
