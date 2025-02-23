import ollama

def handle_prompt(prompt):
    response = ollama.chat(
        model='lappy',  # Specify model explicitly
        messages=[{"role": "user", "content": prompt}],
            
    )
    
    print(response['message']['content'])  # Extract content safely
    return response['message']['content']


