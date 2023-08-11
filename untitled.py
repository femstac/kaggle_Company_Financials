import streamlit as st
import pandas as pd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import textwrap



# Pre-processing:
# 1. Check for column names and Fix Errors
# 2. Remove $ sign and '-' from all columns where they are present
# 3. Change datatype from objects to int after the above two.
# 4. Removing " , " (comma) from all numerical numbers.
# Check File Contents

df = pd.read_csv('Financials.csv')

# Trim All White spaces in object columns in the dataset
# Select columns of object and string data types from the DataFrame 'df'
df_obj = df.select_dtypes(['object', 'string'])

# Apply the strip method to all elements in the selected columns to remove leading and trailing whitespaces
df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

# Remove leading and trailing whitespaces from column names
df.columns = df.columns.str.strip()


# Create variables for Column Names

[ Segment, Country, Product, Discount_Band, Units_Sold,
 Manufacturing_Price, Sale_Price, Gross_Sales, Discounts,
 Sales, COGS, Profit, Date, Month_Number, Month_Name,
 Year
] = ['Segment', 'Country', 'Product', 'Discount Band', 'Units Sold',
 'Manufacturing Price', 'Sale Price', 'Gross Sales', 'Discounts',
 'Sales', 'COGS', 'Profit', 'Date', 'Month Number', 'Month Name', 'Year'] 



# Seperate Columns to Facts (i.e Categorical) and Numerical Columns
Numerical_Columns = [Units_Sold, Manufacturing_Price, Sale_Price, Gross_Sales, Discounts, Sales, COGS, Profit]

Fact_Columns = [Segment, Country, Product, Discount_Band]

Varying_Numerical_Columns =  [Gross_Sales, Discounts, Sales, COGS, Profit]


# Remove all special characters in Numerical Columns
df[Numerical_Columns] = df[Numerical_Columns].replace({'\$':'','-':'0',',':''},regex=True)

# Numbers in () are Negative, therefore Preppend '-' to the values in brackets
df[Numerical_Columns] = df[Numerical_Columns].replace({'\(':'-','\)':'',' ':''},regex=True)
 
# Convert Numerical columns to Float data type and Units Sold to Integer whole number
df[Numerical_Columns] = df[Numerical_Columns].astype(float)
df[Units_Sold] = df[Units_Sold].astype(int)
 
# Convert date to datetime
df[Date] = pd.to_datetime(df[Date])

# Delete Non essential columns
Non_Essential_columns = [Month_Number, Month_Name, Year]
df = df.drop(Non_Essential_columns, axis=1)


# Getting Unique Items in DataFrame

def get_unique_items_list_in_column(column_name):
    """
    Returns a list of unique items in the specified column of a DataFrame 'df'.
    
    Parameters:
    column_name: The name of the column to retrieve unique items from.
    
    Returns:
    full_list: A list of unique items in the specified column. The list is sorted if the column name is not 'Discount_Band' or 'Date'. If the column name is 'Date', the list contains unique years.
    """
  
    # Check if the column name is not 'Discount_Band'
    if column_name != Discount_Band:
        # Get a list of unique items in the specified column and sort it
        full_list = df[column_name].unique().tolist()
        full_list = sorted(full_list)
    
    else:
        # Get a list of unique items in the specified column
        full_list = df[column_name].unique().tolist()
    
    # Check if the column name is 'Date'
    if column_name == Date:
        # Get a list of unique years in the specified column and sort it
        full_list = df[column_name].dt.year.unique().tolist()
        full_list = sorted(full_list)
          
    return full_list



# Pipelines

# # Function to generate bar chart
# def create_bar_chart(x_axis=Segment, y_axis=Sales):
    
#     # Create a copy of the dataframe
#     bar_df = df.copy()
    
#     #if the x-axis is 'Discount Band', set the categories and order
#     if x_axis == Discount_Band:
#         bar_df[x_axis]=pd.Categorical(bar_df[x_axis],
#                                       categories= get_unique_items_list_in_column(Discount_Band), 
#                                      ordered= True)
    
#     # Group the dataframe by the x-axis and sum the numerical columns
#     bar_df = bar_df.groupby(x_axis).sum().reset_index().reset_index(drop=True)
    
#     # Select only the x-axis and y-axis columns
#     bar_df = bar_df[[x_axis, y_axis]]
    
    

#     def get_differentiating_color(value):
    
#         if value== bar_df[y_axis].max():
#             return 'royalblue'
#         elif value== bar_df[y_axis].min():
#             return 'red'
#         else:
#             return 'gray'

#     colors = [get_differentiating_color(value) for value in bar_df[y_axis]]
    
#     # Create a bar chart using Matplotlib
#     fig, ax = plt.subplots()
#     ax.bar(bar_df[x_axis], bar_df[y_axis], color= colors,)
#     ax.set_xlabel(x_axis)
#     ax.set_ylabel(y_axis)
    
#     # Set the y-axis ticks to display as real numbers instead of scientific notation
#     ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))
    
