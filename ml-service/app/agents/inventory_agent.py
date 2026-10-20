from google import genai
from app.clients.inventory_client import check_inventory
import json
from app.agents.tools.inventory import check_inventory_function
from app.agents.tools.documents import retrieve_matching_doc_function, retrieve_matching_doc
import time
import faulthandler
import os

api_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

def run_agentic_loop(user_prompt : str):
    print("running loop")
    system_message = "You assist a supermarket store manager. Use check_inventory to retrieve current stock for a specific inventory record. " \
    "The tool requires an inventory ID, which is different from a product ID. If the user does not provide an inventory ID, ask for it. " \
    "Never invent IDs or stock quantities. If a lookup fails, explain the failure without treating it as zero stock. Answer concisely using the tool result." \
    "Preserve returned values. Do not infer currency or units when absent. Flag negative stock as an inventory discrepancy. Describe stock as recorded stock."
    first_call_start = time.perf_counter()
    print(f"execution time before the model call {first_call_start}")
    faulthandler.dump_traceback_later(15, repeat=False)
    try:
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input = user_prompt,
            system_instruction = system_message,
            tools=[check_inventory_function, retrieve_matching_doc_function],
            timeout = 60,
        )
    except Exception:
        print(
            f"Model call failed after "
            f"{time.perf_counter() - first_call_start:.2f} seconds",
            flush=True,
        )
        raise
    finally:
        faulthandler.cancel_dump_traceback_later()
    print(f"First Gemini call duration: {time.perf_counter() - first_call_start}")
    for i in range(3):
        results = []
        for step  in interaction.steps:

            print("Step type:", step.type)
            if step.type == "function_call":
                if step.name=="retrieve_matching_doc":
                    retrieving_chunks_start = time.perf_counter()
                    result = retrieve_matching_doc(step.arguments["query"])
                    print(f"result {result}")
                    results.append({
                                        "type": "function_result",
                                        "name": step.name,
                                        "call_id": step.id,
                                        "result": [{"type": "text", "text": json.dumps(result)}],
                                    })
                    print(f"Document retrieval: {time.perf_counter() - retrieving_chunks_start}")
                elif step.name=="check_inventory":
                    result = check_inventory(step.arguments["id"])
                    print(f"check inventory {id} {results}")
                    results.append({
                                        "type": "function_result",
                                        "name": step.name,
                                        "call_id": step.id,
                                        "result": [{"type": "text", "text": json.dumps(result)}],
                                    })
                else: continue    
        if not results:
            return interaction.output_text            
        second_call_start = time.perf_counter()    
        print("Number of tool results:", len(results))     
        faulthandler.dump_traceback_later(15, repeat=False)
        try:   
            interaction = client.interactions.create(
                model="gemini-3.8-flash",
                input= results,
                system_instruction = system_message,
                tools=[check_inventory_function, retrieve_matching_doc_function],
                previous_interaction_id=interaction.id,
                timeout = 60,
            )
        except Exception:
                print(
                    f"Model call failed after "
                    f"{time.perf_counter() - second_call_start:.2f} seconds",
                    flush=True,
                )
                raise
        finally:
            faulthandler.cancel_dump_traceback_later()    
        print(f"Second Gemini call duration: {time.perf_counter() - second_call_start}")

        print("Second status:", interaction.status)
        print("Second text:", repr(interaction.output_text))

        for step in interaction.steps:
            print("Second step type:", step.type)
            if step.type == "function_call":
                print("Requested tool:", step.name, step.arguments)
    return interaction.output_text

if __name__ == "__main__":
    query1 = "Check the recorded stock for inventory ID 1 and explain what action I should take according to our inventory policy."
    query2 = "According to our inventory policy, what should staff do when recorded stock falls below the minimum stock level?"
    response = run_agentic_loop(query1)
    print(response)