import os

from flask import send_file
from flask_jwt_extended import jwt_required

import core.config.config
import core.config.paths
from core import helpers
from server.returncodes import SUCCESS
from server.security import roles_accepted_for_resources


def read_all_possible_subscriptions():

    @jwt_required
    @roles_accepted_for_resources('cases')
    def __func():
        return core.config.config.possible_events, SUCCESS

    return __func()


def read_all_device_types():
    @jwt_required
    @roles_accepted_for_resources('apps')
    def __func():
        response = []
        for app, app_api in core.config.config.app_apis.items():
            if 'devices' in app_api:
                for type_name, type_api in app_api['devices'].items():
                    api = dict(type_api)
                    api['name'] = type_name
                    api['app'] = app
                    response.append(api)
        return response, SUCCESS

    return __func()


def validate_path(directory, filename):
    """ Checks that the filename is inside of the given directory
    Args:
        directory (str): The directory in which to search
        filename (str): The given filename

    Returns:
        (str): The sanitized path of the filename if valid, else None
    """
    base_abs_path = os.path.abspath(directory)
    normalized = os.path.normpath(os.path.join(base_abs_path, filename))
    return normalized if normalized.startswith(base_abs_path) else None


def read_client_file(filename):
    file = validate_path(core.config.paths.client_path, filename)
    if file is not None:
        return send_file(file), 200
    else:
        return {"error": "invalid path"}, 463
