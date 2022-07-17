import dash
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np


## reading the dataset 
df = pd.read_csv('Retail Analytics Dataset.csv')
import re

df['Order Date'] = df['Order Date'].replace({r'/':'-'}, regex = True)
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%m-%d-%Y')
df.set_index('Order Date', inplace=True, drop=True)
df['Year'] = df.index.year
df['Month'] = df.index.month
df['Day'] = df.index.day
import calendar
df['Month'] = df['Month'].apply(lambda x: calendar.month_abbr[x])
df['month_year'] = df['Year'].astype(str) + '-' + df['Month']

df['Profit Margin'] = round((df['Profit']/df['Sales']) * 100,2)

######################## total sales,profit, dicount, margin Month level  ###################
monthly_sales_df = df.groupby(['month_year']).agg({'Sales':'sum'}).reset_index()
monthly_profit_df = df.groupby(['month_year']).agg({'Profit':'sum'}).reset_index()
monthly_discount_df = df.groupby(['month_year']).agg({'Discount':'sum'}).reset_index()
monthly_margin_df = df.groupby(['month_year']).agg({'Profit Margin':'sum'}).reset_index()

 
######################### rounding sales,profit,discount,margin to 1 decimal ##################
monthly_sales_df['Sales'] = monthly_sales_df['Sales'].round(1)
monthly_profit_df['Sales'] = monthly_profit_df['Profit'].round(1)
monthly_discount_df['Sales'] = monthly_discount_df['Discount'].round(1)
monthly_margin_df['Sales'] = monthly_margin_df['Profit Margin'].round(1)


########################### store level sales #######################
store_df=df.groupby(['month_year','Customer Name']).agg({'Sales':'sum'}).reset_index()
store_df['Customer Name'] = store_df['Customer Name'].apply(lambda x: str(x))
store_df['Sales'] = store_df['Sales'].round(1)


######################## dept level sales #########################
dept_df=df.groupby(['month_year','Category']).agg({'Sales':'sum'}).reset_index()
dept_df['Category'] = dept_df['Category'].apply(lambda x: 'Dept'+" "+str(x))
dept_df['Sales'] = dept_df['Sales'].round(1)

######################### subcategory level sales ###############
sub_dept_df=df.groupby(['month_year','Sub Category']).agg({'Sales':'sum'}).reset_index()
sub_dept_df['Sales'] = sub_dept_df['Sales'].round(1)

######################### region level sales ###############
region_df=df.groupby(['month_year','Region']).agg({'Sales':'sum'}).reset_index()
region_df['Sales'] = region_df['Sales'].round(1)

######################### region level sales ###############
region_df=df.groupby(['month_year','Region']).agg({'Sales':'sum'}).reset_index()
region_df['Sales'] = region_df['Sales'].round(1)

######################### city level sales ###############
city_df=df.groupby(['month_year','City']).agg({'Sales':'sum'}).reset_index()
city_df['Sales'] = city_df['Sales'].round(1)

######################### orders level sales ###############
order_df=df.groupby(['month_year','Order ID']).agg({'Sales':'sum'}).reset_index()
order_df['Sales'] = order_df['Sales'].round(1)

app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])


navbar = dbc.Navbar( id = 'navbar', children = [
    dbc.Row([
        dbc.Col(
            dbc.NavbarBrand("Retail Sales Dashboard", style = {'color':'white', 'fontSize':'50px','fontFamily':'woff2'}
                            )
            
            )
        
        
        ],align = "left",
        # no_gutters = True
        ),
    
    
    ], color = '#090059')


card_content_dropdwn = [
    dbc.CardBody(
        [
            html.H6('Select Months', style = {'textAlign':'center'}),
            
            dbc.Row([
                
                dbc.Col([
                    
                    html.H6('Current Month'),
                    
                    dcc.Dropdown( id = 'dropdown_base',
        options = [
            {'label':i, 'value':i } for i in monthly_sales_df.sort_values('month_year')['month_year']
        
            ],
        value = "2015-May",
                                )
                    
                    ]),
                
                dbc.Col([
                    
                    html.H6('Reference Month'),
                    
                    dcc.Dropdown( id = 'dropdown_comp',
        options = [
            {'label':i, 'value':i } for i in monthly_sales_df.sort_values('month_year')['month_year']
        
            ],
        value = '2015-Jan',
        
        )   
                    ]),
                
                ])
            ]
        )
    ]


