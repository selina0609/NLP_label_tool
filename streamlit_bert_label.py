import streamlit as st
import json
import os
import pandas as pd
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode , JsCode
st.header('NLP label tools')
label_style = st.sidebar.selectbox('What semantic annotation do you need to process?' , ('binary_level','level_self_defined','context_prompt'))
label_json = {}
st.sidebar.write("""***""")
if label_style == 'binary_level':
    assign_label   = st.sidebar.selectbox('🏷️ assign the context label',['0','1'])
if label_style == 'level_self_defined':
    label_num = st.sidebar.number_input('setting total number of labels:',min_value = 0 , max_value=99 , step=1 )
    assign_label = st.sidebar.selectbox('choose your level number: ', range(2 if label_style == 'binary_level' else label_num if label_style == 'level_self_defined' else 2))
if label_style == 'level_self_defined' or label_style == 'binary_level':
    label_descript = st.sidebar.text_area('write the context description')
    if os.path.exists(label_style+"_label.json") == False:
        with open(label_style+"_label.json", "w",encoding='utf-8') as outfile:
            json.dump({'label_style': label_style}, outfile)
    submitted = st.sidebar.button("📥 upload_label_description")
    if submitted:
        st.write(f"label:{assign_label}:{label_descript}")
        with open(label_style+"_label.json", "r",encoding='utf-8') as file:
            label_json = json.load(file)
            label_json[assign_label] = label_descript
        with open(label_style+"_label.json", "w",encoding='utf-8') as outfile:
            json.dump(label_json, outfile)
    with open(label_style + "_label.json", "r", encoding='utf-8') as file:
        label_json = json.load(file)
    st.sidebar.json(label_json)

    st.sidebar.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>',
             unsafe_allow_html=True)
    st.sidebar.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>',
             unsafe_allow_html=True)
    cancel = st.sidebar.radio('are you sure to cancel all label file?[Y/N]:', ('No' , 'Yes'))

    if st.sidebar.button('🧹 reset_json_kernel') and cancel == 'Yes':

        os.remove(label_style+"_label.json")


    #=====================================================
    st.write("assign the context label")
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>',
            unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>',
            unsafe_allow_html=True)

    slider_val = st.radio("🏷️ Label:",range(2 if label_style == 'binary_level' else label_num if  label_style == 'level_self_defined' else 0))
    try:
        with open(label_style+"_label.json", "r",encoding='utf-8') as file:
            label_json = json.load(file)

        show_discription = label_json[str(slider_val)]
    except:
        show_discription = 'Please write the description in the left sidebar'
    with st.form("myform",clear_on_submit=True):
        st.write('discription:',show_discription)
        nlp_context = st.text_area('🗣️ write NLP label context on below✍🏻️:').replace('\n','')
        # Every form must have a submit button.
        # submitted = st.button("💌 Submit",on_click=clear_form)
        submitted = st.form_submit_button("💌 Submit")
        if submitted:
            st.write("previous saved:\n", f'label:{slider_val} , context:{nlp_context}')
            with open(label_style+"NLP_dataset.csv", "a+",encoding='utf-8') as csv_file:
                csv_file.write(str(slider_val)+','+nlp_context+'\n')
    st.write("""***""")

    if os.path.exists(label_style + "NLP_dataset.csv"):
        with open(label_style + "NLP_dataset.csv", "r",encoding= 'utf-8') as csv_file:
            lines = csv_file.readlines()[-3:]
        df = pd.DataFrame(columns = ['label','context'])
        for line in lines:
            df1 = pd.DataFrame([[line[0] , line[2:]]],columns=['label', 'context'])
            df = df.append(df1)
        # st.dataframe(df)
        AgGrid(df)
    st.write("""***""")

    cancel_csv = st.radio('are you sure to cancel all csv file?[Y/N]:', ('No', 'Yes'))
    if st.button('🧹 reset_csv_kernel') and cancel_csv == 'Yes':
        try:
            os.remove(label_style + "NLP_dataset.csv")
        except:
            st.write('The CSV file has already been cancelled.')


if label_style == 'context_prompt':
    label_num = st.sidebar.number_input('setting total number of action:',min_value = 0 , max_value=99 , step=1)
    label_descript = st.sidebar.text_area('write the context description')
    st.header('😵 Allen is still designing the details of the labeling function, or you can buy him a coffee to console him 🔨🔨')

    pass



#streamlit run streamlit_bert_label.py --server.address 127.0.1.2 --server.port 80