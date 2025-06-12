#!/usr/bin/env python3
import sys
import re
import ast
from graphviz import Digraph

def parse_log(file_path):
    orchestration_re = re.compile(r'Orchestration started for goal: (.+) \(depth=(\d+)\)')
    run_re = re.compile(r'OllamaClient: running (.+)')
    nodes = {}
    edges = []
    context_stack = []   # stack of {'id':..., 'depth':...}
    node_counter = 0

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 1) Orchestration start → a new “goal” node
            m = orchestration_re.search(line)
            if m:
                goal_text, depth_s = m.group(1), m.group(2)
                depth = int(depth_s)
                # Pop contexts at same or deeper depth
                while context_stack and context_stack[-1]['depth'] >= depth:
                    context_stack.pop()
                node_id = f"n{node_counter}"
                nodes[node_id] = {
                    'label': goal_text,
                    'model': None,
                    'prompt': None
                }
                if context_stack:
                    parent_id = context_stack[-1]['id']
                    edges.append((parent_id, node_id))
                context_stack.append({'id': node_id, 'depth': depth})
                node_counter += 1
                continue

            # 2) Model run → a new “run” node under the last orchestration
            m2 = run_re.search(line)
            if m2:
                list_str = m2.group(1)
                try:
                    parts = ast.literal_eval(list_str)
                    # ollama run invocations: [ 'ollama', 'run', MODEL, PROMPT, ... ]
                    model = parts[2]
                    prompt = parts[3].strip().replace('\n', '\\n')
                except Exception:
                    continue

                node_id = f"n{node_counter}"
                nodes[node_id] = {
                    'label': None,
                    'model': model,
                    'prompt': prompt
                }
                if context_stack:
                    parent_id = context_stack[-1]['id']
                    edges.append((parent_id, node_id))
                node_counter += 1

    return nodes, edges

def render_tree(nodes, edges, outname='model_tree'):
    # Collect all model types
    model_types = sorted({n['model'] for n in nodes.values() if n['model']})
    # assign colors
    palette = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'grey']
    colors = {mt: palette[i % len(palette)] for i, mt in enumerate(model_types)}

    dot = Digraph(comment="LLM Call Tree")
    dot.attr('node', style='filled', fontname='Helvetica')

    # add nodes
    for nid, data in nodes.items():
        if data['model']:
            label = f"{data['model']}\\n{data['prompt'][:40]}..."
            dot.node(nid, label=label, fillcolor=colors[data['model']])
        else:
            dot.node(nid, label=data['label'], shape='box', fillcolor='lightgrey')

    # add edges
    for parent, child in edges:
        dot.edge(parent, child)

    # render to PDF (or PNG)
    dot.render(outname, format='pdf', view=True)
    print(f"Rendered tree to {outname}.pdf")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python plot_model_tree.py <log-file>")
        sys.exit(1)
    nodes, edges = parse_log(sys.argv[1])
    render_tree(nodes, edges)
