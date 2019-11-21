#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 22:42:16 2019

@author: xiqiaoliu
"""

import requests 
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import string
import wordcloud
import base64


key = '9b10678a5cd94c019126ee0b8d7880aa'

all_options = {
 'abc-news': 'ABC News',
 'abc-news-au': 'ABC News (AU)',
 'aftenposten': 'Aftenposten',
 'al-jazeera-english': 'Al Jazeera English',
 'ansa': 'ANSA.it',
 'argaam': 'Argaam',
 'ars-technica': 'Ars Technica',
 'ary-news': 'Ary News',
 'associated-press': 'Associated Press',
 'australian-financial-review': 'Australian Financial Review',
 'axios': 'Axios',
 'bbc-news': 'BBC News',
 'bbc-sport': 'BBC Sport',
 'bild': 'Bild',
 'blasting-news-br': 'Blasting News (BR)',
 'bleacher-report': 'Bleacher Report',
 'bloomberg': 'Bloomberg',
 'breitbart-news': 'Breitbart News',
 'business-insider': 'Business Insider',
 'business-insider-uk': 'Business Insider (UK)',
 'buzzfeed': 'Buzzfeed',
 'cbc-news': 'CBC News',
 'cbs-news': 'CBS News',
 'cnbc': 'CNBC',
 'cnn': 'CNN',
 'cnn-es': 'CNN Spanish',
 'crypto-coins-news': 'Crypto Coins News',
 'der-tagesspiegel': 'Der Tagesspiegel',
 'die-zeit': 'Die Zeit',
 'el-mundo': 'El Mundo',
 'engadget': 'Engadget',
 'entertainment-weekly': 'Entertainment Weekly',
 'espn': 'ESPN',
 'espn-cric-info': 'ESPN Cric Info',
 'financial-post': 'Financial Post',
 'focus': 'Focus',
 'football-italia': 'Football Italia',
 'fortune': 'Fortune',
 'four-four-two': 'FourFourTwo',
 'fox-news': 'Fox News',
 'fox-sports': 'Fox Sports',
 'globo': 'Globo',
 'google-news': 'Google News',
 'google-news-ar': 'Google News (Argentina)',
 'google-news-au': 'Google News (Australia)',
 'google-news-br': 'Google News (Brasil)',
 'google-news-ca': 'Google News (Canada)',
 'google-news-fr': 'Google News (France)',
 'google-news-in': 'Google News (India)',
 'google-news-is': 'Google News (Israel)',
 'google-news-it': 'Google News (Italy)',
 'google-news-ru': 'Google News (Russia)',
 'google-news-sa': 'Google News (Saudi Arabia)',
 'google-news-uk': 'Google News (UK)',
 'goteborgs-posten': 'Göteborgs-Posten',
 'gruenderszene': 'Gruenderszene',
 'hacker-news': 'Hacker News',
 'handelsblatt': 'Handelsblatt',
 'ign': 'IGN',
 'il-sole-24-ore': 'Il Sole 24 Ore',
 'independent': 'Independent',
 'infobae': 'Infobae',
 'info-money': 'InfoMoney',
 'la-gaceta': 'La Gaceta',
 'la-nacion': 'La Nacion',
 'la-repubblica': 'La Repubblica',
 'le-monde': 'Le Monde',
 'lenta': 'Lenta',
 'lequipe': "L'equipe",
 'les-echos': 'Les Echos',
 'liberation': 'Libération',
 'marca': 'Marca',
 'mashable': 'Mashable',
 'medical-news-today': 'Medical News Today',
 'msnbc': 'MSNBC',
 'mtv-news': 'MTV News',
 'mtv-news-uk': 'MTV News (UK)',
 'national-geographic': 'National Geographic',
 'national-review': 'National Review',
 'nbc-news': 'NBC News',
 'news24': 'News24',
 'new-scientist': 'New Scientist',
 'news-com-au': 'News.com.au',
 'newsweek': 'Newsweek',
 'new-york-magazine': 'New York Magazine',
 'next-big-future': 'Next Big Future',
 'nfl-news': 'NFL News',
 'nhl-news': 'NHL News',
 'nrk': 'NRK',
 'politico': 'Politico',
 'polygon': 'Polygon',
 'rbc': 'RBC',
 'recode': 'Recode',
 'reddit-r-all': 'Reddit /r/all',
 'reuters': 'Reuters',
 'rt': 'RT',
 'rte': 'RTE',
 'rtl-nieuws': 'RTL Nieuws',
 'sabq': 'SABQ',
 'spiegel-online': 'Spiegel Online',
 'svenska-dagbladet': 'Svenska Dagbladet',
 't3n': 'T3n',
 'talksport': 'TalkSport',
 'techcrunch': 'TechCrunch',
 'techcrunch-cn': 'TechCrunch (CN)',
 'techradar': 'TechRadar',
 'the-american-conservative': 'The American Conservative',
 'the-globe-and-mail': 'The Globe And Mail',
 'the-hill': 'The Hill',
 'the-hindu': 'The Hindu',
 'the-huffington-post': 'The Huffington Post',
 'the-irish-times': 'The Irish Times',
 'the-jerusalem-post': 'The Jerusalem Post',
 'the-lad-bible': 'The Lad Bible',
 'the-new-york-times': 'The New York Times',
 'the-next-web': 'The Next Web',
 'the-sport-bible': 'The Sport Bible',
 'the-times-of-india': 'The Times of India',
 'the-verge': 'The Verge',
 'the-wall-street-journal': 'The Wall Street Journal',
 'the-washington-post': 'The Washington Post',
 'the-washington-times': 'The Washington Times',
 'time': 'Time',
 'usa-today': 'USA Today',
 'vice-news': 'Vice News',
 'wired': 'Wired',
 'wired-de': 'Wired.de',
 'wirtschafts-woche': 'Wirtschafts Woche',
 'xinhua-net': 'Xinhua Net',
 'ynet': 'Ynet'}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True

## Create Word Cloud 
news_dict = requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey={}'.format(key)).json()
cloud_text = []
for row in news_dict['articles']:
    cloud_text.append(row['title'])

cloud_text = "".join(cloud_text)
translator=str.maketrans('','',string.punctuation)
cloud_text=cloud_text.translate(translator)
word_cloud = wordcloud.WordCloud(background_color='white')
word_cloud.generate(cloud_text)
word_cloud.to_file('assets/temp.png')
image_filename = 'temp.png' 
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([
        
        html.Div([html.H1(id='title', children='News Hub', style={'margin-top':'100px','margin-left':'500px','font-family':'Comic Sans MS'}),
        
                  html.Img(src=app.get_asset_url('temp.png'),style={'width':'400px','height':'200px','position':'absolute','left':'760px','top':'35px'})],
                  ),
        
        html.Br(),
        
        html.Div([
                dcc.Input(id='keyword-input',
                          placeholder='Enter a keyword...',
                          type='text',
                          style={'margin-left':'350px','width':'400px'}),
      
                dcc.Dropdown(id='website-dropdown',
                             options=[{'label':j, 'value':i} for i,j in all_options.items()],
                             value = None,
                             style={'width':'400px','left':'15px','position':'relative','zIndex':'1000'}),
                html.Button(id='submit-button', n_clicks=0, children='Search',style={'margin-left':'50px'})],
                style = {'display':'flex','margin-top':'80px'}),
        html.Div(id='content',style={'margin-top':'50px','margin-left':'350px'})
        ],
    
    )

@app.callback(Output('website-dropdown','value'),
              [Input('website-dropdown','option')])

def update_dropdown(option):
    try:
        for key, value in all_options.items(): 
            if option == value: 
                c_value = key 
    except TypeError:
        c_value='abc-news'
        return c_value
    
@app.callback(Output('content','children'),
              [Input('submit-button', 'n_clicks')],
              [State('website-dropdown','value'),
               State('keyword-input','value')])

def search_results(n_clicks,source,keyword):
    if keyword==None and source==None:
        url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey={}'.format(key)
    elif keyword is not None and source==None:
        url = 'https://newsapi.org/v2/top-headlines?country=us&q={}&apiKey={}'.format(keyword,key)
    else:
        url = 'https://newsapi.org/v2/everything?qInTitle={}&sources={}&apiKey={}'.format(keyword,source,key)
    
    r = requests.get(url)
    result = r.json()
    try:
        news = result['articles']

    
    
        children = []
        for i in range(len(news)):
            div = html.Li([
                    html.Div([
                            html.H3(html.A(news[i]['title'], href=news[i]['url'], style={'color':'inherit','outline':'none','text-decoration':'none',
                                           'verticle-align':'baseline','background':'transparent'}),
                                    style={'font-size':'20px','display':'inline','line-height': '2.2rem','margin-bottom':'.8rem'}),
                            
                            html.P(news[i]['description'],style={'display':'block','margin-block-start':'1em','margin-block-end':'1em',
                                   'margin-inline-start':'0px','margin-inline-end':'0px'}),
                            
                            html.A(html.Img(src=news[i]['urlToImage'],style={'position':'relative','width':'120px','height':'80px'}),
                                    href=news[i]['url'])
                              ],
                           style={'padding-top':'40px','width':'700px'}),
                    
                    html.Hr(style={'width':'700px','margin-left':'0px'})
                            ],
                    style={'list-style-type':'none'}
                        )
        
            children.append(div)
    except KeyError:
        children=['No article about {} found on {}'.format(keyword,all_options[source])]
    if len(children)==0:
        try:
            children=['No article about {} found on {}'.format(keyword,all_options[source])]
        except KeyError:
            children=['No article about {} found'.format(keyword)]
        
   
    return children 

    
    

if __name__=='__main__':
    app.run_server(debug=True)
