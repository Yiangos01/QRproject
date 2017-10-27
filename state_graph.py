import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import pylab
import graphviz as gv
import functools

digraph = functools.partial(gv.Digraph, format='svg')

class state(object):

    def __init__(self,i1,i2,j1,j2,k1,k2):
        self.mar_inflow=i1
        self.der_inflow=i2
        self.mar_volume=j1
        self.der_volume=j2
        self.mar_outflow=k1
        self.der_outflow=k2

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return self.mar_inflow+self.der_inflow+self.mar_volume+self.der_volume+self.mar_outflow+self.der_outflow


class entity(object):
    der='+'
    magni='0'
    def __init__(self, space_range):
        self.space = space_range



def infuence(a,b,c):
    if a.magni == '+' and c.magni=='-' :
        b.der = '+'
    elif a.magni == '+' and c.magni=='0':
        d.der = '+'
    elif a.magni == '+' and c.magni=='+':
        d.der = '?'
    elif a.magni == '-' and c.magni=='-':
        d.der='?'

def add_nodes(graph, nodes):
    for n in nodes:
        if isinstance(n, tuple):
            graph.node(n[0], **n[1])
        else:
            graph.node(n)
    return graph

def add_edges(graph, edges):
    for e in edges:
        if isinstance(e[0], tuple):
            graph.edge(*e[0], **e[1])
        else:
            graph.edge(*e)
    return graph

def derivative(a):
    if a.der!='0':
        if a.der=='+' and a.space.index(a.magni)<len(a.space)-1:
            a.magni=a.space[a.space.index(a.magni)+1]
            print(1)
        elif a.der=='-' and a.space.index(a.magni)!=0:
            a.magni=a.space[a.space.index(a.magni)-1]
            print(2)

    return a


def valid_state(current,next_state):

    if current==next_state:
        return False

    if next_state.mar_volume != next_state.mar_outflow:
        return False

    if next_state.der_volume != next_state.der_outflow:
        return False

    if current.der_inflow == '+' and ((next_state.der_volume=='-' and current.der_volume=='0') or (next_state.der_volume=='0' and current.der_volume=='+')):
        return False

    if next_state.mar_inflow == '+' and next_state.mar_outflow == '0' and (next_state.der_volume=='0' or next_state.der_volume=='-'):
        return False

    if next_state.mar_inflow == '0' and next_state.mar_outflow == '+' and (next_state.der_volume=='0' or next_state.der_volume=='+'):
        return False

    if next_state.mar_inflow == '0' and next_state.mar_outflow == '0' and (next_state.der_volume=='+' or next_state.der_volume=='-'):
        return False

    if ((current.der_inflow=='0' and (current.mar_inflow!=next_state.mar_inflow))
    or (current.der_outflow=='0' and (current.mar_outflow!=next_state.mar_outflow)) or (current.der_volume=='0' and (current.mar_volume!=next_state.mar_volume))):
        return False

    if (current.der_volume=='-' and ((current.mar_volume=='+' and next_state.mar_volume=='max') or (current.mar_volume=='0' and next_state.mar_volume=='+'))):
        return False

    if (current.der_inflow=='-' and ((current.mar_inflow=='+' and next_state.mar_inflow=='max') or (current.mar_inflow=='0' and next_state.mar_inflow=='+'))):
        return False

    if (current.der_outflow=='-' and ((current.mar_outflow=='+' and next_state.mar_outflow==max) or (current.mar_outflow=='0' and current.mar_outflow=='+'))):
        return False

    if (current.der_volume=='+' and ((current.mar_volume=='+' and next_state.mar_volume=='0') or (current.mar_volume=='max' and next_state.mar_volume=='-'))):
        return False

    if (current.der_inflow=='+' and ((current.mar_inflow=='+' and next_state.mar_inflow=='0') )):
        return False

    if (current.der_outflow=='+' and ((current.mar_outflow=='+' and next_state.mar_outflow=='0') or (current.mar_outflow=='+' and next_state.mar_outflow=='0'))):
        return False


    if(current.mar_volume=='0' and next_state.mar_volume=='max') or (current.mar_volume=='max' and next_state.mar_volume=='0'):
        return False

    if(current.mar_outflow=='0' and next_state.mar_outflow=='max') or (current.mar_outflow=='max' and next_state.mar_outflow=='0'):
        return False

    if(current.der_inflow=='-' and next_state.der_inflow=='+') or (current.der_inflow=='+' and next_state.der_inflow=='-'):
        return False
    if (current.der_volume=='-' and next_state.der_volume=='+') or (current.der_volume=='+' and next_state.der_volume=='-'):
        return False
    if (current.der_outflow=='-' and next_state.der_outflow=='+') or (current.der_outflow=='+' and next_state.der_outflow=='-'):
        return False

    if current.mar_inflow=='0' and next_state.der_inflow=='-':
        return False

    if current.der_volume=='+' and (next_state.mar_volume=='0' or (current.mar_volume=='max' and next_state.mar_volume=='+')) :
        return False

    if current.der_inflow=='+' and next_state.mar_inflow=='0':
        return False

    if next_state.mar_inflow=='0' and next_state.der_inflow=='-':
        return False

    if current.der_inflow=='-' and ((current.der_volume=='0' and next_state.der_volume=='+') or (current.der_volume=='-' and next_state.der_volume=='0')):
        return False

    if current.der_inflow=='+' and ((current.mar_volume=='+' and next_state.mar_volume=='0') or (current.mar_volume=='max' and next_state.mar_volume=='+')):
        return False

    if current.der_inflow=='0' and ((current.der_volume=='0' and next_state.der_volume=='+') or (current.der_volume=='0' and current.mar_volume=='max' and next_state.der_volume=='-') or (current.mar_volume=='max' and current.der_volume!=next_state.der_volume)):
        return False

    if ((current.der_inflow!=next_state.der_inflow) and (current.der_outflow==next_state.der_outflow) and (current.mar_outflow==next_state.mar_outflow) and (current.der_volume==next_state.der_volume) and (current.mar_volume==next_state.mar_volume)):
        return True
    elif current.der_inflow!=next_state.der_inflow:
        return False

    return True
