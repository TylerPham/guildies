from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
import json
from requestValidator import isValid, isValidName, isValidNumber, isValidEmail


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://gamehive:gamehive@postgres:5432/gamehive'


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


# items to players is many to many, need an association table
item_ownership = db.Table(
    'item_ownership', db.Column(
        'player_id', db.Integer, db.ForeignKey('player.id')), db.Column(
            'item_id', db.Integer, db.ForeignKey('item.id')))

# create our database model


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    skillpoints = db.Column(db.Integer, nullable=False)

    guild_id = db.Column(db.Integer, db.ForeignKey('guild.id'), nullable=True)
    # a player is one to many items
    items = db.relationship('Item',
                            secondary=item_ownership,
                            backref='player')

    def __init__(self, nickname, email, skillpoints):
        self.nickname = nickname
        self.email = email
        self.skillpoints = skillpoints

    def __repr__(self):
        return '<User %r>' % self.nickname


class Guild(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    country_code = db.Column(db.Integer, nullable=True)

    # a guild is one to many players
    players = db.relationship('Player', backref='guild')

    def __init__(self, name, country_code=None):
        self.name = name
        self.country_code = country_code


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skillpoints = db.Column(db.Integer, nullable=False)

    # player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)

    def __init__(self, skillpoints):
        self.skillpoints = skillpoints


@app.route('/')
def root():
    return 'Game Hive Player API'

# Req 1.1 create a player


@app.route('/players/', methods=['POST'])
def create_player():
    # typical usage/request:
    # {
    # 	"nickname": "player1",
    # 	"email": "player1@email.com",
    # 	"skillpoints": 10
    # }
    if not request.json or not isValid(
            ['nickname', 'email', 'skillpoints'], request.json):
        abort(400)

    if not isValidName(
        request.json['nickname']) or not isValidEmail(
        request.json['email']) or not isValidNumber(
            request.json['skillpoints']):
        abort(400)

    nickname = request.json['nickname']
    email = request.json['email']
    skillpoints = request.json['skillpoints']

    newPlayer = Player(nickname, email, skillpoints)

    db.session.add(newPlayer)
    db.session.commit()
    return json.dumps({'success': True}), 200, {
        'ContentType': 'application/json'}

# Req 1.2 update a player


@app.route('/players/<int:id>', methods=['PUT'])
def update_player(id):
    # typical usage/request:
    # /players/1
    # {
    # 	"nickname": "player1",
    # 	"email": "UPDATEDplayer1@email.com",
    # 	"skillpoints": 15
    # }
    # values can be optionally omitted

    # if player exists
    if Player.query.get(id) is None:
        abort(404)
    # have to check indiv since they are optional params
    if isValid(['nickname'], request.json):
        if not isValidName(request.json['nickname']):
            abort(400)
    if isValid(['email'], request.json):
        if not isValidEmail(request.json['email']):
            abort(400)
    if isValid(['skillpoints'], request.json):
        if not isValidNumber(request.json['skillpoints']):
            abort(400)

    player = Player.query.get(id)
    player.nickname = request.json.get('nickname', player.nickname)
    player.email = request.json.get('email', player.email)
    player.skillpoints = request.json.get('skillpoints', player.skillpoints)
    try:
        db.session.commit()
        return json.dumps({'success': True}), 200, {
            'ContentType': 'application/json'}
    except BaseException:
        abort(400)

# Req 1.3 delete a player


@app.route('/players/<int:id>', methods=['DELETE'])
def delete_player(id):
    # typical usage /players/1
    if Player.query.get(id) is None:
        abort(404)

    db.session.delete(Player.query.get(id))
    try:
        db.session.commit()
        return json.dumps({'success': True}), 200, {
            'ContentType': 'application/json'}
    except BaseException:
        abort(404)

# Req 2.1 create a guild


@app.route('/guilds/', methods=['POST'])
def create_guild():
    # typical usage/request:
    # /guilds
    # {
    # 	"name": "guild1",
    # 	"country_code": "105",
    # }
    # country_code can be optional

    if not request.json or not isValid(['name'], request.json):
        abort(400)

    name = request.json['name']

    if 'country_code' not in request.json:
        guild = Guild(name)
    else:
        country_code = request.json['country_code']
        guild = Guild(name, country_code)

    db.session.add(guild)
    try:
        db.session.commit()
        return json.dumps({'success': True}), 200, {
            'ContentType': 'application/json'}
    except BaseException:
        abort(400)
# Req 2.2 update a guild


@app.route('/guilds/<int:id>', methods=['PUT'])
def update_guild(id):
    # typical usage/request:
    # /guilds/1
    # {
    # 	"name": "guild1",
    # 	"country_code": "106"
    # }
    # values can be optionally omitted

    if Guild.query.get(id) is None:
        abort(404)

    guild = Guild.query.get(id)
    guild.name = request.json.get('name', guild.name)
    guild.country_code = request.json.get('country_code', guild.country_code)
    try:
        db.session.commit()
        return json.dumps({'success': True}), 200, {
            'ContentType': 'application/json'}
    except BaseException:
        abort(400)

# Req 2.3 delete a guild


@app.route('/guilds/<int:id>', methods=['DELETE'])
def delete_guild(id):
    # typical usage/request:
    # /guilds/1

    if Guild.query.get(id) is None:
        abort(404)

    db.session.delete(Guild.query.get(id))
    try:
        db.session.commit()
        return json.dumps({'success': True}), 200, {
            'ContentType': 'application/json'}
    except BaseException:
        abort(400)

# Req 3.1 create an item


@app.route('/items/', methods=['POST'])
def create_item():
    # typical usage/request:
    # /items/
    # {
    # 	"skillpoints": "10"
    # }

    if not request.json or not isValid(['skillpoints'], request.json):
        abort(400)

    skillpoints = request.json['skillpoints']
    item = Item(skillpoints)
    db.session.add(item)
    try:
        db.session.commit()
        return json.dumps({'success': True}), 200, {
            'ContentType': 'application/json'}
    except BaseException:
        abort(400)

# Req 3.2 update and item


@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    # typical usage/request:
    # /items/1
    # {
    # 	"skillpoints": "15"
    # }

    if Item.query.get(id) is None:
        abort(400)

    item = Item.query.get(id)
    item.skillpoints = request.json.get('skillpoints', item.skillpoints)

    try:
        db.session.commit()
        return json.dumps({'success': True}), 200, {
            'ContentType': 'application/json'}
    except BaseException:
        abort(400)

# Req 3.3 delete an item


@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    # typical usage/request:
    # /items/1

    if Item.query.get(id) is None:
        abort(404)

    db.session.delete(Item.query.get(id))
    try:
        db.session.commit()
        return json.dumps({'success': True}), 200, {
            'ContentType': 'application/json'}
    except BaseException:
        abort(400)

# Req 4: add player to a guild


@app.route('/guilds/<int:guild_id>/players/<int:player_id>', methods=['PUT'])
def add_player_to_guild(guild_id, player_id):
    # typical usage/request:
    # /guilds/1/players/1/

    if Player.query.get(player_id) is None or Guild.query.get(
            guild_id) is None:
        abort(404)

    player = Player.query.get(player_id)
    player.guild_id = guild_id

    try:
        db.session.commit()
        return json.dumps({'success': True}), 200, {
            'ContentType': 'application/json'}
    except BaseException:
        abort(400)

# Req 5 remove player from a guild


@app.route(
    '/guilds/<int:guild_id>/players/<int:player_id>',
    methods=['DELETE'])
def delete_player_from_guild(guild_id, player_id):
    # typical usage/request:
    # /guilds/1/players/1
    if Player.query.get(player_id) is None or Guild.query.get(
            guild_id) is None:
        abort(404)

    player = Player.query.get(player_id)
    player.guild = None

    try:
        db.session.commit()
        return json.dumps({'success': True}), 200, {
            'ContentType': 'application/json'}
    except BaseException:
        abort(400)

# Req 6 add an item to a player


@app.route('/players/<int:player_id>/items/<int:item_id>', methods=['PUT'])
def add_item_to_player(item_id, player_id):
    # typical usage/request:
    # /players/1/items/1

    item = Item.query.get(item_id)
    player = Player.query.get(player_id)
    guildmates = Player.query.filter(Player.guild_id == player.guild_id).all()

#    decrement guildmates skillpoints by item skillpoints
    for member in guildmates:
        for member_item in member.items:
            # if two guildmates have the same item
            if member_item.id == item.id and member.id != player.id:
                member.skillpoints -= item.skillpoints

    # add item to player
    player.items.append(item)
    # add skillpoints of item onto player
    player.skillpoints += item.skillpoints
    try:
        db.session.commit()
        return json.dumps({'success': True}), 200, {
            'ContentType': 'application/json'}
    except BaseException:
        abort(400)

# Req 7 calculate the total number of skill points in a guild


@app.route('/guilds/<int:id>/skills', methods=['GET'])
def get_guild_total_skillpoints(id):
    # typical usage/request:
    # guilds/1/skills

    guildmembers = Player.query.filter(Player.guild_id == id)

    total_skillpoints = 0
    for member in guildmembers:
        total_skillpoints += member.skillpoints

    return jsonify({'total_skillpoints': total_skillpoints})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
