import requests
import pandas as pd
import json
from difflib import SequenceMatcher

with open('data-all.json') as json_data:
    data = json.load(json_data)

remove = ["Khawzawl","Tirupathur","Saitual","Ranipet","Tenkasi","Yanam","Tenkasi","Hnahthial","Dibang Valley","Gaurela Pendra Marwahi","CAPF Personnel","Chengalpattu","Evacuees","Other State","Other Region","Others","Unknown","Italians","Airport Quarantine","BSF Camp","Foreign Evacuees","Railway Quarantine"]


districts=list()
for key in data.keys():
    for key2 in data[key]:
        try:
            for district in data[key][key2]['districts'].keys():
                if district not in remove:
                    districts.append(district+"_"+key2)
        except:
            z=0

covid_web_district = list(set(districts))
covid_web_district.sort()

with open('neighbor-districts.json') as json_data:
    graph = json.load(json_data)


dist_file = list(graph.keys())
dist_file_repeated = list()
for district in dist_file:
    dist_file_repeated.append(district)
    
dist_file.sort()


mapping = dict()

for district in dist_file:
    score = 0
    for web_district in covid_web_district:
        temp = SequenceMatcher(None, district.split('/')[0], web_district.split('_')[0].lower()).ratio()
        if temp>score:
            score = temp
            correct_city = web_district
    
    mapping[district] = correct_city
    


to_be_remove = {
'adilabad/Q15211': 'Nadia_WB',
'baksa/Q2360266': 'Banka_BR',
'barpeta/Q41249': 'Bametara_CT',
'bhadradri_kothagudem/Q28169767': 'Bhadrak_OR',
'bishwanath/Q28110722': 'Kishanganj_BR',
'bongaigaon/Q42197': 'Kondagaon_CT',
'cachar/Q42209': 'Chatra_JH',
'chandel/Q2301769': 'Chandauli_UP',
'charaideo/Q24039029': 'Chatra_JH',
'chirang/Q2574898': 'Chitradurga_KA',
'churachandpur/Q2577281': 'Burhanpur_MP',
'darrang/Q42461': 'Darbhanga_BR',
'dhemaji/Q42473': 'Dhamtari_CT',
'dhubri/Q42485': 'Madhubani_BR',
'dibrugarh/Q42479': 'Bargarh_OR',
'dima_hasao_district/Q42774': 'Mahasamund_CT',
'east_sikkim_district/Q1772832': 'East Khasi Hills_ML',
'goalpara/Q42522': 'Alwar_RJ',
'golaghat/Q42517': 'Balaghat_MP',
'hailakandi/Q42505': 'Kalahandi_OR',
'hojai/Q24699407': 'Khowai_TR',
'hyderabad/Q15340': 'Ahmedabad_GJ',
'imphal_east/Q1916666': 'Sipahijala_TR',
'imphal_west/Q1822188': 'Champawat_UT',
'jagtial/Q28169780': 'Patiala_PB',
'jangaon/Q28170170': 'Jalgaon_MH',
'jayashankar_bhupalapally/Q28169775': 'Chikkaballapura_KA',
'jiribam/Q28419387': 'Birbhum_WB',
'jogulamba_gadwal/Q27897618': 'Jamnagar_GJ',
'jorhat/Q42611': 'Khordha_OR',
'kakching/Q28173825': 'Mokokchung_NL',
'kamareddy/Q27956125': 'Kamle_AR',
'kamjong/Q28419390': 'Kalimpong_WB',
'kamrup/Q2247441': 'Karur_TN',
'kamrup_metropolitan/Q2464674': 'Amreli_GJ',
'kangpokpi/Q28419386': 'Katni_MP',
'karimganj/Q42542': 'Kasganj_UP',
'karimnagar/Q15373': 'Jamnagar_GJ',
'kokrajhar/Q42618': 'Katihar_BR',
'komram_bheem/Q28170184': 'Mahe_PY',
'konkan_division/Q6268840': 'Kondagaon_CT',
'mahabubabad/Q28169761': 'Ahmedabad_GJ',
'mahabubnagar/Q15380': 'Bhavnagar_GJ',
'majuli/Q28110729': 'Mau_UP',
#'mancherial_district/Q28169747': 'Chengalpattu_TN',
'marigaon/Q42737': 'Umaria_MP',
'medak/Q15386': 'Kheda_GJ',
'medchal–malkajgiri/Q27614841': 'Malkangiri_OR',
'muktsar/Q1947359': 'Amritsar_PB',
'mulugu/Q61746006': 'Kullu_HP',
'nagaon/Q42686': 'Kondagaon_CT',
'nalbari/Q42779': 'Ballari_KA',
'nalgonda/Q15384': 'Nalanda_BR',
'narayanpet/Q61746013': 'Narayanpur_CT',
'nirmal/Q28169750': 'Narmada_GJ',
'nizamabad/Q15391': 'Ahmedabad_GJ',
'noklak/Q48731903': 'Akola_MH',
'noney/Q28419389': 'Indore_MP',
'north_east_delhi/Q429329': 'North Garo Hills_ML',
'north_goa/Q108234': 'North Garo Hills_ML',
'north_sikkim_district/Q1784149': 'North Tripura_TR',
'north_west_delhi/Q766125': 'South West Garo Hills_ML',
'pherzawl/Q28173809': 'Khawzawl_MZ',
'rajanna_sircilla/Q28172781': 'Ratnagiri_MH',
'rangareddy/Q15388': 'Raigad_MH',
#'sangareddy/Q28169753': 'Sagar_MP',
'shahdara/Q83486': 'Bhandara_MH',
'sivasagar/Q42768': 'Sagar_MP',
'sonitpur/Q42765': 'Sitapur_UP',
'south_east_delhi/Q25553535': 'South West Garo Hills_ML',
'south_goa/Q108244': 'South Garo Hills_ML',
'south_salmara-mankachar/Q24907599': 'Chamarajanagara_KA',
'south_sikkim_district/Q1805051': 'South Tripura_TR',
'suryapet/Q28169770': 'Surat_GJ',
'tamenglong/Q2301717': 'Changlang_AR',
'tengnoupal/Q28419388': 'Angul_OR',
'thoubal/Q2086198': 'Bhopal_MP',
'udalguri/Q321998': 'Jalpaiguri_WB',
'ukhrul/Q735101': 'Karauli_RJ',
'vikarabad/Q28170173': 'Faridabad_HR',
'wanaparthy/Q28172504': 'Pratapgarh_RJ',
'warangal_rural/Q28169759': 'Bengaluru Rural_KA',
'warangal_urban/Q213077': 'Aurangabad_BR',
'west_sikkim_district/Q611357': 'West Khasi Hills_ML',
'yadadri_bhuvanagiri/Q28169764': 'Krishnagiri_TN'}

