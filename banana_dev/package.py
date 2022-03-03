from .generics import run_main, start_main, check_main
import concurrent.futures

# Generics
def run(api_key, model_key, model_inputs, strategy = {}):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(run_main,
        api_key = api_key, 
        model_key = model_key, 
        model_inputs = model_inputs,
        strategy = strategy)
        out = future.result()
        return out

def start(api_key, model_key, model_inputs, strategy = {}):
    out = start_main(
        api_key = api_key, 
        model_key = model_key, 
        model_inputs = model_inputs,
        strategy = strategy,
    )
    return out
    
def check(api_key, task_id):
    out_dict = check_main(
        api_key = api_key,
        task_id = task_id
    )
    return out_dict
