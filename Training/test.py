from State import *

Q = np.genfromtxt ('Q100k.csv', delimiter=",")

n = 0
ni = 0
total = 0
state = State()
while n<1000:

    ni+=1

    index = state.get_index()
    action = np.argmax(Q[index])

    if action ==0:
        state.turn_right()
    elif action ==2:
        state.turn_left()

    reward = state.move_get_rewards()

    if reward==-1 or ni>1000:
        print(n)
        state = State()
        n += 1
        ni = 0
    elif reward==1:
        total += reward


ave = total/n

print("Testing size: " + str(n))
# print(gamma, alpha_C, N_e)
print("Average scores: "+ str(ave))
print()
