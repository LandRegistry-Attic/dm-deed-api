import requests
import logging
from application import config
from flask.ext.api import status
from flask import abort

LOGGER = logging.getLogger(__name__)

def sign_by_user(deed_xml, borrower_pos, user_id):  # pragma: no cover
    LOGGER.info("Calling dm-esec-client")
    request_url = config.ESEC_CLIENT_BASE_HOST + '/esec/sign_by_user'
    element_id = 'deedData'
    borrower_path = "/dm-application/operativeDeed/signatureSlots"

    parameters = {
        'borrower-pos': borrower_pos,
        'element-id': element_id,
        'borrowers-path': borrower_path,
        'user-id': user_id
    }

    resp = requests.post(request_url, params=parameters, data=deed_xml)

    if resp.status_code == status.HTTP_200_OK:
        LOGGER.info("Response XML = %s" % resp.content)
        return resp.content, resp.status_code
    else:
        LOGGER.error("Esecurity Client Exception")
        abort(status.HTTP_500_INTERNAL_SERVER_ERROR)


def initiate_signing(first_name, last_name, organisation_id):  # pragma: no cover
    LOGGER.info("Calling dm-esec-client")
    request_url = config.ESEC_CLIENT_BASE_HOST + '/esec/initiate_signing'

    parameters = {
        'first-name': first_name,
        'last-name': last_name,
        'organisation-id': organisation_id
    }

    resp = requests.post(request_url, params=parameters)

    if resp.status_code == status.HTTP_200_OK:
        LOGGER.info("Response XML = %s" % resp.content)
        return resp.content, resp.status_code
    else:
        LOGGER.error("Esecurity Client Exception")
        abort(status.HTTP_500_INTERNAL_SERVER_ERROR)