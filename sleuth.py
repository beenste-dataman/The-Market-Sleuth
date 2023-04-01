import requests
from collections import defaultdict
from jinja2 import Template
import os
import http.server
import socketserver
import webbrowser
import threading
import click
import socket






def get_social_media_results(query):
    url = "https://social-links-search.p.rapidapi.com/search-social-links"
    querystring = {
        "query": query,
        "social_networks": "facebook,tiktok,instagram,snapchat,twitter,youtube,linkedin,github,pinterest"
    }
    headers = {
        "X-RapidAPI-Key": "Put your key here, or just use an env variable like an adult.",
        "X-RapidAPI-Host": "social-links-search.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()["data"]




def aggregate_results(results):
    aggregated = defaultdict(list)
    for network, links in results.items():
        for link in links:
            aggregated[network].append({'network': network, 'url': link})
    return aggregated




def generate_html(aggregated_results):
    html = """
<html>
<head>
<style>
    body {
        font-family: Arial, sans-serif;
        display: flex;
        height: 100vh;
        margin: 0;
        padding: 0;
        background-color: #f0f2f5;
    }

    .sidebar {
        width: 250px;
        background-color: #343a40;
        padding: 30px;
        box-sizing: border-box;
        overflow-y: auto;
    }

    .content {
        flex: 1;
        padding: 30px;
        box-sizing: border-box;
        overflow-y: auto;
        background-color: #ccffcc;
        border-radius: 6px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    h1 {
        font-size: 2rem;
        color: #ffffff;
        margin-bottom: 40px;
    }

    ul {
        list-style-type: none;
        padding: 0;
        margin: 0;
    }

    li {
        cursor: pointer;
        padding: 10px 0;
        border-bottom: 1px solid #495057;
    }

    li:last-child {
        border-bottom: none;
    }

    li:hover {
        background-color: #495057;
    }

    .results {
        display: none;
    }

    .results h1 {
        color: #343a40;
    }

    .results ul {
        padding-left: 20px;
    }

    .results li {
        border-bottom: none;
    }

    a {
        color: #2196F3;
        text-decoration: none;
    }

    a:hover {
        text-decoration: underline;
    }
</style>
<script>
    function showResults(id) {
        const results = document.getElementsByClassName('results');
        for (let i = 0; i < results.length; i++) {
            results[i].style.display = 'none';
        }
        document.getElementById(id).style.display = 'block';
    }
</script>
</head>
<body>
    """

    html += '<div class="sidebar">'
    html += "<h1>Social Networks</h1>"
    html += "<ul>"
    for i, network in enumerate(aggregated_results.keys()):
        html += f'<li onclick="showResults(\'results-{i}\')">{network}</li>'
    html += "</ul>"
    html += "</div>"

    html += '<div class="content">'
    for i, (network, results) in enumerate(aggregated_results.items()):
        html += '<div class="results" id="results-' + str(i) + '"' + (' style="display: block;"' if i == 0 else '') + '>'
        html += f'<h1>{network}</h1>'
        html += "<ul>"
        for result in results:
            url = result['url']
            html += f"<li><a href='{url}' target='_blank'>{url}</a></li>"
        html += "</ul>"
        html += "</div>"
    html += "</div>"

    html += "</body></html>"
    return html












def serve_html(filename, port=8000):
    available_port = find_available_port(port)
    webbrowser.open(f'http://localhost:{available_port}/{filename}')
    os.chdir("output")

    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", available_port), Handler)

    def run_server():
        click.echo(f'Serving on {click.style(f"http://localhost:{available_port}", fg="blue", underline=True)}...')
        httpd.serve_forever()

    t = threading.Thread(target=run_server)
    t.start()

    input("Press enter to stop the server...")
    httpd.shutdown()

def find_available_port(port):
    while True:
        try:
            with socket.create_server(('localhost', port)):
                return port
        except OSError:
            port += 1



def display_summary_stats(aggregated_results):
    print("Summary statistics:")
    total_count = 0
    for network, results in aggregated_results.items():
        count = len(results)
        total_count += count
        print(f"{network.capitalize()}: {count} results")
    print(f"Total: {total_count} results")







def save_html(html, filename):
    if not os.path.exists("output"):
        os.makedirs("output")
    with open(os.path.join("output", filename), "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    query = str(input('Input your search query here:'))
    results = get_social_media_results(query)
    aggregated_results = aggregate_results(results)
    html = generate_html(aggregated_results)
    save_html(html, "search_results.html")
    display_summary_stats(aggregated_results)
    serve_html("search_results.html")

