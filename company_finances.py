import streamlit as st
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
 Sales, COGS, Profit, Date, Month_Number, Month_Name, Year
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

#======================================================================================================
# Function to generate bar chart
def create_bar_table(x_axis, y_axis):
    
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
 
#======================================================================================================    



def get_differentiating_color(bar_df, y_axis, value):
    if value== bar_df[y_axis].max():
        return 'royalblue'
    elif value== bar_df[y_axis].min():
        return 'red'
    else:
        return 'gray'

#======================================================================================================   
    
def plot_bar_chart(bar_df, bar_x_axis, bar_y_axis  ,colors):
    # Create a bar chart using Matplotlib
    fig, ax = plt.subplots()
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
    
    chart1.pyplot(fig)

#======================================================================================================   
    
    
def get_report_on_min_max_bar_values(bar_df,bar_x_axis, bar_y_axis):
    
    max_value = bar_df[bar_y_axis].max()
    
    formatted_max_value = format(max_value,',')
    
    max_category = bar_df.loc[bar_df[bar_y_axis] == max_value, bar_x_axis].iloc[0]
    
    min_value = bar_df[bar_y_axis].min()
    
    formatted_min_value = format(min_value,',')
    
    min_category = bar_df.loc[bar_df[bar_y_axis] == min_value, bar_x_axis].iloc[0]
    
    
    
    if bar_y_axis== Units_Sold:
        report = f'### The {bar_x_axis}  **\"{max_category}\"** has the highest Total {bar_y_axis} value of **{formatted_max_value}** units. \n#### The lowest is **\"{min_category}\"** with a value of **{formatted_min_value}** units.'
    
    else:
        report = f'### The {bar_x_axis}  **\"{max_category}\"** has the highest Total {bar_y_axis} value of **\${formatted_max_value}** \n#### The lowest is **\"{min_category}\"** with a value of **\${formatted_min_value}**'
        
    if max_value==min_value:
        report =  f'### The Total {bar_y_axis} is the same across all The {bar_x_axis} with a value of **\${formatted_min_value}**.'
        
    return report




#=====================================================================



# Create a function to generate a stacked bar chart
def create_stacked_bar_chart(x_axis, y_axis, product_List):
    
    #Create Complimentary colours for stacked graph
    
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
        products_df_pivot = products_df.pivot(index=x_axis, columns= Product, values=y_axis).fillna(0)

        # Create a stacked bar chart using Pandas
        chart = products_df_pivot.plot(kind='bar', stacked=True)
          
        # Set the y-axis ticks to display as real numbers instead of scientific notation
        chart.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.0f'))
    
        
        # Wrap the x-axis tick labels
        tick_labels = [textwrap.fill(label, 10) for label in bar_df[bar_x_axis]]
        chart.set_xticks(range(len(bar_df[bar_x_axis])))
        chart.set_xticklabels(tick_labels, fontsize=9)

        for label in chart.get_xticklabels():
            label.set_fontweight('bold')

        # set rotation for x labels
        chart.set_xticklabels(chart.get_xticklabels(), rotation=0)


        # Display the chart in Streamlit
        chart2.pyplot(chart.figure)
        
    else:
        # Display a message if the x-axis is 'Product'
        chart2.write(f'Product infograph for {y_axis} already available. Please select another section in the For Each drop down menu')



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
    year_list_str = ', '.join(map(str, year_considered))

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
        fig, ax = plt.subplots()
        for column in bump_df_pivot.columns:
            ax.plot(bump_df_pivot.index, bump_df_pivot[column], label=column)
            ax.scatter(bump_df_pivot.index, bump_df_pivot[column])
        
        # Wrap the x-axis tick labels
        tick_labels = [textwrap.fill(label, 5) for label in bump_df_pivot.index]
        ax.set_xticks(bump_df_pivot.index)
        ax.set_xticklabels(tick_labels, fontsize=7)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        ax.legend()
        
        st.pyplot(fig)
        # plt.show()
        
    elif year_considered == []:
        # Display a message if no years are selected
        st.write('Please select the year to view.')
    elif categorical_label_list == []:
        # Display a message if no categorical labels are selected
        st.write('Please select at least one category.')

    
    