def decreaseing_scenario(all_states):

    state3=state('0','0','max','+','max','+')
    state4=state('0','0','max','0','max','0')
    state2=state('0','0','max','-','max','-')
    initial ="000000"
    final = state('0','0','0','0','0','0')
    starting_state=state('+','+','max','+','max','+')
    states=[]
    edges=[]
    transitions=[]
    trace=""
    graph_states=[]
    states=[starting_state]
    graph_states.append(str("I("+str(starting_state.mar_inflow)+","+str(starting_state.der_inflow)+")\nV("+str(starting_state.mar_volume)+","+str(starting_state.der_volume)+")\nO("+str(starting_state.mar_outflow)+","+str(starting_state.der_outflow)+")"))
    G=digraph()
    for state1 in states:
        for index,statei in enumerate(all_states):

            if(valid_state(state1,statei)) and ((statei.der_inflow=='0' and state1.der_inflow=='+') or (statei.der_inflow=='-' and state1.der_inflow=='0') or (statei.der_inflow==state1.der_inflow) or ( statei.mar_inflow=='0' and statei.der_inflow=='0')) and statei!=state3 and statei!=state4 and statei!=state2:

                if statei not in states:
                    states.append(statei)
                    graph_states.append(str("I("+str(statei.mar_inflow)+","+str(statei.der_inflow)+")\nV("+str(statei.mar_volume)+","+str(statei.der_volume)+")\nO("+str(statei.mar_outflow)+","+str(statei.der_outflow)+")"))

                    edges.append([graph_states[states.index(state1)],graph_states[states.index(statei)]])

                    transitions.append(((graph_states[states.index(state1)],graph_states[states.index(statei)]),{"label": transition(state1,statei)}))

                    trace+="for state "+str(states.index(state1))+" "+intra_state(state1)+'\n'
                    trace+='from '+str(states.index(state1))+" to "+str(states.index(statei))+"\n"+inter_state(state1,statei)+'\n'
                    trace+="for state "+str(states.index(statei))+" "+intra_state(statei)+'\n\n\n'



    print(trace)

    add_edges(
        add_nodes(G, graph_states),
        transitions
        ).render('img/decrease')


