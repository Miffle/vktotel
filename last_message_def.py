def group_message(session, zz, i):
    f = open("mes.txt", "a+")
    """Читает последнее сообщение группы из диалогов"""

    """ Получает ID группы, которая написала сообщение"""

    group_id = session.method("groups.getById",
                              {"group_id": zz["items"][i]["conversation"]["peer"]["local_id"]})

    """ 
    Делает проверку сообщения на наличие букв и, если текста нет, то отправляет тип вложения
    """

    if zz["items"][i]["last_message"]["text"] != "":
        print((group_id[0]["name"] + ":"), file=f, flush=True)
        group_last_mes = zz["items"][i]["conversation"]["last_conversation_message_id"]
        group_unread_count = zz["items"][i]["conversation"]["unread_count"]
        start = (group_last_mes - group_unread_count) + 1
        for k in range(start, group_last_mes):
            mes = (session.method("messages.getByConversationMessageId",
                                  {"peer_id": group_id, "conversation_message_ids": k}))
            print(mes["items"][0]["text"], file=f, flush=True)
    else:
        print((group_id[0]["name"] + " | " + zz["items"][i]["last_message"]["attachments"][0]["type"]), file=f,
              flush=True)


def user_message(session, current_conversation):
    """Читает последнее сообщение юзера из диалогов"""
    """Получает id пользователя который написал сообщение"""
    c = session.method("users.get", {"user_ids": current_conversation["conversation"]["peer"]["id"]})
    user_messages = (c[0]["first_name"] + " " + c[0]["last_name"], [])

    """Делает проверку сообщения на наличие букв и, если текста нет, то отправляет тип вложения"""

    user_id = current_conversation["conversation"]["peer"]["id"]
    user_last_mes = current_conversation["conversation"]["last_conversation_message_id"]
    user_unread_count = current_conversation["conversation"]["unread_count"]
    start = (user_last_mes - user_unread_count) + 1
    for current_message_id in range(start, user_last_mes + 1):
        mes = (session.method("messages.getByConversationMessageId",
                              {"peer_id": user_id, "conversation_message_ids": current_message_id}))
        if current_conversation["last_message"]["text"] != "":

            user_messages[1].append(mes["items"][0]["text"])
        else:
            if mes["items"][0]["attachments"][0]["type"] == "video":
                user_messages[1].append((
                    mes["items"][0]["attachments"][0]["video"]["files"]["mp4_360"]))
            elif mes["items"][0]["attachments"][0]["type"] == "photo":
                sizes = mes["items"][0]["attachments"][0]["photo"]["sizes"]
                max_size = max(sizes, key=lambda size: size["height"])
                user_messages[1].append(max_size["url"])
            elif mes["items"][0]["attachments"][0]["type"] == "audio_message":
                user_messages[1].append(
                    (mes["items"][0]["attachments"][0]["audio_message"]["link_ogg"]))
            elif mes["items"][0]["attachments"][0]["type"] == "audio":
                user_messages[1].append(
                    (mes["items"][0]["attachments"][0]["audio"]["url"]))
            else:
                user_messages[1].append(
                    mes["items"][0]["attachments"][0][
                        "type"])

    return user_messages


def chat_message(current_conversation, session):
    """Читает последнее сообщение в чате из диалогов"""
    """Делает проверку сообщения на наличие букв и, если текста нет, то отправляет тип вложения"""
    chat_messages = ((current_conversation["conversation"]["chat_settings"]["title"]), [])

    chat_id = current_conversation["conversation"]["peer"]["id"]
    chat_last_mes = current_conversation["conversation"]["last_conversation_message_id"]
    chat_unread_count = current_conversation["conversation"]["unread_count"]
    start = (chat_last_mes - chat_unread_count) + 1

    for current_message_id in range(start, chat_last_mes + 1):
        mes = (session.method("messages.getByConversationMessageId",
                              {"peer_id": chat_id, "conversation_message_ids": current_message_id}))
        user = (session.method("users.get", {"user_ids": mes["items"][0]["from_id"]}))

        if mes["items"][0]["text"] != "":
            """Несколько id"""
            chat_messages[1].append(
                (user[0]["first_name"] + ' ' + user[0]["last_name"] + ": \n") + mes["items"][0]["text"])
        else:
            if mes["items"][0]["attachments"][0]["type"] == "video":
                chat_messages[1].append(
                    (user[0]["first_name"] + ' ' + user[0]["last_name"]) + ": \n" + (
                        mes["items"][0]["attachments"][0]["video"]["files"]["mp4_360"]))
            elif mes["items"][0]["attachments"][0]["type"] == "photo":
                sizes = mes["items"][0]["attachments"][0]["photo"]["sizes"]
                max_size = max(sizes, key=lambda size: size["height"])
                chat_messages[1].append(
                    (user[0]["first_name"] + ' ' + user[0]["last_name"] + ": \n") + (max_size["url"]))
            elif mes["items"][0]["attachments"][0]["type"] == "audio_message":
                chat_messages[1].append(
                    (user[0]["first_name"] + ' ' + user[0]["last_name"] + ": \n") +
                    (mes["items"][0]["attachments"][0]["audio_message"]["link_ogg"]))
            elif mes["items"][0]["attachments"][0]["type"] == "audio":
                chat_messages[1].append(((user[0]["first_name"] + ' ' + user[0]["last_name"] + ": \n") + (mes["items"][0]["attachments"][0]["audio"]["url"])))
            else:
                chat_messages[1].append(
                    (user[0]["first_name"] + ' ' + user[0]["last_name"] + ": \n") + mes["items"][0]["attachments"][0][
                        "type"])

    return chat_messages