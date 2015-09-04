# MH sampler for the correlation model described in the Cognition cheat sheet titled "Metropolis-Hastings sampling."
# Written by Ilker Yildirim, September 2012.
import matplotlib.pyplot as plt
import numpy
import sqlite3
import pandas
from numpy import log,exp
from scipy.special import beta,gamma as g

def acceptP(lambda_all,adv,x,p):
    return sum(log(beta(lambda_all*adv,1)*(p**(-1.+x+lambda_all*adv))*((1.-p)**(1.-x))))
def acceptF(lambda_all,adv,p):
    return sum(log(g(1.+adv*lambda_all)/g(adv*lambda_all)*(p**(lambda_all*adv))))

# Retrieve data
conn = sqlite3.connect("mlb.db")
data = pandas.read_sql("""SELECT game.HOMETEAM,game.AWAYTEAM,game.DATE,game.HOMEWON as homewon,homeba/awayba as gamma,awayera/homeera as alpha,
homewinperc/awaywinperc as theta from game
left join BARatio as BA on game.GameKey = BA.gameKey
left join EARatio as EA on game.GameKey = EA.gameKey
left join WinRatio as WIN on game.GameKey = WIN.gameKey
where game.date>'20140409' and game.date<'20140801'""",conn)


data = data[['alpha','theta','gamma','homewon']]
alpha = data['alpha']
theta = data['theta']
gamma = data['gamma']
x = data['homewon']
#Sampler parameters
E=150
burn_in = 0
#intiate parameters
r1=numpy.random.uniform(2,3)
r2=numpy.random.uniform(2,3)
r3=numpy.random.uniform(2,3)
adv=numpy.random.uniform(1,1.5)
#Store Samples
chain_r1=numpy.array([0.]*(E-burn_in))
chain_r2=numpy.array([0.]*(E-burn_in))
chain_r3=numpy.array([0.]*(E-burn_in))
chain_adv=numpy.array([0.]*(E-burn_in))
#Starts @ 20140801 Arizona vs Pittsburgh
alpha_t = 0.886
gamma_t = 1
theta_t = 0.833
lamda_t = alpha_t**r1*theta_t**r2*gamma_t**r3
chain_p=numpy.array([0.]*(E-burn_in))
p = numpy.random.beta(lamda_t*adv,1)
#Sample p
for e in range(E):
    print "At iteration "+str(e)
    lambda_all = alpha**r1*theta**r2*gamma**r3
    #Sample p
    p_candi = numpy.random.beta(lamda_t*adv,1)
    #Accept Function
    accept = acceptP(lambda_all,adv,x,p_candi)
    accept = accept - acceptP(lambda_all,adv,x,p)
    accept=min([0,accept])
    accept=exp(accept)

    # Accept rho_candidate with probability accept.
    if numpy.random.uniform(0,1)<accept:
        p = p_candi
    else:
        p = p
    #store
    if e>=burn_in:
        chain_p[e-burn_in]=p
    #Sample r1
    r1_candi = numpy.random.uniform(0,2)
    lambda_candi = alpha**r1_candi*theta**r2*gamma**r3
    #Accept Function
    accept = acceptF(lambda_candi,adv,p)
    accept = accept - acceptF(lambda_all,adv,p)
    accept=min([0,accept])
    accept=exp(accept)
    # Accept rho_candidate with probability accept.
    if numpy.random.uniform(0,1)<accept:
        r1 = r1_candi
        lambda_all = lambda_candi
    else:
        r1 = r1
    #store
    if e>=burn_in:
        chain_r1[e-burn_in]=r1
    #Sample r2
    r2_candi = numpy.random.uniform(0,2)
    lambda_candi = alpha**r1*theta**r2_candi*gamma**r3
    #Accept Function
    accept = acceptF(lambda_candi,adv,p)
    accept = accept - acceptF(lambda_all,adv,p)
    accept=min([0,accept])
    accept=exp(accept)
    # Accept rho_candidate with probability accept.
    if numpy.random.uniform(0,1)<accept:
        r2 = r2_candi
        lambda_all = lambda_candi
    else:
        r2 = r2
    #store
    if e>=burn_in:
        chain_r2[e-burn_in]=r2
    #Sample r3
    r3_candi = numpy.random.uniform(0,2)
    lambda_candi = alpha**r1*theta**r2*gamma**r3_candi
    #Accept Function
    accept = acceptF(lambda_candi,adv,p)
    accept = accept - acceptF(lambda_all,adv,p)
    accept=min([0,accept])
    accept=exp(accept)
    # Accept rho_candidate with probability accept.
    if numpy.random.uniform(0,1)<accept:
        r3 = r3_candi
    else:
        r3 = r3
	#store
    if e>=burn_in:
		chain_r3[e-burn_in]=r3
    #Sample Adv
    adv_candi = numpy.random.uniform(0,2)
    #Accept Function
    accept = acceptF(lambda_all,adv_candi,p)
    accept = accept - acceptF(lambda_all,adv,p)
    accept=min([0,accept])
    accept=exp(accept)
    # Accept rho_candidate with probability accept.
    if numpy.random.uniform(0,1)<accept:
        adv = adv_candi
    else:
        adv = adv
    #store
    if e>=burn_in:
        chain_adv[e-burn_in]=adv
    print p,adv,r1,r2,r3

f, (ax1,ax2,ax3,ax4,ax5)=plt.subplots(5,1)
# plot things
ax1.plot(chain_p,'b')
ax2.plot(chain_adv)
ax3.plot(chain_r1)
ax4.plot(chain_r2)
ax5.plot(chain_r3)
plt.show()
conn.close()



