from flask import Blueprint, Flask, Response
import requests
from bs4 import BeautifulSoup

def ss(tbody):
    links = tbody.find_all('a')
    cs = []
    for link in links:
        href = link.get('href')
        if href.startswith('/company'):
            cs.append([href.split("/")[2],'BSE'if href.split("/")[2].isdigit() else 'NSE'])
    return cs
def noofpages(a):
    with open(a, 'r') as f:
        contents = f.read()
    soup = BeautifulSoup(contents, 'html.parser')
    elements = soup.find_all(class_='flex-baseline options')
    p = []
    if len(elements) != 0:
        for element in elements:
            p.append(element.text)
        pag = p[0].split('\n')
        pag = pag[1:-4]
        return pag
    else: 
        return 1

def extract_text(elements):
    text_list = []
    for element in elements:
        text_list.append(element.text.strip())
    text_list.pop(0)
    text_list.pop(-1)
    # text_list.pop(1)
    text_list.pop(1)
    text_list.pop(2)
    return text_list
def extract_all(elements):
    a = list(elements.children)
    if len(a) <34 :
        a.pop(0)
        a.pop(-1)
        a.pop(0)
        t = []
        for i in a:
            t.append(list(i))
        t = [t[i] for i in range(len(t)) if i % 2 != 0]
        output = []
        for i in t:
            output.append(extract_text(i))
        return output
    else:
        a.pop(0)
        a.pop(-1)
        a.pop(0)
        t = []
        for i in a:
            t.append(list(i))
        t = [t[i] for i in range(len(t)) if i % 2 != 0]
        t.pop(15)
        output = []
        for i in t:
            output.append(extract_text(i))
        return output
    
app = Blueprint("app",__name__)

@app.route('/')

def index():
    url = 'https://www.screener.in/screens/1566134/trendx-breakout-setup/'
    response = requests.get(url)
    with open('output.html', 'w') as file:
        file.write(response.text)
    p = noofpages('output.html')
    totalstocks = []
    stocksy = []
    if type(p) is list :
        for i in p:
            l = url+"?page="+i
            response = requests.get(l)
            with open('output.html', 'w') as file:
                file.write(response.text)
            with open('output.html', 'r') as file:
                content = file.read()
            soup = BeautifulSoup(content, 'html.parser')
            tbody = soup.find('tbody')
            totalstocks += extract_all(tbody)
            stocksy += ss(tbody)
    else:
        with open('output.html', 'r') as file:
                content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        tbody = soup.find('tbody')
        totalstocks += extract_all(tbody)
        stocksy += ss(tbody)
    extracted_text = """
            <head>
            <meta http-equiv="refresh" content="180"> 
            <title>Breakout Stocks</title>
            </head>
            <style>
            .header {
                display: flex;
                justify-content: space-between;
                padding: 20px;
                background-color: #f2f2f2; /* Light gray */
            }
            .contact-info {
                position: absolute;
                font-size: 14px;
                line-height: 1.5;
                color: #333;
                text-align: left;
                top: 85px;
                left: 70px;
            }
            body {
                font-family: "Times New Roman", Times, serif;
                background-color: #ADD8E6; /* Light gray */
            }
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            img {
                padding: 9.8px 9.8px 0 0;
            }
            footer {
                
                left: 0;
                bottom: 0;
                width: 100%;
                background-color: #f8f9fa;
                color: black;
                text-align: center;
            }
            </style>
            <header class="header">
            <h1 align="center" >Trendx Institute of Technical Analysis</h1>
            <div class="contact-info">
            <span>Email: TrendxInstitute@gmail.com</span><br>
            <span>Contact: +91 8800-611-235(only whatsapp)</span>
            </div class="contact-info">
            <img src="https://yt3.googleusercontent.com/T3QgXh2XsVBqMbdj8-1Srup3WOZSGihRYC54bTbpUrvnnO5F3c8FLkWj_MFMXZQ-VdrAIhZsMxI=s176-c-k-c0x00ffffff-no-rj" style="position:absolute; top:0; right:0;" height="120" width="120">
            </header>
            <body>
            <h3 >Breakout Stocks</h3>
            <table>
            <tr>
                <th>S.No.</th>
                <th>Name</th>
                <th>Chart</th>
                <th>CMP Rs.</th>
                <th>P/E</th>
                <th>Mar Cap Rs.Cr.</th>
                <th>Div Yld %</th>
                <th>NP Qtr Rs.Cr.</th>
                <th>Qtr Profit Var %</th>
                <th>Sales Qtr Rs.Cr.</th>
                <th>Qtr Sales Var %</th>
                <th>ROCE %</th>
                <th>52w High Rs.</th>
                <th>52w Low Rs.</th>
            </tr>
            """
    for i in range(len(totalstocks)):
        extracted_text += "<tr>"
        for index, text in enumerate(totalstocks[i]):
            if index == 1:
                extracted_text += f"<td><a href='https://web.sensibull.com/futures-options-data?tradingsymbol={stocksy[i][0]}' target='_blank' >{text}</a></td>"
                extracted_text += f"<td><a href='https://web.sensibull.com/chart?tradingSymbol={stocksy[i][0]}' target='_blank' >ChartLink</a></td>"

            else:
                extracted_text += "<td>" + text + "</td>"
        extracted_text += "</tr>"
    extracted_text += """</table>
            </body>
            <footer>
                <p>Copyright © Trendx Institute of Technical Analysis. All rights reserved.</p>
            </footer>
        </html>
            """
    return Response(extracted_text, mimetype='text/html')