body_app = dbc.Container([
    
    html.Br(),
    html.Br(),
    
    dbc.Row([
        dbc.Col([dbc.Card(card_content_dropdwn,style={'height':'150px'})],width = 2),
        dbc.Col([dbc.Card(id = 'card_num1',style={'height':'150px'})]),
        dbc.Col([dbc.Card(id = 'card_num2',style={'height':'150px'})]),
        dbc.Col([dbc.Card(id = 'card_num3',style={'height':'150px'})]),
        dbc.Col([dbc.Card(id = 'card_num4',style={'height':'150px'})]),

        ]),
    
    html.Br(),
    html.Br(),
    
    dbc.Row([
        
        dbc.Col([dbc.Card(id = 'card_num5',style={'height':'150px'})]),
        dbc.Col([dbc.Card(id = 'card_num6',style={'height':'150px'})]),
        dbc.Col([dbc.Card(id = 'card_num7',style={'height':'150px'})]),
        dbc.Col([dbc.Card(id = 'card_num8',style={'height':'150px'})]),
        ]),
    
    html.Br(),
    html.Br(),
    
    dbc.Row([
        dbc.Col([dbc.Card(id = 'card_num9',style={'height':'350px'})]),
        dbc.Col([dbc.Card(id = 'card_num10',style={'height':'350px'})]),
        dbc.Col([dbc.Card(id = 'card_num11',style={'height':'350px'})]),
        
        ]),
    
    html.Br(),
    html.Br(),
    
    dbc.Row([
        dbc.Col([dbc.Card(id = 'card_num12',style={'height':'350px'})],width = 6),
        dbc.Col([dbc.Card(id = 'card_num13',style={'height':'350px'})]),
        dbc.Col([dbc.Card(id = 'card_num14',style={'height':'350px'})]),
        

        ]),
    
    html.Br(),
    html.Br()
    
    
    
    ], 
    style = {'backgroundColor':'#778899'},
    fluid = True)


app.layout = html.Div(id = 'parent', children = [navbar,body_app])


@app.callback([Output('card_num1', 'children'),
               Output('card_num2', 'children'),
               Output('card_num3', 'children'),
               Output('card_num4', 'children'),
               Output('card_num5', 'children'),
               Output('card_num6', 'children'),
               Output('card_num7', 'children'),
               Output('card_num8', 'children'),
               Output('card_num9', 'children'),
               Output('card_num10', 'children'),
               Output('card_num11', 'children'),
               Output('card_num12', 'children'),
               Output('card_num13', 'children'),
               Output('card_num14', 'children')
               
               ],
              [Input('dropdown_base','value'), 
                Input('dropdown_comp','value')])

