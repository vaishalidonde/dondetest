import os
from flask import Flask, render_template_string, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HTML = """
<!doctype html>
<html>
<head><title>Donde</title>
<style>body{font-family:Arial;max-width:800px;margin:50px auto;padding:20px;}
input,button{padding:10px;margin:5px;font-size:16px;}
.recommendation{background:#f0f8ff;padding:20px;border-radius:10px;margin-top:20px;}</style>
</head>
<body>
<h1>🌃 Welcome to Donde</h1>
<p>Chicago's calm restaurant picker. Tell me your vibe, get 1-2 perfect spots.</p>

<form method="post">
  <label>Vibe (cozy, lively, romantic...):</label><br>
  <input type="text" name="vibe" style="width:100%;" required><br><br>
  
  <label>Place type (bar, Italian, cocktails...):</label><br>
  <input type="text" name="type" style="width:100%;" required><br><br>
  
  <button type="submit">Find My Spot →</button>
</form>

{% if recommendation %}
<div class="recommendation">
  <h2>🍽️ Your Donde Pick{{ 's' if 'or' in recommendation else '' }}</h2>
  <pre>{{ recommendation }}</pre>
</div>
{% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    recommendation = None
    
    if request.method == "POST":
        vibe = request.form["vibe"]
        place_type = request.form["type"]
        
        prompt = f"""
        You are Donde, Chicago's minimalist restaurant guide. 
        
        User wants: {vibe} {place_type}
        
        Suggest EXACTLY 1-2 specific Chicago venues.
        Include: name, neighborhood, 2-sentence why it fits.
        End with "Go to [venue] tonight."
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        
        recommendation = response.choices[0].message.content
    
    return render_template_string(HTML, recommendation=recommendation)

if __name__ == "__main__":
    app.run(debug=True)
