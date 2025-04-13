import streamlit as st
import pandas as pd
import os 
from io import BytesIO

st.set_page_config(page_title= "Data Sweeper" , layout = "wide")

# custom css 
st.markdown(
    """
    <style>
    .stApp{
    background-color: black;
    color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("Muhammad Maaz | DataSweeper + Sterling Integration Solution")
st.write("Making data beautiful: Automated CSV to Excel conversion with smart cleaning & visual insights. Quarter 3 project by Muhammad Maaz.")

# uploading_files 

uploaded_files=st.file_uploader("Upload your file (accepts CVS or Excel.):", type=["cvs","xlsx"],accept_multiple_files=(True))

if uploaded_files:
    for files in uploaded_files:
        file_ext = os.path.splitext(files.name)[-1].lower()

        if file_ext == ".cvs":
            df = pd.read_csv(files)
        elif file_ext == "xlsx":
            df=pd.read_excel(files)
        else :
            st.error(f"Unsupported File Type:{file_ext}")
            continue

        # file details
        st.write("Preview the head of the Dataframe")
        st.dataframe(df.head())

        # data Cleaning options
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"Cleaning Data For {files.name}"):
            col1,col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from this file: {files.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!") 

                    with col2:
                        if st.button(f"Fill missing values {files.name}"):
                            numeric_cols= df.select_dtypes(include=['number']).columns
                            df[numeric_cols]=df[numeric_cols].fillna(df[numeric_cols].mean())
                            st.write("Missing Value Have Been Filled")
                
                st.subheader("Selet Columns to Keep")
                columns = st.multiselect(f"Choose columns for {files.name}",df.columns, default=df.columns)
                df = df[columns]


                # data visualization
                st.subheader("Data Visualizations")
                if st.checkbox(f"Show Data Visualizations {files.name}"):
                    st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])


                #conversion options

                st.subheader("Conversion Options")
                conversion_type = st.radio(f"Conversion {files.name} to:", ["CVS" , "Excel"], key=files.name)
                if st.button(f"Convert{files.name}"):
                    buffer = BytesIO()
                    if conversion_type == "CVS":
                        df.to.cvs(buffer, index=False)
                        files_name = files.name.replace(file_ext,".cvs")
                        mime_type="text/cvs" 

                    elif conversion_type == "Excel":
                        df.to.to_excel(buffer ,index=False)
                        file_name = files.name.replace(file_ext, "xlsx") 
                        mime_type = "application/vnd.openxmlformets-officedocument.spreedsheetml.sheet"
                    buffer.seek(0)

                    st.download_button(
                        label=f"Download {files.name} as {conversion_type}",
                        data=buffer,
                        file_name=file_name,
                        mime=mime_type
                    )

st.success("All files processed successfully")











