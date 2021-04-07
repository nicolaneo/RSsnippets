# author: Nicola Neophytou
# homemade KW test to sanity check results

import scipy.stats as ss

def get_rank_avg(group, scorerank):
    """
    Calculates the sum of ranks of scores in 'group', and divides by the 
    number of scores in the group to get the average.

    """
    
    ranksum=0
    for score in (group):
        ranksum+=scorerank[score]
    return ranksum/len(group)

def KWtest(group1, group2, group3):
    """
    A function to perform a Kruskal-Wallis statistical significance test on 
    three groups of data, at significance level alpha = 0.01. 
    Significant differences corresponds to a H statistic > 9.21034.
    Used to test for statistical differences between NDCG scores amongst three 
    groups of users.
    
    The KW test can only tell you if there are significant differences between 
    groups of data; it cannot tell you between which groups there are 
    significant differences.

    Parameters
    ----------
    group1, group2, group3 : lists
        Groups of NDCG scores.

    Returns
    -------
    bool
        Returns True for significant differences, False for no significant 
        differences.

    """
    # combine all scores
    joinedscores = group1 + group2 + group3
    # order these scores and get their rank
    ranks = ss.rankdata(joinedscores)
    # store ranks as values in a dictionary, with scores as keys
    scorerank = dict(zip(joinedscores, ranks))
    
    # get the average rank of each group
    group1avg = get_rank_avg(group1, scorerank)
    group2avg = get_rank_avg(group2, scorerank)
    group3avg = get_rank_avg(group3, scorerank)
    
    # calculate the mean score (N+1)/2
    rbar = (len(joinedscores)+1.0)/2.0
    
    # numerator of H statistic
    numerator=len(group1)*((group1avg-rbar)**2)
    numerator+=len(group2)*((group2avg-rbar)**2)
    numerator+=len(group3)*((group3avg-rbar)**2)
    
    # denominator of H statistic
    denominator=0
    for score in group1:
        denominator+=(scorerank[score]-rbar)**2.0
    for score in group2:
        denominator+=(scorerank[score]-rbar)**2.0
    for score in group3:
        denominator+=(scorerank[score]-rbar)**2.0
    
    # calculate H statistic
    H=numerator/denominator
    H*=(len(joinedscores)-1.0)
    
    # evaluate H statistic
    if H > 9.21034:
        print("H statistic = {0:.3f}.\n".format(H))
        print("There are significant difference between these data groups at "\
              "significance level alpha = 0.01.\n" \
              "Reject the null hypothesis.\n")

        return True
    else:
        print("H statistic = {0:.3f}.\n".format(H))
        print("There are no statistical differences between these data groups "\
              "at significance level alpha = 0.01.\n"\
              "Cannot reject the null hypothesis.")
        return False

# main function
if __name__=="__main__":
    group1 = [8.2,10.3,9.1,12.6,11.4,13.2]
    group2 = [10.2,9.1,13.9,14.5,9.1,16.4]
    group3 = [13.5,8.4,9.6,13.8,17.4,15.3]
    KWtest(group1, group2, group3)

