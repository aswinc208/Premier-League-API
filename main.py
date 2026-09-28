from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import re
app = Flask(__name__)

PREMIER_LEAGUE_API = "https://footballapi.pulselive.com/football"
PREMIER_LEAGUE_API_HEADERS = {
    "Origin": "https://www.premierleague.com",
    "User-Agent": "Mozilla/5.0",
}


def premier_league_api_get(endpoint, params):
    response = requests.get(
        f"{PREMIER_LEAGUE_API}/{endpoint}",
        params=params,
        headers=PREMIER_LEAGUE_API_HEADERS,
        timeout=15,
    )
    response.raise_for_status()
    return response.json()

@app.route('/')
def index():
    return "Hey there! Welcome to the Premier League API 2.0 \n\n you can use the following endpoints:\n\n /players/<player_name> \n /fixtures \n /fixtures/<team> \n /table \n\n Enjoy!"

@app.route('/players/<player_name>', methods=['GET'])
def get_player(player_name):
    try:
        query = player_name.strip().casefold()
        seasons = premier_league_api_get(
            "competitions/1/compseasons", {"page": 0, "pageSize": 1}
        ).get("content", [])
        if not seasons:
            return jsonify({"error": "Could not find the current Premier League season."}), 502

        season_id = int(seasons[0]["id"])
        page_size = 100
        roster_params = {
            "compSeasons": season_id,
            "page": 0,
            "pageSize": page_size,
            "altIds": "true",
        }
        roster = premier_league_api_get("players", roster_params)
        player = None

        for page_number in range(roster.get("pageInfo", {}).get("numPages", 1)):
            if page_number:
                roster_params["page"] = page_number
                roster = premier_league_api_get("players", roster_params)

            player = next(
                (
                    item
                    for item in roster.get("content", [])
                    if query in item.get("name", {}).get("display", "").casefold()
                ),
                None,
            )
            if player:
                break

        if not player:
            return jsonify({"error": f"No current Premier League player matched '{player_name}'."}), 404

        player_id = int(player["id"])
        profile = premier_league_api_get(
            f"players/{player_id}",
            {"comp": 1, "compSeasons": season_id, "altIds": "true"},
        )
        stats_data = premier_league_api_get(
            f"stats/player/{player_id}", {"comp": 1, "compSeasons": season_id}
        )

        player_info = profile.get("info", {})
        birth = profile.get("birth", {})
        nationality_info = profile.get("nationalTeam", {})
        detailed_stats = {
            stat["name"]: stat.get("value")
            for stat in stats_data.get("stats", [])
            if stat.get("name")
        }

        return jsonify({
            "name": player.get("name", {}).get("display", player_name),
            "position": player_info.get("positionInfo", "Unknown"),
            "club": profile.get("currentTeam", {}).get("name", "No longer part of EPL"),
            "key_stats": detailed_stats,
            "Nationality": nationality_info.get("country", "Unknown"),
            "Date of Birth": birth.get("date", {}).get("label", "Unknown"),
            "Height": f"{profile['height']} cm" if profile.get("height") else "Unknown",
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/fixtures')
def fixtures_list():
    link = "https://onefootball.com/en/competition/premier-league-9/fixtures"
    source = requests.get(link).text
    page = BeautifulSoup(source, "lxml")
    fix = page.find_all("a", class_=re.compile(r"^MatchCard_matchCard__"))

    fixtures = []
    for match in fix:
        fixture = match.get_text(separator=" ").strip()  # Use get_text with separator
        fixtures.append(fixture)

    return jsonify({"fixtures": fixtures})


@app.route('/fixtures/<team>', methods=['GET'])
def get_fixtures(team):
    link = "https://onefootball.com/en/competition/premier-league-9/fixtures"
    source = requests.get(link).text
    page = BeautifulSoup(source, "lxml")
    fix = page.find_all("a", class_=re.compile(r"^MatchCard_matchCard__"))

    fixtures = []
    for match in fix:
        fixture = match.get_text(separator=" ").strip()  # Use get_text with separator
        fixtures.append(fixture)

    filtered_fixtures = [fixture for fixture in fixtures if team.lower() in fixture.lower()]

    return jsonify({"team_fixtures": filtered_fixtures})

@app.route('/table')
def table():
    link = "https://onefootball.com/en/competition/premier-league-9/table"
    source = requests.get(link).text
    page = BeautifulSoup(source, "lxml")

    # Find all rows in the standings table
    rows = page.find_all("li", class_=re.compile(r"^Standing_standings__row__"))

    # Initialize the table
    table = []
    table.append(["Position", "Team", "Played", "Wins", "Draws", "Losses", "Goal Difference", "Points"])

    # Extract data for each row
    for row in rows:
        position_elem = row.find("div", class_=re.compile(r"^Standing_standings__cell__"))
        team_elem = row.find("p", class_=re.compile(r"^Standing_standings__teamName__"))
        stats = row.find_all("div", class_=re.compile(r"^Standing_standings__cell__"))

        if position_elem and team_elem and len(stats) >= 8:
            position = position_elem.text.strip()
            team = team_elem.text.strip()
            played = stats[2].text.strip()
            wins = stats[3].text.strip()
            draws = stats[4].text.strip()
            losses = stats[5].text.strip()
            goal_difference = stats[6].text.strip()
            points = stats[7].text.strip()

            # Append the extracted data to the table
            table.append([position, team, played, wins, draws, losses, goal_difference, points])

    # Return the table as a JSON response
    return jsonify({"table": table})



if __name__ =="__main__":
    app.run(debug=True)
