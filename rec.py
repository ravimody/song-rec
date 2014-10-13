from scipy import sparse
from sklearn.preprocessing import normalize


# 
def find_similar_users(dataset, user, num_users):
   # normalize matrix so each user's plays sum to 1 
   normalized_dataset = normalize(dataset,norm='l1', axis=1)
   
   # get the dot product of the user with every user, this is effectively a similarity score 
   score = normalized_dataset[user,:] * normalized_dataset.transpose()
   
   

def get_rand_dataset(num_users = 10000, num_songs = 1000000, avg_songs_per_user = 10, max_plays = 20, seed = 100):
   density = float(avg_songs_per_user) / num_songs
   dataset = sparse.rand(num_users, num_songs, density, random_state = seed, format = 'csr') * max_plays
   dataset = dataset.ceil()
   return(dataset)
   # todo rhm: remove users with no listens; for now i'll assume this will generate users with at least one listen   
   