import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import textwrap



# Check File Contents
df = pd.read_csv('Financials.csv')


# Pre-processing:
# 1. Check for column names and Fix Errors
# 2. Remove $ sign and '-' from all columns where they are present
# 3. Change datatype from objects to int after the above two.
# 4. Removing " , " (comma) from all numerical numbers.
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
 Sales, COGS, Profit, Date, Month_Number, Month_Name, Year
] = ['Segment', 'Country', 'Product', 'Discount Band', 'Units Sold',
 'Manufacturing Price', 'Sale Price', 'Gross Sales', 'Discounts',
 'Sales', 'COGS', 'Profit', 'Date', 'Month Number', 'Month Name', 'Year'] 


# Seperate Columns into Facts (i.e Categorical) and Numerical Columns
Numerical_Columns = [Units_Sold, Manufacturing_Price, Sale_Price, Gross_Sales, Discounts, Sales, COGS, Profit]

Fact_Columns = [Segment, Country, Product, Discount_Band]

Varying_Numerical_Columns =  [Gross_Sales, Discounts, Sales, COGS, Profit]

#This is basically repeated in the Date Column
Non_Essential_columns = [Month_Number, Month_Name, Year]


# Remove all special characters in Numerical Columns
df[Numerical_Columns] = df[Numerical_Columns].replace({'\$':'','-':'0',',':''},regex=True)

# Numbers in () are Negative, therefore Preppend '-' to the values in brackets
df[Numerical_Columns] = df[Numerical_Columns].replace({'\(':'-','\)':'',' ':''},regex=True)
 
# Convert Numerical columns to Float data type and Units Sold column to Integer whole numbers
df[Numerical_Columns] = df[Numerical_Columns].astype(float)
df[Units_Sold] = df[Units_Sold].astype(int)
 
# Convert date column to datetime
df[Date] = pd.to_datetime(df[Date])

# Delete Non essential columns
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

#======================================================================================================
# Function to generate bar chart
def create_bar_table(x_axis, y_axis):
    """
    Generates a table for a bar chart.
    
    Parameters:
    x_axis: The column name to use as the x-axis.
    y_axis: The column name to use as the y-axis.
    
    Returns:
    bar_df: A dataframe containing the data for the bar chart.
    """
    
    # Create a copy of the dataframe
    bar_df = df.copy()
    
    # Check if the x-axis is 'Discount Band'
    if x_axis == Discount_Band:
        # Set the categories and order for the 'Discount Band' column
        bar_df[x_axis] = pd.Categorical(bar_df[x_axis],
                                        categories=get_unique_items_list_in_column(Discount_Band),
                                        ordered=True)
    
    # Group the dataframe by the x-axis and sum the numerical columns
    bar_df = bar_df.groupby(x_axis).sum().reset_index().reset_index(drop=True)
    
    # Select only the x-axis and y-axis columns
    bar_df = bar_df[[x_axis, y_axis]]
    
    return bar_df

 
#======================================================================================================    


def get_differentiating_color(bar_df, y_axis, value):
    """
    Returns a color based on the value of a bar in a bar chart.
    
    Parameters:
    bar_df: The dataframe containing the data for the bar chart.
    y_axis: The column name to use as the y-axis.
    value: The value of the bar to get the color for.
    
    Returns:
    color: A string representing the color of the bar. 'royalblue' if the value is the maximum value in the y-axis column, 'red' if it is the minimum value, and 'gray' otherwise.
    """
    
    # Check if the value is the maximum or minimum value in the y-axis column
    if value == bar_df[y_axis].max():
        return 'royalblue'
    elif value == bar_df[y_axis].min():
        return 'red'
    else:
        return 'gray'
#======================================================================================================   
    
def plot_bar_chart(bar_df, bar_x_axis, bar_y_axis, colors):
    """
    Plots a bar chart using Matplotlib.
    
    Parameters:
    bar_df: The dataframe containing the data for the bar chart.
    bar_x_axis: The column name to use as the x-axis.
    bar_y_axis: The column name to use as the y-axis.
    colors: A list of colors to use for each bar in the chart.
    
    Returns:
    None
    """
    # Create a bar chart using Matplotlib
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(bar_df[bar_x_axis], bar_df[bar_y_axis],  color= colors,)
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
    
    bar_chart.pyplot(fig)

