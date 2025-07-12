import ollama
import re

# Prompt to send to the model
prompts1 = [
    {"role": "system", "content": "You are a helpful assistant that responds in Markdown."},
    {"role": "user", "content": "How do I decide if a business problem is suitable for an LLM solution? Please respond in Markdown."}
]

# Request model output in streaming mode with temperature set for creativity
stream = ollama.chat(
    model="llama3.2",
    messages=prompts1,
    stream=True,  # Enables real-time output (streaming chunks)
    options={"temperature": 0.7}  # Controls randomness (0.0 = strict, 1.0 = creative)
)

# Process and clean each streamed chunk of content
for chunk in stream:
    # Extract only the message content from the chunk
    content = chunk.get("message", {}).get("content", "")

    # Step 1: Convert Markdown headings like ### Heading into bold section headers
    content = re.sub(r'^#{1,6}\s*(.+)', r'\n\1\n' + '-' * 40, content, flags=re.MULTILINE)

    # Step 2: Remove remaining Markdown formatting characters
    content = content.replace("**", "")   # Remove bold markers
    content = content.replace("*", "")    # Remove italic markers
    content = content.replace("`", "")    # Remove inline code markers

    # Step 3: Print in real-time without line breaks between chunks
    print(content, end="", flush=True)  # flush=True forces real-time printing