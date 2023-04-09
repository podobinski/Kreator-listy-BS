import pandas as pd

def save_to_excel(data, output_file):
    df = pd.DataFrame(data)
    df.to_excel(output_file, index=False, engine="openpyxl")
    print(f"Data saved to {output_file}")