#======================================================================================================   
    
def get_report_on_min_max_bar_values(bar_df, bar_x_axis, bar_y_axis):
    """
    Generates a report on the minimum and maximum values in a bar chart.
    
    Parameters:
    bar_df: The dataframe containing the data for the bar chart.
    bar_x_axis: The column name to use as the x-axis.
    bar_y_axis: The column name to use as the y-axis.
    
    Returns:
    report: A string containing a report on the minimum and maximum values in the y-axis column of the dataframe.
    """
    
    # Get the maximum value in the y-axis column
    max_value = bar_df[bar_y_axis].max()
    
    # Format the maximum value as a string with thousands separators
    formatted_max_value = format(max_value, ',')
    
    # Get the category associated with the maximum value
    max_category = bar_df.loc[bar_df[bar_y_axis] == max_value, bar_x_axis].iloc[0]
    
    # Get the minimum value in the y-axis column
    min_value = bar_df[bar_y_axis].min()
    
    # Format the minimum value as a string with thousands separators
    formatted_min_value = format(min_value, ',')
    
    # Get the category associated with the minimum value
    min_category = bar_df.loc[bar_df[bar_y_axis] == min_value, bar_x_axis].iloc[0]
    
    # Check if the y-axis is 'Units Sold'
    if bar_y_axis == Units_Sold:
        # Generate a report for 'Units Sold'
        report = f'#### The {bar_x_axis}  **\"{max_category}\"** has the highest Total {bar_y_axis} value of :green[**{formatted_max_value}**] units. The lowest is **\"{min_category}\"** with a value of :red[**{formatted_min_value}**] units.'
    
    else:
        # Generate a report for other y-axis values
        report = f'#### The {bar_x_axis} **\"{max_category}\"** has the highest Total {bar_y_axis} value of :green[**\${formatted_max_value}**]. The lowest is **\"{min_category}\"** with a value of :red[**\${formatted_min_value}**]'
        
    # Check if the maximum and minimum values are equal
    if max_value == min_value:
        # Generate a report for equal values
        report = f'#### The Total {bar_y_axis} is the same across all The {bar_x_axis} with a value of :green[**\${formatted_min_value}**].'
        
    return report




#=====================================================================

def create_stacked_bar_chart(x_axis, y_axis, product_List):
    """
    Generates a stacked bar chart using Pandas.
    
    Parameters:
    x_axis: The column name to use as the x-axis.
    y_axis: The column name to use as the y-axis.
    product_List: A list of products to include in the chart.
    
    Returns:
    None
    """
    
    # Define a list of complimentary colors for the stacked bar chart
    complimentary_colors = ["#ba2649", "#ffa7ca", "#1a6b54", "#f7d560", "#5c3c92", "#f2a0a1"]
    
    # Check if the x-axis is not 'Product'
    if x_axis != Product:
        # Create a copy of the dataframe
        products_df = df.copy()

        # Group the dataframe by x-axis and product and sum the y-axis values
        products_df = products_df.groupby([x_axis, Product])[y_axis].sum().reset_index()

        # Filter the data to include only products in product_List
        products_df = products_df[products_df[Product].isin(product_List)]

        # Pivot the data to create a stacked bar chart
        products_df_pivot = products_df.pivot(index=x_axis, columns=Product, values=y_axis).fillna(0)

        # Create a stacked bar chart using Pandas
        chart = products_df_pivot.plot(kind='bar', stacked=True, color=complimentary_colors, figsize=(8, 5))
        
        # Set the y-axis ticks to display as real numbers instead of scientific notation
        chart.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))
        
            # Wrap the x-axis tick labels
        tick_labels = [textwrap.fill(label, 10) for label in products_df_pivot.index]

        # Set the x-axis ticks and tick labels
        chart.set_xticks(range(len(products_df_pivot.index)))
        chart.set_xticklabels(tick_labels, fontsize=9)

