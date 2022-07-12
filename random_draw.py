import sys
import random
import numpy as np
import time
RANDOM_SEED = int(time.time()*1000%1000000)

teams_per_group = 4

class RandomDraw:
    def __init__(self,_all,_static,RANDOM_SEED=None):
        self.rand = random.Random(RANDOM_SEED)
        self.teams = {}
        
        self.teams_static = {}
        self.teams_random_num = []
        self.teams_random_draw = []

        self.teams_res = {}
        self.res = {}
        self._read_teams(_all,_static)
        while True:
            self.random()
            res = self.check_valid()
            if res:
                break
    def print_res(self):
        for group in range(len(self.teams) // teams_per_group):
            groups = {}
            for i in range(teams_per_group):
                ind = group*teams_per_group+i
                if ind not in self.res:
                    print('Err33333333333')
                groups[i] = self.res[ind]+" "+self.teams[self.res[ind]][1]
            g = chr(ord('A')+group)
            print("组别",g)
            for n in groups:
                print('\t',g+str(n),groups[n])

    def check_valid(self):
        for group in range(len(self.teams) // teams_per_group):
            groups = {}
            univset = set()
            for i in range(teams_per_group):
                ind = group*teams_per_group+i
                if ind not in self.res:
                    print('Err33333333333')
                groups[i] = self.res[ind]
                univset.add(self.teams[self.res[ind]][0])
            if len(univset) != teams_per_group:
                return False
        return True



    def random(self):
        self.teams_res = {}
        self.res = {}
        self.teams_random_draw = list(range(len(self.teams)))
        for num in self.teams_static:
            draw = self.teams_static[num]
            if draw not in self.teams_random_draw:
                print("Error11111")
            self.teams_random_draw.remove(draw)
        assert(len(self.teams_random_draw)==len(self.teams_random_num))
        self.rand.shuffle(self.teams_random_draw)
        self.teams_res.update(self.teams_static)
        self.teams_res.update(dict(zip(self.teams_random_num,self.teams_random_draw)))
        self.res = dict((v,k) for k,v in self.teams_res.items())
    def _read_teams(self,_all,_static):
        with open(_static) as f:
            lines = f.readlines()
            for l in lines:
                info = l.split('\t')
                num = info[0]
                static_draw_temp = info[-1]
                static_draw_group = ord(static_draw_temp[0])-ord('A')
                static_draw_group_num = int(static_draw_temp[1])-1
                static_draw = static_draw_group*teams_per_group+static_draw_group_num
                if num in self.teams_static:
                    print("num {} exist more than once. !!!!!!!!!!".format(num))
                self.teams_static[num] = static_draw
        with open(_all) as f:
            lines = f.readlines()
            for l in lines:
                info = l.split('\t')
                if len(info) != 4:
                    print("error occur skip! ",info)
                num = info[0]
                name = (info[3]+"-"+info[1]).replace('\n','')
                univ = info[3]
                if num in self.teams:
                    print("num {} exist more than once. !!!!!!!!!!".format(num))
                self.teams[num] = [univ,name]
                if num not in self.teams_static:
                    self.teams_random_num.append(num)
            print("total nums of team : {}".format(len(self.teams)))

def test_random(seed):
    rand = random.Random(seed)
    x = list(range(5))
    print(x)
    for i in range(4):
        rand.shuffle(x)
        print(x)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        t_name = "teams_example.txt"
        t_static_name = "teams_static_example.txt"
    else:
        t_name = sys.argv[1]
        t_static_name = sys.argv[2]
    
    print("seed : ",RANDOM_SEED)
    draw = RandomDraw(t_name,t_static_name,RANDOM_SEED)
    draw.print_res()
