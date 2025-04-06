import requests
import xml.etree.ElementTree as ET
from typing import List, Optional


def find_top_x_drivers_at_race_n(
    year: int, driver_positions: int, race_number: int
) -> List[str]:
    url = "http://ergast.com/api/f1/{}/{}/driverStandings".format(year, race_number)
    try:
        # Make the API call
        response = requests.get(url)
        response.raise_for_status()

        # Parse the XML content from the response text
        xml_content = response.text
        root = ET.fromstring(xml_content)

        # Define the namespace (must match the xmlns attribute in the XML)
        namespaces = {"mrd": "http://ergast.com/mrd/1.5"}

        # Find all DriverStanding elements using the namespace
        all_standings = root.findall(".//mrd:DriverStanding", namespaces=namespaces)

        top_x_drivers_list = []

        count = 0
        # Iterate and filter by position attribute
        for standing in all_standings:
            position = int(standing.get("position", 999))  # Get attribute, default high

            if 1 <= position <= driver_positions:
                count += 1
                # Find driver names within this standing element
                driver = standing.find("mrd:Driver", namespaces=namespaces)
                if driver is not None:
                    given_name_elem = driver.find(
                        "mrd:GivenName", namespaces=namespaces
                    )
                    family_name_elem = driver.find(
                        "mrd:FamilyName", namespaces=namespaces
                    )

                    given_name = (
                        given_name_elem.text if given_name_elem is not None else "N/A"
                    )
                    family_name = (
                        family_name_elem.text if family_name_elem is not None else "N/A"
                    )
                    top_x_drivers_list.append(f"{given_name} {family_name}")

                else:
                    print(f"{position}. Driver info not found")

            # Stop after finding the first 3. The list is always sorted
            if count >= driver_positions:
                break

        print(f"{year} top {driver_positions} drivers at race #3: {top_x_drivers_list}")
        return top_x_drivers_list

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def find_winner(year: int) -> Optional[str]:
    url = "http://ergast.com/api/f1/{}/driverStandings".format(year)
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Parse the XML content from the response text
        xml_content = response.text
        root = ET.fromstring(xml_content)

        namespaces = {"mrd": "http://ergast.com/mrd/1.5"}

        all_standings = root.findall(".//mrd:DriverStanding", namespaces=namespaces)

        count = 0

        # Iterate and filter by position attribute
        for standing in all_standings:
            position = int(standing.get("position", 999))  # Get attribute, default high

            if position == 1:
                count += 1
                # Find driver names within this standing element
                driver = standing.find("mrd:Driver", namespaces=namespaces)
                if driver is not None:
                    given_name_elem = driver.find(
                        "mrd:GivenName", namespaces=namespaces
                    )
                    family_name_elem = driver.find(
                        "mrd:FamilyName", namespaces=namespaces
                    )

                    given_name = (
                        given_name_elem.text if given_name_elem is not None else "N/A"
                    )
                    family_name = (
                        family_name_elem.text if family_name_elem is not None else "N/A"
                    )
                    print(f"{year} winner: {given_name} {family_name}")
                    return f"{given_name} {family_name}"

                else:
                    print("Driver info not found")

            # Stop after finding the first 1. The list is always sorted
            if count >= 1:
                break

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    prediction_mathces = 0
    for year in range(1950, 2024):
        top_x_drivers_list_at_race_n = find_top_x_drivers_at_race_n(
            year,
            3,  # at race #3
            5,  # first 5 drivers in standings
        )
        winner = find_winner(year)

        if winner in top_x_drivers_list_at_race_n:
            prediction_mathces += 1

    prediction_freq = (prediction_mathces / (2024 - 1950)) * 100
    print(
        f"The prediction came true {prediction_mathces} times out of {2024 - 1950} years"
    )
    print(f"The frequency is {prediction_freq}%")


if __name__ == "__main__":
    main()
