import requests

def generate_report(ph, moisture, density, organic, strength, usage):

    # Prompt for AI
    prompt = f"""
    Generate a professional soil analysis report.

    Soil Data:
    - pH: {ph}
    - Moisture: {moisture}%
    - Density: {density}
    - Organic Content: {organic}%
    - Strength: {strength}
    - Usage: {usage}

    Include:
    1. Soil condition explanation
    2. Risks involved
    3. Improvement suggestions
    4. Final conclusion
    """

    # Send request to Ollama (LLaMA3)
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    # Return AI response
    return response.json()["response"]