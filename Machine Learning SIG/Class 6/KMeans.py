import sys
import numpy as np
import time
from matplotlib import pyplot as plt

def GenerateDataset():
    num_points = 40
    points = np.random.random_sample(num_points * 2)
    points.shape = (num_points, 2)
    for i in range(num_points):
        if np.random.randint(0, 2):
            points[i][0] -= 1
        else:
            points[i][0] += 1
        if np.random.randint(0, 2):
            points[i][1] -= 1
        else:
            points[i][1] += 1
    np.save("data", points)

def EuclideanDistance(point_x, point_y): 
    s = 0
    # The sum of the squared differences of the elements
    for i in range(len(point_x)):
        s += ((point_x[i] - point_y[i]) ** 2)
    return s ** 0.5 #The square root of the sum

def Classify(means, item):
    # Classify item to the mean with minimum distance
    minimum = sys.maxsize
    index = -1
    for i in range(len(means)):
        # Find distance from item to mean
        dis = EuclideanDistance(item, means[i])
        if (dis < minimum):
            minimum = dis
            index = i
    return index

def UpdateMean(means, items_cluster):
    dimensions = len(means[0])
    for i in range(len(means)):
        sum = [[0, 0] for _ in range(dimensions)]
        size = len(items_cluster[i])
        for j in range(size):
            for k in range(dimensions):
                sum[k] += items_cluster[i][j][k]
            for k in range(dimensions):
                sum[k] = sum[k] / size
                means[i][k] = sum[k]

def PlotPoints(points):
    for point in points:
        plt.plot(point[0], point[1], 'ko')
    plt.show()

def PlotClusters(items_cluster, means):
    colors = {0: 'ro', 1: 'bo', 2: 'go', 3: 'yo', 4: 'ko', 5: 'co', 6: 'mo'}
    for i in items_cluster.keys():
        for point in items_cluster[i]:
            plt.plot(point[0], point[1], colors[i])
    for point in means:
        plt.plot(point[0], point[1], 'co')
    plt.show()

def KMeans():
    points = np.load("data.npy")
    k = int(input("Enter Number of Clusters: "))
    means = [np.random.random_sample(2) for i in range(k)]
    PlotPoints(points)
    iterations = 100
    for _ in range(iterations):
        # start_time = time.time()
        items_cluster = {i: [] for i in range(k)}
        for item in points:
            items_cluster[Classify(means, item)].append(item)
            UpdateMean(means, items_cluster)
        # print(_, means, time.time() - start_time)
    PlotClusters(items_cluster, means)

GenerateDataset()
KMeans()