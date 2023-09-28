from typing import List, Dict, Tuple
from api_site.utils.check_time_for_log import decorator_for_check_time
from data_users.models.favorite import Favorite
from tg_bot.bot_utils.manager_db_util import ManagerDB


def get_text_help() -> str:
    """
    Функция отправляет текст в раздел меню "Помощи",
    в которой коротко описаны основные команды, что умеет выполнять бот.
    Returns:
        srt: Текст с командами.
    Raises:
        None.
    """
    text: str = (f'Команды:\n'
                 f'/main - возврат в главное меню.\n'
                 f'/low - вывод одного товара.\n'
                 f'/high - вывод максимального кол-ва товаров.\n'
                 f'/custom — вывод отсортированных товаров.\n'
                 f'/about - информация о боте.\n'
                 f'/help - помощь с командами.\n'
                 f'/contacts - контакты\n'
                 f'/favorite - список избранных')
    return text


def get_text_about() -> str:
    """
    Функция возвращает детальную информацию о боте. Где более в развернутом виде описываются подробно команды.
    Returns:
        str: Подробно о боте.
    """
    text: str = (r'Бот выполняет запросы в поисковикe. '
                 'Обрабатывает результаты  предоставляет информацию о товаре в'
                 ' виде готового шаблона и ссылкой на него в интернет-магазине.\n'
                 'Так же в любой момент доступны строковые команды и меню.\n'
                 'В разделе Поиск товара с сортировкой ⚙ /custom доступна опция сортировать по цене, '
                 'как в рост, так и на убыль или же вывод по умолчанию.'
                 'Будет предоставлен список, который можно будет просматривать '
                 'с помощью кнопок навигации в панели меню. Так же можно будет добавлять и удалять из избранных'
                 'товаров не покидая интерфейс поиска,'
                 'это опционально при любых других запросах поиска.\n'
                 'В Разделе История запросов 📝 /history хранятся сведения о последних 10 запросах.'
                 'Будут выведены ваши результаты, которые можно будет снова запросить в 1 клик.\n'
                 'В разделе Избранное ⭐️ /favorite можно сохранить до 100 результатов, а так же удалять не'
                 'актуальные товары из вашего списка избранных товаров.\n'
                 'В разделе Найти один результат 🔍 /low будет представлен всего один экземпляр из'
                 ' топ ссылок поискового запроса.\n'
                 'В разделе Найти максимум результатов 🔎 /high будет предоставлен список в 30 результатов.\n'
                 'В разделе Помощь" 💡 /help доступен список основных команд. ')
    return text


@decorator_for_check_time
def create_date_favorite(id_user: int, favorite_dict: Dict,
                         favorite_dict_cache: Dict) -> Tuple[Dict, Dict]:
    """
    Создает временные ссылки на сохраненные в БД данные.
    Args:
        id_user: ID пользователя.
        favorite_dict: Данные сохраненных избранных товаров для вывода в меню избранного.
        favorite_dict_cache: Данные избранных товаров для кеша.
    Returns:
        Tuple[Dict, Dict]: Возвращает кортеж из двух словарей, которые принадлежат определенною юзеру по ID.
    Raises:
        None
    Notes:
        Функция обращается к БД, извлекает от туда данные, после чего формируются два словаря,
         один с кеш данными, другой с данными сохраненных товаров.
    """

    favorite_data: List[Favorite] = ManagerDB.read_favorite(id_user)
    list_favorite: List = favorite_dict.get(id_user, [])
    cache_list: List[str] = []
    if favorite_data:
        for prod in favorite_data:
            data: List = [prod.link_web, prod.link_foto, prod.about]
            cache_list.append(prod.link_web)
            if data not in list_favorite:
                list_favorite.append(data)
    favorite_dict_cache[id_user] = cache_list
    favorite_dict[id_user] = list_favorite
    return favorite_dict, favorite_dict_cache