def increasing_scenario(all_states):

    initial ="000000"
    final = state('+','+','max','+','max','+')
    starting_state=state('0','0','0','0','0','0')
    states=[]
    edges=[]
    transitions=[]
    trace=""
    graph_states=[]
    states=[starting_state]
    graph_states.append(str("I("+str(starting_state.mar_inflow)+","+str(starting_state.der_inflow)+")\nV("+str(starting_state.mar_volume)+","+str(starting_state.der_volume)+")\nO("+str(starting_state.mar_outflow)+","+str(starting_state.der_outflow)+")"))
    G=digraph()
    for state1 in states:
        for index,statei in enumerate(all_states):
            if(valid_state(state1,statei)) and statei.der_inflow=='+':
                if statei not in states:
                    states.append(statei)
                    graph_states.append(str("I("+str(statei.mar_inflow)+","+str(statei.der_inflow)+")\nV("+str(statei.mar_volume)+","+str(statei.der_volume)+")\nO("+str(statei.mar_outflow)+","+str(statei.der_outflow)+")"))

                    edges.append([graph_states[states.index(state1)],graph_states[states.index(statei)]])

                    transitions.append(((graph_states[states.index(state1)],graph_states[states.index(statei)]),{"label": transition(state1,statei)}))


                    trace+="for state "+str(states.index(state1))+" "+intra_state(state1)+'\n'
                    trace+='from '+str(states.index(state1))+" to "+str(states.index(statei))+"\n"+inter_state(state1,statei)+'\n'
                    trace+="for state "+str(states.index(statei))+" "+intra_state(statei)+'\n\n\n'



    print(trace)


    add_edges(
        add_nodes(G, graph_states),
        transitions
        ).render('img/increase')


def createStateGraph(all_states,):

    starting_state = state('0','0','0','0','0','0')
    state3=state('0','0','max','+','max','+')
    state4=state('0','0','max','0','max','0')
    state2=state('0','0','max','-','max','-')
    states=[starting_state]
    child_states=[]
    edges=[]
    transitions=[]
    graph_states=[]
    graph_states.append(str("I("+str(starting_state.mar_inflow)+","+str(starting_state.der_inflow)+")\nV("+str(starting_state.mar_volume)+","+str(starting_state.der_volume)+")\nO("+str(starting_state.mar_outflow)+","+str(starting_state.der_outflow)+")"))
    #G = nx.MultiDiGraph()
    #G.add_node(0)
    G=digraph()
    i=1
    for state1 in states:
        child_states=[]
        for index,statei in enumerate(all_states):
            if(valid_state(state1,statei)) and statei!=state3 and statei!=state4 and statei!=state2:
            #print(statei.__repr__,index)
                child_states.append(statei)
                if statei not in states:
                    states.append(statei)
                    graph_states.append(str("I("+str(statei.mar_inflow)+","+str(statei.der_inflow)+")\nV("+str(statei.mar_volume)+","+str(statei.der_volume)+")\nO("+str(statei.mar_outflow)+","+str(statei.der_outflow)+")"))
                    #G.add_node(i)
                    #G.add_node(statei)
                    i+=1
                edges.append([graph_states[states.index(state1)],graph_states[states.index(statei)]])
                #labels = {(0,1):'foo', (2,3):'bar'}
                #edges.append()
                transitions.append(((graph_states[states.index(state1)],graph_states[states.index(statei)]),{"label": transition(state1,statei)}))
                #G.add_edge(states.index(state1),states.index(statei))
                # print (statei)
    #print (edges)
    #print (states)
    #print (graph_states)
    print (transitions)
    #print (intra_state(state3))
    for i,state1 in enumerate(states):
        print(str(i)+" -> " + str(state1) )

    #add_nodes(G, graph_states)
    styles = {
    'graph': {
        'label': 'State Graph',
        'fontsize': '16',
        'fontcolor': 'white',
        'bgcolor': '#333333',
    },
    'nodes': {
        'fontname': 'Helvetica',
        'shape': 'hexagon',
        'fontcolor': 'white',
        'color': 'white',
        'style': 'filled',
        'fillcolor': '#006699',
    },
    'edges': {
        'style': 'dashed',
        'color': 'white',
        'arrowhead': 'open',
        'fontname': 'Courier',
        'fontsize': '12',
        'fontcolor': 'white',
        }
    }


    add_edges(
        add_nodes(G, graph_states),
        transitions
        ).render('img/g4')

    apply_styles(G,styles)

    filename = G.render(filename='img/g4')
    return G
    #print (filename)
    # #save_graph(G)

