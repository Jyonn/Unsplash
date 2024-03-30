import heapq


class SimilarPhoto(object):
    def __init__(self, k):
        self.k = k
        self.heap = []

    def push(self, dist, photo):
        dist = -dist
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, (dist, photo))
        else:
            small_dist, tmp_photo = self.heap[0]
            if dist > small_dist:
                heapq.heapreplace(self.heap, (dist, photo))

    def top(self):
        return self.heap
