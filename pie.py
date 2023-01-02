from analyzer import df
import matplotlib.pyplot as plt
import polars as pl#
from config import *

# generating pie chart, tailored to specific data

vals = []
colors = []

total = df.select(pl.col("duration").sum())[0,0]

tagGroups = [{"Lernen","Vorbereitung","Nachbereitung"},{"Homework","Übung"},{"Vorlesung"}]

tags = df.filter(pl.col("client") == "Uni").select([
    pl.col('duration'),
    pl.col("tags").arr.first().alias("tag")
]).groupby("tag").agg(pl.sum("duration").cast(pl.Int64))

tagsDict = {item['tag']:item['duration'] for item in tags.to_dicts()}

del tagsDict[None]
for gr in tagGroups:
    val = 0
    colors.append(colormap[next(iter(gr))])
    for t in gr:
        val += tagsDict[t] or 0
        del tagsDict[t]
    vals.append(val)

vals.append(sum(tagsDict.values()))
colors.append(colormap["Uni"])

clients = df.groupby("client").agg(pl.sum("duration").cast(pl.Int64)).sort("duration",reverse=True)

vals.append(clients.filter(pl.col("client") == "Work")[0,"duration"])
colors.append(colormap["Work"])

projects = df.filter((pl.col("client") != "Uni") & (pl.col("client") != "Work")).groupby("project").agg(pl.sum("duration").cast(pl.Int64)).sort("duration",reverse=True)

other = 0
for (prj,val) in projects.iterrows():
    if(prj in colormap):
        vals.append(val)
        colors.append(colormap[prj])
    else:
        print(prj)
        other += val

vals.append(other)
colors.append(colormap['__default'])

plt.figure(figsize=(3,3))
fig = plt.pie(vals,colors=['#'+c for c in colors],autopct=lambda x:'{:.1f}%'.format(x) if x > 3 else '', textprops={'fontsize': 9},radius=3)
plt.savefig('out/pie.png', dpi=300,bbox_inches='tight')