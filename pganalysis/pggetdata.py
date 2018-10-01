import json,time
import heroid as id

sliced_data=['slice1.txt','slice2.txt','slice3.txt','slice4.txt','slice5.txt','slice6.txt','slice7.txt','slice8.txt','slice9.txt','slice10.txt','slice11.txt',]
total_hero_num = 122#with Grimstroke, the length of the list should be 122
stuns_mat=[[] for i in range(total_hero_num)]
pick_count=[0 for i in range(total_hero_num)] #count of the total appearance of the target hero in the sample pool

targethero = 0#change those two variables when you switch heroes
targetdata = 'stuns_per_min'
mark = 1
start_time=time.time()
for i2 in sliced_data:
    with open(i2,'r') as ms:
        for row in ms:
            data = json.loads(row)
            if 'players' in data:
                for i in range(10):
                    if data['players'][i]['radiant_win']==True:
                        if i<=4:
                            mark=1
                        else:
                            mark=0
                    else:#dire win
                        if i<=4:
                            mark=0
                        else:
                            mark=1
                    stuns_mat[data['players'][i]['hero_id']].append([data['players'][i]['benchmarks'][targetdata]['pct'],mark])
                    pick_count[data['players'][i]['hero_id']] += 1


for i in range(total_hero_num):
    print('Hero name:',id.heroes[i]['localized_name'],stuns_mat[i])
    print('Times the hero picked:', pick_count[i])
print("--- %s seconds ---" % (time.time() - start_time))
#1 turn the data into list(maybe you need to break it) (done)
#2 derive data from the list, into a usable dict (done)
#3 record the stuns_per_min data and game results of earthshake in one dict, using the sample matches (done)
#4 do a logistic regression with numpy or sklearn
#5 get and record the win-rate & stuns_per_min correlation in a csv file