# def save_graph(graph):
#     #initialze Figure
#     plt.figure(num=None, figsize=(20, 20), dpi=80)
#     plt.axis('off')
#     fig = plt.figure(1)
#     pos = nx.spring_layout(graph)
#     nx.draw_networkx_nodes(graph,pos)
#     nx.draw_networkx_edges(graph,pos)
#     nx.draw_networkx_labels(graph,pos)

    # xmax = cut * max(xx for xx, yy in pos.values())
    # ymax = cut * max(yy for xx, yy in pos.values())
    # plt.xlim(0, xmax)
    # plt.ylim(0, ymax)
    #
    # plt.show()
    # # plt.savefig(file_name,bbox_inches="tight")
    # pylab.close()
    # del fig

def transition(state1,statei):
    transition=""

    if state1.mar_volume!=statei.mar_volume:
        if (state1.mar_volume=='+' and statei.mar_volume=='max') or (state1.mar_volume=='0' and statei.mar_volume=='+'):
            transition+= " + Volume "
        else:
            transition+= " - Volume "

    if state1.mar_outflow!=statei.mar_outflow:
        if (state1.mar_outflow=='+' and statei.mar_outflow=='max') or (state1.mar_outflow=='0' and statei.mar_outflow=='+'):
            transition+= " + outflow"
        else:
            transition+= " - outflow"

    if state1.mar_inflow!=statei.mar_inflow:
        if state1.mar_inflow=='0' and statei.mar_inflow=='+':
            transition+= " + inflow"
        else:
            transition+= " - inflow"

    if state1.der_volume!=statei.der_volume:
        if (state1.der_volume=='0' and statei.der_volume=='+'):
            transition+= " + der Volume "
        elif (state1.der_volume=='-' and statei.der_volume=='0'):
            transition+= " + der Volume"
        else :
            transition+= " - der Volume"

    if state1.der_inflow!=statei.der_inflow:
        if (state1.der_inflow=='0' and statei.der_inflow=='+'):
            transition+= " + der inflow "
        elif (state1.der_inflow=='-' and statei.der_inflow=='0'):
            transition+= " + der inflow "
        else :
            transition+= " - der inflow"

    if state1.der_outflow!=statei.der_outflow:
        if (state1.der_outflow=='0' and statei.der_outflow=='+'):
            transition+= " + der outflow "
        elif (state1.der_outflow=='-' and statei.der_outflow=='0'):
            transition+= " + der outflow "
        else :
            transition+= " - der outflow"

    return transition

def apply_styles(graph, styles):
    graph.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )
    graph.node_attr.update(
        ('nodes' in styles and styles['nodes']) or {}
    )
    graph.edge_attr.update(
        ('edges' in styles and styles['edges']) or {}
    )
    return graph

def intra_state(state):
    explanation=""

    if state.mar_inflow=='0':
        explanation+="There's no water flowing. "
    else:
        explanation+="There's water flowing. "

    if state.der_inflow=='+':
        explanation+='We increasing the rate of wate flowing. '
    elif state.der_inflow=='0':
        explanation+='The rate of water flowing is nor increasing or decreasing. '
    else:
        explanation+='the rate of water flowing is decreasing. '

    if state.mar_volume=='0':
        explanation+="There's no water in the sink. "
    elif state.mar_volume=='+':
        explanation+="There's water in the sink. "
    else:
        explanation+="There's the maximum capacity of water in the sink. "

    if state.der_volume=='+':
        explanation+='The rate of water flowing in the container is increasing. '
    elif state.der_volume=='0':
        explanation+='The rate of water flowing in the container  is nor increasing or decreasing. '
    else:
        explanation+='The rate of water flowing in the container is decreasing. '

    if state.mar_outflow=='0':
        explanation+="There's no water flowing out from the sink. "
    elif state.mar_outflow=='+':
        explanation+="There's water flowing out from the sink. "
    else:
        explanation+="There's no water flowing in maximum rate out from the sink. "

    if state.der_outflow=='+':
        explanation+='The rate of the out-flowing water is increasing. '
    elif state.der_outflow=='0':
        explanation+='The rate of the out-flowing water  is nor increasing or decreasing. '
    else:
        explanation+='The rate of the out-flowing water is decreasing. '

    return explanation

