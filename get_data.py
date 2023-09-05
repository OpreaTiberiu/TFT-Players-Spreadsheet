from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_players_data(url):
    data = get_site_data(url)
    if len(data) > 0:
        headers = [key.title() for key in data[0].keys()]
        return_data = [headers]
        for d in data:
            values = [d[key.lower()] for key in headers]
            return_data.append(values)
        return return_data
    return None


def get_site_data(url):
    driver = webdriver.Chrome()

    driver.get(url)
    sleep(5)

    servers_list = driver.find_elements(by=By.CSS_SELECTOR, value='ul li.nav-item')

    players = []
    for server_index in range(len(servers_list)):
        servers_list[server_index].click()
        sleep(1)
        servers_list = driver.find_elements(by=By.CSS_SELECTOR, value='ul li.nav-item')
        players_list = driver.find_elements(by=By.CSS_SELECTOR, value='table tbody tr')
        for player_element in players_list:
            player = {}
            try:
                player["server"] = servers_list[server_index].text
                player["name"] = player_element.find_element(by=By.CSS_SELECTOR, value='td.summoner a').text
                player["link"] = player_element.find_element(
                    by=By.CSS_SELECTOR, value='td.summoner a').get_attribute('href')
                player["rank"] = player_element.find_element(by=By.CSS_SELECTOR, value='td.tier').text
                player["lp"] = player_element.find_element(by=By.CSS_SELECTOR, value='td.lp').text
                player["winrate"] = player_element.find_element(by=By.CSS_SELECTOR, value='td.winrate').text
                player["toprate"] = player_element.find_element(by=By.CSS_SELECTOR, value='td.toprate').text
                player["played"] = player_element.find_element(by=By.CSS_SELECTOR, value='td.played').text
                player["wins"] = player_element.find_element(by=By.CSS_SELECTOR, value='td.wins').text
                player["tops"] = player_element.find_element(by=By.CSS_SELECTOR, value='td.tops').text
            except Exception as e:
                print(player_element.text)
            else:
                players.append(player)

    return players
