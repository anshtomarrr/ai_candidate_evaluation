from flask import Flask, render_template_string
import json

app = Flask(__name__)

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Candidate Rankings</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .Excellent { background: #c8e6c9; }
        .Good { background: #fff9c4; }
        .Average { background: #ffe0b2; }
        .Below\ Average { background: #ffcdd2; }
    </style>
</head>
<body>
    <h1>Candidate Rankings</h1>
    <table>
        <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Score</th>
            <th>Tier</th>
            <th>Pros</th>
            <th>Cons</th>
        </tr>
        {% for c in candidates %}
        <tr class="{{c['tier']}}">
            <td>{{c['name']}}</td>
            <td>{{c['email']}}</td>
            <td>{{c['score']}}</td>
            <td>{{c['tier']}}</td>
            <td><ul>{% for p in c['pros'] %}<li>{{p}}</li>{% endfor %}</ul></td>
            <td><ul>{% for con in c['cons'] %}<li>{{con}}</li>{% endfor %}</ul></td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''

@app.route('/')
def index():
    with open('candidate_rankings.json') as f:
        candidates = json.load(f)
    return render_template_string(TEMPLATE, candidates=candidates)

if __name__ == '__main__':
    app.run(debug=True) 