def inter_state(state1,state2):
    trace=""
    #Inflow
    if state1.mar_inflow=='0' and state2.mar_inflow=='+':
        trace+="water start flowing. "

    if state1.mar_inflow=='+' and state2.mar_inflow=='0':
        trace+="water stop flowing. "

    if state1.der_inflow=='0' and state2.der_inflow=='+':
        trace+="we turn the tap, so the rate of water flowing is increasing. "
    elif state1.der_inflow=='+' and state2.der_inflow=='0':
        trace+="we stoped turning the tap, so the rate of water flowing is steady. "
    elif state1.der_inflow=='0' and state2.der_inflow=='-':
        trace+="we are closing the tap , so the rate of water is flowing decreasing. "
    elif state1.der_inflow=='-' and state2.der_inflow=='0':
        trace+="we stopped turning the tap , so the rate of water is steady. "

    #Volume
    if state1.mar_volume=='0' and state2.mar_volume=='+':
        trace+="Container from no water now has some water. "

    if state1.mar_volume=='+' and state2.mar_volume=='0':
        trace+="Container become empty. "

    if state1.mar_volume=='+' and state2.mar_volume=='max':
        trace+="Container from no water now has some water."

    if state1.der_volume=='0' and state2.der_volume=='+':
        trace+="The amount of water in the container start to increases. "
    elif state1.der_volume=='+' and state2.der_volume=='0':
        trace+="The amount of water in the container become steady. "
    elif state1.der_volume=='0' and state2.der_volume=='-':
        trace+="The amount of water in the container start to decreases. "
    elif state1.der_volume=='-' and state2.der_volume=='0':
        trace+="The amount of water in the container become steady. "

    #Outflow
    if state1.mar_outflow=='0' and state2.mar_outflow=='+':
        trace+="Water start flowing thought the sink. "

    if state1.mar_outflow=='+' and state2.mar_outflow=='0':
        trace+="Water stop flowing thought the sink. "

    if state1.mar_outflow=='+' and state2.mar_outflow=='max':
        trace+="Water flow become has its maximun capacity. "

    if state1.der_outflow=='0' and state2.der_outflow=='+':
        trace+="The amount of water flowing out through the sink start increase. "
    elif state1.der_outflow=='+' and state2.der_outflow=='0':
        trace+="The amount of water flowing out through the sink becomes steady. "
    elif state1.der_outflow=='0' and state2.der_outflow=='-':
        trace+="The amount of water flowing out through the sink start to decrease. "
    elif state1.der_outflow=='-' and state2.der_outflow=='0':
        trace+="The amount of water flowing out through the sink becomes steady. "

    return trace

def posible_states():

    states=[]
    for i_marg in ['0','+']:
        for i_der in ['-','0','+']:
            for v_marg in ['0','+','max']:
                for v_der in ['-','0','+']:
                    for o_marg in ['0','+','max']:
                        for o_der in ['-','0','+']:
                            #print (i_marg)
                            state_new=state(i_marg,i_der,v_marg,v_der,o_marg,o_der)
                            states.append(state_new)
                            #print(state_new.__repr__)
    return states

def main():
    states=[]
    Inflow=entity(['0','+'])
    Outflow=entity(['0','+','max'])
    Volume=entity(['0','+','max'])

    states=posible_states()
    G=createStateGraph(states)
    print("Trace for the senario where the water flowing increasing\n")
    increasing_scenario(states)
    print("\n\n\nTrace for the senario where the water flowing decreasing\n")
    decreaseing_scenario(states)
    #print(len(states))
    #for state in states:
        #print (state)

if __name__ == '__main__':
    main()
