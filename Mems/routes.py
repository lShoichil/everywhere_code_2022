import json
import random

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
                          rev=1
                          )

    for image in mems["items"]:
        vk_links = f'https://vk.com/id{image["user_id"]}'
        vk_id = image["user_id"]
        likes_parse = image["likes"]["count"]
        url_image = image["sizes"][-1]["url"]

        new_mem = Mems(vk_links=vk_links,
                       vk_id=vk_id,
                       likes_parse=likes_parse,
                       url_image=url_image,
                       likes_count=0,  # для 2,3 заданий
                       promote=0)  # для 3 задания
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
        mem_data['likes_parse'] = mem.likes_parse
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


count_mems = 0
it_first = True


@main_routes.route('/likes_or_skip', methods=["POST"])
def likes_or_skip():
    global count_mems, it_first
    rows = db.session.query(Mems).count()
    id = Mems.query.all()[count_mems].id
    mem = Mems.query.filter_by(id=id).first()

    if rows == 0:
        return jsonify({'message': 'У вас нет мемов:('})
    elif rows == count_mems + 1:
        count_mems = 0
        it_first = True
        mem.likes_count += 1
        db.session.commit()
        return jsonify({'message': 'Это был последний! Больше мемов у нас нет. :( '
                                   'При следующем запросе вы начнёте сначала'})

    elif request.method == 'POST':

        if count_mems == 0 and it_first:
            it_first = False
            message = f'Это первый мем из {rows}! Лайкните или пропустите?'
            return jsonify({'message': message,
                            'url_mem_now': Mems.query.all()[count_mems].url_image})
        l_or_p = request.form['l_or_p']

        count_mems += 1
        if l_or_p == '1':
            mem.likes_count += 1
            db.session.commit()
            message = f'Вы лайкнули {count_mems} мем из {rows}! Вы сейчас на {count_mems + 1} меме.'
            return jsonify({'message': message,
                            'url_mem_liked': Mems.query.all()[count_mems - 1].url_image,
                            'url_mem_now': Mems.query.all()[count_mems].url_image})
        if l_or_p == '0':
            message = f'Вы пропустили {count_mems} мем из {rows}! Вы сейчас на {count_mems + 1} меме.'
            return jsonify({'message': message,
                            'url_mem_now': Mems.query.all()[count_mems].url_image,
                            'url_mem_skiped': Mems.query.all()[count_mems - 1].url_image})


@main_routes.route('/update_promote/<int:mem_id>')
def update_promote(mem_id):
    mems = Mems.query.all()
    if not mems:
        return jsonify({'message': 'У вас нет мемов:('})
    mem = Mems.query.filter_by(id=mem_id).first()
    if not mem:
        return jsonify({'message': 'Мема с таким id не существует'})

    mems_sorted = db.session.query(Mems).order_by(Mems.likes_count).all()
    print(mems_sorted)
    db.session.commit()
    return jsonify({'message': 'Теперь этот мем в приоритете!'})


@main_routes.route('/test_for_third')
def test_for_third():
    mems = Mems.query.all()

    for mem in mems:
        tt = random.randint(1, 3)
        if tt != 1:
            mem.likes_count = random.randint(25, 1000)
    db.session.commit()
    return jsonify({'message': "Успешно"})
