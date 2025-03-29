import urllib.request
import datetime
import os

os.makedirs("downloads")

def download(n):
    time = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    url = f"https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={n}&year1=1981&year2=2025&type=Mean"
    vhi_url = urllib.request.urlopen(url)
    
    out_path = os.path.join("downloads", f"vhi_id_{n}_{time}.csv")
    with open(out_path, 'wb') as out:
        out.write(vhi_url.read()) 
    print(f"VHI for provinceID={n} is downloaded to {out_path}...")

for i in range(1, 28):
    download(i)