def update_cards(base, comparison):
    
    sales_base = monthly_sales_df.loc[monthly_sales_df['month_year']==base].reset_index()['Sales'][0]
    sales_comp = monthly_sales_df.loc[monthly_sales_df['month_year']==comparison].reset_index()['Sales'][0]
    
    profit_base = monthly_profit_df.loc[monthly_profit_df['month_year']==base].reset_index()['Profit'][0]
    profit_comp = monthly_profit_df.loc[monthly_profit_df['month_year']==comparison].reset_index()['Profit'][0]

    discount_base = monthly_discount_df.loc[monthly_discount_df['month_year']==base].reset_index()['Discount'][0]
    discount_comp = monthly_discount_df.loc[monthly_discount_df['month_year']==comparison].reset_index()['Discount'][0]

    margin_base = monthly_margin_df.loc[monthly_margin_df['month_year']==base].reset_index()['Profit Margin'][0]
    margin_comp = monthly_margin_df.loc[monthly_margin_df['month_year']==comparison].reset_index()['Profit Margin'][0]

    
    sales_base1 = monthly_sales_df.loc[monthly_sales_df['month_year']==base].reset_index()
    sales_comp1 = monthly_sales_df.loc[monthly_sales_df['month_year']==comparison].reset_index()

    diff_1 = np.round(sales_base -sales_comp,1)
    diff_2 = np.round(profit_base -profit_comp,1)
    diff_3 = np.round(discount_base -discount_comp,1)
    diff_4 = np.round(margin_base -margin_comp,1)
    
    

    base_st_ct = df.loc[df['month_year']==base,'Customer Name'].drop_duplicates().count()
    comp_st_ct = df.loc[df['month_year']==comparison,'Customer Name'].drop_duplicates().count()

    diff_store = np.round(base_st_ct-comp_st_ct,1)
    
    base_order_ct = df.loc[df['month_year']==base,'Order ID'].drop_duplicates().count()
    comp_order_ct = df.loc[df['month_year']==comparison,'Order ID'].drop_duplicates().count()

    diff_order = np.round(base_order_ct-comp_order_ct,1)
    
    
    store_base = store_df.loc[store_df['month_year']==base].sort_values('Sales',ascending = False).reset_index()[:10]
    store_comp = store_df.loc[store_df['month_year']==comparison].sort_values('Sales',ascending = False).reset_index()[:10]
    
    base_store_ct = df.loc[df['month_year']==base,'Category'].drop_duplicates().count()
    comp_store_ct = df.loc[df['month_year']==comparison,'Category'].drop_duplicates().count()
    
    base_sub_ct = df.loc[df['month_year']==base,'Sub Category'].drop_duplicates().count()
    comp_sub_ct = df.loc[df['month_year']==comparison,'Sub Category'].drop_duplicates().count()
    
    dept_base = dept_df.loc[dept_df['month_year']==base].sort_values('Sales',ascending = False).reset_index()[:10]
    dept_base=dept_base.rename(columns = {'Sales':'Sales_base'})
    dept_comp = dept_df.loc[dept_df['month_year']==comparison].sort_values('Sales',ascending = False).reset_index()
    dept_comp=dept_comp.rename(columns = {'Sales':'Sales_comp'})
    
    merged_df=pd.merge(dept_base, dept_comp, on = 'Category', how = 'left')
    merged_df['diff'] = merged_df['Sales_base']-merged_df['Sales_comp']

    sub_dept_base = sub_dept_df.loc[sub_dept_df['month_year']==base].sort_values('Sales',ascending = False).reset_index()[:10]
    sub_dept_base=sub_dept_base.rename(columns = {'Sales':'Sales_base'})
    sub_dept_comp = sub_dept_df.loc[sub_dept_df['month_year']==comparison].sort_values('Sales',ascending = False).reset_index()
    sub_dept_comp=sub_dept_comp.rename(columns = {'Sales':'Sales_comp'})
    
    merged_df2=pd.merge(sub_dept_base, sub_dept_comp, on = 'Sub Category', how = 'left')
    merged_df2['diff'] = merged_df2['Sales_base']-merged_df2['Sales_comp']
    
    region_base = region_df.loc[region_df['month_year']==base].sort_values('Sales',ascending = False).reset_index()[:10]
    region_base=region_base.rename(columns = {'Sales':'Sales_base'})
    region_comp = region_df.loc[sub_dept_df['month_year']==comparison].sort_values('Sales',ascending = False).reset_index()
    region_comp=region_comp.rename(columns = {'Sales':'Sales_comp'})
    
    merged_df3=pd.merge(region_base, region_comp, on = 'Region', how = 'left')
    merged_df3['diff'] = merged_df3['Sales_base']-merged_df3['Sales_comp']
    
    city_base = city_df.loc[city_df['month_year']==base].sort_values('Sales',ascending = False).reset_index()[:10]
    city_base=city_base.rename(columns = {'Sales':'Sales_base'})
    city_comp = city_df.loc[city_df['month_year']==comparison].sort_values('Sales',ascending = False).reset_index()
    city_comp=city_comp.rename(columns = {'Sales':'Sales_comp'})
    
    merged_df4=pd.merge(city_base, city_comp, on = 'City', how = 'left')
    merged_df4['diff'] = merged_df4['Sales_base']-merged_df4['Sales_comp']
    
    order_base = order_df.loc[order_df['month_year']==base].sort_values('Sales',ascending = False).reset_index()[:10]
    order_base=order_base.rename(columns = {'Sales':'Sales_base'})
    order_comp = order_df.loc[order_df['month_year']==comparison].sort_values('Sales',ascending = False).reset_index()
    order_comp=order_comp.rename(columns = {'Sales':'Sales_comp'})
    
    merged_df5=pd.merge(order_base, order_comp, on = 'Order ID', how = 'left')
    merged_df5['diff'] = merged_df5['Sales_base']-merged_df5['Sales_comp']
    
    
    fig = go.Figure(data = [go.Bar(x = sales_base1['month_year'], y = sales_base1['Sales'],\
                                   base = dict(marker_color = '#FA8072', color = '#FA8072', width = 4),name = '{}'.format(base)),
                        go.Bar(x = sales_comp1['month_year'], y = sales_comp1['Sales'],\
                                   base = dict(color = '#4863A0', width = 4),name = '{}'.format(comparison))])

    
    fig.update_layout(plot_bgcolor = 'white',
                      margin=dict(l = 40, r = 5, t = 60, b = 40),
                      yaxis_tickprefix = 'INR',
                      yaxis_ticksuffix = 'M')


    fig2 = go.Figure([go.Bar(x = store_base['Sales'], y = store_base['Customer Name'], marker_color = '#FA8072',name = '{}'.format(base),\
                             orientation = 'h',
                             textposition = 'outside'
                             ),
                 ])
        
        
    fig3 = go.Figure([go.Bar(x = store_comp['Sales'], y = store_comp['Customer Name'], marker_color = '#4863A0',name = '{}'.format(comparison),\
                            orientation = 'h',
                             textposition = 'outside'
                             ),
                 ])
        
    fig2.update_layout(plot_bgcolor = 'white',
                       xaxis = dict(range = [0,'{}'.format(store_base['Sales'].max()+10000)]),
                      margin=dict(l = 40, r = 5, t = 60, b = 40),
                      xaxis_tickprefix = 'INR ',
                      xaxis_ticksuffix = ' ',
                      title = '{}'.format(base),
                      title_x = 0.5)
    
    fig3.update_layout(plot_bgcolor = 'white',
                       xaxis = dict(range = [0,'{}'.format(store_comp['Sales'].max()+10000)]),
                      margin=dict(l = 40, r = 5, t = 60, b = 40),
                      xaxis_tickprefix = 'INR ',
                      xaxis_ticksuffix = ' ',
                      title = '{}'.format(comparison),
                      title_x = 0.5)

    fig4 = go.Figure([go.Bar(x = merged_df['diff'], y = merged_df['Category'], marker_color = '#4863A0',\
                              orientation = 'h',
                             textposition = 'outside'
                             ),
                 ])
        
    fig4.update_layout(plot_bgcolor = 'white',
                       margin=dict(l = 40, r = 5, t = 60, b = 40),
                      xaxis_tickprefix = 'INR ',
                      xaxis_ticksuffix = ' '
                     )
    fig5 = go.Figure([go.Bar(x = merged_df2['diff'], y = merged_df2['Sub Category'], marker_color = '#4863A0',\
                              orientation = 'h',
                             textposition = 'outside'
                             ),
                 ])
        
    fig5.update_layout(plot_bgcolor = 'white',
                       margin=dict(l = 40, r = 5, t = 60, b = 40),
                      xaxis_tickprefix = 'INR ',
                      xaxis_ticksuffix = ' '
                     )

    fig6 = go.Figure([go.Bar(x = merged_df3['diff'], y = merged_df3['Region'], marker_color = '#4863A0',\
                              orientation = 'h',
                             textposition = 'outside'
                             ),
                 ])
        
    fig6.update_layout(plot_bgcolor = 'white',
                       margin=dict(l = 40, r = 5, t = 60, b = 40),
                      xaxis_tickprefix = 'INR ',
                      xaxis_ticksuffix = ' '
                     )
    
    fig7 = go.Figure([go.Bar(x = merged_df4['diff'], y = merged_df4['City'], marker_color = '#4863A0',\
                              orientation = 'h',
                             textposition = 'outside'
                             ),
                 ])
        
    fig7.update_layout(plot_bgcolor = 'white',
                       margin=dict(l = 40, r = 5, t = 60, b = 40),
                      xaxis_tickprefix = 'INR ',
                      xaxis_ticksuffix = ' '
                     )
    
    if diff_1 >= 0:
        a =   dcc.Markdown( dangerously_allow_html = True,
                   children = ["<sub>+{0}{1}{2}</sub>".format('INR ',diff_1,' ')], style = {'textAlign':'center'})
        
    elif diff_1 < 0:
        
        a =    dcc.Markdown( dangerously_allow_html = True,
                   children = ["<sub>-{0}{1}{2}</sub>".format('INR ',np.abs(diff_1),' ')], style = {'textAlign':'center'})
    if diff_2 >= 0:
        a =   dcc.Markdown( dangerously_allow_html = True,
                   children = ["<sub>+{0}{1}{2}</sub>".format('INR ',diff_1,' ')], style = {'textAlign':'center'})
        
    elif diff_2 < 0:
        
        a =    dcc.Markdown( dangerously_allow_html = True,
                   children = ["<sub>-{0}{1}{2}</sub>".format('INR ',np.abs(diff_1),' ')], style = {'textAlign':'center'})
    if diff_3 >= 0:
        a =   dcc.Markdown( dangerously_allow_html = True,
                   children = ["<sub>+{0}{1}{2}</sub>".format('INR ',diff_1,' ')], style = {'textAlign':'center'})
        
    elif diff_3 < 0:
        
        a =    dcc.Markdown( dangerously_allow_html = True,
                   children = ["<sub>-{0}{1}{2}</sub>".format('INR ',np.abs(diff_1),' ')], style = {'textAlign':'center'})
                          
        
    if diff_4 >= 0:
        a =   dcc.Markdown( dangerously_allow_html = True,
                   children = ["<sub>+{0}{1}{2}</sub>".format('INR ',diff_1,' ')], style = {'textAlign':'center'})
        
    elif diff_4 < 0:
        
        a =    dcc.Markdown( dangerously_allow_html = True,
                   children = ["<sub>-{0}{1}{2}</sub>".format('INR ',np.abs(diff_1),' ')], style = {'textAlign':'center'})
                          
    if diff_store >= 0:
        c =   dcc.Markdown( dangerously_allow_html = True,
                   children = ["<sub>+{0}</sub>".format(diff_store)], style = {'textAlign':'center'})
        
    elif diff_store < 0:
        
        c =   dcc.Markdown( dangerously_allow_html = True,
                   children = ["<sub>-{0}</sub>".format(np.abs(diff_store))], style = {'textAlign':'center'})
        
        
    
    card_content = [
        
        dbc.CardBody(
            [
                html.H6('Total sales', style = {'fontWeight':'bold', 'textAlign':'center'}),
                
                html.H3('{0}{1}{2}'.format("INR ", sales_base, " "), style = {'color':'#090059','textAlign':'center'}),
                a
                
                ]
                   
            )  
        ]
    
    card_content2 = [
        
        dbc.CardBody(
            [
                html.H6('Total profit', style = {'fontWeight':'bold', 'textAlign':'center'}),
                
                html.H3('{0}{1}{2}'.format("INR ", profit_base, " "), style = {'color':'#090059','textAlign':'center'}),
                a
                
                ]
                   
            )  
        ]
    
    card_content3 = [
        
        dbc.CardBody(
            [
                html.H6('Total discount', style = {'fontWeight':'bold', 'textAlign':'center'}),
                
                html.H3('{0}{1}{2}'.format("INR ", discount_base, " "), style = {'color':'#090059','textAlign':'center'}),
                a
                
                ]
                   
            )  
        ]
    
    card_content4 = [
        
        dbc.CardBody(
            [
                html.H6('Total Profit Margin', style = {'fontWeight':'bold', 'textAlign':'center'}),
                
                html.H3('{0}{1}{2}'.format("INR ", margin_base, " "), style = {'color':'#090059','textAlign':'center'}),
                a
                
                ]
                   
            )  
        ]
    
    card_content5 = [
        
        dbc.CardBody(
            [
                html.H6('Total Customers', style = {'fontWeight':'bold', 'textAlign':'center'}),
                
                html.H5('{0}'.format( base_st_ct), style = {'color':'#090059','textAlign':'center'}),
                
                c
                ]
                   
            )  
        ]
    
    card_content6 = [
        
        dbc.CardBody(
            [
                html.H6('Total Orders', style = {'fontWeight':'bold', 'textAlign':'center'}),
                
                html.H5('{0}'.format( base_order_ct), style = {'color':'#090059','textAlign':'center'}),
                
                c
                ]
                   
            )  
        ]
    
    card_content7 = [
        
        dbc.CardBody(
            [
                html.H6('Total Categories', style = {'fontWeight':'bold', 'textAlign':'center'}),
                
                html.H3('{0}'.format( base_store_ct), style = {'color':'#090059','textAlign':'center'}),
                
                
                
                ]
                   
            )  
        ]
    card_content8 = [
        
        dbc.CardBody(
            [
                html.H6('Total Sub Categories', style = {'fontWeight':'bold', 'textAlign':'center'}),
                
                html.H3('{0}'.format( base_sub_ct), style = {'color':'#090059','textAlign':'center'}),
                
                
                
                ]
                   
            )  
        ]
    
    card_content9 = [
        
        dbc.CardBody(
            [
                html.H6('Monthly Sales Comparison', style = {'fontWeight':'bold', 'textAlign':'center'}),
                
                dcc.Graph(figure = fig, style = {'height':'250px'})
                
                
                ]
                   
            )  
        ] 
    
    card_content10 = [
        
        dbc.CardBody(
            [
                html.H6('Sales difference between Categories ({} - {})'.format(base, comparison), style = {'fontWeight':'bold', 'textAlign':'center'}),
                
                dcc.Graph(figure = fig4, style = {'height':'300px'})
                
                
                ]
                   
            )  
        ]
    
    
    
    card_content11 = [
        
        dbc.CardBody(
            [
                html.H6('Sales difference between Sub Categories ({} - {})'.format(base, comparison), style = {'fontWeight':'bold', 'textAlign':'center'}),
                
                dcc.Graph(figure = fig5, style = {'height':'290px'})
                
                
                ]
                   
            )  
        ] 
    
    card_content12 = [
        
        dbc.CardBody(
            [
                html.H6('Customers with highest Sales', style = {'fontWeight':'bold', 'textAlign':'center'}),
                
                dbc.Row([
                    dbc.Col([dcc.Graph(figure = fig2, style = {'height':'300px'}),
                ]),
                    dbc.Col([dcc.Graph(figure = fig3, style = {'height':'300px'}),
                ])
                    
                    ])
                
                
                
                ]
                   
            )  
        ]
    
    
    card_content13 = [
        
        dbc.CardBody(
            [
                html.H6('Sales difference between Regions ({} - {})'.format(base, comparison), style = {'fontWeight':'bold', 'textAlign':'center'}),
                
                dcc.Graph(figure = fig6, style = {'height':'300px'})
                
                
                ]
                   
            )  
        ] 
    
    card_content14 = [
        
        dbc.CardBody(
            [
                html.H6('Sales difference between Cities ({} - {})'.format(base, comparison), style = {'fontWeight':'bold', 'textAlign':'center'}),
                
                dcc.Graph(figure = fig7, style = {'height':'300px'})
                
                
                ]
                   
            )  
        ] 

    
    return card_content, card_content2,card_content3, card_content4, card_content5, card_content6, card_content7, card_content8,card_content9, card_content10, card_content11,card_content12, card_content13, card_content14


if __name__ == "__main__":
    app.run_server()
    #debug = True
