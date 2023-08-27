import csv
import openai
import concurrent.futures
from typing import List

openai.api_key = 'ADD OPENAI API KEY HERE'  

def get_ai_response(prompt: str, system_message: str) -> str:
    print("Getting AI response...")
    model = "gpt-3.5-turbo"
    messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
    result = openai.ChatCompletion.create(model=model, messages=messages, max_tokens=3000)  # set your desired max tokens
    print("AI response received.")
    return result["choices"][0]["message"]["content"]

def process_input_csv_file(input_file_name: str, output_file_name: str, system_message_file: str):
    print("Processing input CSV file...")
    with open(input_file_name, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)
    print("Input CSV file processed.")

    print("Reading system message file...")
    with open(system_message_file, 'r') as file:
        system_message = file.read()
    print("System message file read.")

    prompts = [row[0] for row in rows]  # assuming prompt is on the first column

    print("Starting ThreadPoolExecutor...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        data_for_executor = [(prompt, system_message) for prompt in prompts]
        future_to_data = {executor.submit(get_ai_response, prompt, system_prompt): (prompt, system_prompt) for (prompt, system_prompt) in data_for_executor}
        for future in concurrent.futures.as_completed(future_to_data):
            (prompt, system_prompt) = future_to_data[future]
            try:
                print(f"Processing prompt: {prompt}")
                ai_response = future.result()
                with open(output_file_name, 'a', newline='') as file:  # use the mode 'a' for appending
                    writer = csv.writer(file)
                    writer.writerow([prompt, system_prompt, ai_response])
                print(f"Prompt: {prompt} processed.")
            except Exception as exc:
                print(f'Generating output for {prompt} generated an exception: {exc}')
    print("ThreadPoolExecutor finished.")

process_input_csv_file('input.csv', 'output.csv', 'system_prompt.txt')