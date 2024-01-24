import re
from streamlit_agraph import Edge, Node, agraph, Config
class ProcNode:
    def __init__(self, pid: int):
        self.pid = pid
        self.req = set()
        self.used = set()
    def __str__(self):
        return str(self.pid)

class ResoNode:
    def __init__(self, rid: int, value: int):
        self.rid = rid
        self.value = value # 剩下的
        self.used = 0  #使用的
    def __str__(self):
        return str(self.rid) + ":" + str(self.value)

class AllocateGraph:
    def __init__(self, from_txt=None):
        self.reso_nodes = None
        self.proc_nodes = None
        self.init_graph(from_txt)


    def add_proc(self, pid):
        print(pid)
        pid = int(pid)
        if pid in self.proc_nodes:
            return False
        else:
            self.proc_nodes[pid] = ProcNode(pid)
        return True

    def add_reso(self, rid, value):
        print(rid, value)
        rid = int(rid)
        if rid in self.reso_nodes:
            return False
        else:
            self.reso_nodes[rid] = ResoNode(rid, value)

    def del_proc(self, pid):
        pid = int(pid)
        if pid not in self.proc_nodes:
            return False
        else:
            # 归还资源
            proc = self.proc_nodes[pid]
            for rid, val in proc.used:
                self.reso_nodes[rid].value += val
                self.reso_nodes[rid].used -= val


            del self.proc_nodes[pid]
        return True

    def del_reso(self, rid):
        global tup
        rid = int(rid)
        if rid not in self.reso_nodes:
            return False
        else:
            del self.reso_nodes[rid]
            # 还要删除nodes中所有有关记忆
            for pid, proc in self.proc_nodes.items():
                print(pid, proc.req, proc.used)
                flag = False
                for tup in proc.req:
                    if tup[0] == rid:
                        flag = True
                        break
                if flag:
                    proc.req.remove(tup)
                flag = False
                for tup in proc.used:
                    if tup[0] == rid:
                        flag = True
                        break
                if flag:
                    proc.used.remove(tup)
        return True

    def add_req(self, pid, rid, val=1):
        pid = int(pid)
        rid = int(rid)
        if pid in self.proc_nodes and rid in self.reso_nodes:
            self.proc_nodes[pid].req.add((rid,val))
            return True
        else:
            return False

    def add_alloc(self, pid, rid,val=1):
        pid = int(pid)
        rid = int(rid)
        if pid in self.proc_nodes and rid in self.reso_nodes:
            self.proc_nodes[pid].used.add((rid, val))
            self.reso_nodes[rid].value -= val
            self.reso_nodes[rid].used += val
            return True
        else:
            return False

    def get_graph_data(self, proc_color=None, req_color=None,
                       alloc_color=None, reso_color=None,
                       non_block_nodes=None, non_block_color=None):
        print("ni",non_block_nodes)
        graph_nodes = []
        graph_edges = []
        for pid, proc in self.proc_nodes.items():
            proc_name = "P{}".format(pid)
            if non_block_nodes and pid in non_block_nodes:
                graph_node = Node(id=proc_name, title=proc_name,
                                  label=proc_name,
                                  color=non_block_color,
                                  font={"color":non_block_color},
                                  shape="dot",
                                  physics=False,
                                  mass=2)
            else:
                graph_node = Node(id=proc_name, title=proc_name,
                                  label=proc_name,
                                  color=proc_color,
                                  font={"color": proc_color},
                                  shape="dot",
                                  physics=False,
                                  mass=2)
            graph_nodes.append(graph_node)
            for rid, val in proc.req:
                reso_name = "R{}".format(rid)
                graph_edge = Edge(proc_name, reso_name, label="请求{}".format(val),font={"color":req_color},
                                  color=req_color, width=2,
                                  smooth={
                                      "enabled":True,
                                      "type": "straightCross"
                                  },
                                  length=200)
                graph_edges.append(graph_edge)
            for rid, val in proc.used:
                reso_name = "R{}".format(rid)
                graph_edge = Edge(reso_name, proc_name,  label="占用{}".format(val), font={"color":alloc_color},
                                  color=alloc_color, width=2,
                                  smooth={
                                      "enabled": True,
                                      "type":"straightCross"
                                  },
                                  length=200)
                graph_edges.append(graph_edge)
        for rid, reso in self.reso_nodes.items():
            reso_name = "R{}".format(rid)
            graph_nodes.append(Node(id=reso_name,
                                    title=reso_name,
                                    label="{}[{}/{}]".format(reso_name,reso.value, reso.value + reso.used),
                                    shape="square",
                                    color=reso_color,
                                    font={"color": reso_color},
                                    physics=False,
                                    mass=2))
        return graph_nodes, graph_edges

    def save_as_txt(self, file_path):
        num_req = 0
        num_alloc = 0
        with open(file_path, 'w', encoding='utf8') as f:
            f.write(str(len(self.proc_nodes)) + '\n')
            for pid, proc in self.proc_nodes.items():
                num_req += len(proc.req)
                num_alloc += len(proc.used)
                f.write(str(pid) + ' ')
            f.write('\n')
            f.write(str(len(self.reso_nodes)) + '\n')
            for rid, reso in self.reso_nodes.items():
                f.write(str(rid) + ' ')
            f.write('\n')
            for rid, reso in self.reso_nodes.items():
                f.write(str(reso.value + reso.used) + ' ')
            f.write('\n')
            f.write(str(num_req) + '\n')
            for pid, proc in self.proc_nodes.items():
                for req in proc.req:
                    triple = map(str, [pid, req[0], req[1]])
                    f.write("(" + ",".join(triple) + ") ")
            f.write('\n')
            f.write(str(num_alloc))
            f.write('\n')
            for pid, proc in self.proc_nodes.items():
                for alloc in proc.used:
                    triple = map(str, [pid, alloc[0], alloc[1]])
                    f.write("(" + ",".join(triple) + ") ")


    def __str__(self):
        return str([(str(x), y.req, y.used) for x,y in self.proc_nodes.items()])\
            + '\n' + str([str(y) for x,y in self.reso_nodes.items()])

    def ret(self):
        procs = []
        for proc in self.proc_nodes.values():
            if proc.used or proc.req:
                procs.append(proc.pid)
        resos = []
        for reso in self.reso_nodes.values():
            if reso.used != 0:
                resos.append(reso.rid)
        return procs, resos


    def init_graph(self, from_txt):
        self.proc_nodes = {}
        self.reso_nodes = {}
        if from_txt:
            with open(from_txt, 'r', encoding='utf8') as f:
                s = f.read()
            strs = re.split(r"\W+", s)
            strs = filter(lambda x: str(x).isdigit(), strs)
            nums = list(map(int, strs))
            # 读进程
            num_proc = nums[0]
            proc_start_idx = 1
            for pid in nums[proc_start_idx: proc_start_idx + num_proc]:
                proc_node = ProcNode(pid)
                self.proc_nodes[pid] = proc_node

            num_reso = nums[1 + num_proc]
            reso_start_idx = proc_start_idx + num_proc + 1
            for rid, value in zip(nums[reso_start_idx: reso_start_idx + num_reso],
                                  nums[reso_start_idx + num_reso: reso_start_idx + num_reso * 2]):
                reso_node = ResoNode(rid, value)
                self.reso_nodes[rid] = reso_node

            num_req = nums[reso_start_idx + 2 * num_reso]
            req_start_idx = reso_start_idx + 2 * num_reso + 1
            idx = req_start_idx
            for _ in range(num_req):
                pid, rid, val = nums[idx: idx + 3]
                self.proc_nodes[pid].req.add((rid, val))
                idx += 3

            num_alloc = nums[idx]
            idx += 1
            for _ in range(num_alloc):
                pid, rid, val = nums[idx: idx + 3]
                self.proc_nodes[pid].used.add((rid, val))
                self.reso_nodes[rid].value -= val
                self.reso_nodes[rid].used += val
                idx += 3





if __name__ == "__main__":
    ag = AllocateGraph("test.txt")
    print(ag)
