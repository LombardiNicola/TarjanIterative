class TarjanSCC(object):
    def __init__(self, graph, N):
        self.N = N
        self.graph = graph
        self.stack = []
        self.on_stack = [False]*N
        self.init_time = [None]*N
        self.low_link = [None]*N
        self.time = 0
        self.sccs = {}
        self.scc_count = 0
        self.condensation_graph = {}

    def dfs_non_rec(self, i):
        dfs = [i]
        while dfs:
            i = dfs[-1]
            if not self.on_stack[i]:
                self.stack.append(i)
                self.on_stack[i] = True
            if self.init_time[i] is None:
                self.init_time[i] = self.time
                self.low_link[i] = self.time
                self.time += 1
            for j in self.graph[i]:
                if self.init_time[j] is None:  # if unvisited
                    dfs.append(j)
                    break
                if self.on_stack[j]:  # if it's on the stack it's been visited
                    self.low_link[i] = min(self.low_link[i], self.low_link[j])  # propagate low_link value

            if dfs[-1] != i:
                continue

            if self.init_time[i] == self.low_link[i]:  # if we're at beginning of scc
                cur_comp = set()
                while self.on_stack[i]:
                    j = self.stack.pop()
                    self.low_link[j] = self.low_link[i]
                    self.on_stack[j] = False
                    cur_comp.add(j)
                self.sccs[self.scc_count] = cur_comp
                self.scc_count += 1
            dfs.pop()

    def find_sccs(self):
        N = self.N
        for i in range(N):
            if self.init_time[i] is None:
                self.dfs_non_rec(i)
        return self.sccs
    
    def get_condensation_graph(self):
        if self.condensation_graph:
            return self.condensation_graph
        if not self.sccs:
            self.find_sccs()
        N_scc = self.scc_count
        scc_dict = {e:i for i in range(N_scc) for e in self.sccs[i]}
        self.condensation_graph = {}
        for i in range(N_scc):
            self.condensation_graph[i] = set()
        for i in self.graph:
            self.condensation_graph[scc_dict[i]].update([scc_dict[node] for node in self.graph[i] if scc_dict[node] != scc_dict[i]])
        for i in range(N_scc):
            self.condensation_graph[i] = list(self.condensation_graph[i])
        return self.condensation_graph