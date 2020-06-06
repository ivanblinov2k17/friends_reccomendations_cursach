import requests
import json
import time
import networkx
import collections
import re
import numpy as np
import vk

def getFFs(friends):
    cnt = 0
    members = []
    while cnt < friends['count']:
        code = '''
                var friends = ''' + str(friends['items']) + ''';
                var members = [];
                var cnt = 0;
                var requests = '''+str(cnt)+''';
                var ret = [];
                while (cnt<25 && requests<'''+str(friends['count']) + ''') {
                    members = API.friends.get({"user_id": friends[requests]});
                    ret.push(members.items);
                    cnt = cnt+1;
                    requests = requests + 1;
                }
                return ret;'''
        payload = {
                    "code": code,
                    "access_token": ACCESS_TOKEN,
                    "v": '5.103',
        }
        req = requests.post('https://api.vk.com/method/execute', data=payload)
        cnt += 25
        members.append(req.json()['response'])
        time.sleep(0.33)
    ans = []
    for group in members:
        for member in group:
            ans.append(member)
    return ans


def reccomendFriend(start_uid, friends, ffs):
    set_ffs = set()
    #set of friends friends that are not in your friendlist
    for friend_arr in ffs:
        for ff in friend_arr:
            if ff not in set_ffs and ff not in friends:
                set_ffs.add(ff)
    counter = []
    print()
    for ff in set_ffs:
        cnt = 0
        for friend_arr in ffs:
            if ff in friend_arr:
                cnt += 1
        counter.append([ff, cnt])
    print(counter)



token = open('token.txt')
for line in token:
    token = line
ACCESS_TOKEN = token
ACCESS_TOKEN = re.sub('[\t\r\n]', '', ACCESS_TOKEN)
print(ACCESS_TOKEN)

session = vk.Session(access_token=ACCESS_TOKEN)
vk_api = vk.API(session, v='5.103')

start_uid = 247405142
f = 'deactivated,country,city,career,education,occupation,schools'
start_node = vk_api.users.get(user_id=start_uid, fields=f)

lvl_1 = vk_api.friends.get(user_id=start_uid, order='hints')
ffs = getFFs(lvl_1)
reccomendFriend(start_uid, lvl_1, ffs)

# for uid in lvl_1['items']:
#     lvl_2.append(vk_api.friends.get(user_ids=uid, order='hints'))
#     time.sleep(0.33)
# print(lvl_2)

# group_get_members = "https://api.vk.com/method/groups.getMembers?group_id={}&offset={}&v=5.103&access_token={}"
# # id,offset,token
#
# group_get_count = "https://api.vk.com/method/groups.getById?group_id={}&fields=members_count&v=5.103&access_token={}"
# #id, token
#
# # открываем файл с названиями групп, выкачиваем id групп в массив
# group_file = open('programmers.txt', 'r')
# group_list = []
# for line in group_file:
#     group = line.split('/')[3].split('\n')[0].replace(' ', '')
#     if re.fullmatch(r'club\d+', group):
#         group = group[4:]
#     if re.fullmatch(r'public\d+', group):
#         group = group[6:]
#     group_list.append(group)
#
# # получаем количество участников группы
#
#
# def getGroupCount(group_id):
#     json_resp = requests.get(
#         group_get_count.format(group_id, ACCESS_TOKEN)).json()
#     time.sleep(0.33)
#     if json_resp.get('error'):
#         print(json_resp)
#         return 0
#     else:
#         print(json_resp['response'][0]['name'],
#               json_resp['response'][0]['members_count'])
#         return json_resp['response'][0]['members_count']
#
#
# def getAllGroupMembers(group_id):
#     group_count = getGroupCount(group_id)
#     if group_count == 0:
#         return list()
#     offset = 0
#     members = []
#     cnt = 0
#     # while (offset < group_count):
#     #     members = members + requests.get(group_get_members.format(
#     #         group_id, offset, ACCESS_TOKEN)).json()['response']['items']
#     #     offset += 1000
#     #     time.sleep(0.33)
#     while(cnt*25000 < group_count):
#         code = '''
#         var offset = ''' + str(offset) + ''';
#         var group_id= "''' + str(group_id) + '''";
#         var members;
#         var requests = 0;
#         var ret = [];
#         while (requests<25) {
#             members = API.groups.getMembers({"group_id": group_id, "offset": offset, "count": 1000});
#             ret = ret + members.items;
#             requests = requests+1;
#             offset = offset+1000;
#         }
#         return ret;'''
#         payload = {
#             "code": code,
#             "access_token": ACCESS_TOKEN,
#             "v": '5.103',
#         }
#         req = requests.post('https://api.vk.com/method/execute', data=payload)
#         cnt += 1
#         members += req.json()['response']
#         offset += 25000
#         time.sleep(0.33)
#     return members
#
#
# result = open('table.csv', 'a')
#
#
# # проходимся по каждой группе
# for group in group_list:
#
#     members = getAllGroupMembers(group)
#     for member in members:
#         result.write(str(group)+','+str(member)+'\n')
#
# result.close()
