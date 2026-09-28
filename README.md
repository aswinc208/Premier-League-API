<h1>Premier League API 2.0</h1>
  <p>This is an unofficial Flask API for current Premier League player stats, fixtures, and standings. Player data comes from the Premier League API; fixtures and standings are scraped from OneFootball.</p>


<h2>API Endpoints</h2>

<p>The application provides the following API endpoints:</p>
<h3>GET /fixtures</h3>
<p>Returns the fixtures currently listed on OneFootball's Premier League fixtures page.</p>

<h3>GET  /players/{player_name}</h3>
<p>Returns profile information and current-season statistics for a current Premier League player. The player name should be provided as a URL parameter.</p>
<p>The API returns a JSON object with the following structure:</p>
<pre><code>{
  "name": "Erling Haaland",
  "position": "Centre Striker",
  "club": "Manchester City",
  "Nationality": "Norway",
  "Date of Birth": "21 July 2000",
  "Height": "195 cm",
  "key_stats": { "appearances": 5, "goals": 5 }
}</code></pre>


<h3>GET /table</h3>
<p>Returns a table array. The first row contains column names; subsequent rows contain each team's position, name, played, wins, draws, losses, goal difference, and points.</p>

<h3>GET /fixtures/{team_name}</h3>
<p>Filters the currently listed fixtures to those containing the requested team name.</p>

<h2>Instructions to run this repo</h2>
<p>Install Python 3.11, open a terminal in the repository folder, then create and activate a virtual environment and install the dependencies:</p>

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

<p>Start the Flask API:</p>

```bat
python main.py
```

<p>Keep that terminal open and visit <a href="http://127.0.0.1:5000/">http://127.0.0.1:5000/</a>. Example endpoints:</p>

<ul>
  <li><a href="http://127.0.0.1:5000/fixtures">/fixtures</a></li>
  <li><a href="http://127.0.0.1:5000/fixtures/Arsenal">/fixtures/Arsenal</a></li>
  <li><a href="http://127.0.0.1:5000/players/Haaland">/players/Haaland</a></li>
  <li><a href="http://127.0.0.1:5000/table">/table</a></li>
</ul>

<p>Player lookup searches the current Premier League season. Stop the server with Ctrl+C.</p>



<H2>Individual PLayer PL Stats</H2> 
<ul>
  <li>Example response for a current Premier League player. Player lookup accepts a name such as Haaland.</li>
  <br> <img src="assets/player_stats.png"><br>
</ul>
 <H2>Premier League Table</H2> 
<ul>
  <li>Current Premier League Table</li>
  <br> <img src="assets/table.png"><br>
 </ul>
 <H2>Premier League Fixtures </H2> 
<ul>
  <li>Fixtures currently listed by OneFootball</li>
  <br> <img src="assets/fixtures.png"> <br>
 </ul>
<H2>Update 🚀 </H2>
The API has been enhanced with new features and improvements:
<ul>
  <li>✨ Optimized the code for better performance.</li>
  <li>🔄 Rebased and updated to ensure compatibility with the latest dependencies.</li>
</ul>
You can also search player stats using the player's reference image ( Face Recognition ) as well - <a href=https://github.com/tarun7r/Premier-League-Face-Recognition>Repo</a> 📸

<H2>Disclaimer</H2>
This project is created solely for learning and educational purposes. It is not intended for production-level use or commercial applications
