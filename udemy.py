import requests
import json
from datetime import datetime
from dateutil import parser
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

receiver_email = str(os.environ['r_e']).strip('][').split(', ')
print(receiver_email)

def Sender(category,desp,image,u_link):
    for rec_email in receiver_email:
        sender_email = os.environ['s_e']
        password = os.environ['pass']
        message = MIMEMultipart("alternative")
        message["Subject"] = "Udemy free coupon code & course link"
        message["From"] = sender_email
        message["To"] = rec_email
        html = """\
        <html>
          <body>
            <h2>Category : <font style='color:#a200ff'>"""+category+"""</font></h2>
            <h3><font style='color:#a200ff'>Name : </font>"""+desp+"""</h3>
            <img src='"""+image+"""'>
            <button style='border:none;outline:none;height:60px;width:120px;color:#fff;font-size:20px;font-weight:bolder;background:#a200ff;border-radius:5px;margin:0 auto;display:block;'><a style='color:#fff;text-decoration:none;' href='"""+u_link+"""'>Enroll Now</a></button>
          </body>
        </html>
        """

        part2 = MIMEText(html, "html")
        message.attach(part2)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

url = "https://www.real.discount/api-web/all-courses/?store=Udemy&page=1&per_page=10000&orderby=date&free=1&search=&language=English"

response = requests.request("GET", url)
data = json.loads(response.text)

Category = ''
Name = ''
file = open('till_time.txt','r').readline()
Time = parser.parse(str(file))
print(f'Time :- {Time}')
send = 0

for i in data['results'][::-1]:
    if 'category' in i:
        if i['category']: #in ['Development','IT & Software']:
            try:
                curr = datetime.strptime(i["sale_start"][:25], '%a, %d %b %Y %H:%M:%S')
            except:
                curr = parser.parse(str(i["sale_start"][:25]))
            #print(f'Current :- {curr}')
            if (Time < curr):
                Category = i['category']
                Name = i['name']
                Image = i['image']
                if ('https' == i['url'][:5]):
                    Link = i['url']
                else:
                    eLink = i['url']
                    Link = eLink[eLink.index('https'):]
                Sender(Category,Name,Image,Link)
                send += 1
                print(f'{send} link has been send')
writefile = open('till_time.txt','w').write(i['sale_start'][:25])
print('process completed...')
