from .vk_api import VkApi
import json
import datetime


def get_winner(token: str, album_link: str, date: datetime.datetime) -> str:
    album_link = album_link.replace("https://vk.com/album-", "").split("_")
    owner_id = int(album_link[0])
    album_id = int(album_link[1])
    session = VkApi(token)
    album = session.photos_get(owner_id, album_id)
    if len(album) > 50:
        return "Количество фотографий в альбоме превышает 50!"
    members_list = session.get_members(owner_id)
    output = str()
    winner_output = str()
    winner_points = 0
    number = 0
    result_dict = {"result": {}, "winners": []}
    winners_list = list()
    for photo in album:
        number += 1
        photo_id = photo["id"]
        photo_text = photo["text"]
        likes_list = session.likes_get_list(owner_id, "photo", photo_id)
        count = 0
        for user in likes_list:
            if user in members_list:
                count += 1
        if count == 0 and len(likes_list) == 0:
            return "0/0 ошибка..."
        if count > winner_points:
            winner_points = count
            winner_output = f"\nID победителя: {photo_id}\n{photo_text}\nРезультат: {count}/{len(likes_list)}"
            winners_list = list()
            winners_list.append(photo_id)
        elif count == winner_points:
            winners_list.append(photo_id)
        result_dict["result"][photo_id] = {
            "text": photo_text,
            "counted": count,
            "likes": len(likes_list),
        }
        output += f"№{number} | {photo_id} | {photo_text}: {count}/{len(likes_list)}\n"
        print(f"[INFO] Обработано: {number}/{len(album)}")
    result_dict["winners"] = winners_list
    result_dict["time_start"] = date.strftime("%d/%m/%Y | %H:%M:%S")
    with open("photo_contest_result.json", "w", encoding="UTF-8") as file:
        json.dump(result_dict, file, indent=4, ensure_ascii=False)
    output += winner_output
    return output
