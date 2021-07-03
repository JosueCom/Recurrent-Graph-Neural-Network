import torch as th

from lign.utils.functions import similarity_matrix

class NN():

    def __init__(self, X = None, Y = None, p = 2):
        self.p = p
        self.train_pts = None
        self.train_label = None
        self.train(X, Y)

    def train(self, X, Y):
        self.train_pts = X
        self.train_label = Y

    def __call__(self, x):
        return self.predict(x)

    def predict(self, x):
        if self.train_pts == None:
            raise RuntimeError("NN wasn't trained. Need to execute NN.train() first")
        
        dist = similarity_matrix(x, self.train_pts, self.p) ** (1/self.p)
        labels = th.argmin(dist, dim=1)
        return self.train_label[labels]

class KNN(NN):

    def __init__(self, X = None, Y = None, p = 2, k = 3):
        super().__init__(X, Y, p)
        self.k = k

    def predict(self, x):
        if self.train_pts == None:
            raise RuntimeError("KNN wasn't trained. Need to execute self.train() first")
        
        dist = similarity_matrix(x, self.train_pts, self.p) ** (1/self.p)

        votes = dist.argsort(dim=1)[:,:self.k]
        votes = self.train_label[votes]

        print(votes)
        print(th.unique(votes, dim = 1, return_counts=True))
        
        #max_count = count.argmax(dim=1)
        return votes[10]


class Spectral(NN):

    def __init__(self, X, Y, p = 2):
        super().__init__(X, Y, p)
        pass

    def predict(self):
        pass

if __name__ == '__main__':
    a = th.Tensor([
        [1, 1],
        [0.88, 0.90],
        [-1, -1],
        [-1, -0.88]
    ])

    b = th.LongTensor([3, 3, 5, 5])

    c = th.Tensor([
        [-0.5, -0.5],
        [0.88, 0.88]
    ])

    knn = KNN(a, b)
    print(knn(c))
