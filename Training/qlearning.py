from Training.State import State
import numpy as np
import random
import time

def q_learn(gamma, alpha_C,N_e):
    # discount factor
    gamma = gamma
    # learning rate, start at 1, decay as O(1/t), t starts as 1
    def alpha(t):
        return alpha_C/(alpha_C+t-1)

    def find_action(qs,ns):
        my_q = np.zeros(3)
        for i in range(3):
            if ns[i] < N_e:
                my_q[i] = 1
            else:
                my_q[i] = qs[i]

        return np.argmax(my_q)


    n = 0

    state = State()
    s = state.discretize_get_index()
    a_t = random.randint(0,2)



    # Q(s,a) (r,stay,l)
    Q = np.zeros((state.total_state_num,3))
    N = np.zeros((state.total_state_num,3))


    start_time = time.time()
    while n<10000:
        # terminal state
        if s == state.total_state_num-1:
            n +=1
            Q[s] = [-1,-1,-1]
            if n%1000 ==0 :
                print(n)
            # start a new trial
            state = State()
            s = state.get_index()


        else:
            # get action
            N[s,a_t] += 1

            # take action change state
            if a_t == 0:
                state.turn_right()
            elif a_t == 2:
                state.turn_left()

            # reward of taking a_t at s
            r_t = state.move_get_rewards()

            # get next state
            s_prime =  state.get_index()

            alph = alpha(N[s,a_t])
            Q[s,a_t] = Q[s,a_t] + alph*(r_t+gamma*max(Q[s_prime])-Q[s,a_t])


            a_t = find_action(Q[s_prime],N[s_prime])
            s = s_prime

    end_time = time.time()
    # print(n,t, diff)
    # print(end_time-start_time)

    print("Training size: "+str(n))

    np.savetxt("Q10.csv", Q, delimiter=",")
    np.savetxt("N10.csv", N, delimiter=",")

q_learn(0.9,20,10)