for i in to_be_remove:
    del mapping[i]


mapping['aurangabad/Q43086']= 'Aurangabad_BR'
mapping['aurangabad/Q592942']= 'Aurangabad_MH'
mapping['baleshwar/Q2022279']='Balasore_OR'
mapping['balrampur/Q16056268']= 'Balrampur_CT'
mapping['balrampur/Q1948380']= 'Balrampur_UP'
mapping['bid/Q814037'] = 'Beed_MH'
mapping['bidar_district/Q1790568'] = 'Bidar_KA'
mapping['bijapur_district/Q1727570'] = 'Vijayapura_KA'
mapping['bilaspur/Q100157']='Bilaspur_CT'
mapping['bilaspur/Q1478939']= 'Bilaspur_HP'
mapping['bishnupur/Q938190']='Bankura_WB'
mapping['botad_district/Q14505072'] = 'Botad_GJ'
mapping['dantewada/Q100211'] = 'Dakshin Bastar Dantewada_CT'
mapping['debagarh/Q2269639']='Deogarh_OR'
mapping['faizabad/Q1814132'] = 'Ayodhya_UP'
mapping['east_karbi_anglong/Q42558']='Karbi Anglong_AS'
mapping['hamirpur/Q2019757']= 'Hamirpur_UP'
mapping['hamirpur/Q2086180']= 'Hamirpur_HP'
mapping['hugli/Q548518'] = 'Hooghly_WB'
mapping['jyotiba_phule_nagar/Q1891677'] = 'Amroha_UP'
mapping['kheri/Q1755447']='Lakhimpur Kheri_UP'
mapping['leh_district/Q1921210'] = 'Leh_LA'
mapping['mahe_district/Q639279'] = 'Mahe_PY'
mapping['mahesana_district/Q2019694']='Mehsana_GJ'
mapping['muktsar/Q1947359']='Sri Muktsar Sahib_PB'
mapping['palghat/Q1535742']='Palakkad_KL'
mapping['pashchim_champaran/Q100124']='West Champaran_BR'
mapping['pashchimi_singhbhum/Q1950527']='West Singhbhum_JH'
mapping['pratapgarh/Q1473962']= 'Pratapgarh_UP'
mapping['pratapgarh/Q1585433']= 'Pratapgarh_RJ'
mapping['rae_bareilly/Q1321157']='Rae Bareli_UP'
mapping['sahibzada_ajit_singh_nagar/Q2037672']='S.A.S. Nagar_PB'
mapping['sant_ravidas_nagar/Q127533']='Bhadohi_UP'
mapping['sonapur/Q1473957']='Subarnapur_OR'
mapping['ysr/Q15342']='Y.S.R. Kadapa_AP'
mapping['noklak/Q48731903']='Tuensang_NL'


