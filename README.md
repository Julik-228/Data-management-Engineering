# Data-management-Engineering

This is a repository for the **ITMO Engineering Data Management** project.

## Dataset Links

**Link to datasets**: [Google Drive folder](https://drive.google.com/drive/folders/1QAz7jx7AGHJcXc0OftuolaaU4slls4CO?usp=sharing)  

**Original source of dataset**: [RCSB PDB Macromolecular Structure Dataset on Kaggle](https://www.kaggle.com/datasets/samiraalipour/rcsb-pdb-macromolecular-structure-dataset?utm_source=chatgpt.com&select=RCSB_PDB_Macromolecular_Structure_Dataset.csv)

## Project Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setting up Virtual Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Julik-228/Data-management-Engineering.git
   cd Data-management-Engineering
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   
   **On Windows:**
   ```bash
   venv\Scripts\activate
   ```
   
   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Data Loader Script

To execute the main data loading script:

```bash
python data_loader.py
```

This script will:
- Download data from the Google Drive dataset
- Load the data using pandas
- Display the first 10 rows of the dataset

### Project Structure

```
Data-management-Engineering/
├── data_loader.py          # Main script for loading and displaying data
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## Script Output Example

**Homework №2**: <img width="1150" height="291" alt="image" src="https://github.com/user-attachments/assets/3fc164d9-4047-4271-bb18-cee4129a2038" />

## Dependencies

The project uses the following Python packages:
- `pandas` - Data manipulation and analysis
- `requests` - HTTP library for making requests
- `numpy` - Numerical computing library

All dependencies are listed in `requirements.txt` and will be installed automatically when following the setup instructions above.
