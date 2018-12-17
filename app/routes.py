import socket
import subprocess
import time

from flask import render_template
from flask.json import jsonify
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, HiddenField

from app import app
from app.forms import CommandTextField, CommandCheckBoxField, CommandNumberField
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
    if form.is_submitted():
        for command in form.commands:
            if command.data != command.default:
                send_command(command.name + ' ' + str(command.data))
                time.sleep(1)
        if form.maps.data is not None:
            send_command('map ' + form.maps.data)
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

    for command in section_id.commands:
        setattr(CommandForm, command.name, get_field_from_value_type(command))

    class SectionForm(FlaskForm):
        pass

    choices = []
    for single_map in section_id.maps:
        choices.append((single_map.name, single_map.name))
    setattr(SectionForm, 'seta g_gametype', HiddenField(default=section_id.id))
    setattr(SectionForm, 'maps', RadioField(choices=choices))
    setattr(SectionForm, 'submit', SubmitField('Submit'))
    setattr(SectionForm, 'commands', CommandForm(csrf_enabled=False))
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
        return CommandTextField(command=command)
    elif command.value_type == 'boolean':
        return CommandCheckBoxField(command=command)
    elif command.value_type == 'number':
        return CommandNumberField(command=command)
