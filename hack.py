
from hackernews import HackerNews
global titles
titles=dict()
urls=dict()
x=HackerNews()
i=0
for id in x.top_stories(limit=6):
    titles[i]=x.get_item(id).title
    urls[i]=x.get_item(id).url
    i+=1
print(titles[0])
