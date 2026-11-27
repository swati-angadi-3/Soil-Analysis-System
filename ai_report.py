import json

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"  # for faster output on a weak PC, try "llama3.2:3b"


def _describe_ph(ph):
    if ph < 6.5:
        return "acidic"
    if ph <= 7.5:
        return "near neutral"
    return "alkaline"


def _describe_density(density):
    if density >= 1.5:
        return "dense (good load bearing)"
    if density >= 1.3:
        return "medium density"
    return "loose (low load bearing)"


def _describe_moisture(moisture):
    if moisture > 50:
        return "high (waterlogged risk)"
    if moisture >= 25:
        return "moderate"
    return "low"


def generate_report_stream(ph, moisture, density, organic, strength, usage):
    """Yield the report text piece by piece as the model writes it.
    Raises a requests exception if Ollama is not reachable."""

    prompt = f"""Write a short soil analysis report (maximum 250 words) in plain text.

Soil data:
- pH {ph} ({_describe_ph(ph)})
- Moisture {moisture}% ({_describe_moisture(moisture)})
- Bulk density {density} g/cm3 ({_describe_density(density)})
- Organic matter {organic}%
- Classification: {strength}
- Recommended use: {usage}

Rules you must follow:
- Use the descriptions given in brackets above. Do not contradict them.
- pH below 7 is acidic, 7 is neutral, above 7 is alkaline. Never call an acidic pH neutral.
- Your risks and improvements must match the recommended use. For construction, talk about
  load bearing, settlement, drainage and compaction. For agriculture, talk about crops and fertility.
- Do not suggest changes that contradict the classification.

Use these four headings:
Condition, Risks, Improvements, Conclusion.
Keep each section to 2-3 sentences."""

    with requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": True,
            "keep_alive": "30m",
            "options": {"num_predict": 350, "temperature": 0.2},
        },
        stream=True,
        timeout=(5, 120),
    ) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            chunk = json.loads(line)
            if chunk.get("response"):
                yield chunk["response"]
            if chunk.get("done"):
                break