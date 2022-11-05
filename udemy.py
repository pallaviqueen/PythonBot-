import requests
import json
from datetime import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

sender_email = sys.argv[0]
receiver_email = sys.argv[1]
password = sys.argv[2]
print(sender_email,receiver_email,password)
message = MIMEMultipart("alternative")
message["Subject"] = "Udemy free course link"
message["From"] = sender_email
message["To"] = receiver_email


def Sender(category,desp,image,u_link):
    html = """\
    <html>
      <body>
        <h2>Category : <font style='color:#c45edd'>"""+category+"""</font></h2>
        <h3>Name : """+desp+"""</h3>
        <img src='"""+image+"""'>
        <br><p>Link : """+u_link+"""</p>
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
Time = datetime.strptime(file, '%a, %d %b %Y %H:%M:%S')
print(f'Time :- {Time}')
send = 0

for i in data['results'][::-1]:
    if 'category' in i:
        if i['category']: #in ['Development','IT & Software']:
            curr = datetime.strptime(i["sale_start"][:25], '%a, %d %b %Y %H:%M:%S')
            #print(f'Current :- {curr}')
            if (Time < curr):
                print('success')
                Category = i['category']
                Name = i['name']
                Image = i['image']
                if ('https' == i['url'][:5]):
                    Link = i['url']
                else:
                    eLink = i['url']
                    Link = eLink[eLink.index('https'):]
                #Sender(Category,Name,Image,Link)
                send += 1
                print(f'{send} link has been send')
writefile = open('till_time.txt','w').write(i['sale_start'][:25])
print('process completed...')
