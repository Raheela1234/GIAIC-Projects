#imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up our app
st.set_page_config(page_title="🎫 Data Sweeper", layout="wide")
st.title("🎫 Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization")

# Upload files
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue  # Skip unsupported files

        # Display info about the file
        st.write(f"*File Name:* {file.name}")
        st.write(f"*File Size:* {file.size / 1024:.2f} KB")

        # Show 5 rows of our DataFrame
        st.write("👀 Preview the Head of the DataFrame")
        st.dataframe(df.head())

        # Options for data cleaning
        st.subheader(f"🛴 Data Cleaning Options for {file.name}")

        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing Values Filled!")

        # Select specific columns
        st.subheader("Select Columns to Keep")
        selected_columns = st.multiselect(f"🧮 Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]

        # Create visualizations
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :21])

        # Convert the file (CSV <-> Excel)
        st.subheader("📀 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                new_file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='xlsxwriter')
                new_file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"📩 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=new_file_name,
                mime=mime_type
            )

            st.success("🎉 All files processed successfully!")