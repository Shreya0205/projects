import json
import numpy as np
from urllib.request import urlopen
import difflib


with open('neighbor-districts.json') as f:
  data = json.load(f)
nlist=[]
k=0
for d in data:
    for j in data[d]:
        nlist.append(j)

url="https://api.covid19india.org/v4/data-all.json"
json_url = urlopen(url)

data2 = json.loads(json_url.read())
print("data loaded")
'''
creating list of districts present in covid data.
'''

dislist=[]
for i in data2:
    for j in data2[i]:
        if('districts' in data2[i][j]):
            k=data2[i][j]['districts']
            for p in k:
                dislist.append(p)
len(set(dislist))

'''
Mapping neighbor-data district to covid data district
'''
m={}
dislist=set(dislist)
nlist=set(nlist)
for i in nlist:
    key=i
    i=i[0:i.find('/')]
    i=i[0:i.find('_district')]
    i=i.title()
    if(difflib.get_close_matches(i, dislist)):
        m[key]=difflib.get_close_matches(i, dislist)[0]
m['jyotiba_phule_nagar/Q1891677']='Amroha'
m['sant_ravidas_nagar/Q127533'] = 'Bhadohi'
m['bijapur_district/Q1727570']='Vijayapura'
m['palghat/Q1535742'] = 'Palakkad'
m['faizabad/Q1814132'] =  'Ayodhya'
m['baleshwar/Q2022279']='Balasore'
m['kochbihar/Q2728658']='Cooch Behar'
m['dantewada/Q100211']='Dakshin Bastar Dantewada'
m['debagarh/Q2269639']='Deogarh'
m['hugli/Q548518']='Hooghly'
m['patan/Q1815269']='Patan'
m['ysr/Q15342']='Y.S.R. Kadapa'
m['purbi_singhbhum/Q2452921']='East Singhbhum'
m['purba_champaran/Q49159']='East Champaran'
m['pashchimi_singhbhum/Q1950527']='West Singhbhum'
m['muktsar/Q1947359']='Sri Muktsar Sahib'
m['sahibzada_ajit_singh_nagar/Q2037672']='S.A.S. Nagar'
m['sri_potti_sriramulu_nellore/Q15383']='S.P.S. Nellore'
m['rohtak/Q967388']='Rohtak'
m['badgam/Q2594218']='Budgam'
m['banda/Q2131759']='Banda'
m['baudh/Q2363639']='Boudh'
m['bid/Q814037']='Beed'
m['pashchim_champaran/Q100124']='West Champaran'
m['siang/Q18642331']='Siang'
m['sonapur/Q1473957']='Subarnapur'
m['kheri/Q1755447']='Lakhimpur Kheri'
m['bishnupur/Q938190']='Bankura'
print("Unmapped")
unmapped={'adilabad/Q15211': 'Ahmedabad',
 'baksa/Q2360266': 'Basti',
 'barpeta/Q41249': 'Barmer',
 'bishwanath/Q28110722': 'Kishanganj',
 'bongaigaon/Q42197': 'Kondagaon',
 'cachar/Q42209': 'Saiha',
 'chandel/Q2301769': 'Thane',
 'charaideo/Q24039029': 'Chatra',
 'chirang/Q2574898': 'Chatra',
 'churachandpur/Q2577281': 'Burhanpur',
 'darrang/Q42461': 'Saran',
 'dhemaji/Q42473': 'Dhar',
 'dhubri/Q42485': 'Durg',
 'dibrugarh/Q42479': 'Virudhunagar',
 'goalpara/Q42522': 'Kolar',
 'golaghat/Q42517': 'Balaghat',
 'hailakandi/Q42505': 'Palakkad',
 'hojai/Q24699407': 'Howrah',
 'jagtial/Q28169780': 'Datia',
 'jangaon/Q28170170': 'Jalgaon',
 'jorhat/Q42611': 'Khordha',
 'kakching/Q28173825': 'Kallakurichi',
 'kamareddy/Q27956125': 'Kamle',
 'kamjong/Q28419390': 'Kalimpong',
 'kamrup/Q2247441': 'Karur',
 'karimganj/Q42542': 'Kasganj',
 'karimnagar/Q15373': 'Srinagar',
 'khammam/Q15371': 'Kohima',
 'kokrajhar/Q42618': 'Kolkata',
 'mahabubabad/Q28169761': 'Madhubani',
 'mahabubnagar/Q15380': 'Maharajganj',
 'majuli/Q28110729': 'Mau',
 'marigaon/Q42737': 'Mahisagar',
 'medak/Q15386': 'Malda',
 'mulugu/Q61746006': 'Kullu',
 'nagaon/Q42686': 'Nagaur',
 'nagarkurnool/Q28169773': 'Nagaur',
 'nalbari/Q42779': 'Nandurbar',
 'nalgonda/Q15384': 'Nalanda',
 'narayanpet/Q61746013': 'Narayanpur',
 'nirmal/Q28169750': 'Sirmaur',
 'nizamabad/Q15391': 'Narmada',
 'noklak/Q48731903': 'Wokha',
 'noney/Q28419389': 'Nanded',
 'rangareddy/Q15388': 'Raigad',
 'senapati/Q2301706': 'Sonipat',
 'shahdara/Q83486': 'Sheohar',
 'siddipet/Q28169756': 'Sidhi',
 'sivasagar/Q42768': 'Sivaganga',
 'sonapur/Q1473957': 'Subarnapur',
 'sonitpur/Q42765': 'Sonipat',
 'suryapet/Q28169770': 'Surat',
 'thoubal/Q2086198': 'Mahoba',
 'udalguri/Q321998': 'Udaipur',
 'ukhrul/Q735101': 'Churu',
 'vikarabad/Q28170173': 'Varanasi',
 'wanaparthy/Q28172504': 'Pratapgarh',
 'warangal_rural/Q28169759': 'Nabarangapur',
 'warangal_urban/Q213077': 'Aurangabad',
}

