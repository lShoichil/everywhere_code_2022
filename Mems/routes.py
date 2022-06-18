from flask import Blueprint, redirect, url_for, jsonify, request
import vk_api

from . import db
from .models import Mems

main_routes = Blueprint("main", __name__, template_folder="templates")


@main_routes.route("/")
def home():
    return f'Hi, go to load your mems'


@main_routes.route("/load_mems", methods=['POST'])
def load_mems():
    login = request.form['login']
    password = request.form['password']
    url_albom_mems = request.form['url']

    try:
        vk_session = vk_api.VkApi(login=login, password=password)
        vk_session.auth()
        access_token = vk_session.token['access_token']

        album_id = url_albom_mems.split('/')[-1].split('_')[1]
        owner_id = url_albom_mems.split('/')[-1].split('_')[0].replace('album', '')

        vk = vk_session.get_api()

        mems = vk.photos.get(album_id=album_id,
                             owner_id=owner_id,
                             access_token=access_token,
                             extended=1)

        for image in mems["items"]:
            user = vk.users.get(access_token=access_token,
                                user_ids=image["user_id"])
            vk_id = image["user_id"]
            username = f'{user[0]["first_name"]} {user[0]["last_name"]}'
            likes = image["likes"]["count"]
            url_image = image["sizes"][-1]["url"]

            new_mem = Mems(vk_id=vk_id,
                           username=username,
                           likes=likes,
                           url_image=url_image)
            db.session.add(new_mem)
            db.session.commit()

        return redirect(url_for('main.get_all_mems'))
    except vk_api.exceptions.BadPassword:
        return jsonify({'message': 'Неверный Логин/Пароль'})


@main_routes.route("/get_all_mems", methods=['GET'])
def get_all_mems():
    mems = Mems.query.all()

    output = []

    for mem in mems:
        mem_data = {}
        mem_data['username'] = mem.username
        mem_data['vk_id'] = mem.vk_id
        mem_data['likes'] = mem.likes
        mem_data['url_image'] = mem.url_image
        output.append(mem_data)

    if mems:
        return jsonify({'mems': output})
    else:
        return jsonify({'message': 'У вас нет мемов :('})


@main_routes.route('/delete_all_mems', methods=['DELETE'])
def delete_all_mems():
    mems = Mems.query.all()
    print(mems)
    if not mems:
        return jsonify({'message': 'Мемы уже удалены'})

    for mem in mems:
        db.session.delete(mem)
    db.session.commit()

    return jsonify({'message': 'Все мемы были удалены'})
