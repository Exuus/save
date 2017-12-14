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
    province_id = province_id.split(',')
    return kenessa.get_district(province_id)


@api.route('/kenessa/<district_id>/sectors/')
@json
def get_kenessa_sector(district_id):
    district_id = district_id.split(',')
    return kenessa.get_sector(district_id)


@api.route('/kenessa/<sector_id>/cells/')
@json
def get_kenessa_cell(sector_id):
    sector_id = sector_id.split(',')
    return kenessa.get_cell(sector_id)


@api.route('/kenessa/<cell_id>/villages/')
@json
def get_kenessa_village(cell_id):
    cell_id = cell_id.split(',')
    return kenessa.get_village(cell_id)


@api.route('/kenessa/<village_id>/locations/')
@json
def get_name_location(village_id):
    return kenessa.get_all_from_village_id(village_id)