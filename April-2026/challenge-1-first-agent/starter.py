"""
Challenge 1: Your First AI Agent
Build a simple agent using Strands SDK + Ollama (runs locally!)

Instructions:
  1. Fill in the TODO sections below
  2. Run: python starter.py
  3. Make sure 'ollama serve' is running in another terminal
"""

from strands import agents

from strands.models.ollama import OllamaModel


ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.2:3b"
)


agent = Agent(
    model=ollama_model,
    tools=[],
    system_prompt="You are a helpful assistant. Be brief."
)

print("🤖 Agent: ", end="")

response = agent(
    "Tell me a fun fact about Python programming"
)

print(response)

print("\n✅ Challenge 1 complete!")
