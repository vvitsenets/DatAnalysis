class GOT(thinkbayes2.Suite, thinkbayes2.Joint):
    def Likelihood(self, data, hypo):
        """Determines how well a given k and lam 
           predict the life/death of a character """
        age, alive = data
        k, lam = hypo
        if alive:
            prob = 1-exponweib.cdf(age, k, lam)
        else:
            prob = exponweib.pdf(age, k, lam)
        return prob

def Update(k, lam, age, alive):
    """Performs the Baysian Update and returns the PMFs
           of k and lam"""
    joint = thinkbayes2.MakeJoint(k, lam)
    suite = GOT(joint)
    suite.Update((age, alive))
    k = suite.Marginal(0, label=k.label), 
    lam = suite.Marginal(1, label=lam.label)
    return k, lam

def MakeDistr(introductions, lifetimes,k,lam):
    """Iterates through all the characters for a given k 
            and lambda.  It then updates the k and lambda
            distributions"""
    k.label = 'K'
    lam.label = 'Lam'
    print("Updating deaths")
    for age in lifetimes:
        k, lam = Update(k, lam, age, False)
    print('Updating alives')
    for age in introductions:
        k, lam = Update(k, lam, age, True)
    return k,lam