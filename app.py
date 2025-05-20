from flask import Flask, render_template, request, jsonify
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx

app = Flask(__name__)

# ----- Cycle Detection -----
def has_cycle(graph, node, visited, rec_stack):
    visited.add(node)
    rec_stack.add(node)
    for neighbor in graph.get(node, []):
        if neighbor not in visited:
            if has_cycle(graph, neighbor, visited, rec_stack):
                return True
        elif neighbor in rec_stack:
            return True
    rec_stack.remove(node)
    return False

def detect_deadlock(graph, processes):
    visited = set()
    for node in processes:
        if node not in visited:
            if has_cycle(graph, node, visited, set()):
                return True
    return False

def remove_process(graph, proc):
    if proc in graph:
        del graph[proc]
    for key in graph:
        if proc in graph[key]:
            graph[key].remove(proc)

def order(graph):
    visited = set()
    result = []
    def dfs(node):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
        result.append(node)
    for node in graph:
        if node not in visited:
            dfs(node)
    return result[::-1]

# ---------- ROUTES ----------

@app.route('/')
def index():
    return render_template('index.html')

# 🔒 Global storage
graph_cache = {
    'graph': {},
    'processes': [],
    'allocation': [],
    'request': []
}

@app.route('/detect-deadlock', methods=['POST'])
def detect_deadlock_route():
    try:
        data = request.get_json(force=True)

        processes = data['processes']
        allocation = data['allocation']
        request_matrix = data['request']

        # Store inputs globally
        graph_cache['processes'] = processes
        graph_cache['allocation'] = allocation
        graph_cache['request'] = request_matrix

        wfg = nx.DiGraph()
        for i in range(len(processes)):
            for j in range(len(processes)):
                for r in range(len(request_matrix[0])):
                    if request_matrix[i][r] > 0 and allocation[j][r] > 0:
                        wfg.add_edge(processes[i], processes[j])

        # Save graph
        pos = nx.spring_layout(wfg)
        plt.figure(figsize=(8, 6))
        nx.draw(wfg, pos, with_labels=True,node_size=2000,font_size=10, node_color='skyblue')
        plt.title("Wait-For Graph")
        plt.savefig(os.path.join('static', 'graph.png'))
        plt.close()

        graph_cache['graph'] = {node: list(wfg.successors(node)) for node in wfg.nodes}

        if detect_deadlock(graph_cache['graph'], processes):
            return jsonify({'deadlock': True, 'graphUrl': '/static/graph.png'})
        else:
            return jsonify({'deadlock': False, 'graphUrl': '/static/graph.png'})

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/recover', methods=['POST'])
def recover_route():
    try:
        data = request.get_json(force=True)
        terminate = data['terminate']

        # Copy the current graph to modify without altering original
        current_graph = {k: list(v) for k, v in graph_cache['graph'].items()}

        if terminate not in current_graph:
            return jsonify({'error': 'Invalid process entered.'}), 400

        remove_process(current_graph, terminate)
        if detect_deadlock(current_graph, graph_cache['processes']):
            return jsonify({
        'terminated': terminate,
        'deadlock': True,
        'updatedOrder': [],
        'message': 'Deadlock still present. Please choose a different process to terminate.'
    })
        else:
            updated_order = order(current_graph)
            return jsonify({
        'terminated': terminate,
        'deadlock': False,
        'updatedOrder': updated_order,
        'message': 'Deadlock handled successfully!'
    })


    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
if __name__ == '__main__':
    app.run(debug=True, port=5050)