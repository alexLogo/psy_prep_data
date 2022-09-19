import numpy as np
from functools import reduce
from feature_calculations.read_features import read_k_subjects, read_features

class Agglomerative_clustring:
    def __init__(self, max_size, n_clusters):
        self.max_size = max_size
        self.n_clusters = n_clusters
        
    def fit(self, distance_matrix):
        np.fill_diagonal(distance_matrix, np.inf)
        self.distance_matrix = distance_matrix
        self.distance_cluster = np.copy(distance_matrix)
        self.cluster_sets = [set([x]) for x in range(len(distance_matrix))]
        self.cluster_sets_keeper = []
        
        while len(self.cluster_sets) + len(self.cluster_sets_keeper) > self.n_clusters:
            i, j = np.argwhere(self.distance_cluster == np.min(self.distance_cluster))[0]
            i, j = min(i,j), max(i,j)
            self.merge(i, j)
            self.recalculation(i, j)
            
            if (len(self.cluster_sets) + len(self.cluster_sets_keeper)) % 100 == 0:
                print(f"num of clusters: {len(self.cluster_sets) + len(self.cluster_sets_keeper)}")
        
        self.cluster_sets += self.cluster_sets_keeper
        self.create_cluster_index()   
        
            
    def create_cluster_index(self):
        self.clusters_index = np.zeros(shape=len(self.distance_matrix))
        for i, cluster in enumerate(self.cluster_sets):
            for entry in list(cluster):
                self.clusters_index[entry] = i
                
    
    def drop_cluster(self, idx, keep=False):
        self.distance_cluster = np.delete(self.distance_cluster, idx, axis=0)
        self.distance_cluster = np.delete(self.distance_cluster, idx, axis=1)
        
        cluster = self.cluster_sets.pop(idx)
        if keep:
            self.cluster_sets_keeper.append(cluster)
            
            
    def merge(self, idx_i, idx_j):
        self.cluster_sets[idx_i] = self.cluster_sets[idx_i] | self.cluster_sets[idx_j]
        self.drop_cluster(idx_j)
        
    
    def recalculation(self, idx_i, idx_j):  
        if len(self.cluster_sets[idx_i]) > self.max_size:
            self.drop_cluster(idx_i, keep=True)
            return
        self.recalculate(idx_i)
            
        
    def recalculate(self, idx):
        '''
        recalculate distance for the new cluster
    
        Parameters
        ----------
        distance_matrix : ndarray
            original distance matrix.
        cluster_distance : ndarray
            cluster distance matrix.
        idx : TYPE
            index of new cluster.
    
        Returns
        -------
        None.
    
        '''
        new_cluster = self.cluster_sets[idx]
        
        for i, cluster in enumerate(self.cluster_sets):
            if i == idx:
                continue
            new_dis = self.calculate_distance(i, idx)
            self.distance_cluster[idx, i] = new_dis
            self.distance_cluster[i, idx] = new_dis



    def calculate_distance(self, cluster_a_idx, cluster_b_idx):
        '''
        calculate distance between two clusters
    
        Parameters
        ----------
        distance_matrix : ndarray
            distance matrix
        cluster_a : set
            indices of the first cluster
        cluster_b : TYPE
            indices of the second cluster
    
        Returns
        -------
        mean distance
    
        '''
        # cast the sets to tuples
        cluster_a = tuple(self.cluster_sets[cluster_a_idx])
        cluster_b = tuple(self.cluster_sets[cluster_b_idx])
        
        # create distances list
        dis_list = []
        # iterate over the indices
        for idx_a in cluster_a:
            for idx_b in cluster_b:
                dis_list.append(self.distance_matrix[idx_a, idx_b])
                
        mean = np.mean(dis_list)
        
        return mean 
        
if __name__ == "__main__":
    data_raw = read_k_subjects(range(1,11), mode='clean', z=True)
    data = data_raw.iloc[:,3:]
    test = np.array(data)
    corr = np.corrcoef(test.T)
    dis = 1 - abs(corr)
    cluster = Agglomerative_clustring(max_size=200, n_clusters=50)
    cluster.fit(dis)