for k in unmapped:
  del m[k]
#Nagaland=[ 'noklak/Q48731903']
m['noklak/Q48731903']='Nagaland'
delhi=['north_delhi/Q693367','north_west_delhi/Q766125','west_delhi/Q549807','new_delhi/Q987','shahdara/Q83486','south_east_delhi/Q25553535','central_delhi/Q107941','east_delhi/Q107960','north_east_delhi/Q429329','south_delhi/Q2061938', 'south_west_delhi/Q2379189']
assam =['west_karbi_anglong/Q24949218','tinsukia/Q42756', 'south_salmara-mankachar/Q24907599','kamrup_metropolitan/Q2464674','east_karbi_anglong/Q42558','dima_hasao_district/Q42774','baksa/Q2360266' ,'barpeta/Q41249', 'bishwanath/Q28110722', 'bongaigaon/Q42197', 'cachar/Q42209', 'charaideo/Q24039029', 'chirang/Q2574898', 'darrang/Q42461', 'dhemaji/Q42473', 'dhubri/Q42485', 'dibrugarh/Q42479', 'goalpara/Q42522', 'golaghat/Q42517', 'hailakandi/Q42505',  'hojai/Q24699407', 'jorhat/Q42611', 'kamrup/Q2247441', 'karimganj/Q42542', 'kokrajhar/Q42618', 'majuli/Q28110729', 'marigaon/Q42737', 'nagaon/Q42686', 'nalbari/Q42779',  'sivasagar/Q42768','sonitpur/Q42765', 'sonapur/Q1473957', 'udalguri/Q321998']
manipur=['tengnoupal/Q28419388','tamenglong/Q2301717','pherzawl/Q28173809','kangpokpi/Q28419386', 'jiribam/Q28419387','chandel/Q2301769','churachandpur/Q2577281',  'kakching/Q28173825', 'kamjong/Q28419390','noney/Q28419389', 'thoubal/Q2086198', 'senapati/Q2301706', 'ukhrul/Q735101','imphal_east/Q1916666','imphal_west/Q1822188','jayashankar_bhupalapally/Q28169775']
telangana=['hyderabad/Q15340', 'yadadri_bhuvanagiri/Q28169764', 'rajanna_sircilla/Q28172781','peddapalli/Q27614797', 'medchal–malkajgiri/Q27614841', 'komram_bheem/Q28170184','bhadradri_kothagudem/Q28169767', 'jogulamba_gadwal/Q27897618','jogulamba_gadwal', 'adilabad/Q15211', 'jagtial/Q28169780', 'jangaon/Q28170170', 'kamareddy/Q27956125', 'karimnagar/Q15373', 'khammam/Q15371', 'mahabubabad/Q28169761', 'mahabubnagar/Q15380', 'medak/Q15386', 'mulugu/Q61746006', 'nagarkurnool/Q28169773', 'nalgonda/Q15384', 'narayanpet/Q61746013',  'nirmal/Q28169750', 'nizamabad/Q15391', 'rangareddy/Q15388', 'siddipet/Q28169756', 'suryapet/Q28169770', 'vikarabad/Q28170173', 'wanaparthy/Q28172504', 'warangal_rural/Q28169759', 'warangal_urban/Q213077']
Mumbai=['konkan_division/Q6268840']
Sikkim=['south_sikkim_district/Q1805051','west_sikkim_district/Q611357','east_sikkim_district/Q1772832','north_sikkim_district/Q1784149']
Goa=['north_goa/Q108234','south_goa/Q108244']

for dis in delhi:
  m[dis]='Delhi' 
for dis in assam:
  m[dis]='Assam' 
for dis in manipur:
  m[dis]='Manipur' 
for dis in telangana:
  m[dis]='Telangana' 
for dis in Sikkim:
  m[dis]='Sikkim'
for dis in Goa:
  m[dis]='Goa' 
for dis in Mumbai:
  m[dis]='Mumbai'
 

newd={}
for d in data:
    tmp=[]
    for i in data[d]:
      tmp.append(m[i])
    if m[d] in newd.keys():
      for p in tmp:      
        newd[m[d]].append(p)

    else:
      newd[m[d]]=tmp

for i in newd:
  newd[i]=set(newd[i])

print(newd)
f={}
for i in newd:
  f[i]=list(newd[i])
#f

with open("out.json", "w") as outfile:  
    json.dump(f, outfile,indent=4) 
