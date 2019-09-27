import pandas as pd
import chardet

file_path ="files\\20190925_175931_a.csv"
def get_enc(file):
    with open(file, "rb") as f:
        res = chardet.detect(f.read())
        enc = res["encoding"]
    return enc

if __name__ == "__main__":
    enc_code = get_enc(file_path)
    df = pd.read_csv(file_path, sep='\t', encoding=enc_code)
    df = df[df["Keyword"].isnull() == False].sort_values("Position History Date")
    print(df.drop_duplicates(subset='Keyword').reset_index(drop=True))