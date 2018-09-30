import json,time
import heroid as id

sliced_data=['slice1.txt','slice2.txt','slice3.txt','slice4.txt','slice5.txt','slice6.txt','slice7.txt','slice8.txt','slice9.txt','slice10.txt','slice11.txt',]
total_hero_num = 120#with Grimstroke, the length of the list should be 120
stuns_mat=[[] for i in range(total_hero_num)]

targethero = 7#change those two variables when you switch heroes and features
targetdata = 'stuns_per_min'    #the feature you want
count=0       #count total pieces of data used

start_time=time.time()
for i1 in range(total_hero_num):
    if id.heroes[i1]['id']!=0:
        for i2 in sliced_data:
            with open(i2,'r') as ms:
                targethero=i1
                for row in ms:#row is of string type, read every line, every line is the data of one game
                    data = json.loads(row)#use json to transform row into dict type
                    if 'players' in data:#in case error
                        for i in range(10):
                            if data['players'][i]['hero_id'] == targethero:#find if the target hero is in this match
                                stuns_mat[targethero].append(data['players'][i]['benchmarks'][targetdata]['pct'])
                                count+=1
                                break
                    else:
                        break
for i in range(total_hero_num):
    print('Hero name:',id.heroes[i]['localized_name'],stuns_mat[i])
print("--- %s seconds ---" % (time.time() - start_time))
print(count)
#1 turn the data into list(maybe you need to break it) (done)
#2 derive data from the list, into a usable dict (done)
#3 record the stuns_per_min data and game results of earthshake in one dict, using the sample matches
#4 do a logistic regression with numpy or sklearn
#5 get and record the win-rate & stuns_per_min correlation in a csv file

#data = req.json()  # change response type into a list
    #out = {data['players'][i]['hero_id']: data['players'][i]['benchmarks']['stuns_per_min']['pct'] for i in range(10)}
    #print(out)
    #print(data['players'][8][''])