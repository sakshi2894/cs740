import numpy as np
from scipy.optimize import linprog
from DataGenerator import generate_data


def simplex(rls, gre, ce, fl, pm, qrm, fl_e):
    c = []
    num_rls = 0
    rls_arr = []

    A = []
    b = []

    # Optimization function
    for i in range(len(rls)):
        f = fl_e[i]
        rl_count = 0
        for j in rls[i]:
            c.append(f * -1)
            num_rls = num_rls + 1
            rl_count = rl_count + 1
        rls_arr.append(rl_count)
    constants = np.array(c)

    # Equation 1
    cum_rls = 0
    for i in range(len(fl)):
        arr = [0] * num_rls
        for j in range(cum_rls, cum_rls + rls_arr[i]):
            arr[j] = 1
        cum_rls = cum_rls + rls_arr[i]
        A.append(arr)
        b.append(1)

    # Equation 2
    for key in ce:
        cum_rls = 0
        arr = [0] * num_rls
        for i in range(len(fl)):
            for j in range(cum_rls, cum_rls + rls_arr[i]):
                if key in gre[j]:
                    arr[j] = fl[i] * gre[j][key]
            cum_rls = cum_rls + rls_arr[i]
        A.append(arr)
        b.append(ce[key])

    # Equation 4
    for key in pm:
        cum_rls = 0
        arr = [0] * num_rls
        for i in range(len(fl)):
            for j in range(cum_rls, cum_rls + rls_arr[i]):
                if key in qrm[j]:
                    arr[j] = fl[i] * qrm[j][key]
            cum_rls = cum_rls + rls_arr[i]
        A.append(arr)
        b.append(pm[key])

    # Equation 5
    iterator = 0
    for i in range(len(rls)):
        for j in rls[i]:
            arr = [0] * num_rls
            arr[iterator] = -1
            iterator = iterator + 1
            A.append(arr)
            b.append(0)

    res = linprog(constants, A_ub=np.array(A), b_ub=np.array(b), bounds=(0, None), method='interior-point')
    print('Optimal value:', res.fun, '\nX:', res.x)


if __name__ == '__main__':
    rls, gre, ce, fl, pm, qrm, fl_e,fl_pm = generate_data()


    #print("rls: " + str(rls))
    #print(gre)
    #print(ce)
    #print(fl)
    #print(pm)
    #print(qrm)
    #print("fl_e" + str(fl_e))

    simplex(rls, gre, ce, fl, pm, qrm, fl_e)

    sum = 0
    for i in range(0, len(fl_e)):
        sum  = sum + fl_e[i]
    print("Maximum Throughput: " + str(sum))
