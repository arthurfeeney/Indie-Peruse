'''
module contains classes that can be used as frontiers. A frontier contain
urls to pages that have been seen, but not downloaded yet.
'''

import heapq
import queue
import queuelib
import data_generation.url_util as uu
import time


class Frontier:
    '''
    treated as an abstract class that each frontier class must implement
    '''

    def __init__(self):
        pass

    def view_frontier(self):
        raise NotImplementedError('Frontier.view_frontier not implemented')

    def empty(self):
        raise NotImplementedError('Frontier.empty not implemented')

    def size(self):
        raise NotImplementedError('Frontier.size not implemented')

    def add(self, url, **kwargs):
        raise NotImplementedError('Fronter.add not implemented')

    def add_many(self, urls, **kwargs):
        for url in urls:
            self.add(url)

    def get(self):
        raise NotImplementedError('Fronter.get not implemented')


class FIFOFrontier(Frontier):
    '''
    Simple FIFO Queue. Very impolite. :(
    Essentially just a wrapper for that implements view_frontier()
    '''

    def __init__(self):
        super(FIFOFrontier, self).__init__()
        self.frontier_queue = queue.Queue()

    def view_frontier(self):
        return list(self.frontier_queue.queue)

    def empty(self):
        return self.frontier_queue.empty()

    def size(self):
        return self.frontier_queue.qsize()

    def add(self, url, **kwargs):
        self.frontier_queue.put(url)

    def get(self):
        # returns and removes the first item from q
        return self.frontier_queue.get()


class PriorityFunctor:
    '''
    base class for PriorityFunctors. 
    '''

    def __init__(self):
        # domain -> information required for functor
        # keeps track of the last time the domain was popped.
        self.last_pulled = {}

    def priority(self, domain):
        raise NotImplementedError('Frontier.priority not implemented')

    def __call__(self, domain):
        raise NotImplementedError('Frontier.__call__ not implemented')

    def num_pulled(self):
        return len(self.last_pulled)

    def k_oldest(self, k):
        # the oldest keys will have the earliest time pulled. So
        # sort and get the first k elements.
        oldest = sorted(self.last_pulled.items(),
                        key=lambda kv: (kv[1], kv[0]))[:k]
        out, _ = zip(*oldest)
        return list(out)


class DomainPriorityFunctor(PriorityFunctor):
    '''
    Priority Queue based Frontier. A bit more polite than fifo.
    Keeps limit domains. Prioritizes new domains, domains not crawled in a
    while
    should be used as a functor for priority queue class.
    '''

    def __init__(self):
        super(DomainPriorityFunctor, self).__init__()

    def priority(self, domain):
        time_pulled = time.time()

        if domain in self.last_pulled:
            # large negative if it has not been seen in a while.
            # small negative if it has been seen recently :)
            priority = self.last_pulled[domain] - time_pulled

        else:
            # if the domain is totally new, give it great priority.
            priority = -time_pulled

        # update the last time pulled to now
        self.last_pulled[domain] = time_pulled

        return priority

    def __call__(self, domain):
        return self.priority(domain)


class SeenPriorityFunctor(PriorityFunctor):
    '''
    Prioritezes domains not SEEN in a while. One site may link many other
    sites that are in a different domain. This spaces them out a bit.
    should be used as a functor for priority queue class.
    '''

    def __init__(self, scale_jump=20):
        super(SeenPriorityFunctor, self).__init__()
        self.scale_jump = scale_jump

    def priority(self, domain):
        time_pulled = time.time()

        if domain in self.last_pulled:
            last_time_pulled, scale = self.last_pulled[domain]
            priority = last_time_pulled - time_pulled + scale
            scale += self.scale_jump  # artifically add seconds
        else:
            # if the domain is totally new, give it great priority.
            priority = -time_pulled
            scale = self.scale_jump

        # update the domain's last time pulled to now
        self.last_pulled[domain] = (time_pulled, scale)

        return priority

    def __call__(self, domain):
        return self.priority(domain)

    def lower_scale(self, domain):
        time, scale = self.last_pulled[domain]
        self.last_pulled[domain] = (time, scale - self.scale_jump)


class MemoryPriorityFrontier(Frontier):
    '''
    In-memory version of priority queue.
    '''

    def __init__(self, priority_functor, limit=None):
        # functor used to compute priority.
        self.priority_functor = priority_functor

        # option to store a finite number of elements since this structure
        # is in memory.
        # max number of things stored in last_pulled.
        # If it is None, there is no limit.
        self.limit = limit

        # use list and heapq functions for priority queue.
        self.q = []

    def view_frontier(self):
        return self.q

    def empty(self):
        return self.size() == 0

    def size(self):
        return len(self.q)

    def k_oldest(self, k):
        self.priority_functor.k_oldest(self.limit)

    def add(self, url):

        domain = uu.domain_name(url)

        if self.limit and self.priority_functor.num_pulled() >= self.limit:
            oldest_keys = self.priority_functor.k_oldest(
                int(self.limit / 2) + 1)
            for key in oldest_keys:
                del self.priority_functor.last_pulled[key]

        priority = self.priority_functor(domain)

        # push the url on the heap, not the domain
        heapq.heappush(self.q, (priority, url))

    def get(self):
        # return the url on the top of the heap, ignoring the priority
        return heapq.heappop(self.q)[1]


def memory_domain_priority_frontier(limit=None):
    '''
    convenient function so you can make one call instead of the two that
    are requried to construct the priority_functors and the frontier
    '''
    return MemoryPriorityFrontier(DomainPriorityFunctor(), limit)


def memory_seen_priority_frontier(limit=None):
    '''
    convenient function so you can make one call instead of the two that
    are requried to construct the priority_functors and the frontier
    '''
    return MemoryPriorityFrontier(SeenPriorityFunctor(), limit)
