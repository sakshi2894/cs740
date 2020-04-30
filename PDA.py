from DataGenerator import generate_data
from Nework import nw_graph


def pda(rls, gre, ce, fl, pm, qrm):
    #Compute B*
    max_gre = -1
    for i in range(len(gre)):
        max_gre = max(max_gre, max(gre[i].values()))
    print (max_gre)

    max_qrm = -1
    for i in range(len(qrm)):
        max_qrm = max(max_qrm, max(qrm[i].values()))
    print (max_qrm)

    b_star = max(max_qrm, max_gre)
    epsilon = 0.001

    chi = b_star/epsilon

    # Initialize all dual values

    lamb = {}
    theta = {}
    pie = []
    n = len(ce.keys()) + len(nw_graph.keys())

    for edge in ce:
        lamb[edge] = 0

    for mbox in pm:
        theta[mbox] = 0

    for flow in fl:
        pie.append(0)

    # Algorithm
    cum_rls = 0
    for i in range(len(fl)):

        # Compute r*

        r_star = rls[i][0]
        k_r = float("inf")
        ind = 0
        rl = 0

        for j in range(cum_rls, cum_rls+len(rls[i])):

            sum_gre = 0
            sum_qrm = 0
            for edge in gre[j]:
                sum_gre = sum_gre + gre[j][edge]*lamb[edge]
            for mbox in qrm[j]:
                sum_qrm = sum_qrm + qrm[j][mbox]*theta[mbox]

            if (sum_gre + sum_qrm) < k_r:
                k_r = sum_gre + sum_qrm
                r_star = rls[i][rl]
                ind = j

            rl = rl + 1

        cum_rls = cum_rls + len(rls[i])
        print("k_r: " + str(k_r))

        if k_r >= 1:
            print("PDA rejected flow " + str(flows[i]))
            pie[i] = 0

        else:
            print("Route flow " + str(i) + " through " + str(r_star))
            pie[i] = fl[i] - (fl[i] * k_r)

            #print("lambda before " + str(lamb))
            #print("theta before " + str(theta))
            for edge in ce:
                if edge in gre[ind]:
                    lamb[edge] = lamb[edge] + lamb[edge]*fl[i]*gre[ind][edge]/ce[edge] + fl[i]*gre[ind][edge]/(n*chi*ce[edge])


            for mbox in pm:
                if mbox in qrm[ind]:
                    theta[mbox] = theta[mbox] + theta[mbox] * fl[i] * qrm[ind][mbox] / pm[mbox] + fl[i] * qrm[ind][
                        mbox] / (n * chi * pm[mbox])

            #print("lambda after " + str(lamb))
            #print("theta after " + str(theta))


if __name__ == '__main__':
    rls, gre, ce, fl, pm, qrm = generate_data()
    print(rls)
    print(gre)
    print(ce)
    print(fl)
    print(pm)
    print(qrm)
    pda(rls, gre, ce, fl, pm, qrm)