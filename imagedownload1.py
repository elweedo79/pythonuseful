import requests
import pandas as pd
import io
from PIL import Image
import pillow_avif

avif = {
    "Accept": "image/avif,image/webp,*/*", #AVIF
}
webp = {
    "Accept": "image/webp,*/*", #WEBP
}
jpeg = {
    "Accept": "image/jpeg,*/*", #JPEG
}

s = requests.Session()
df = pd.read_csv('BATCH 1 Episodic Image URLs.csv')

for index, row in df.iterrows():
    size_jpeg = int(s.head(row["URL"], headers=jpeg).headers['Content-length'])
    print ("Progress:", index, "out of", df[df.columns[0]].count(), ":", int(index/df[df.columns[0]].count()*100), "%")
    if size_jpeg >= 512000: 
        df.at[index,'jpeg'] = size_jpeg
        size_webp = int(s.head(row["URL"], headers=webp).headers['Content-length'])
        size_avif = int(s.head(row["URL"], headers=avif).headers['Content-length'])
        df.at[index,'webp'] = size_webp
        df.at[index,'avif'] = size_avif
        imgrequest = requests.get(row['URL'], headers={})
        imgstring = imgrequest.content # the image as a string
        imgiostream = io.BytesIO(imgstring) # PIL needs a file-like object like io.BytesIO
        img = Image.open(imgiostream)
        width, height = img.size
        df.at[index,'Resolution'] = str(width) + "x" + str(height)
        #df.at[index, 'Type'] = img.format
        print(df.at[index,'URL'], df.at[index,'jpeg'], df.at[index,'Resolution'])
    df.to_excel('images_batch1.xlsx',index=False)