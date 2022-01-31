from json import dumps, loads
from flask import Response, request, abort, render_template
from data_validators import *
from pydantic import ValidationError
from flask_login import login_required


@login_required
def classes():
    return render_template('endpoints/classes.html.jinja2')


# postman command: {"class_name":"1 testowa", "class_short":"1T"}
def post():
    repo = None
    data = loads(request.data.decode('utf-8'))
    try:
        validated_data = ClassesValidation(**data)
        added_class = repo.add_class(dict(validated_data))
        return Response(dumps({'class_id': added_class}), mimetype='application/json', status=201)
    except ValidationError as error:
        return Response(error.json(), mimetype='application/json', status=400)


def delete(class_id):  # parametr wpada wprost z add_url_rule('endpoint/<param>')
    repo = None
    if not repo.class_exists(class_id):
        return abort(404)
    repo.delete_class(class_id)
    return Response(dumps({'status': 'OK'}), mimetype='application/json', status=200)
