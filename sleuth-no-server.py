import requests
from collections import defaultdict
from jinja2 import Template

art = '''
 ___________  __    __    _______      ___      ___       __        _______   __   ___  _______  ___________       ________  ___       _______  ____  ____  ___________  __    __      
("     _   ")/" |  | "\  /"     "|    |"  \    /"  |     /""\      /"      \ |/"| /  ")/"     "|("     _   ")     /"       )|"  |     /"     "|("  _||_ " |("     _   ")/" |  | "\     
 )__/  \\__/(:  (__)  :)(: ______)     \   \  //   |    /    \    |:        |(: |/   /(: ______) )__/  \\__/     (:   \___/ ||  |    (: ______)|   (  ) : | )__/  \\__/(:  (__)  :)    
    \\_ /    \/      \/  \/    |       /\\  \/.    |   /' /\  \   |_____/   )|    __/  \/    |      \\_ /         \___  \   |:  |     \/    |  (:  |  | . )    \\_ /    \/      \/     
    |.  |    //  __  \\  // ___)_     |: \.        |  //  __'  \   //      / (// _  \  // ___)_     |.  |          __/  \\   \  |___  // ___)_  \\ \__/ //     |.  |    //  __  \\     
    \:  |   (:  (  )  :)(:      "|    |.  \    /:  | /   /  \\  \ |:  __   \ |: | \  \(:      "|    \:  |         /" \   :) ( \_|:  \(:      "| /\\ __ //\     \:  |   (:  (  )  :)    
     \__|    \__|  |__/  \_______)    |___|\__/|___|(___/    \___)|__|  \___)(__|  \__)\_______)     \__|        (_______/   \_______)\_______)(__________)     \__|    \__|  |__/     
                                                                                                                                                                                       
                                                                                                                                                                                       
                                                                                                                                                                                       
                                                                                                                                                                                       
                                                                                                                                                                                       
                                                                                                                                                                                       
                                                                                                                                                                                       
                                                                                                                                                                                       
                                                                                                                                                                                       
 _______  ___  ___  ____                                                                                                                                                               
|   _  "\|"  \/"  |))_ ")                                                                                                                                                              
(. |_)  :)\   \  /(____(                                                                                                                                                               
|:     \/  \\  \/  _____                                                                                                                                                               
(|  _  \\  /   /   ))_ ")                                                                                                                                                              
|: |_)  :)/   /   (____(                                                                                                                                                               
(_______/|___/                                                                                                                                                                         
                                                                                                                                                                                       
                                                                                                                                                                                       
                                                                                                                                                                                       
                                                                                                                                                                                       
                                                                                                                                                                                       
                                                                                                                                                                                       
                                                                                                                                                                                       
                                                                                                                                                                                       
                                                                                                                                                                                       
 _______    _______  _____  ___        ________                                                                                                                                        
|   _  "\  /"     "|(\"   \|"  \      /"       )                                                                                                                                       
(. |_)  :)(: ______)|.\\   \    |    (:   \___/                                                                                                                                        
|:     \/  \/    |  |: \.   \\  |     \___  \                                                                                                                                          
(|  _  \\  // ___)_ |.  \    \. |      __/  \\  _____                                                                                                                                  
|: |_)  :)(:      "||    \    \ |     /" \   :)))_  ")                                                                                                                                 
(_______/  \_______) \___|\____\)    (_______/(_____(                                                                                                                                  
                                                                                                                                                                                       
'''


print(art)






def get_social_media_results(query):
    url = "https://social-links-search.p.rapidapi.com/search-social-links"
    querystring = {
        "query": query,
        "social_networks": "facebook,tiktok,instagram,snapchat,twitter,youtube,linkedin,github,pinterest"
    }
    headers = {
        "X-RapidAPI-Key": "Input your key here, or better yet... env variable.",
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






def save_html(html, filename):
    with open(filename, 'w') as f:
        f.write(html)

if __name__ == "__main__":
    query = str(input('Input your search query here:'))
    results = get_social_media_results(query)
    aggregated_results = aggregate_results(results)
    html = generate_html(aggregated_results)
    save_html(html, "search_results.html")
