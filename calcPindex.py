# author: Nicola Neophytou
# calculate the p-index, a measure of popularity, for each user in lastfm dataset.

import h5py
from scipy.sparse import csr_matrix
import numpy as np
import progressbar

def calc_pindex(plays):
    """
    A function to calculate the p-index, a measure of popularity, for each user.
    A user's p-index is defined as the largest possible integer x such that x% 
    of the other users share at least x% of the given user's artists.
    Parameters
    ----------
    plays : csr_matrix
        an item-user matrix of size (m=number of artists, n=number of users), 
        containing each users listen count to each artist.

    Returns
    -------
    pIndex : list
        Containing the p-index for every user.

    """
    
    pindices=[]
    (m,n) = plays.shape
    # get the number of artists per user
    playlistLength = (plays != 0).sum(0)
    
    # converting the matrix to booleans and multiplying by the column for 
    # each user, to get the number of common artists with every other user
    playsBool = (plays != 0)
    playsBoolT = playsBool.transpose() 
    
    # loop over users
    for i in progressbar.progressbar(range(n)):
        # get i'th users column and transpose
        columni = playsBool[:,i].transpose()
        # multiply by the rest of the matrix 
        A = (playsBoolT.multiply(columni)).transpose()
        # sum the non zero values, corresponding to common artists shared with 
        # other users
        common = A.sum(0)
        
        # get the percentage of common artists over user i's total artists
        percentShared = (common/playlistLength[0,i])*100.0
        percentShared = np.array(percentShared)[0].tolist()
        # covert to integers
        percentShared = [int(y) for y in percentShared]
        
        # get sorted list of unique integers 
        sharedset = set(percentShared) 
        sharedset = (list(sharedset))
        sorted(sharedset)
        
        # find maximum int x for which x% of other users share x% of users artists
        Found=False
        # count the other users, not including user i themselves
        j=len(sharedset)-1
        count=0
        while not Found:
            # count the percentage of users sharing this percentage of artists
            count+=percentShared.count(sharedset[j])
            # if it's greater than or equal to x, the p-index is found
            if ((count-1)/(n-1))*100.0 >= sharedset[j]:
                pindex = sharedset[j]
                Found=True
            j-=1
        
        # append p-index to list of all pindices for all users
        pindices.append(pindex)
    
    return pindices

# main function
if __name__ == "__main__":
    # read in lastfm dataset
    with h5py.File('lastfm_TRAIN.h5', 'r') as f:
        m = f.get('artist_user_plays')
        # get item-user matrix
        plays = csr_matrix((m.get('data'), m.get('indices'), m.get('indptr')))
        # calculate p-indices
        pIndex = calc_pindex(plays)

    # write to text file
    with open('pIndices.txt', 'w') as h:
        for item in pIndex:
            h.write("%s\n" % item)