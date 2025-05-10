import os
import streamlit as st
import pandas as pd
from basic.savePlot import savePlot
from basic.choose_folder import choose_folder
from toleranceInterval import two_sided_toleranceInterval
from toleranceInterval import one_sided_toleranceInterval

if "progress" not in st.session_state:
    st.session_state.progress = 0

if "result_folder" not in st.session_state:
    st.session_state.result_folder = ''

if "clicked" not in st.session_state:
    st.session_state.clicked = False

if "data" not in st.session_state:
    st.session_state.data = None

if "limits" not in st.session_state:
    st.session_state.limits = True

if "alpha" not in st.session_state:
    st.session_state.alpha = 0.05

if "proportion" not in st.session_state:
    st.session_state.proportion = 0.95

if "analyze" not in st.session_state:
    st.session_state.analyze = False

if "sided" not in st.session_state:
    st.session_state.sided = "Two Sided"

if "up_low" not in st.session_state:
    st.session_state.up_low = "Upper Limit"

def update_progress(progress):
    st.session_state.progress = progress
    # st.write(f"PROGRESS UPDATE: {st.session_state.progress}")

def update_folder(result_folder):
    if result_folder !='':
        st.session_state.result_folder = result_folder
    else:
        st.warning("A folder must be selected")

def update_clicked():
    st.session_state.clicked = True

def update_data(data)->pd.DataFrame:
    if data.name.endswith(".csv"):
        df = pd.read_csv(data)
        update_progress(2)
    elif data.name.endswith(".xlsx"):
        df = pd.read_excel(data)
        update_progress(2)
    else:
        st.error("File type not valid. Upload .csv or .xlsx files only.")
        df = pd.DataFrame()
    return df

def update_limits(limits):
    if limits == "Yes":
        st.session_state.limits = True
        st.write(f"Witin function {st.session_state.limits}")
    else:
        st.session_state.limits = False
        st.write(f"in da func {st.session_state.limits}")

def update_analyze():
    st.session_state.analyze = True

def reset_analyze():
    st.session_state.analyze=False

st.title("Tolerance Interval Constructor")

clicked = st.button("Select a folder to store results")
if clicked:
    result_folder = choose_folder()
    update_folder(result_folder)
    update_clicked()

if st.session_state.result_folder != '':
    st.success(f"Folder selected: {st.session_state.result_folder}")
    update_progress(1)
else:
    st.warning("Please select a folder")

if st.session_state.progress > 0:

    data = st.file_uploader("Upload a .csv or .xlsx file containing your data")

    if data is not None:
        df = update_data(data)
        st.dataframe(df)

if st.session_state.progress > 1:
    st.write("Enter parameters of the tolerance interval")
    limits = st.selectbox("Are there specification limits?",[True,False],key='limits')
    st.write(f"limits session state {st.session_state.limits}")

    alpha = st.slider(
        "Alpha (α)",
        min_value=0.01,
        max_value=0.10,
        step= 0.01,
        value = 0.05,
        on_change=reset_analyze, # to cancel the analysis if you make a change. Note, the function is not called for on_change
        key='alpha')
    
    proportion = st.slider(
        "Proportion (p)",
        min_value=0.01,
        max_value=0.99,
        step = 0.01,
        value = 0.95,
        on_change=reset_analyze,
        key = 'proportion')
    
    side = st.selectbox("One Sided or Two Sided",["Two Sided","One Sided - Upper Limit","One Sided - Lower Limit"],key='sided')
    
    if st.session_state.limits:
        if st.session_state.sided == "Two Sided":
            lower_limit = st.number_input(
                "Lower Limit: ",
                on_change=reset_analyze)
            
            upper_limit = st.number_input(
                "Upper Limit: ",
                on_change=reset_analyze)
        elif st.session_state.sided == "One Sided - Upper Limit":
            upper_limit = st.number_input(
                "Upper Limit: ",
                on_change=reset_analyze)
            lower_limit = upper_limit
        elif st.session_state.sided == "One Sided - Lower Limit":
            lower_limit = st.number_input(
                "Lower Limit: ",
                on_change=reset_analyze)
            upper_limit = lower_limit
    else:
        lower_limit = None
        upper_limit = None
    
    analyze = st.button("Construct tolerance interval",on_click=update_analyze)

    if st.session_state.analyze:
        update_progress(3)
        if st.session_state.progress > 2 and st.session_state.sided == "Two Sided":
            result = two_sided_toleranceInterval(
                data = df,
                xlab=df.columns[0],
                plot_title=data.name.rsplit(".",1)[0],
                p=proportion,
                alpha=alpha,
                upper_lim=upper_limit,
                lower_lim=lower_limit
            )
        
            st.pyplot(result[0])
            st.dataframe(result[1])
            st.write(result[2])

            save_results = st.button("Save Results")
            if save_results:
                savePlot(os.path.join(st.session_state.result_folder,f"{data.name.rsplit('.',1)[0]} {st.session_state.sided} Tolerance Interval_alpha {alpha}_proportion {proportion}"))
                result[1].to_csv(os.path.join(st.session_state.result_folder,f"{data.name.rsplit('.',1)[0]} {st.session_state.sided} Tolerance Interval Summary_alpha {alpha}_proportion {proportion}.csv"))

        if st.session_state.progress > 2 and "One Sided" in st.session_state.sided:
            result = one_sided_toleranceInterval(
                data = df,
                xlab=df.columns[0],
                plot_title=data.name.rsplit(".",1)[0],
                p=proportion,
                alpha=alpha,
                up_low=st.session_state.sided,
                limit=upper_limit
            )
        
            st.pyplot(result[0])
            st.dataframe(result[1])
            st.write(result[2])

            save_results = st.button("Save Results")
            if save_results:
                savePlot(os.path.join(st.session_state.result_folder,f"{data.name.rsplit('.',1)[0]} {st.session_state.sided} Tolerance Interval_alpha {alpha}_proportion {proportion}"))
                result[1].to_csv(os.path.join(st.session_state.result_folder,f"{data.name.rsplit('.',1)[0]} {st.session_state.sided} Tolerance Interval Summary_alpha {alpha}_proportion {proportion}.csv"))
