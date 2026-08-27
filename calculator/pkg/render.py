import json


def format_json_output(expression: str, result: float, indent: int = 2) -> str:
    #Supply integer result (if applicable)
    if isinstance(result, float) and result.is_integer():
        result_to_dump = int(result)
    #Otherwise supply float result
    else:
        result_to_dump = result

    output_data = {
        "expression": expression,
        "result": result_to_dump,
    }
    return json.dumps(output_data, indent=indent)