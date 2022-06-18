from flask import Blueprint, redirect, url_for, jsonify, request
import vk

from . import db
from .models import Mems
from .config import access_token

main_routes = Blueprint("main", __name__, template_folder="templates")


@main_routes.route("/")
def home():
    return f'Hi, go to load your mems'


@main_routes.route("/load_mems", methods=['POST'])
def load_mems():
    url_albom_mems = request.form['url']

    session = vk.Session()
    api = vk.API(session)

    album_id = url_albom_mems.split('/')[-1].split('_')[1]
    owner_id = url_albom_mems.split('/')[-1].split('_')[0].replace('album', '')

    mems = api.photos.get(v=5.131,
                          album_id=album_id,
                          owner_id=owner_id,
                          access_token=access_token,
                          extended=1,
                          )

    for image in mems["items"]:
        vk_links = f'https://vk.com/id{image["user_id"]}'
        vk_id = image["user_id"]
        likes = image["likes"]["count"]
        url_image = image["sizes"][-1]["url"]

        new_mem = Mems(vk_links=vk_links,
                       vk_id=vk_id,
                       likes=likes,
                       url_image=url_image)
        db.session.add(new_mem)
        db.session.commit()

    return redirect(url_for('main.get_all_mems'))


@main_routes.route("/get_all_mems", methods=['GET'])
def get_all_mems():
    mems = Mems.query.all()

    output = []

    for mem in mems:
        mem_data = {}
        mem_data['vk_links'] = mem.vk_links
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
    if not mems:
        return jsonify({'message': 'Мемы уже удалены'})

    for mem in mems:
        db.session.delete(mem)
    db.session.commit()

    return jsonify({'message': 'Все мемы были удалены'})
