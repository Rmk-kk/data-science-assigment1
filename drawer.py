import warnings
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

tesla_rev_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
gamestop_rev_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

def get_stock_data(ticket, period = 'max'):
    stock = yf.Ticker(ticket)
    history = stock.history(period)
    data_frame = pd.DataFrame(history)
    data_frame.reset_index(inplace=True)
    #print(data_frame.head())
    print(data_frame.head())
    return data_frame
#get_stock_data('TSLA', 'max')

def get_revenue_data(url):
    html_data = requests.get(url).text
    soup = BeautifulSoup(html_data, 'html5lib')
    stock_dataframe = pd.DataFrame(columns=["Date", "Revenue"])
    for row in soup.find_all('tbody')[1].find_all('tr'):
        col = row.find_all("td")
        date = col[0].text
        revenue = col[1].text
        stock_dataframe = stock_dataframe._append({"Date":date, "Revenue":revenue}, ignore_index = True)  

    stock_dataframe["Revenue"] = stock_dataframe['Revenue'].str.replace(',|\\$', "", regex=True)
    stock_dataframe.dropna(inplace=True)
    stock_dataframe = stock_dataframe[stock_dataframe['Revenue'] != ""]
    print(stock_dataframe.tail())
    return stock_dataframe

#get_revenue_data(gamestop_rev_url)

#make_graph(get_stock_data('TSLA', 'max'), get_revenue_data(tesla_rev_url), 'Tesla')
make_graph(get_stock_data('GME', 'max'), get_revenue_data(gamestop_rev_url), 'GameStop')

