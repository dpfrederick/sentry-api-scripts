import argparse
import json
import os
from datetime import datetime

from dotenv import load_dotenv

from .backstage import check_team_exists
from .sentry import list_projects_for_org


def create_csv_file_with_project_and_teams(
    org_slug: str, sentry_api_token: str, backstage_base_url: str
):
    projects = list_projects_for_org(org_slug, sentry_api_token)

    date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    with open(f"output/output-{date}.csv", "w") as f:
        f.write("project,team,team exists in backstage\n")

        for project in projects:
            teams_to_list = [
                team["slug"]
                for team in project["teams"]
                if team["slug"] not in ["noc-team", "engineering-productivity"]
            ]

            try:
                team_exists_in_backstage = check_team_exists(
                    teams_to_list[0], backstage_base_url
                )
            except IndexError:
                team_exists_in_backstage = "check it yourself"

            f.write(
                f"{project['slug']},{','.join(teams_to_list)}, {team_exists_in_backstage}\n"
            )


def main():
    load_dotenv(".env")
    backstage_base_url = os.environ.get("BACKSTAGE_BASE_URL")
    sentry_api_token = os.environ.get("SENTRY_API_TOKEN")
    parser = argparse.ArgumentParser(
        description="Create an output csv file containing projects and teams, and whether the team exists in backstage."
    )
    parser.add_argument("organization", help="The organization slug")
    args = parser.parse_args()

    create_csv_file_with_project_and_teams(
        args.organization, sentry_api_token, backstage_base_url
    )


if __name__ == "__main__":
    main()
