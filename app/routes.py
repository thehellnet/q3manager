import socket
import subprocess
import time

from flask import render_template
from flask.json import jsonify
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, HiddenField, StringField, validators
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired, Required

from app import app
from app.models import Section


@app.route('/')
@app.route('/home')
def index():
    section_ids = Section.query.all()
    return render_template('index.html', section_ids=section_ids)


@app.route('/section/<section>', methods=["POST", "GET"])
def section(section):
    section_id = find_map_by_section(section).first()

    form = compose_command_form(section_id)
    if form.validate_on_submit():
        for command in form.commands:
            if command.data != command.default:
                command_str = command.name + ' ' + str(command.data)
                send_command(command_str)
                print('Executing command -> ' + command_str)
                time.sleep(1)
        if hasattr(form, 'map') and form.map.data is not None:
            map_command_str = 'map ' + form.map.data
            send_command(map_command_str)
            print('Executing command -> ' + map_command_str)
        return render_template('section.html', form=form, section=section)
    else:
        pass

    return render_template('section.html', form=form, section=section)


def find_map_by_section(section):
    return Section.query.filter(Section.name == section)


def send_command(command=""):
    if len(command) == 0:
        return

    str_command = "rcon %s %s" % (app.config['SERVER_RCONPASSWORD'], command)
    raw_data = b"\xff\xff\xff\xff" + str_command.encode()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(raw_data, (app.config['SERVER_ADDRESS'], app.config['SERVER_PORT']))


def compose_command_form(section_id):
    class CommandForm(FlaskForm):
        pass

    setattr(CommandForm, 'seta g_gametype', HiddenField(default=section_id.id))

    for command in section_id.commands:
        setattr(CommandForm, command.name, get_field_from_value_type(command))

    class SectionForm(FlaskForm):
        pass

    choices = []
    for single_map in section_id.maps:
        choices.append((single_map.name, single_map.name))
    if len(choices) > 0:
        setattr(SectionForm, 'map',
                RadioField(choices=choices, validators=[DataRequired(message="You must select a map!")]))
    setattr(SectionForm, 'commands', CommandForm(csrf_enabled=False))
    setattr(SectionForm, 'submit', SubmitField('Confirm'))
    form = SectionForm()
    return form


def check_server_status():
    check_server_command = 'pgrep -x "ioq3ded.x86_64"'
    server_start_command = '/opt/ioquake3/ioq3ded.x86_64'
    try:
        server_process = subprocess.Popen(check_server_command.split(' '), stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE)
        pid, error = server_process.communicate()
        if pid:
            return "Server is running!!"
        else:
            subprocess.Popen([server_start_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        return jsonify(e)


def get_field_from_value_type(command):
    if command.value_type == 'string':
        return StringField(label=command.name, description=command.description, default=command.current_value)
    elif command.value_type == 'boolean':
        return RadioField(label=command.name, choices=[(1, "yes"), (0, "no")], description=command.description,
                          default=command.current_value)
    elif command.value_type == 'number':
        return IntegerField(label=command.name, description=command.description, default=command.current_value)
