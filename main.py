import requests
import os
from dotenv import load_dotenv
load_dotenv()
link = os.getenv('api_url')
class UserAchievementsComparator:
    #Инициализация
    def __init__(self, api_url):

        self.api_url = api_url
        self.first_data = {}
        self.second_data = {}

    #Запрос GET с получением словаря
    def fetch_data(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return {}
    #Два запроса к API и сохранение
    def collect_data(self):
        self.first_data = self.fetch_data()

        self.second_data = self.fetch_data()

    #Сравнение достижений из словарей и формирование ответа
    def new_achievements(self):

        changes = {}

        for user_id, user_data in self.second_data.items():
            # Достижения из первого и второго запросов
            achievements1 = set(self.first_data.get(user_id, {}).get("achievements", {}).keys())
            achievements2 = set(user_data.get("achievements", {}).keys())

            # Найти новые достижения
            new_achievements = achievements2 - achievements1

            if new_achievements:
                # Сохраняем пользователя с новыми достижениями
                changes[user_id] = {
                    "metadata": user_data["metadata"],
                    "achievements": {achievement: True for achievement in new_achievements}
                }

        return changes

    def start(self):
        self.collect_data()
        changes = self.new_achievements()

        return changes


if __name__ == "__main__":
    # URL API
    api_url = link

    comparator = UserAchievementsComparator(api_url)

    # Запуск процесса
    changes = comparator.start()
    print(changes)
