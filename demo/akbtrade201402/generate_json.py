# -*- coding: utf-8 -*-
import json

def main():
    teams = open('teams.txt').readlines()
    nodes = []
    from_teams = []
    to_teams = []
    for i,v in enumerate(teams):
        cells = v.split('\t')
        temp_from = {'id':i,'name':cells[0].strip(),'color':cells[1].strip()}
        temp_to = {'id':i+len(teams),'name':cells[0].strip(),'color':cells[1].strip()}
        nodes.append(temp_from)
        nodes.append(temp_to)
        from_teams.append(temp_from)
        to_teams.append(temp_to)
    print nodes
    trades = open('trades.txt').readlines()
    links = []
    for t in trades:
        cells = t.split('\t')
        for f in from_teams:
            if cells[1].strip() == f['name']:
                source = f['id']
                break
        for tt in to_teams:
            if cells[2].strip() == tt['name']:
                target = tt['id']
                break
        links.append({'name':cells[0].strip(),'source':source,'target':target,'score':int(cells[3].strip())})
    print links
    output = open('akb_trades.json','w')
    output.write(json.dumps({'nodes':nodes,'links':links},ensure_ascii=False))
    output.close()

if __name__ == '__main__':
    main()
    