#     # Reduce the font size of the x-axis tick labels
#     # ax.set_xticklabels(ax.get_xticklabels(), fontsize=8)
    
#     # Wrap the x-axis tick labels
#     tick_labels = [textwrap.fill(label, 10) for label in bar_df[x_axis]]
#     ax.set_xticks(range(len(bar_df[x_axis])))
#     ax.set_xticklabels(tick_labels, fontsize=9)
    
#     for label in ax.get_xticklabels():
#         label.set_fontweight('bold')
    
#     st.pyplot(fig)





# # Use columns to display widgets side by side 
# first_chart_y_widget,first_chart_x_widget = st.columns(2)  
    
# # Create widgets to select the x-axis and y-axis columns
# bar_x_axis = first_chart_x_widget.selectbox('Select x-axis column', Fact_Columns)
# bar_y_axis = first_chart_y_widget.selectbox('Select y-axis column', Numerical_Columns)

# #Title of the first chart
# st.markdown(f'# Total {bar_y_axis} per {bar_x_axis}')


# # Call the create_bar_chart function with the selected columns
# create_bar_chart(bar_x_axis, bar_y_axis)

 

#======================================================


# Function to generate bar chart
def create_bar_table(x_axis=Segment, y_axis=Sales):
    
    # Create a copy of the dataframe
    bar_df = df.copy()
    
    #if the x-axis is 'Discount Band', set the categories and order
    if x_axis == Discount_Band:
        bar_df[x_axis]=pd.Categorical(bar_df[x_axis],
                                      categories= get_unique_items_list_in_column(Discount_Band), 
                                     ordered= True)
    
    # Group the dataframe by the x-axis and sum the numerical columns
    bar_df = bar_df.groupby(x_axis).sum().reset_index().reset_index(drop=True)
    
    # Select only the x-axis and y-axis columns
    bar_df = bar_df[[x_axis, y_axis]]
    
    return bar_df
 
    



def get_differentiating_color(bar_df, y_axis, value):
    if value== bar_df[y_axis].max():
        return 'royalblue'
    elif value== bar_df[y_axis].min():
        return 'red'
    else:
        return 'gray'

   
    
def plot_bar_chart(bar_df, bar_x_axis, bar_y_axis ):#,colors):
    # Create a bar chart using Matplotlib
    fig, ax = plt.subplots()
    ax.bar(bar_df[bar_x_axis], bar_df[bar_y_axis], )#color= colors,)
    ax.set_xlabel(bar_x_axis)
    ax.set_ylabel(bar_y_axis)
    
    # Set the y-axis ticks to display as real numbers instead of scientific notation
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))
    
    # Reduce the font size of the x-axis tick labels
    # ax.set_xticklabels(ax.get_xticklabels(), fontsize=8)
    
    # Wrap the x-axis tick labels
    tick_labels = [textwrap.fill(label, 10) for label in bar_df[bar_x_axis]]
    ax.set_xticks(range(len(bar_df[bar_x_axis])))
    ax.set_xticklabels(tick_labels, fontsize=9)
    
    for label in ax.get_xticklabels():
        label.set_fontweight('bold')
    
    st.pyplot(fig)

def get_report_on_min_max_bar_values(bar_df,bar_x_axis, bar_y_axis):
    
    max_value = bar_df[bar_y_axis].max()
    
    max_category = bar_df.loc[bar_df[bar_y_axis] == max_value, bar_x_axis].iloc[0]
    
    min_value = bar_df[bar_y_axis].min()
    
    min_category = bar_df.loc[bar_df[bar_y_axis] == min_value, bar_x_axis].iloc[0]
    
    report = (f'The **{bar_x_axis}** **\"{max_category}\"** has the highest Total **{bar_y_axis}** value of **\${max_value}**. The lowest is **\"{min_category}\"** with a value of **\${min_value}**.')
    
    return report



# Use columns to display widgets side by side 
first_chart_y_widget,first_chart_x_widget = st.columns(2)  
    
# Create widgets to select the x-axis and y-axis columns
bar_x_axis = first_chart_x_widget.selectbox('Select x-axis column', Fact_Columns)
bar_y_axis = first_chart_y_widget.selectbox('Select y-axis column', Numerical_Columns)

    
bar_df=create_bar_table(bar_x_axis, bar_y_axis)

colors = [get_differentiating_color(bar_df, bar_y_axis, value) for value in bar_df[ bar_y_axis]]
    

#Title of the first chart
st.markdown(f'# Total {bar_y_axis} per {bar_x_axis}')


st.markdown(get_report_on_min_max_bar_values(bar_df,bar_x_axis, bar_y_axis))

# Call the create_bar_chart function with the selected columns
plot_bar_chart(bar_df, bar_x_axis, bar_y_axis )#, colors)


    








# # Create a multiselect widget for column selection
# selected_columns = st.multiselect('Select columns', df.columns)

# # Display the selected columns of the DataFrame
# st.write(df[selected_columns])