#======================================================================================================
def scatter_chart(x_axis,
                  y_axis,
                  fact_category,
                  fact_subcategory_list):
    
   
    if x_axis != y_axis:
        scatter_df = df.copy()
        scatter_df_filtered = scatter_df[scatter_df[fact_category].isin(fact_subcategory_list)].reset_index().reset_index(drop=True)
        scatter_df_filtered = scatter_df_filtered[[x_axis,y_axis,fact_category]]
        
        scatter_df_filtered = scatter_df_filtered.sort_values(by=fact_category)
                
        complimentary_colors = ["#ba2649", "#ffa7ca", "#1a6b54", "#f7d560", "#5c3c92", "#f2a0a1"]   
        
        colors = dict(zip(fact_subcategory_list, complimentary_colors))
       
        scatter_colors= [colors[c] for c in  scatter_df_filtered[fact_category]]

        fig,ax = plt.subplots()
        ax.scatter(scatter_df_filtered[x_axis], scatter_df_filtered[y_axis], color=scatter_colors,  )
        
        for parts in fact_subcategory_list :
            plt.scatter([],[], c=colors[parts], label=parts )
            plt.legend()
        # for items in fact_subcategory_list:
        #     scatter_df_filtered = scatter_df_filtered[scatter_df_filtered[fact_category]==items]
        #     ax.scatter(scatter_df_filtered[x_axis], scatter_df_filtered[y_axis], color=complimentary_colors)
            # ax.scatter()
        
        st.pyplot(fig)
        with st.expander("show table"):
            st.write(scatter_df_filtered)
    
    else:
        st.write(f'## Please Select different X and Y Axes to view Relationship.')
    

        

#======================================================================================================


# Use columns to display widgets side by side 
first_chart_y_widget,first_chart_x_widget = st.columns(2)  

    
# Create widgets to select the x-axis and y-axis columns
bar_x_axis = first_chart_x_widget.selectbox('For each', Fact_Columns)
bar_y_axis = first_chart_y_widget.selectbox('Select total amount of :', Numerical_Columns)

    
bar_df=create_bar_table(bar_x_axis, bar_y_axis)

colors = [get_differentiating_color(bar_df, bar_y_axis, value) for value in bar_df[ bar_y_axis]]
    

#Title of the first chart
st.markdown(f'# Total {bar_y_axis} per {bar_x_axis}')
st.markdown(get_report_on_min_max_bar_values(bar_df,bar_x_axis, bar_y_axis))


selected_products= st.multiselect('Select Products to view', get_unique_items_list_in_column(Product),
                                  default= get_unique_items_list_in_column(Product))
    

chart1, chart2= st.columns(2)


# Call the create_bar_chart function with the selected columns
plot_bar_chart(bar_df, bar_x_axis, bar_y_axis, colors)


#================================================================================================
    

#check if the selected product list is empty
if selected_products != []:
    # Call the create_stacked_bar_chart function with the selected columns
    create_stacked_bar_chart(bar_x_axis, bar_y_axis, selected_products)  
else:
        #Display a select a product message
    chart2.write(f'#### Please Select Products to view how the {bar_x_axis} is subdivided')
        
    
        
#======================================================================================================        
        

bump_chart_x_widget, bump_chart_y_widget = st.columns(2)
 
    
    
# Create widgets to select the x-axis and y-axis columns
bump_x_widget= bump_chart_x_widget.selectbox('Select X axis', Fact_Columns)
bump_y_widget=bump_chart_y_widget.selectbox('Select y axis :', Numerical_Columns)



categorical_label_list= st.multiselect('Select Subcategory to view',  get_unique_items_list_in_column(bump_x_widget),
                                  default= get_unique_items_list_in_column(bump_x_widget))

year_considered = st.multiselect('Select Category :', get_unique_items_list_in_column(Date), default = [min(df['Date'].dt.year)])

        

create_bump_chart(bump_y_widget, bump_x_widget, year_considered , categorical_label_list)
    
    
    
#======================================================================================================
 
    
scatter_chart_x_widget, scatter_chart_y_widget = st.columns(2)

    
    
# Create widgets to select the x-axis and y-axis columns
Scatter_x_axis = scatter_chart_x_widget.selectbox('Select X axis', Varying_Numerical_Columns, index= 0 )
Scatter_y_axis = scatter_chart_y_widget.selectbox('Select y axis :', Varying_Numerical_Columns, index= 1)
Scatter_Category_to_view = scatter_chart_x_widget.selectbox('Select Category :', Fact_Columns)


selected_category= st.multiselect('Select Subcategory to view',     
                                  get_unique_items_list_in_column(Scatter_Category_to_view),
                                  default= get_unique_items_list_in_column(Scatter_Category_to_view))
    
#check if the selected product list is empty
if selected_category != []:
    # Call the create_stacked_bar_chart function with the selected columns
    scatter_chart(Scatter_x_axis, Scatter_y_axis, Scatter_Category_to_view, selected_category)  
    
else:
        #Display a select a product message
        st.write(f'### Please select the subcategory of {Scatter_Category_to_view} to view.')
        
  

