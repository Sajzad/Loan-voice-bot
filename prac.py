import pandas as pd


columns = ["a", "b"]
data =[ 
{
    "a":"2",
    "b":"2"
},
{
    "a":"5",
    "b":"6"
},
]
output_file = "test.csv"
def results(data, columns, output_file):
    if data:
        print("results are storing ......")
        try:
            master_df = pd.read_csv(output_file)
        except:
            df = pd.DataFrame(columns = columns)
            df.to_csv(output_file)
            master_df = pd.read_csv(output_file)

        df = pd.DataFrame(columns = columns)
        df = df.append(data, ignore_index = True)
        df = pd.concat([df, master_df])
        df = df.drop_duplicates()
        df = df[columns]
        df.to_csv(output_file, index=False)
        print("Data taken")


def read_excel(filename):
    read_excel = pd.read_csv(filename)
    
results(data, columns, output_file)