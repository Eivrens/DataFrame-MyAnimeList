import pandas as pd

from bs4 import BeautifulSoup
from urllib.request import urlopen

list_animes = []
seasons = ['winter', 'spring', 'summer', 'fall']

for year in range(1981, 2022):
    for season in seasons:
        url_by_year = 'https://myanimelist.net/anime/season/' + str(year) + '/' + season
        response_by_year = urlopen(url_by_year)
        html_by_year = response_by_year.read()
        soup_by_year = BeautifulSoup(html_by_year, 'html.parser')
    
        for results in soup_by_year.find_all('h2', {'class':  'h2_anime_title'}):
            url_of_anime = results.find('a').get('href')
            response_anime_selected = urlopen(url_of_anime)
            html_anime_selected = response_anime_selected.read()
            soup_anime_selected = BeautifulSoup(html_anime_selected, 'html.parser')
        
            anime_type = soup_anime_selected.find('h2', string='Information').find_next('a').get_text()
            
            anime_aired = soup_anime_selected.find('span', string='Aired:').parent.get_text().replace('Aired:', '').strip()[:12]
            if anime_aired[5] == ',':
                anime_aired = anime_aired.split(' ')
                anime_aired = anime_aired[0] + ' ' + '0' + anime_aired[1] + ' ' + anime_aired[2]
            check_anime_aired = int(anime_aired.split(' ')[2])
        
            if (anime_type == 'TV') and (check_anime_aired == year):
                anime_name = soup_anime_selected.find('h1', {'class': 'title-name h1_bold_none'}).find('strong').get_text()
                anime_studio = soup_anime_selected.find('span', string='Studios:').find_next('a').get_text()
                anime_rank = soup_anime_selected.find('span', {'class': 'numbers ranked'}).find('strong').get_text().replace('#', '')
                anime_members = soup_anime_selected.find('span', string='Members:').parent.get_text().replace('Members:', '').replace(',', '').strip()
                anime_score = soup_anime_selected.find('span', string='Score:').find_next().get_text()
                
                if anime_score == 'N/A':
                    anime_scored_by = '0'
                else:
                    anime_scored_by = soup_anime_selected.find('div', {'class': 'po-r js-statistics-info di-ib'}).find('span', {'itemprop': 'ratingCount'}).get_text()
                
                anime_favorited_by = soup_anime_selected.find('span', string='Favorites:').parent.get_text().replace('Favorites:', '').replace(',', '').strip()
                
                anime_season = soup_anime_selected.find('span', {'class': 'information season'}).find('a').get_text().split(' ')[0]
                
                anime_status = soup_anime_selected.find('span', string='Status:').parent.get_text().replace('Status:', '').strip()
                if anime_status == 'Finished Airing':
                    anime_status = 'Terminado'
                elif anime_status == 'Currently Airing':
                    anime_status = 'Em Progresso'
                
                anime_episodes = soup_anime_selected.find('span', string='Episodes:').parent.get_text().replace('Episodes:', '').strip()
                if anime_episodes == 'Unknown':
                    anime_episodes = 'Em Andamento'
                
                anime_duration = soup_anime_selected.find('span', string='Duration:').parent.get_text().replace('Duration:', '').strip()[:2]
                
                anime_rating = soup_anime_selected.find('span', string='Rating:').parent.get_text().replace('Rating:', '').strip().split(' ')[0]
                if anime_rating == 'None':
                    anime_rating = 'N/A'
               
                anime_source = soup_anime_selected.find('span', string='Source:').parent.get_text().replace('Source:', '').strip()
                if anime_source == 'Unknown':
                    anime_source = 'Desconhecido'
                
                anime_genres = soup_anime_selected.find('span', string='Genres:').parent.find_all('a')
                list_anime_genres = []
                for genre_selected in anime_genres:
                    genre_selected.get_text()
                    list_anime_genres.append(genre_selected.get_text())
                anime_genres = ', '.join(list_anime_genres)
                
                anime_name_english = soup_anime_selected.find('h2', string='Alternative Titles').find_next().get_text().split(':')[0].strip()
                if anime_name_english == 'English':
                    anime_name_english = soup_anime_selected.find('h2', string='Alternative Titles').find_next().get_text().replace('English: ', '').strip()
                else:
                    anime_name_english = 'N/A'
                   
                datas_anime_selected = {}
                
                datas_anime_selected['Título'] = anime_name
                datas_anime_selected['Estúdio'] = anime_studio
                datas_anime_selected['Rank'] = int(anime_rank)
                datas_anime_selected['Membros'] = int(anime_members)
                datas_anime_selected['Pontos'] = anime_score
                datas_anime_selected['Pontuado por'] = int(anime_scored_by)
                datas_anime_selected['Favoritado por'] = int(anime_favorited_by)
                datas_anime_selected['Lançado'] = anime_aired
                datas_anime_selected['Temporada/Estação'] = anime_season
                datas_anime_selected['Status'] = anime_status
                datas_anime_selected['Episódios'] = anime_episodes
                datas_anime_selected['Classificação'] = anime_rating
                datas_anime_selected['Fonte'] = anime_source
                datas_anime_selected['Gêneros'] = anime_genres
                datas_anime_selected["Título em Inglês"] = anime_name_english
                datas_anime_selected['Link'] = url_of_anime
            
                list_animes.append(datas_anime_selected)
                
                if (len(list_animes) > 1):
                    for x in range(len(list_animes) - 1):
                        if ((list_animes[x]['Título'] == anime_name) and (list_animes[x]['Estúdio'] == anime_studio)):
                            list_animes.pop()
                    print(len(list_animes))
                
df_animes = pd.DataFrame(list_animes)

df_animes.to_csv('./df_myanimelist.csv', sep = ';', index = False, encoding = 'utf-8')