#         # Wrap the x-axis tick labels
#         tick_labels = [textwrap.fill(label, 10) for label in bar_df[bar_x_axis]]
        
#         # Set the x-axis ticks and tick labels
#         chart.set_xticks(range(len(bar_df[bar_x_axis])))
#         chart.set_xticklabels(tick_labels, fontsize=9)
        
        # Set the font weight of the x-axis tick labels to bold
        for label in chart.get_xticklabels():
            label.set_fontweight('bold')
        
        # Set the rotation of the x-axis tick labels to 0 degrees
        chart.set_xticklabels(chart.get_xticklabels(), rotation=0)

        # Display the chart in Streamlit
        stacked_chart.pyplot(chart.figure)
        
    else:
        # Display a message if the x-axis is 'Product'
        stacked_chart.write(f'Product infograph for {y_axis} already available. Please select another section in the For Each drop down menu')

#====================================================================


def create_bump_chart(y_axis, categorical_label, year_considered, categorical_label_list):
    """
    Creates a bump chart using matplotlib.
    
    Parameters:
    y_axis: The column name to use as the y-axis.
    categorical_label: The column name to use as the categorical label.
    year_considered: A list of years to include in the chart.
    categorical_label_list: A list of categorical labels to include in the chart.
    
    Returns:
    None
    """
     
    # Convert the year_considered list to a string
    get_year_as_String(year_considered)

    # Check if year_considered and categorical_label_list are not empty
    if year_considered != [] and categorical_label_list != []:
        # Create a copy of the dataframe
        bump_df = df 

        # Set the index to the 'Date' column
        bump_df = bump_df.set_index(Date)

        # Sort the dataframe by date
        bump_df = bump_df.sort_values(by=Date)

        # Group the dataframe by date and categorical label and sum the y-axis values
        bump_df = bump_df.groupby([Date, categorical_label])[y_axis].sum().reset_index().reset_index(drop=True)

        # Filter the data to include only items in categorical_label_list
        bump_df_filtered = bump_df[bump_df[categorical_label].isin(categorical_label_list)]

        # Filter the data to include only years in year_considered
        bump_df_filtered = bump_df_filtered[bump_df_filtered[Date].dt.year.isin(year_considered)].reset_index(drop=True)

        # Pivot the data to create a bump chart
        bump_df_pivot = bump_df_filtered.pivot(index=Date, 
                                               columns=categorical_label,
                                               values=y_axis).fillna(0)
        
        # Format the dates to only include the month and day
        bump_df_pivot.index = bump_df_pivot.index.strftime('%d-%m %Y')

        
        # Create a line chart using matplotlib
        fig, ax = plt.subplots(figsize=(6
                                        ,3))
        for column in bump_df_pivot.columns:
            ax.plot(bump_df_pivot.index, bump_df_pivot[column], label=column)
            ax.scatter(bump_df_pivot.index, bump_df_pivot[column])
        
        # Wrap the x-axis tick labels
        tick_labels = [textwrap.fill(label, 5) for label in bump_df_pivot.index]
        ax.set_xticks(bump_df_pivot.index)
        ax.set_xticklabels(tick_labels, fontsize=7)
        ax.set_xticklabels(ax.get_xticklabels(),fontsize=9, rotation=0)
        
        
        fig.legend(ncol=1, loc='right', bbox_to_anchor=(1.2,0.7))
        
        bump_chart.pyplot(fig)
        # plt.show()
        
    elif year_considered == []:
        # Display a message if no years are selected
        bump_chart.write('Please select the year to view.')
    elif categorical_label_list == []:
        # Display a message if no categorical labels are selected
        bump_chart.write('Please select at least one category.')

    
    
#======================================================================================================

