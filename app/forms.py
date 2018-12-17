from flask_wtf import FlaskForm, Form
from wtforms import TextField, BooleanField, FieldList, RadioField, HiddenField, SelectField
from wtforms.fields.html5 import IntegerField


class CommandTextField(TextField):
    def __init__(self, label='', validators=None, command=None, **kwargs):
        super(TextField, self).__init__(label, validators, **kwargs)
        self.label = command.name
        self.type = command.value_type
        self.description = command.description
        self.default = command.current_value if command.current_value else None


class CommandHiddenField(HiddenField):
    def __init__(self, label='', validators=None, command=None, **kwargs):
        super(HiddenField, self).__init__(label, validators, **kwargs)
        self.label = command.name
        self.description = command.description
        self.default = command.current_value if command.current_value else None


class CommandCheckBoxField(RadioField):
    def __init__(self, label='', validators=None, command=None, **kwargs):
        super(RadioField, self).__init__(label, validators, choices=[(1, "yes"), (0, "no")], **kwargs)
        self.label = command.name
        self.description = command.description
        self.default = command.current_value if command.current_value else None


class CommandNumberField(IntegerField):
    def __init__(self, label='', validators=None, command=None, **kwargs):
        super(IntegerField, self).__init__(label, validators, **kwargs)
        self.label = command.name
        self.type = command.value_type
        self.description = command.description
        self.default = command.current_value if command.current_value else None


class MapRadio(RadioField):
    def __init__(self, label='', validators=None, maps=[], **kwargs):
        choices = []
        for single_map in maps:
            choices.append((single_map.name, single_map.name))
        super(RadioField, self).__init__(label, validators, choices=choices, **kwargs)
