import pandas as pd
import requests
from io import StringIO

FILE_ID = "13zgzC8uRvxcaHqphsqfw7BCHUILOSeXO"
file_url = f"https://drive.google.com/uc?export=download&id={FILE_ID}"

response = requests.get(file_url)
raw_data = pd.read_csv(StringIO(response.text))
print(raw_data.head(10))