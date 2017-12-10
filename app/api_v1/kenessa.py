from . import api
from ..decorators import json
from .. import kenessa


@api.route('/kenessa/provinces/')
@json
def get_kenessa_province():
    return kenessa.get_province()


@api.route('/kenessa/<province_id>/districts/')
@json
def get_kenessa_district(province_id):
    return kenessa.get_district(province_id)


@api.route('/kenessa/<district_id>/sectors/')
@json
def get_kenessa_sector(district_id):
    return kenessa.get_sector(district_id)


@api.route('/kenessa/<sector_id>/cells/')
@json
def get_kenessa_cell(sector_id):
    return kenessa.get_cell(sector_id)


@api.route('/kenessa/<cell_id>/villages/')
@json
def get_kenessa_village(cell_id):
    return kenessa.get_village(cell_id)