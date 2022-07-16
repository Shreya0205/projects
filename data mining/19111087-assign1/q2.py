import requests
import pandas as pd
import json
import datetime

#data = requests.get('https://api.covid19india.org/v4/data-all.json').json()
#df = pd.DataFrame(requests.get('https://api.covid19india.org/v4/data-all.json',verify=False).json())

with open('data-all.json') as json_data:
    data = json.load(json_data)

with open('mapping.json') as json_data:
    mapping = json.load(json_data)

date_list=['2020-03-15', '2020-03-16', '2020-03-17', '2020-03-18', '2020-03-19', '2020-03-20', '2020-03-21', '2020-03-22', '2020-03-23', '2020-03-24', '2020-03-25', '2020-03-26', '2020-03-27', '2020-03-28', '2020-03-29', '2020-03-30', '2020-03-31', '2020-04-01', '2020-04-02', '2020-04-03', '2020-04-04', '2020-04-05', '2020-04-06', '2020-04-07', '2020-04-08', '2020-04-09', '2020-04-10', '2020-04-11', '2020-04-12', '2020-04-13', '2020-04-14', '2020-04-15', '2020-04-16', '2020-04-17', '2020-04-18', '2020-04-19', '2020-04-20', '2020-04-21', '2020-04-22', '2020-04-23', '2020-04-24', '2020-04-25', '2020-04-26', '2020-04-27', '2020-04-28', '2020-04-29', '2020-04-30', '2020-05-01', '2020-05-02', '2020-05-03', '2020-05-04', '2020-05-05', '2020-05-06', '2020-05-07', '2020-05-08', '2020-05-09', '2020-05-10', '2020-05-11', '2020-05-12', '2020-05-13', '2020-05-14', '2020-05-15', '2020-05-16', '2020-05-17', '2020-05-18', '2020-05-19', '2020-05-20', '2020-05-21', '2020-05-22', '2020-05-23', '2020-05-24', '2020-05-25', '2020-05-26', '2020-05-27', '2020-05-28', '2020-05-29', '2020-05-30', '2020-05-31', '2020-06-01', '2020-06-02', '2020-06-03', '2020-06-04', '2020-06-05', '2020-06-06', '2020-06-07', '2020-06-08', '2020-06-09', '2020-06-10', '2020-06-11', '2020-06-12', '2020-06-13', '2020-06-14', '2020-06-15', '2020-06-16', '2020-06-17', '2020-06-18', '2020-06-19', '2020-06-20', '2020-06-21', '2020-06-22', '2020-06-23', '2020-06-24', '2020-06-25', '2020-06-26', '2020-06-27', '2020-06-28', '2020-06-29', '2020-06-30', '2020-07-01', '2020-07-02', '2020-07-03', '2020-07-04', '2020-07-05', '2020-07-06', '2020-07-07', '2020-07-08', '2020-07-09', '2020-07-10', '2020-07-11', '2020-07-12', '2020-07-13', '2020-07-14', '2020-07-15', '2020-07-16', '2020-07-17', '2020-07-18', '2020-07-19', '2020-07-20', '2020-07-21', '2020-07-22', '2020-07-23', '2020-07-24', '2020-07-25', '2020-07-26', '2020-07-27', '2020-07-28', '2020-07-29', '2020-07-30', '2020-07-31', '2020-08-01', '2020-08-02', '2020-08-03', '2020-08-04', '2020-08-05', '2020-08-06', '2020-08-07', '2020-08-08', '2020-08-09', '2020-08-10', '2020-08-11', '2020-08-12', '2020-08-13', '2020-08-14', '2020-08-15', '2020-08-16', '2020-08-17', '2020-08-18', '2020-08-19', '2020-08-20', '2020-08-21', '2020-08-22', '2020-08-23', '2020-08-24', '2020-08-25', '2020-08-26', '2020-08-27', '2020-08-28', '2020-08-29', '2020-08-30', '2020-08-31', '2020-09-01', '2020-09-02', '2020-09-03', '2020-09-04', '2020-09-05']


dist_name_list=mapping.keys()
dist_list = mapping.values()

df = pd.DataFrame(columns=date_list, index=dist_list)

