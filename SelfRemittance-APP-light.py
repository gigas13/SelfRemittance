import pandas as pd
import numpy as np
import streamlit as st
import itertools

st.set_page_config(page_title="Self Remittance", page_icon=":sun_with_face:",
                   layout="wide")

uploaded_file = None
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is None:
    df = pd.DataFrame({"Invoice":['x','y','z'],"Value":[1,2,3]})
else:
    df = pd.read_csv(uploaded_file)
df.drop_duplicates(inplace=True)


#--- MAINPAGE ---
st.title(":sun_with_face: Self Remittance")

xl, left_column, right_column, xr = st.columns(4)
with left_column:
    target_string = st.text_input("Enter Payment: (number)")
    if target_string == "" : target_string=0
with right_column:
    error_string = st.text_input("Enter tolerance allowed: (number)")
    if error_string == "" : error_string=0

### in the prompt: streamlit run app.py

target = float(target_string)
error = float(error_string)

a,b,c,d, = st.columns(4)
with b:
    st.text("Search Range: {} - {}".format(target-error, target+error))
st.markdown("---")

### identify the possible combinations (mathematically) and return the first combination found
def get_subset(numbers, taget=target, error=error):
    numbers = [number for number in numbers if number<=(target+error)]
    check=0
    outcome = ()
    for L in range(1,len(numbers)+1):    
        if check == 0:
            for subset in itertools.combinations(numbers, L):
                if (target-error) <= sum(subset) <= (target+error):
                    outcome = list(subset)
                    check=1
                    break
        else:
            break
    return outcome


### Generate the filtered dataframe
def df_generator(lst):
    df_construct = pd.DataFrame(columns=["Invoice", "Value"])
    for i, row in df.iterrows():
        for j, value in enumerate(lst):
            if row.Value == value:
                df_construct = pd.concat([df_construct,pd.DataFrame(row).T])
                del lst[j]
                break
    return df_construct


###Add totals to a DataFrame
def add_total(df):
    df_blank = pd.DataFrame(['Total', np.nan], index=['Invoice','Value']).T
    df_final = pd.concat([df, df_blank])
    df_final.iloc[-1,-1] = df.Value.sum()
    return df_final


###Convert df to .csv
def convert_df(df):
   return df.to_csv(index=True).encode('utf-8')


left_column, mid_column, right_column = st.columns(3)
with left_column:
    st.subheader("Invoices loaded: {}".format(df.shape[0]))
    st.dataframe(add_total(df).set_index('Invoice'))
with mid_column:
    st.subheader("Exact match:")
    df1 = add_total(df_generator(get_subset(df.Value.to_list(), error=0))).set_index('Invoice')
    st.download_button("To_csv", convert_df(df1), "file.csv", "text/csv", key='a')
    st.dataframe(df1)
    st.markdown("---")
with right_column:
    st.subheader("Loose match:")
    if df1.Value.sum() == 0:
        df2 = add_total(df_generator(get_subset(df.Value.to_list(), error=error))).set_index('Invoice')
        st.download_button("To_csv", convert_df(df2), "file.csv", "text/csv", key='b')
        st.dataframe(df2)
        st.markdown("---")        

        