Mumbai=['konkan_division/Q6268840']
for district in Mumbai:
    mapping[district]='Mumbai_MH'
    
Goa=['north_goa/Q108234','south_goa/Q108244']
for district in Goa:
    mapping[district]='Goa_GA' 

delhi=['north_delhi/Q693367','north_west_delhi/Q766125','west_delhi/Q549807','new_delhi/Q987','shahdara/Q83486','south_east_delhi/Q25553535','central_delhi/Q107941','east_delhi/Q107960','north_east_delhi/Q429329','south_delhi/Q2061938', 'south_west_delhi/Q2379189']
for district in delhi:
    mapping[district]='Delhi_DL' 



Telangana=['adilabad/Q15211',  'bhadradri_kothagudem/Q28169767',  'hyderabad/Q15340',  'jagtial/Q28169780',  'jangaon/Q28170170',  'jogulamba_gadwal/Q27897618',  'kamareddy/Q27956125',  'karimnagar/Q15373',  'khammam/Q15371',  'komram_bheem/Q28170184',  'mahabubabad/Q28169761',  'mahabubnagar/Q15380',  'mancherial_district/Q28169747',  'medak/Q15386',  'medchal–malkajgiri/Q27614841',  'mulugu/Q61746006',  'nagarkurnool/Q28169773',  'nalgonda/Q15384',  'narayanpet/Q61746013',  'nirmal/Q28169750',  'nizamabad/Q15391',  'peddapalli/Q27614797',  'rajanna_sircilla/Q28172781',  'rangareddy/Q15388',  'sangareddy/Q28169753',  'siddipet/Q28169756',  'suryapet/Q28169770',  'vikarabad/Q28170173',  'wanaparthy/Q28172504',  'warangal_rural/Q28169759',  'warangal_urban/Q213077',  'yadadri_bhuvanagiri/Q28169764']
Sikkim=['east_sikkim_district/Q1772832',  'north_sikkim_district/Q1784149',  'south_sikkim_district/Q1805051',  'west_sikkim_district/Q611357']
Assam=['baksa/Q2360266',  'barpeta/Q41249',  'bishwanath/Q28110722',  'bongaigaon/Q42197',  'cachar/Q42209',  'charaideo/Q24039029',  'chirang/Q2574898',  'darrang/Q42461',  'dhemaji/Q42473',  'dhubri/Q42485',  'dibrugarh/Q42479',  'dima_hasao_district/Q42774',  'east_karbi_anglong/Q42558',  'goalpara/Q42522',  'golaghat/Q42517',  'hailakandi/Q42505',  'hojai/Q24699407',  'jorhat/Q42611',  'kamrup/Q2247441',  'kamrup_metropolitan/Q2464674',  'karimganj/Q42542',  'kokrajhar/Q42618',  'majuli/Q28110729',  'marigaon/Q42737',  'nagaon/Q42686',  'nalbari/Q42779',  'sivasagar/Q42768', 'sonitpur/Q42765',  'south_salmara-mankachar/Q24907599',  'tinsukia/Q42756',  'udalguri/Q321998',  'west_karbi_anglong/Q24949218']
Manipur=['chandel/Q2301769', 'churachandpur/Q2577281', 'imphal_east/Q1916666', 'imphal_west/Q1822188', 'jayashankar_bhupalapally/Q28169775', 'jiribam/Q28419387', 'kakching/Q28173825', 'kamjong/Q28419390', 'kangpokpi/Q28419386', 'noney/Q28419389', 'pherzawl/Q28173809', 'senapati/Q2301706', 'tamenglong/Q2301717', 'tengnoupal/Q28419388', 'thoubal/Q2086198', 'ukhrul/Q735101']

for district in Sikkim:
    mapping[district]='Sikkim_SK'

for district in Assam:
    mapping[district]='Assam_AS' 

for district in Telangana:
    mapping[district]='Telangana_TN' 

for district in Manipur:
    mapping[district]='Manipur_MN' 


final_dict=dict()
for key in graph.keys():
        try:
            if mapping[key] not in final_dict.keys():
                final_dict[mapping[key]]=set()

            for key_value in graph[key]:
                try:
                    final_dict[mapping[key]].add(mapping[key_value])
                except:
                    print(key_value)
        except:
            print(key)


for key in final_dict:
    final_dict[key]=list(final_dict[key])

with open("neighbor-districts-modified.json", "w") as f:  
    json.dump(final_dict,f,indent=4) 

dist_list=[]
for key in final_dict:
    dist_list.extend(final_dict[key])

dist_list=list(set(dist_list))
dist_list.sort()

j=101
dist_dict={}

for i in dist_list:
    dist_dict[i]=j
    j=j+1
    
with open("mapping.json", "w") as f:  
       json.dump(dist_dict,f,indent=4) 

print("New modified neighbor file generated")
