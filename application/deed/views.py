from application.deed.model import Deed
from application.deed.utils import validate_helper, valid_dob, is_unique_list
from flask import request, abort
from flask import Blueprint
from flask.ext.api import status
import json
from application.borrower.server import BorrowerService
from underscore import _
from application.borrower.model import Borrower

deed_bp = Blueprint('deed', __name__,
                    template_folder='templates',
                    static_folder='static')


@deed_bp.route('/<deed_reference>', methods=['GET'])
def get_deed(deed_reference):
    result = Deed.query.filter_by(token=str(deed_reference)).first()

    if result is None:
        abort(status.HTTP_404_NOT_FOUND)
    else:
        result.deed['token'] = result.token

    return json.dumps({"deed": result.deed}), status.HTTP_200_OK


@deed_bp.route('/', methods=['POST'])
def create():
    deed = Deed()
    deed_json = request.get_json()
    borrowerService = BorrowerService()

    error_count, error_message = validate_helper(deed_json)

    if error_count > 0:
        return error_message, status.HTTP_400_BAD_REQUEST
    else:
        deed.deed = deed_json

        json_doc = {
            "title_number": deed_json['title_number'],
            "md_ref": deed_json['md_ref'],
            "borrowers": []
            }

        deed.token = Deed.generate_token()

        valid_dob_result = _(deed_json['borrowers']).chain()\
            .map(lambda x, *a: x['dob'])\
            .reduce(valid_dob, True).value()

        if not valid_dob_result:
            abort(status.HTTP_400_BAD_REQUEST)

        phone_number_list = _(deed_json['borrowers']).chain()\
            .map(lambda x, *a: x['phone_number'])\
            .value()

        if not is_unique_list(phone_number_list):
            abort(status.HTTP_400_BAD_REQUEST)

        try:
            for borrower in deed_json['borrowers']:
                borrower_json = {
                    "id": "",
                    "forename": borrower['forename'],
                    "surname": borrower['surname']
                }

                if 'middle_name' in borrower:
                    borrower_json['middle_name'] = borrower['middle_name']

                borrower_json["id"] = borrowerService.saveBorrower(borrower)
                json_doc['borrowers'].append(borrower_json)

            deed.deed = json_doc

            deed.save()
            url = request.base_url + str(deed.token)
            return url, status.HTTP_201_CREATED
        except Exception as e:
            print("Database Exception - %s" % e)
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR)


@deed_bp.route('/borrowers/delete/<borrower_id>', methods=['DELETE'])
def delete_borrower(borrower_id):
    borrower = None
    borrowerModel = Borrower()
    try:
        borrower = borrowerModel.delete(borrower_id)
    except Exception as inst:
        print(str(type(inst)) + ":" + str(inst))

    if borrower is None:
        abort(status.HTTP_404_NOT_FOUND)
    else:
        return json.dumps({'id': borrower_id}), status.HTTP_200_OK


@deed_bp.route('/<deed_reference>', methods=['PUT'])
def get_existing_deed_and_update(deed_reference):

    # Firstly check payload coming in is valid:
    new_deed_json = request.get_json()
    borrowerService = BorrowerService()
    print ("Hello - New JSON is here")
    error_count, error_message = validate_helper(new_deed_json)

    if error_count > 0:
        return error_message, status.HTTP_400_BAD_REQUEST
    else:
        # If Valid:
        # Get Current Deed
        result = Deed.query.filter_by(token=str(deed_reference)).first()
        print ("I've even found the old deed!")
        existing_deed_borrowers = result.deed['borrowers']
        i = 0
        for existing_borrower in existing_deed_borrowers:
            print ("Existing ID is = " + str(existing_borrower['id']))
            new_deed_json['borrowers'][i]['id'] = existing_borrower['id']
            i = i + 1

    if result is None:
        abort(status.HTTP_404_NOT_FOUND)
    else:

        result.deed = new_deed_json
        print ("Better start sorting out this new deed!")
        json_doc = {
            "title_number": new_deed_json['title_number'],
            "md_ref": new_deed_json['md_ref'],
            "borrowers": []
            }
        print ("Starting Deed = " + str(json_doc))
        # Set token to current token (not generate)

        # Make a deed out of new information
        valid_dob_result = _(new_deed_json['borrowers']).chain()\
            .map(lambda x, *a: x['dob'])\
            .reduce(valid_dob, True).value()

        if not valid_dob_result:
            abort(status.HTTP_400_BAD_REQUEST)

        phone_number_list = _(new_deed_json['borrowers']).chain()\
            .map(lambda x, *a: x['phone_number'])\
            .value()

        if not is_unique_list(phone_number_list):
            abort(status.HTTP_400_BAD_REQUEST)

        print ("Happy with DOB and Mobile!")
        print ("Deed so far: = " + str(json_doc))

        print ("Current new deed = " + str(new_deed_json))
        try:
            for borrower in new_deed_json['borrowers']:
                print ("Current Borrower please:" + str(borrower))
                print ("Result info = " + str(result.deed['borrowers']))
                borrower_json = {
                    "id": borrower['id'],
                    "forename": borrower['forename'],
                    "surname": borrower['surname']
                }
                if 'middle_name' in borrower:
                    borrower_json['middle_name'] = borrower['middle_name']
                json_doc['borrowers'].append(borrower_json)

            print ("Borrower Print = " + str(borrower))

            borrowerService.saveBorrower(borrower, borrower_json["id"])

            print ("FINAL DOC IS " + str(json_doc))
            # Set whole deed to new JSON doc
            result.deed = json_doc

            # Save the Deed
            print ("Saving Deed Now")
            result.save()
            url = request.base_url
            return url, status.HTTP_200_OK
        except Exception as e:
            print("Database Exception - %s" % e)
            abort(status.HTTP_500_INTERNAL_SERVER_ERROR)

