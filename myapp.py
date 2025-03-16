import pandas as pd
import plotly.express as px
import streamlit as st
    


st.set_page_config(
    page_title='Sidd Anaiytic',
    page_icon='📊',
)
st.title("Data :red[Analytic] :blue[Portal]",)
st.subheader(":green[Explore Data With Ease]",divider="blue")


file=st.file_uploader('drop csv or excel file',type=['xlsx','csv'])
if(file!=None):
    if(file.name.endswith("csv")):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)    

    st.dataframe(data)
    st.info("Successfully Uploaded..!!",icon="✔️")      

    st.subheader(":green[Basic Information Of DataSet]",divider='rainbow')
    tab1,tab2,tab3,tab4 = st.tabs(['Summary','Top Botom Row','DataType','Columns'])

    with tab1:
        st.write(f'There Are {data.shape[0]} row in data set and {data.shape[1]} columns in data set')
        st.subheader(':gray[Summary of data set]')
        st.dataframe(data.describe())

    with tab2:
        st.subheader(':gray[Top Rows]')
        toprows = st.slider('numbers of row you want',1,data.shape[0],key='top')
        st.dataframe(data.head(toprows))

        st.subheader(':gray[Bottom Rows]')
        bottomrows = st.slider('numbers of row you want',1,data.shape[0],key='bottom')
        st.dataframe(data.tail(bottomrows))


    with tab3:
        st.subheader(':grey[Data Type Of Columns]')
        st.dataframe(data.dtypes)

    with tab4: 
        st.subheader(':grey[Column name in dataset]')
        st.write(list(data.columns))


    st.subheader(':green[Column values to count]',divider='green')
    with st.expander('Value Count'):
        col1,col2 = st.columns(2)
        with col1:
            column = st.selectbox('Choose Columns name',options=list(data.columns))
        with col2:
            toprows = st.number_input('Top rows',min_value=1,step=1)    

        count = st.button('count')
        if(count==True):
            result = data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)
            st.subheader('Visualization',divider='grey')
            fig = px.bar(data_frame=result,x=column,y='count',text='count',template='plotly_dark')
            st.plotly_chart(fig)
            fig = px.line(data_frame=result,x=column,y='count',text='count',template='plotly_dark')
            st.plotly_chart(fig)
            fig = px.pie(data_frame=result,names=column,values='count')
            st.plotly_chart(fig)
            # fig = px.sunburst(data_frame=result,names=column,values='count')
            # st.plotly_chart(fig)

    st.subheader(':green[Group : Simplify Your Data Analysis]',divider='grey')        
    st.write('The group by is a summarize data by specific categories and group:- ')
    with st.expander('Group By Your Columns'):
        col1,col2,col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect('Choose Your Columns To Group By..!',options = list(data.columns))
        with col2:
            operation_col = st.selectbox('Choose Your Columns For Oprations',options=list(data.columns))    
        with col3:
            operation = st.selectbox('Choose Operation',options=['sum','min','max','mediam','count','mean'])

        if(groupby_cols):
            result = data.groupby(groupby_cols).agg(
                newcol = (operation_col,operation)
            ).reset_index()

            st.dataframe(result)
            
            st.subheader(':green[Data Visualization]',divider='grey')
            graphs = st.selectbox('Choose your graphs', options=['line','bar','scatter','pie','sunburst'])
            if (graphs=='line'):
                x_A=st.selectbox('chose X axis',options=list(result.columns))
                y_A=st.selectbox('chose Y axis',options=list(result.columns))
                color = st.selectbox('color information',options=[None]+list(result.columns))    
                fig=px.line(data_frame=result,x=x_A,y=y_A,color=color)
                st.plotly_chart(fig)
            elif(graphs=='bar'):
                x_A=st.selectbox('chose X axis',options=list(result.columns))
                y_A=st.selectbox('chose Y axis',options=list(result.columns))
                color = st.selectbox('color information',options=[None]+list(result.columns))
                facet_col = st.selectbox('Columns Informations',options=[None]+list(result.columns))
                fig = px.bar(data_frame=result,x=x_A,y=y_A,color=color,facet_col=facet_col,barmode='group')
                st.plotly_chart(fig)
            elif(graphs=='scatter'):
                x_A=st.selectbox('chose X axis',options=list(result.columns))
                y_A=st.selectbox('chose Y axis',options=list(result.columns))
                color = st.selectbox('color information',options=[None]+list(result.columns))
                size = st.selectbox('Size column',options=[None]+list(result.columns))
                fig = px.scatter(data_frame=result,x=x_A,y=y_A,color=color,size=size)
                st.plotly_chart(fig)
            elif(graphs=='pie'):
                values = st.selectbox('Choose numerical values', options=list(result.columns))
                Names = st.selectbox('Chose labels',options=list(result.columns))
                fig = px.pie(data_frame=result,values=values,names=Names)
                st.plotly_chart(fig)
            elif(graphs=='sunburst'):
                path = st.multiselect('Choose your path',options=list(result.columns))    
                fig = px.sunburst(data_frame=result,path=path,values='newcol')
                st.plotly_chart(fig)