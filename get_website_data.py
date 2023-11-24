from __future__ import annotations

import datetime
from time import sleep

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from player import Player
from player_manager import PlayerManager


def get_players(url) -> PlayerManager | None:
    manager = get_site_data(url)
    if len(manager.players) > 0:
        return manager
    return None


def get_player_site_data(url, set) -> Player | None:
    try:
        driver = webdriver.Chrome()
        driver.set_window_position(0, -1500)
        driver.get(url)
        sleep(2)
        player_dict = {}
        player_dict["link"] = driver.current_url.replace(set, "")
        try:
            player_dict["server"] = player_dict["link"].split("/")[4].upper()
            player_dict["rank"] = driver.find_element(
                by=By.CSS_SELECTOR, value="div.tier strong"
            ).text
            player_dict["lp"] = driver.find_element(
                by=By.CSS_SELECTOR, value="div.tier span"
            ).text
            player_dict["nume"] = driver.find_element(
                by=By.CSS_SELECTOR, value="div.info div h2"
            ).text
            player_dict["wins"] = driver.find_elements(
                by=By.CSS_SELECTOR, value="ul.ratings li div strong"
            )[0].text
            player_dict["winrate"] = driver.find_elements(
                by=By.CSS_SELECTOR, value="ul.ratings li div strong"
            )[1].text
            player_dict["nr. top4"] = driver.find_elements(
                by=By.CSS_SELECTOR, value="ul.ratings li div strong"
            )[2].text
            player_dict["top4"] = driver.find_elements(
                by=By.CSS_SELECTOR, value="ul.ratings li div strong"
            )[3].text
            player_dict["nr. meciuri"] = driver.find_elements(
                by=By.CSS_SELECTOR, value="ul.ratings li div strong"
            )[4].text
        except Exception as e:
            print(driver.current_url, "   ", e)
        else:
            return Player(player_dict)
    except Exception as e:
        print(e)
        return None


def get_site_data(url) -> PlayerManager | None:
    try:
        driver = webdriver.Chrome()
        driver.set_window_position(0, -1500)
        driver.get(url)
        sleep(3)
        servers_list = driver.find_elements(by=By.CSS_SELECTOR, value="ul li.nav-item")

        player_manager = PlayerManager()
        for server_index in range(len(servers_list)):
            servers_list[server_index].click()
            sleep(1)
            servers_list = driver.find_elements(
                by=By.CSS_SELECTOR, value="ul li.nav-item"
            )
            players_list = driver.find_elements(
                by=By.CSS_SELECTOR, value="table tbody tr"
            )
            for player_element in players_list:
                player_dict = {}
                try:
                    player_dict["server"] = servers_list[server_index].text
                    player_dict["nume"] = player_element.find_element(
                        by=By.CSS_SELECTOR, value="td.summoner a"
                    ).text
                    player_dict["link"] = player_element.find_element(
                        by=By.CSS_SELECTOR, value="td.summoner a"
                    ).get_attribute("href")
                    player_dict["rank"] = player_element.find_element(
                        by=By.CSS_SELECTOR, value="td.tier"
                    ).text.upper()
                    player_dict["lp"] = player_element.find_element(
                        by=By.CSS_SELECTOR, value="td.lp"
                    ).text
                    player_dict["winrate"] = player_element.find_element(
                        by=By.CSS_SELECTOR, value="td.winrate"
                    ).text
                    player_dict["top4"] = player_element.find_element(
                        by=By.CSS_SELECTOR, value="td.toprate"
                    ).text
                    player_dict["nr. meciuri"] = player_element.find_element(
                        by=By.CSS_SELECTOR, value="td.played"
                    ).text
                    player_dict["wins"] = player_element.find_element(
                        by=By.CSS_SELECTOR, value="td.wins"
                    ).text
                    player_dict["nr. top4"] = player_element.find_element(
                        by=By.CSS_SELECTOR, value="td.tops"
                    ).text
                    player_obj = Player(player_dict)
                except Exception as e:
                    print(player_element.text)
                else:
                    player_manager.add_player(player_obj)
        return player_manager
    except Exception as e:
        print(e)
        return None


def get_player_data(url, set) -> Player | None:
    try:
        resp = requests.get(f"{url}/{set}")
        resp.raise_for_status()
        html_content = resp.text

        soup = BeautifulSoup(html_content, "html.parser")
        player_dict = {}
        player_dict["rank"] = (
            soup.find("div", {"class": "tier"}).find("strong").text.strip()
        )
        player_dict["server"] = (
            soup.find("div", {"class": "name"}).find("span").text.strip()
        )
        player_dict["nume"] = (
            soup.find("div", {"class": "name"}).find("h2").text.strip()
        )
        player_dict["link"] = url
        player_dict["lp"] = (
            soup.find("div", {"class": "tier"})
            .find("span")
            .text.strip()
            .replace(",", "")
        )
        stats_list_elements = soup.find("ul", {"class": "ratings"}).find_all("li")
        player_dict["wins"] = stats_list_elements[0].find("strong").text.strip()
        player_dict["winrate"] = stats_list_elements[1].find("strong").text.strip()
        player_dict["nr. top4"] = stats_list_elements[2].find("strong").text.strip()
        player_dict["top4"] = stats_list_elements[3].find("strong").text.strip()
        player_dict["nr. meciuri"] = stats_list_elements[4].find("strong").text.strip()
        player_obj = Player(player_dict)
    except Exception as e:
        print(e)
        date = datetime.date.today()
        with open(f"failed_{date}.txt", "a+") as f:
            f.write(f"{e}")
            f.write("\n")
            f.write(url)
            f.write("\n")
        return None
    else:
        return player_obj
