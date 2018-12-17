from flask import url_for

from app import db


class Command(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=False)
    default_value = db.Column(db.String(64))
    current_value = db.Column(db.String(64))
    value_type = db.Column(db.String(16))  # string, boolean, number
    description = db.Column(db.String(128))
    type = db.Column(db.Integer, db.ForeignKey('section.id'))

    def __repr__(self):
        return '<Command {}>'.format(self.name)


section_maps = db.Table('section_maps',
                        db.Column('section_id', db.Integer, db.ForeignKey('section.id'), primary_key=True),
                        db.Column('map_id', db.Integer, db.ForeignKey('map.id'), primary_key=True)
                        )


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(64))
    show_in_view = db.Column(db.Boolean, default=True)
    image = db.Column(db.String(128))
    maps = db.relationship('Map', secondary=section_maps, lazy='subquery',
                           backref=db.backref('sections', lazy=True))
    commands = db.relationship('Command', backref='sections', lazy='dynamic')

    def __repr__(self):
        return '<Section {}>'.format(self.name)


class Map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(64))
    image = db.Column(db.String(128))

    def __repr__(self):
        return '<Map {}>'.format(self.name)

    def image_url(self):
        return url_for('static', filename='images/' + self.name.upper() + '.jpg')
