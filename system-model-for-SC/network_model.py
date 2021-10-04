import networkx
import pandas as pd
import os
import json
import matplotlib.pyplot as plt

path = "data"
filename = os.path.join(path, "network.gml")
physical_network = nx.read_gml(filename, label="id")
physical_node_size = len(physical_network.nodes())
print("物理ネットワークのノード集合", physical_network.nodes())
print("物理ネットワークのリンク集合", physical_network.edges())

print(r"データ転送の処理遅延$d_{i}^{\mathrm{node}}$", nx.get_node_attributes(physical_network, "delay"))
print(r"伝送遅延$d_{i,j}^{\mathrm{link}}$", nx.get_edge_attributes(physical_network, "delay"))
print(r"処理容量$P_i$", nx.get_node_attributes(physical_network, "capacity"))
print(r"帯域幅$B_{i,j}$", nx.get_edge_attributes(physical_network, "bandwidth"))

pos = {n: (physical_network.nodes()[n]["lng"], physical_network.nodes()[n]["lat"]) for n in physical_network.nodes()}
nx.draw_networkx(physical_network, pos=pos)

filename = os.path.join(path, "service_chain_requirements.json")
with open(filename) as f:
  requests = json.load(f)
for request in requests:
  request['required_processing_func'] = {int(k): v for k, v in request['required_processing_func'].items()}

filename = os.path.join(path, "function_placement.json")
with open(filename) as f:
  function_placement = json.load(f)
placement = function_placement["placement"]
F = set(function_placement['functions'])
print(r"ネットワーク機能の集合$\mathcal{F}$", F)
"""
各数値は以下のネットワーク機能に対応する
便宜上，数値で表現している．
# NAT: Network Address Translator.             1
# FW: Firewall                                 2
# TM: Traffic Monitoring                       3
# IDPS: Intrusion Detection Prevention System. 4
# VOC: Video Optimization Controller           5
"""

virtual_links   = pd.DataFrame.from_dict(placement)
imaginary_nodes = {f: f+physical_node_size for f in F}
"""
print(imaginary_nodes)
{0: 12, 1: 13, 2: 14, 3: 15, 4: 16, 5: 17}
例えば，{0: 12}はネットワーク機能0(NAT)に対応する架空ノードのIDは12であることを示している．
架空ノードをfunctionのID+物理ノード数として定義することで，架空ノードのIDからfunction IDを計算できる．
"""

augmented_network = physical_network.copy()
for func, node in imaginary_nodes.items():
  augmented_network.add_node(node, lng=-(func+1)*8 - 70, lat=60, delay=0)
imaginary_links.apply(lambda x: augmented_network.add_edge(x.physical_node, imaginary_nodes[x.function], delay=0), axis=1)
imaginary_links.apply(lambda x: augmented_network.add_edge(imaginary_nodes[x.function], x.physical_node, delay=x.delay * 1e-3), axis=1) # d_{i,j}^{func}
print("拡張ネットワークのノード集合", augmented_network.nodes())
print("拡張ネットワークのリンク集合", augmented_network.edges())

pos = {n: (augmented_network.nodes()[n]["lng"], augmented_network.nodes()[n]["lat"]) for n in augmented_network.nodes()}
nx.draw_networkx(augmented_network, pos=pos)
