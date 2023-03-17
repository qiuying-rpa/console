import json


def generate_python_code(process_info):
    prefix_str = 'import qiuying\n\n'
    python_row_code_list = []
    for process in process_info["processes"]:
        python_row_code_list.append("# " + process["name"])
        param_list = []
        if process["params"]:
            for param in process["params"]:
                param_list.append(param["field"] + "=" + param["default"] if param["default"] else param["field"])
        params = ", ".join(param_list)
        python_row_code_list.append("def " + process["method"] + "(" + params + "):")
        python_row_code_list += analysis_nodes(process["nodes"])
        python_row_code_list.append("\nmain()\n")
    return prefix_str + "\n".join(python_row_code_list)


def generate_condition_code(condition_type, conditions):
    condition_list = []
    for condition in conditions:
        if condition["middle"] == "truthy":
            condition_list.append(condition["left"])
        elif condition["middle"] == "falsy":
            condition_list.append("not " + condition["left"])
        else:
            condition_list.append(" ".join([condition["left"], condition["middle"], condition["right"]]))
    return condition_type.join(condition_list)


def analysis_nodes(nodes, layer=1):
    python_row_code_list = []
    prefix_str = " " * (layer * 4)
    for node in nodes:
        code_list = []
        if node["func"] == "exec-conditional":
            condition_type = " and " if node["kwargs"]["type"] == "all" else " or "
            condition_code = generate_condition_code(condition_type, node["kwargs"]["conditions"])
            code_list.append(f'{prefix_str}if {condition_code}:')
            true_code_list = analysis_nodes(node["kwargs"]["executionTruthy"], layer=layer + 1) \
                if node["kwargs"]["executionTruthy"] \
                else [(" " * (layer + 1) * 4) + "pass"]
            code_list += true_code_list
            code_list.append(prefix_str + "else:")
            false_code_list = analysis_nodes(node["kwargs"]["executionFalsy"], layer=layer + 1) \
                if node["kwargs"]["executionFalsy"] \
                else [(" " * (layer + 1) * 4) + "pass"]
            code_list += false_code_list
        elif node["func"] == "exec-circular":
            circular_type = "for" if node["kwargs"]["type"] == "iteration" else "while"
            if circular_type == "for":
                code_list.append(
                    f'{prefix_str}for {node["kwargs"]["iterationConf"]["index"]}, {node["kwargs"]["iterationConf"]["item"]} in enumerate({node["kwargs"]["iterationConf"]["target"]}):')
            else:
                condition_type = "and" if node["kwargs"]["type"].startswith("all") else "or"
                condition_code = generate_condition_code(condition_type, node["kwargs"]["conditions"])
                code_list.append(f'{prefix_str}while {condition_code}:')
            exec_code = analysis_nodes(node["kwargs"]["execution"], layer=layer + 1)
            code_list += exec_code
        elif node["func"] == "set-variable":
            python_row_code = prefix_str + node["kwargs"]["variable"] + " = " + node["kwargs"]["variableValue"]
            code_list.append(python_row_code)
        else:
            if node["func"] == 'set-variable':
                method_code = f'{node["kwargs"]["variable"]} = {node["kwargs"]["variableValue"]}'
            elif node["func"] == 'print-log':
                method_code = f'print({node["kwargs"]["content"]})'
            else:
                ret = node["kwargs"].get("ret") or ''
                if ret:
                    del node['kwargs']['ret']
                    ret += " = "
                param_list = []
                if node["kwargs"]:
                    for key, value in node["kwargs"].items():
                        param_list.append(key + "=" + value)
                params = ", ".join(param_list)
                method_code = ret + 'qiuying.' + node["func"] + "(" + params + ")"

            # method_code = f'{node["func"]}(**{node["kwargs"]})'
            python_row_code = prefix_str + method_code
            code_list.append(python_row_code)
        python_row_code_list += code_list
    return python_row_code_list


if __name__ == '__main__':
    json_file = "nodes.json"
    with open(json_file, 'r', encoding="utf-8") as fp:
        json_data = json.load(fp)
    print(generate_python_code(json_data))