def create_scatter_chart(x_axis, y_axis, fact_category, fact_subcategory_list):
    """
    Generates a scatter chart using Matplotlib.
    
    Parameters:
    x_axis: The column name to use as the x-axis.
    y_axis: The column name to use as the y-axis.
    fact_category: The column name to use as the category for coloring the points.
    fact_subcategory_list: A list of subcategories to include in the chart.
    
    Returns:
    None
    """
    
    # Check if the x-axis and y-axis are different
    if x_axis != y_axis:
        # Create a copy of the dataframe
        scatter_df = df.copy()
        
        # Filter the data to include only subcategories in fact_subcategory_list
        scatter_df_filtered = scatter_df[scatter_df[fact_category].isin(fact_subcategory_list)].reset_index().reset_index(drop=True)
        
        # Select only the x-axis, y-axis, and fact_category columns
        scatter_df_filtered = scatter_df_filtered[[x_axis, y_axis, fact_category]]
        
        # Sort the data by fact_category
        scatter_df_filtered = scatter_df_filtered.sort_values(by=fact_category)
        
        # Define a list of complimentary colors for the scatter chart
        complimentary_colors = ["#ba2649", "#ffa7ca", "#1a6b54", "#f7d560", "#5c3c92", "#f2a0a1"]
        
        # Create a dictionary mapping subcategories to colors
        colors = dict(zip(fact_subcategory_list, complimentary_colors))
       
        # Create a list of colors for each point in the chart
        scatter_colors = [colors[c] for c in scatter_df_filtered[fact_category]]

        # Create a scatter chart using Matplotlib
        fig, ax = plt.subplots(figsize=(5,3))
        ax.scatter(scatter_df_filtered[x_axis], scatter_df_filtered[y_axis], color=scatter_colors)
         # Set the y-axis ticks to display as real numbers instead of scientific notation
            
        
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%.f'))
        # ax.set_xticklabels(tick_labels, fontsize = 7)
        ax.set_xticklabels(ax.get_xticklabels(),fontsize = 7, rotation= 0)
        
        
        # Add a legend to the chart
        for parts in fact_subcategory_list:
            plt.scatter([], [], c=colors[parts], label=parts)
            # plt.legend(loc='lower left', ncol=2)
        
        fig.legend(bbox_to_anchor=(0.9, 0.5), loc='lower left',  ncol=1)
        # Display the chart in Streamlit
        scatter_chart.pyplot(fig)
        
        # Display an expander with the data used to create the chart
        with st.expander(f'## :memo: **Click to Show Correlation Table**'):
            st.write(scatter_df_filtered.reset_index(drop=True))
    
    else:
        # Display a message if the x-axis and y-axis are the same
        scatter_chart.write(f'## Please Select different X and Y Axes to view Relationship.')


        

#======================================================================================================


def get_year_as_String(year_considered):
     # Convert the year_considered list to a string
    year_list_str = ', '.join(map(str, year_considered))
    
    return year_list_str

#======================================================================================================

st.set_page_config(layout='wide')

st.sidebar.header('Company\'s Financials Dashboard. `version 0.2`')

st.sidebar.markdown('''

---

Created by [Ajigbayi, Oluwafemi Tosin.](https://www.linkedin.com/in/oluwafemi-ajigbayi) 


This dashboard was created using the [Company Financials](https://www.kaggle.com/datasets/atharvaarya25/financials) Dataset from Kaggle. 

The code for this project is available on [Github](https://github.com/femstac/kaggle_Company_Financials.git).

--- 
I am always looking for ways to improve my work and will welcome any feedback or suggestions. 

If you have any ideas for improvements or would like to collaborate, please don’t hesitate to reach out to me. Thank you! :heart:
''')


st.title(':chart: :office: Interactive Web App for Analysis of a Company\'s Financial Record' )

st.divider()


st.markdown(f'## VISUALIZATION 1: :blue[BAR CHART] & :blue[STACKED BAR CHART]')

col_aa,col_ab,col_ac=st.columns([1,7,1])




# Use columns to display widgets side by side 
col11,col12 = col_ab.columns(2)  

    
# Create widgets to select the x-axis and y-axis columns
bar_x_axis = col11.selectbox('**For each**', Fact_Columns)
bar_y_axis = col11.selectbox('**Select total amount of :**', Numerical_Columns)

selected_products= col12.multiselect('**Select Products to view**', get_unique_items_list_in_column(Product),
                                  default= get_unique_items_list_in_column(Product),
                                   key='selected_products')
       