remove = ["Khawzawl","Tirupathur","Saitual","Ranipet","Tenkasi","Yanam","Tenkasi","Hnahthial","Dibang Valley","Gaurela Pendra Marwahi","CAPF Personnel","Chengalpattu","Evacuees","Other State","Other Region","Others","Unknown","Italians","Airport Quarantine","BSF Camp","Foreign Evacuees","Railway Quarantine"]


## Handling separately those states which are merged

states_list = ['AS','GA','MN','SK','TG']
state_map=dict()
state_map['AS']="Assam_AS"
state_map['GA']="Goa_GA"
state_map['MN']="Manipur_MN"
state_map['SK']="Sikkim_SK"
state_map['TG']="Telangana_TN"

districts=list()
st=set()
count=0
present=0


## Inserting cases into dataframe with column values as date and row values as district indexes
for date in date_list:
    for state in data[date]:
        
        if state in states_list:
            #print(state)
            idx = mapping[state_map[state]]
            if "delta" in data[date][state].keys():
                if "confirmed" in data[date][state]['delta']:
                    df[date][idx] = data[date][state]['delta']['confirmed']
                    count+=data[date][state]['delta']['confirmed']
                    
        #print(state)
        if "districts" in data[date][state].keys():
            for district in data[date][state]['districts'].keys():
                if district not in remove:
                    dist_name=district+"_"+state
                    try:
                        idx = mapping[dist_name]
                        if "delta" in data[date][state]['districts'][district].keys():
                            present=1
                            if "confirmed" in data[date][state]['districts'][district]['delta'].keys():
                                df[date][idx] = data[date][state]['districts'][district]['delta']['confirmed']
                                count+=data[date][state]['districts'][district]['delta']['confirmed']
                                
                    except:
                        print(dist_name)
                        pass
                        
        
                                 

df=df.fillna(0)

week_list=set()

## getting the week number from the date
for i in date_list:
    i=i.split("-")
    x = datetime.datetime(int(i[0]),int(i[1][1]),int(i[2]))
    week_list.add(x.strftime("%U"))

week_list = list(week_list)
week_list.sort()
min_week_num=min(week_list)

newList = [int(x) - int(min_week_num)+1 for x in week_list]
week_list = newList


## week_dict have district ids as keys and their weekly cases as values
week_dict = {}
for idx in df.index.values:
    week_dict[idx] = {}
    for week_num in week_list:
        week_dict[idx][week_num] = 0

for idx in dist_list:
    for date in date_list:
        i=date
        i=i.split("-")
        x = datetime.datetime(int(i[0]),int(i[1][1]),int(i[2]))
        week_num = int(x.strftime("%U"))-int(min_week_num)+1
        
        week_dict[idx][week_num]+=df[date][idx]


## storing values in cases-week.csv
f=open('cases-week.csv','a')

for idx in week_dict.keys():
    for week in week_dict[idx]:
        f.write(str(idx)+","+str(week)+","+str(week_dict[idx][week])+"\n")
                
f.close()

month_map=dict()
month_map['03']=1
month_map['04']=2
month_map['05']=3
month_map['06']=4
month_map['07']=5
month_map['08']=6
month_map['09']=7
month_list = month_map.keys()


## month_dict have district ids as keys and their monthly cases as values
month_dict = {}
for idx in df.index.values:
    month_dict[idx] = {}
    for month_num in month_list:
        month_dict[idx][month_map[month_num]] = 0

for idx in dist_list:
    for date in date_list:
        i=month_map[date.split("-")[1]]
        month_dict[idx][i]+=df[date][idx]


## storing values in cases-month.csv
f=open('cases-month.csv','a')

for idx in month_dict.keys():
    for month in month_dict[idx]:
        f.write(str(idx)+","+str(month)+","+str(month_dict[idx][month])+"\n")
                
f.close()


## overall_dict have district ids as keys and their overall cases as values
overall_dict = {}
for idx in df.index.values:
    overall_dict[idx] = 0

for idx in dist_list:
    for date in date_list:
        overall_dict[idx]+=df[date][idx]

## storing values in cases-overall.csv
f=open('cases-overall.csv','a')

for idx in overall_dict.keys():
    f.write(str(idx)+",1,"+str(overall_dict[idx])+"\n")
                
f.close()

print("Cases file generated")


