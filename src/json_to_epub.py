# pip install GenEpub
# python json_to_epub.py common_data.json

import json
import sys
from collections import OrderedDict 
from GenEpub import gen_epub


fname = sys.argv[1]
j = json.loads(open(fname, encoding='utf8').read())

d = OrderedDict()
for it in j:
    cate = it['school_cate']
    univ = it['university']
    dpmt = it['department']
    sv   = it['supervisor']
    rate = it['rate']
    desc = it['description'] or ''
    desc = '<p>' + desc.replace('<br><br>', '</p><p>') + '</p>'
    d.setdefault(cate, OrderedDict())
    d[cate].setdefault(univ, OrderedDict())
    d[cate][univ].setdefault(dpmt, OrderedDict())
    d[cate][univ][dpmt].setdefault(sv, [])
    d[cate][univ][dpmt][sv].append(f'<p>评分：{rate}</p>{desc}')
    
    
articles = [{
    'title': '导师评价网备份 2020', 
    'content': f'<p>来源：<a href="https://github.com/pengp25/RateMySupervisor">pengp25/RateMySupervisor</a></p>',
}]

for cate, univs in d.items():
    articles.append({'title': f'==={cate}===', 'content': ''})
    for univ, dpmts in univs.items():
        articles.append({'title': univ, 'content': ''})
        for dpmt, svs in dpmts.items():
            parts = []
            for sv, rates in svs.items():
                rates = '<hr/>'.join(rates)
                co = f'''
                    <h2>{sv}</h2>
                    <p>学校：{univ}</p>
                    <p>院系：{dpmt}</p>
                    <hr/>{rates}
                '''
                parts.append(co)
            articles.append({'title': f'{univ} - {dpmt}', 'content': ''.join(parts)})
gen_epub(articles, {})