bar_df=create_bar_table(bar_x_axis, bar_y_axis)

colors = [get_differentiating_color(bar_df, bar_y_axis, value) for value in bar_df[ bar_y_axis]]
    

#Title of the first chart
st.markdown(f'#### Total {bar_y_axis} per {bar_x_axis} ')
st.markdown(get_report_on_min_max_bar_values(bar_df,bar_x_axis, bar_y_axis))


bar_chart, stacked_chart= st.columns(2)


# Call the create_bar_chart function with the selected columns
plot_bar_chart(bar_df, bar_x_axis, bar_y_axis, colors)

st.markdown('''---''')
st.markdown('''---''')


#================================================================================================
    

#check if the selected product list is empty
if selected_products != []:
    # Call the create_stacked_bar_chart function with the selected columns
    create_stacked_bar_chart(bar_x_axis, bar_y_axis, selected_products)  
else:
        #Display a select a product message
    stacked_chart.write(f' \n #### Please Select Products to view their distribution among {bar_x_axis}.')
        
    
        
#======================================================================================================        

st.markdown(f'## VISUALIZATION 2 : :blue[BUMP CHART]')
col_ba,col_bb,col_bc=st.columns([1,7,1])

col21, col22 = col_bb.columns(2)
col31, col32 =col_bb.columns(2)


col41,col42,col43 = st.columns([1,7,1]) #create 3 columns, where the middle one is 7 times bigger than either side.
  
    
# Create widgets to select the x-axis and y-axis columns
bump_x_widget= col21.selectbox(' **Select Category :**', Fact_Columns)

bump_y_widget=col31.selectbox('**Select Numerical Section :**', Numerical_Columns)



categorical_label_list= col22.multiselect('**Select Subcategories to view :**',  get_unique_items_list_in_column(bump_x_widget),
                                  default= get_unique_items_list_in_column(bump_x_widget))

year_considered = col32.multiselect('**Select Year :**', get_unique_items_list_in_column(Date), default = [min(df['Date'].dt.year)])


col42.markdown(f'#### Total {bump_y_widget} in each {bump_x_widget} in the year {get_year_as_String(year_considered)} ')

# Create a column using the st.columns function
bump_chart= col42.columns(1)[0]    

create_bump_chart(bump_y_widget, bump_x_widget, year_considered , categorical_label_list)
    

st.markdown('''---''')
st.markdown('''---''')
#======================================================================================================

st.markdown(f'## VISUALIZATION 3 :  :blue[ SCATTER CHART]')


st.markdown('    ')
col_ca,col_cb,col_cc=st.columns([1,7,1])

col51, col52 = col_cb.columns(2)
col61, col62 =col_cb.columns(2)
col71,col72,col73 = st.columns([1,7,1]) #create 3 columns, where the middle one is 7 times bigger than either side.
    
 
 
# Create widgets to select the x-axis and y-axis columns
Scatter_x_axis = col51.selectbox('**Select X-axis :**', Varying_Numerical_Columns, index= 0 )

Scatter_y_axis = col52.selectbox('**Select Y-axis :**', Varying_Numerical_Columns, index= 1)



Scatter_Category_to_view = col61.selectbox('**Select the Category :**', Fact_Columns)


selected_category= col62.multiselect('**Select Subcategory to view**',     
                                  get_unique_items_list_in_column(Scatter_Category_to_view),
                                  default= get_unique_items_list_in_column(Scatter_Category_to_view),
                                   key='selected_category')

col72.markdown(f'#### Relationship between {Scatter_x_axis} and {Scatter_y_axis} for Selected {Scatter_Category_to_view} ')
    
#check if the selected product list is empty
if selected_category != []:
    # Call the create_stacked_bar_chart function with the selected columns
    scatter_chart=col72.columns(1)[0]
    create_scatter_chart(Scatter_x_axis, Scatter_y_axis, Scatter_Category_to_view, selected_category)
    
    
else:
        #Display a select a product message
        scatter_chart=st.write(f'### Please select the subcategory of {Scatter_Category_to_view} to view.')
        
  

