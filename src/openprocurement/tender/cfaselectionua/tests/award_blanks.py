# -*- coding: utf-8 -*-
from openprocurement.tender.cfaselectionua.tests.base import (
    test_organization
)


# TenderAwardResourceTest


def create_tender_award_invalid(self):
    self.app.authorization = ('Basic', ('token', ''))
    request_path = '/tenders/{}/awards?acc_token={}'.format(self.tender_id, self.tender_token)
    response = self.app.post(request_path, 'data', status=415)
    self.assertEqual(response.status, '415 Unsupported Media Type')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description':
            u"Content-Type header should be one of ['application/json']", u'location': u'header', u'name': u'Content-Type'}
    ])

    response = self.app.post(
        request_path, 'data', content_type='application/json', status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'No JSON object could be decoded',
            u'location': u'body', u'name': u'data'}
    ])

    response = self.app.post_json(request_path, 'data', status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Data not available',
            u'location': u'body', u'name': u'data'}
    ])

    response = self.app.post_json(
        request_path, {'not_data': {}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Data not available',
            u'location': u'body', u'name': u'data'}
    ])

    response = self.app.post_json(request_path, {'data': {
                                  'invalid_field': 'invalid_value'}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Rogue field', u'location':
            u'body', u'name': u'invalid_field'}
    ])

    response = self.app.post_json(request_path, {
                                  'data': {'suppliers': [{'identifier': 'invalid_value'}]}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': {u'identifier': [
            u'Please use a mapping for this field or Identifier instance instead of unicode.']}, u'location': u'body', u'name': u'suppliers'}
    ])

    response = self.app.post_json(request_path, {
                                  'data': {'suppliers': [{'identifier': {'id': 0}}]}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [{u'contactPoint': [u'This field is required.'], u'identifier': {u'scheme': [u'This field is required.']}, u'name': [u'This field is required.'], u'address': [u'This field is required.']}], u'location': u'body', u'name': u'suppliers'},
        {u'description': [u'This field is required.'], u'location': u'body', u'name': u'bid_id'}
    ])

    response = self.app.post_json(request_path, {'data': {'suppliers': [
                                  {'name': 'name', 'identifier': {'uri': 'invalid_value'}}]}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [{u'contactPoint': [u'This field is required.'], u'identifier': {u'scheme': [u'This field is required.'], u'id': [u'This field is required.'], u'uri': [u'Not a well formed URL.']}, u'address': [u'This field is required.']}], u'location': u'body', u'name': u'suppliers'},
        {u'description': [u'This field is required.'], u'location': u'body', u'name': u'bid_id'}
    ])

    response = self.app.post_json(request_path, {'data': {
        'suppliers': [test_organization],
        'status': 'pending',
        'bid_id': self.initial_bids[0]['id'],
        'lotID': '0' * 32
    }}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': [u'lotID should be one of lots'], u'location': u'body', u'name': u'lotID'}
    ])

    response = self.app.post_json('/tenders/some_id/awards', {'data': {
                                  'suppliers': [test_organization], 'bid_id': self.initial_bids[0]['id']}}, status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'tender_id'}
    ])

    response = self.app.get('/tenders/some_id/awards', status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'tender_id'}
    ])

    self.set_status('complete')

    response = self.app.post_json('/tenders/{}/awards'.format(
        self.tender_id), {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': self.initial_bids[0]['id']}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't create award in current (complete) tender status")


def create_tender_award(self):
    self.app.authorization = ('Basic', ('token', ''))
    request_path = '/tenders/{}/awards'.format(self.tender_id)
    response = self.app.post_json(request_path, {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': self.initial_bids[0]['id']}})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    award = response.json['data']
    self.assertEqual(award['suppliers'][0]['name'], test_organization['name'])
    self.assertIn('id', award)
    self.assertIn(award['id'], response.headers['Location'])

    response = self.app.get(request_path)
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'][-1], award)

    award_request_path = '/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, award['id'], self.tender_token)
    response = self.app.patch_json(award_request_path, {"data": {"status": "active"}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], u'active')

    response = self.app.get('/tenders/{}'.format(self.tender_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], u'active.awarded')

    response = self.app.patch_json(award_request_path, {"data": {"status": "cancelled"}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], u'cancelled')
    self.assertIn('Location', response.headers)


def patch_tender_award(self):
    auth = self.app.authorization
    self.app.authorization = ('Basic', ('token', ''))
    request_path = '/tenders/{}/awards'.format(self.tender_id)
    response = self.app.post_json(request_path, {'data': {'suppliers': [test_organization], 'status': u'pending', 'bid_id': self.initial_bids[0]['id'], "value": {"amount": 500}}})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    award = response.json['data']

    self.app.authorization = auth
    response = self.app.patch_json('/tenders/{}/awards/some_id?acc_token={}'.format(self.tender_id, self.tender_token),
                                   {"data": {"status": "unsuccessful"}}, status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'award_id'}
    ])

    response = self.app.patch_json('/tenders/some_id/awards/some_id?acc_token={}'.format(self.tender_token),
                                   {"data": {"status": "unsuccessful"}}, status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'tender_id'}
    ])

    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, award['id'], self.tender_token),
                                   {"data": {"awardStatus": "unsuccessful"}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'], [
        {"location": "body", "name": "awardStatus", "description": "Rogue field"}
    ])

    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, award['id'], self.tender_token),
                                   {"data": {"status": "unsuccessful"}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertIn('Location', response.headers)
    new_award_location = response.headers['Location']

    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, award['id'], self.tender_token),
                                   {"data": {"status": "pending"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't update award in current (unsuccessful) status")

    response = self.app.get(request_path)
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(len(response.json['data']), 2)
    self.assertIn(response.json['data'][1]['id'], new_award_location)
    new_award = response.json['data'][-1]

    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, new_award['id'], self.tender_token),
                                   {"data": {"title": "title", "description": "description"}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['title'], 'title')
    self.assertEqual(response.json['data']['description'], 'description')

    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, new_award['id'], self.tender_token),
                                   {"data": {"status": "active"}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')

    response = self.app.get(request_path)
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(len(response.json['data']), 2)

    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, new_award['id'], self.tender_token),
                                   {"data": {"status": "cancelled"}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertIn('Location', response.headers)

    response = self.app.get(request_path)
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(len(response.json['data']), 3)

    self.set_status('complete')

    response = self.app.get('/tenders/{}/awards/{}'.format(self.tender_id, award['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']["value"]["amount"], 500)

    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, award['id'], self.tender_token),
                                   {"data": {"status": "unsuccessful"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't update award in current (complete) tender status")


def patch_tender_award_unsuccessful(self):
    auth = self.app.authorization
    self.app.authorization = ('Basic', ('token', ''))
    request_path = '/tenders/{}/awards'.format(self.tender_id)
    response = self.app.post_json(request_path, {'data': {'suppliers': [test_organization], 'status': u'pending', 'bid_id': self.initial_bids[0]['id'], "value": {"amount": 500}}})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    award = response.json['data']

    self.app.authorization = auth
    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, award['id'], self.tender_token),
                                   {"data": {"status": "unsuccessful"}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertIn('Location', response.headers)
    new_award_location = response.headers['Location']

    response = self.app.patch_json('{}?acc_token={}'.format(new_award_location[-81:], self.tender_token), {"data": {"status": "active"}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertNotIn('Location', response.headers)

    response = self.app.get(request_path)
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(len(response.json['data']), 2)


def get_tender_award(self):
    auth = self.app.authorization

    self.app.authorization = ('Basic', ('token', ''))
    response = self.app.post_json('/tenders/{}/awards'.format(
        self.tender_id), {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': self.initial_bids[0]['id']}})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    award = response.json['data']
    self.app.authorization = auth

    response = self.app.get('/tenders/{}/awards/{}'.format(self.tender_id, award['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    award_data = response.json['data']
    self.assertEqual(award_data, award)

    response = self.app.get('/tenders/{}/awards/some_id'.format(self.tender_id), status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'award_id'}
    ])

    response = self.app.get('/tenders/some_id/awards/some_id', status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'tender_id'}
    ])


def patch_tender_award_Administrator_change(self):
    self.app.authorization = ('Basic', ('token', ''))
    response = self.app.post_json('/tenders/{}/awards'.format(
        self.tender_id), {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': self.initial_bids[0]['id']}})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    award = response.json['data']

# TenderLotAwardResourceTest


def create_tender_lot_award(self):
    auth = self.app.authorization
    self.app.authorization = ('Basic', ('token', ''))
    request_path = '/tenders/{}/awards'.format(self.tender_id)
    response = self.app.post_json(request_path, {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': self.initial_bids[0]['id']}}, status=422)
    self.assertEqual(response.status, '422 Unprocessable Entity')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'], [
        {"location": "body", "name": "lotID", "description": ["This field is required."]}
    ])

    response = self.app.post_json(request_path, {'data': {'suppliers': [test_organization], 'status': 'pending', 'bid_id': self.initial_bids[0]['id'], 'lotID': self.initial_lots[0]['id']}})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    award = response.json['data']
    self.assertEqual(award['suppliers'][0]['name'], test_organization['name'])
    self.assertEqual(award['lotID'], self.initial_lots[0]['id'])
    self.assertIn('id', award)
    self.assertIn(award['id'], response.headers['Location'])

    response = self.app.get(request_path)
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'][-1], award)

    self.app.authorization = auth
    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, award['id'], self.tender_token),
                                   {"data": {"status": "active"}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], u'active')

    response = self.app.get('/tenders/{}'.format(self.tender_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], u'active.awarded')

    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, award['id'], self.tender_token),
                                   {"data": {"status": "cancelled"}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], u'cancelled')
    self.assertIn('Location', response.headers)


def patch_tender_lot_award(self):
    request_path = '/tenders/{}/awards'.format(self.tender_id)
    response = self.app.patch_json('/tenders/{}/awards/some_id?acc_token={}'.format(self.tender_id, self.tender_token),
                                   {"data": {"status": "unsuccessful"}}, status=404)
    self.assertEqual((response.status, response.content_type), ('404 Not Found', 'application/json'))
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'award_id'}
    ])

    response = self.app.patch_json('/tenders/some_id/awards/some_id?acc_token={}'.format(self.tender_token),
                                   {"data": {"status": "unsuccessful"}}, status=404)
    self.assertEqual((response.status, response.content_type), ('404 Not Found', 'application/json'))
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'tender_id'}
    ])

    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), {"data": {"awardStatus": "unsuccessful"}}, status=422)
    self.assertEqual((response.status, response.content_type), ('422 Unprocessable Entity', 'application/json'))
    self.assertEqual(response.json['errors'], [
        {"location": "body", "name": "awardStatus", "description": "Rogue field"}
    ])
    # cant patch award to  unsuccessful if tender status is active.qualification
    #  and there is no cancelled earlier award with the same bid_id
    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), {"data": {"status": "unsuccessful"}}, status=403)
    self.assertEqual((response.status, response.content_type), ('403 Forbidden', 'application/json'))
    self.assertEqual(
        response.json['errors'][0]['description'],
        "Can't update award status to unsuccessful, if tender status is active.qualification"
        " and there is no cancelled award with the same bid_id")
    # successful patch award to active
    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), {"data": {"status": "active"}})
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))
    self.assertEqual(response.json['data']['status'], 'active')

    response = self.app.get('/tenders/{}?acc_token={}'.format(self.tender_id, self.tender_token))
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))
    self.assertEqual(response.json['data']['status'], 'active.awarded')
    self.assertIn('contracts', response.json['data'])
    self.assertEqual(response.json['data']['contracts'][0]['status'], 'pending')
    self.assertEqual(len(response.json['data']['awards']), 1)
    # success patch award into  cancelled -> new pending award is generated
    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), {"data": {"status": "cancelled"}})
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))
    self.assertEqual(response.json['data']['status'], 'cancelled')
    self.assertIn('Location', response.headers)
    new_award_location = response.headers['Location']

    response = self.app.get('/tenders/{}?acc_token={}'.format(self.tender_id, self.tender_token))
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))
    self.assertEqual(response.json['data']['status'], 'active.qualification')
    self.assertEqual(response.json['data']['contracts'][0]['status'], 'cancelled')
    self.assertEqual(len(response.json['data']['awards']), 2)
    self.assertEqual(response.json['data']['awards'][1]['status'], 'pending')
    self.assertEqual(response.json['data']['awards'][0]['bid_id'], response.json['data']['awards'][1]['bid_id'])
    self.assertIn(response.json['data']['awards'][1]['id'], new_award_location)
    new_award_id = response.json['data']['awards'][1]['id']
    # can't change cancelled award
    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), {"data": {"status": "unsuccessful"}}, status=403)
    self.assertEqual((response.status, response.content_type), ('403 Forbidden', 'application/json'))
    self.assertEqual(response.json['errors'][0]['description'], "Can't update award in current (cancelled) status")
    # patch pending award to unsuccessful
    self.award_id = new_award_id
    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), {"data": {"status": "unsuccessful"}})
    self.assertEqual(response.json['data']['status'], 'unsuccessful')
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))
    self.assertIn('Location', response.headers)
    new_award_location = response.headers['Location']

    response = self.app.get('/tenders/{}?acc_token={}'.format(self.tender_id, self.tender_token))
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))
    self.assertEqual(response.json['data']['status'], 'active.qualification')
    self.assertEqual(len(response.json['data']['contracts']), 1)
    self.assertEqual(len(response.json['data']['awards']), 3)
    self.assertEqual(response.json['data']['awards'][2]['status'], 'pending')
    self.assertNotEqual(response.json['data']['awards'][1]['bid_id'], response.json['data']['awards'][2]['bid_id'])
    self.assertIn(response.json['data']['awards'][2]['id'], new_award_location)

    self.award_id = response.json['data']['awards'][-1]['id']
    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), {"data": {"status": "active"}})
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))

    response = self.app.get('/tenders/{}?acc_token={}'.format(self.tender_id, self.tender_token))
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))
    self.assertEqual(response.json['data']['status'], 'active.awarded')
    self.assertEqual(len(response.json['data']['contracts']), 2)
    self.assertEqual(len(response.json['data']['awards']), 3)
    self.assertEqual(response.json['data']['awards'][-1]['status'], 'active')

    self.set_status('complete')

    response = self.app.get('/tenders/{}/awards/{}'.format(self.tender_id, self.award_id))
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))
    self.assertEqual(response.json['data']["value"]["amount"], 479)

    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), {"data": {"status": "unsuccessful"}}, status=403)
    self.assertEqual((response.status, response.content_type), ('403 Forbidden', 'application/json'))
    self.assertEqual(response.json['errors'][0]["description"], "Can't update award in current (complete) tender status")


def patch_tender_lot_award_unsuccessful(self):
    request_path = '/tenders/{}/awards'.format(self.tender_id)
    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), {"data": {"status": "unsuccessful"}}, status=403)
    self.assertEqual((response.status, response.content_type), ('403 Forbidden', 'application/json'))
    self.assertEqual(
        response.json['errors'][0]['description'],
        "Can't update award status to unsuccessful, if tender status is active.qualification and"
        " there is no cancelled award with the same bid_id")

    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), {"data": {"status": "active"}})
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))
    self.assertEqual(response.json['data']['status'], 'active')

    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), {"data": {"status": "cancelled"}})
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))
    self.assertEqual(response.json['data']['status'], 'cancelled')

    response = self.app.get('/tenders/{}?acc_token={}'.format(self.tender_id, self.tender_token))
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))
    new_award_id = response.json['data']['awards'][-1]['id']
    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
        self.tender_id, new_award_id, self.tender_token), {"data": {"status": "unsuccessful"}})
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))
    self.assertIn('Location', response.headers)
    new_award_location = response.headers['Location']

    response = self.app.patch_json(new_award_location[-81:] + '?acc_token={}'.format(self.tender_token),
                                   {"data": {"status": "active"}})
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))
    self.assertNotIn('Location', response.headers)

    response = self.app.get(request_path)
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))
    self.assertEqual(len(response.json['data']), 3)


# Tender2LotAwardResourceTest


def create_tender_lots_award(self):
    auth = self.app.authorization

    request_path = '/tenders/{}/awards'.format(self.tender_id)
    response = self.app.post_json('/tenders/{}/cancellations?acc_token={}'.format(self.tender_id, self.tender_token), {'data': {
        'reason': 'cancellation reason',
        'status': 'active',
        "cancellationOf": "lot",
        "relatedLot": self.initial_lots[0]['id']
    }})
    self.assertEqual(response.status, '201 Created')

    self.app.authorization = ('Basic', ('token', ''))
    response = self.app.post_json(request_path, {'data': {
        'suppliers': [test_organization],
        'status': 'pending',
        'bid_id': self.initial_bids[0]['id'],
        'lotID': self.initial_lots[0]['id']
    }}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can create award only in active lot status")

    response = self.app.post_json(request_path, {'data': {
        'suppliers': [test_organization],
        'status': 'pending',
        'bid_id': self.initial_bids[0]['id'],
        'lotID': self.initial_lots[1]['id']
    }})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    award = response.json['data']
    self.assertEqual(award['suppliers'][0]['name'], test_organization['name'])
    self.assertEqual(award['lotID'], self.initial_lots[1]['id'])
    self.assertIn('id', award)
    self.assertIn(award['id'], response.headers['Location'])

    response = self.app.get(request_path)
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'][-1], award)

    self.app.authorization = auth
    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, award['id'], self.tender_token), {"data": {"status": "active"}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], u'active')

    response = self.app.get('/tenders/{}'.format(self.tender_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], u'active.awarded')

    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, award['id'], self.tender_token), {"data": {"status": "cancelled"}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], u'cancelled')
    self.assertIn('Location', response.headers)


def patch_tender_lots_award(self):
    auth = self.app.authorization
    self.app.authorization = ('Basic', ('token', ''))
    request_path = '/tenders/{}/awards'.format(self.tender_id)
    response = self.app.post_json(request_path, {'data': {'suppliers': [test_organization], 'status': u'pending', 'bid_id': self.initial_bids[0]['id'], 'lotID': self.initial_lots[0]['id'], "value": {"amount": 500}}})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    award = response.json['data']

    self.app.authorization = auth
    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, award['id'], self.tender_token),
                                   {"data": {"status": "active"}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')

    response = self.app.get(request_path)
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(len(response.json['data']), 2)
    new_award = response.json['data'][-1]

    response = self.app.post_json('/tenders/{}/cancellations?acc_token={}'.format(self.tender_id, self.tender_token), {'data': {
        'reason': 'cancellation reason',
        'status': 'active',
        "cancellationOf": "lot",
        "relatedLot": self.initial_lots[1]['id']
    }})
    self.assertEqual(response.status, '201 Created')

    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(self.tender_id, new_award['id'], self.tender_token),
                                   {"data": {"status": "unsuccessful"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can update award only in active lot status")


def not_found_award_document(self):
    response = self.app.post('/tenders/some_id/awards/some_id/documents?acc_token={}'.format(self.tender_token), status=404, upload_files=[
                             ('file', 'name.doc', 'content')])
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'tender_id'}
    ])

    response = self.app.post('/tenders/{}/awards/some_id/documents?acc_token={}'.format(self.tender_id, self.tender_token), status=404, upload_files=[('file', 'name.doc', 'content')])
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'award_id'}
    ])

    response = self.app.post('/tenders/{}/awards/{}/documents?acc_token={}'.format(self.tender_id, self.award_id, self.tender_token), status=404, upload_files=[
                             ('invalid_value', 'name.doc', 'content')])
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'body', u'name': u'file'}
    ])

    response = self.app.get('/tenders/some_id/awards/some_id/documents', status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'tender_id'}
    ])

    response = self.app.get('/tenders/{}/awards/some_id/documents'.format(self.tender_id), status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'award_id'}
    ])

    response = self.app.get('/tenders/some_id/awards/some_id/documents/some_id', status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'tender_id'}
    ])

    response = self.app.get('/tenders/{}/awards/some_id/documents/some_id'.format(self.tender_id), status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'award_id'}
    ])

    response = self.app.get('/tenders/{}/awards/{}/documents/some_id'.format(self.tender_id, self.award_id), status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'document_id'}
    ])

    response = self.app.put('/tenders/some_id/awards/some_id/documents/some_id?acc_token={}'.format(self.tender_token), status=404,
                            upload_files=[('file', 'name.doc', 'content2')])
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'tender_id'}
    ])

    response = self.app.put('/tenders/{}/awards/some_id/documents/some_id?acc_token={}'.format(self.tender_id, self.tender_token), status=404,
                            upload_files=[('file', 'name.doc', 'content2')])
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'url', u'name': u'award_id'}
    ])

    response = self.app.put('/tenders/{}/awards/{}/documents/some_id?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), status=404, upload_files=[('file', 'name.doc', 'content2')])
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location': u'url', u'name': u'document_id'}
    ])


def create_tender_award_document(self):
    response = self.app.post('/tenders/{}/awards/{}/documents?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), upload_files=[('file', 'name.doc', 'content')])
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    self.assertIn(doc_id, response.headers['Location'])
    self.assertEqual('name.doc', response.json["data"]["title"])
    if self.docservice:
        self.assertIn('Signature=', response.json["data"]["url"])
        self.assertIn('KeyID=', response.json["data"]["url"])
        self.assertNotIn('Expires=', response.json["data"]["url"])
        key = response.json["data"]["url"].split('/')[-1].split('?')[0]
        tender = self.db.get(self.tender_id)
        self.assertIn(key, tender['awards'][-1]['documents'][-1]["url"])
        self.assertIn('Signature=', tender['awards'][-1]['documents'][-1]["url"])
        self.assertIn('KeyID=', tender['awards'][-1]['documents'][-1]["url"])
        self.assertNotIn('Expires=', tender['awards'][-1]['documents'][-1]["url"])
    else:
        key = response.json["data"]["url"].split('?')[-1].split('=')[-1]

    response = self.app.get('/tenders/{}/awards/{}/documents'.format(self.tender_id, self.award_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"][0]["id"])
    self.assertEqual('name.doc', response.json["data"][0]["title"])

    response = self.app.get('/tenders/{}/awards/{}/documents?all=true'.format(self.tender_id, self.award_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"][0]["id"])
    self.assertEqual('name.doc', response.json["data"][0]["title"])

    response = self.app.get('/tenders/{}/awards/{}/documents/{}?download=some_id'.format(
        self.tender_id, self.award_id, doc_id), status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location': u'url', u'name': u'download'}
    ])

    if self.docservice:
        response = self.app.get('/tenders/{}/awards/{}/documents/{}?download={}'.format(
            self.tender_id, self.award_id, doc_id, key))
        self.assertEqual(response.status, '302 Moved Temporarily')
        self.assertIn('http://localhost/get/', response.location)
        self.assertIn('Signature=', response.location)
        self.assertIn('KeyID=', response.location)
        self.assertNotIn('Expires=', response.location)
    else:
        response = self.app.get('/tenders/{}/awards/{}/documents/{}?download={}'.format(
            self.tender_id, self.award_id, doc_id, key))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/msword')
        self.assertEqual(response.content_length, 7)
        self.assertEqual(response.body, 'content')

    response = self.app.get('/tenders/{}/awards/{}/documents/{}'.format(
        self.tender_id, self.award_id, doc_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    self.assertEqual('name.doc', response.json["data"]["title"])

    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), {"data": {"status": "active"}})
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))

    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), {"data": {"status": "cancelled"}})
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))

    response = self.app.get('/tenders/{}/awards'.format(self.tender_id))
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))
    pending_award_id = response.json['data'][-1]['id']

    response = self.app.post('/tenders/{}/awards/{}/documents?acc_token={}'.format(
        self.tender_id, pending_award_id, self.tender_token), upload_files=[('file', 'name.doc', 'content')])
    self.assertEqual((response.status, response.content_type), ('201 Created', 'application/json'))
    doc_id = response.json["data"]['id']
    self.assertIn(doc_id, response.headers['Location'])
    self.assertEqual('name.doc', response.json["data"]["title"])

    self.set_status('complete')

    response = self.app.post('/tenders/{}/awards/{}/documents?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), upload_files=[('file', 'name.doc', 'content')], status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't add document in current (complete) tender status")


def put_tender_award_document(self):
    response = self.app.post('/tenders/{}/awards/{}/documents?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), upload_files=[('file', 'name.doc', 'content')])
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    self.assertIn(doc_id, response.headers['Location'])

    response = self.app.put('/tenders/{}/awards/{}/documents/{}?acc_token={}'.format(self.tender_id, self.award_id, doc_id, self.tender_token),
                            status=404,
                            upload_files=[('invalid_name', 'name.doc', 'content')])
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'body', u'name': u'file'}
    ])

    response = self.app.put('/tenders/{}/awards/{}/documents/{}?acc_token={}'.format(
        self.tender_id, self.award_id, doc_id, self.tender_token), upload_files=[('file', 'name.doc', 'content2')])
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    if self.docservice:
        self.assertIn('Signature=', response.json["data"]["url"])
        self.assertIn('KeyID=', response.json["data"]["url"])
        self.assertNotIn('Expires=', response.json["data"]["url"])
        key = response.json["data"]["url"].split('/')[-1].split('?')[0]
        tender = self.db.get(self.tender_id)
        self.assertIn(key, tender['awards'][-1]['documents'][-1]["url"])
        self.assertIn('Signature=', tender['awards'][-1]['documents'][-1]["url"])
        self.assertIn('KeyID=', tender['awards'][-1]['documents'][-1]["url"])
        self.assertNotIn('Expires=', tender['awards'][-1]['documents'][-1]["url"])
    else:
        key = response.json["data"]["url"].split('?')[-1].split('=')[-1]

    response = self.app.get('/tenders/{}/awards/{}/documents/{}?download={}'.format(
        self.tender_id, self.award_id, doc_id, key))
    if self.docservice:
        self.assertEqual(response.status, '302 Moved Temporarily')
        self.assertIn('http://localhost/get/', response.location)
        self.assertIn('Signature=', response.location)
        self.assertIn('KeyID=', response.location)
        self.assertNotIn('Expires=', response.location)
    else:
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/msword')
        self.assertEqual(response.content_length, 8)
        self.assertEqual(response.body, 'content2')

    response = self.app.get('/tenders/{}/awards/{}/documents/{}'.format(
        self.tender_id, self.award_id, doc_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    self.assertEqual('name.doc', response.json["data"]["title"])

    response = self.app.put('/tenders/{}/awards/{}/documents/{}?acc_token={}'.format(
        self.tender_id, self.award_id, doc_id, self.tender_token), 'content3', content_type='application/msword')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    if self.docservice:
        self.assertIn('Signature=', response.json["data"]["url"])
        self.assertIn('KeyID=', response.json["data"]["url"])
        self.assertNotIn('Expires=', response.json["data"]["url"])
        key = response.json["data"]["url"].split('/')[-1].split('?')[0]
        tender = self.db.get(self.tender_id)
        self.assertIn(key, tender['awards'][-1]['documents'][-1]["url"])
        self.assertIn('Signature=', tender['awards'][-1]['documents'][-1]["url"])
        self.assertIn('KeyID=', tender['awards'][-1]['documents'][-1]["url"])
        self.assertNotIn('Expires=', tender['awards'][-1]['documents'][-1]["url"])
    else:
        key = response.json["data"]["url"].split('?')[-1].split('=')[-1]

    response = self.app.get('/tenders/{}/awards/{}/documents/{}?download={}'.format(
        self.tender_id, self.award_id, doc_id, key))
    if self.docservice:
        self.assertEqual(response.status, '302 Moved Temporarily')
        self.assertIn('http://localhost/get/', response.location)
        self.assertIn('Signature=', response.location)
        self.assertIn('KeyID=', response.location)
        self.assertNotIn('Expires=', response.location)
    else:
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/msword')
        self.assertEqual(response.content_length, 8)
        self.assertEqual(response.body, 'content3')

    self.set_status('complete')

    response = self.app.put('/tenders/{}/awards/{}/documents/{}?acc_token={}'.format(
        self.tender_id, self.award_id, doc_id, self.tender_token), upload_files=[('file', 'name.doc', 'content3')], status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't update document in current (complete) tender status")


def patch_tender_award_document(self):
    response = self.app.post('/tenders/{}/awards/{}/documents?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), upload_files=[('file', 'name.doc', 'content')])
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    self.assertIn(doc_id, response.headers['Location'])

    response = self.app.patch_json('/tenders/{}/awards/{}/documents/{}?acc_token={}'.format(self.tender_id, self.award_id, doc_id, self.tender_token), {"data": {"description": "document description"}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])

    response = self.app.get('/tenders/{}/awards/{}/documents/{}'.format(
        self.tender_id, self.award_id, doc_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    self.assertEqual('document description', response.json["data"]["description"])

    self.set_status('complete')

    response = self.app.patch_json('/tenders/{}/awards/{}/documents/{}?acc_token={}'.format(self.tender_id, self.award_id, doc_id, self.tender_token), {"data": {"description": "document description"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can't update document in current (complete) tender status")


def create_award_document_bot(self):
    self.app.authorization = ('Basic', ('bot', 'bot'))
    response = self.app.post('/tenders/{}/awards/{}/documents'.format(
        self.tender_id, self.award_id), upload_files=[('file', 'edr_request.yaml', 'content')])
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    self.assertIn(doc_id, response.headers['Location'])
    self.assertEqual('edr_request.yaml', response.json["data"]["title"])
    if self.docservice:
        self.assertIn('Signature=', response.json["data"]["url"])
        self.assertIn('KeyID=', response.json["data"]["url"])
        self.assertNotIn('Expires=', response.json["data"]["url"])
        key = response.json["data"]["url"].split('/')[-1].split('?')[0]
        tender = self.db.get(self.tender_id)
        self.assertIn(key, tender['awards'][-1]['documents'][-1]["url"])
        self.assertIn('Signature=', tender['awards'][-1]['documents'][-1]["url"])
        self.assertIn('KeyID=', tender['awards'][-1]['documents'][-1]["url"])
        self.assertNotIn('Expires=', tender['awards'][-1]['documents'][-1]["url"])


def patch_not_author(self):
    authorization = self.app.authorization
    self.app.authorization = ('Basic', ('bot', 'bot'))
    response = self.app.post('/tenders/{}/awards/{}/documents?acc_token={}'.format(self.tender_id, self.award_id, self.tender_token),
                             upload_files=[('file', 'name.doc', 'content')])
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    self.assertIn(doc_id, response.headers['Location'])

    self.app.authorization = authorization
    response = self.app.patch_json('/tenders/{}/awards/{}/documents/{}?acc_token={}'.format(self.tender_id, self.award_id, doc_id, self.tender_token),
                                   {"data": {"description": "document description"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can update document only author")

# Tender2LotAwardDocumentResourceTest


def create_tender_lots_award_document(self):
    response = self.app.post('/tenders/{}/awards/{}/documents?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), upload_files=[('file', 'name.doc', 'content')])
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    self.assertIn(doc_id, response.headers['Location'])
    self.assertEqual('name.doc', response.json["data"]["title"])
    if self.docservice:
        self.assertIn('Signature=', response.json["data"]["url"])
        self.assertIn('KeyID=', response.json["data"]["url"])
        self.assertNotIn('Expires=', response.json["data"]["url"])
        key = response.json["data"]["url"].split('/')[-1].split('?')[0]
        tender = self.db.get(self.tender_id)
        self.assertIn(key, tender['awards'][-1]['documents'][-1]["url"])
        self.assertIn('Signature=', tender['awards'][-1]['documents'][-1]["url"])
        self.assertIn('KeyID=', tender['awards'][-1]['documents'][-1]["url"])
        self.assertNotIn('Expires=', tender['awards'][-1]['documents'][-1]["url"])
    else:
        key = response.json["data"]["url"].split('?')[-1].split('=')[-1]

    response = self.app.get('/tenders/{}/awards/{}/documents'.format(self.tender_id, self.award_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"][0]["id"])
    self.assertEqual('name.doc', response.json["data"][0]["title"])

    response = self.app.get('/tenders/{}/awards/{}/documents?all=true'.format(self.tender_id, self.award_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"][0]["id"])
    self.assertEqual('name.doc', response.json["data"][0]["title"])

    response = self.app.get('/tenders/{}/awards/{}/documents/{}?download=some_id'.format(
        self.tender_id, self.award_id, doc_id), status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location': u'url', u'name': u'download'}
    ])

    response = self.app.get('/tenders/{}/awards/{}/documents/{}?download={}'.format(
        self.tender_id, self.award_id, doc_id, key))
    if self.docservice:
        self.assertEqual(response.status, '302 Moved Temporarily')
        self.assertIn('http://localhost/get/', response.location)
        self.assertIn('Signature=', response.location)
        self.assertIn('KeyID=', response.location)
        self.assertNotIn('Expires=', response.location)
    else:
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/msword')
        self.assertEqual(response.content_length, 7)
        self.assertEqual(response.body, 'content')

    response = self.app.get('/tenders/{}/awards/{}/documents/{}'.format(
        self.tender_id, self.award_id, doc_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    self.assertEqual('name.doc', response.json["data"]["title"])

    response = self.app.post_json('/tenders/{}/cancellations?acc_token={}'.format(self.tender_id, self.tender_token), {'data': {
        'reason': 'cancellation reason',
        'status': 'active',
        "cancellationOf": "lot",
        "relatedLot": self.initial_lots[0]['id']
    }})
    self.assertEqual(response.status, '201 Created')

    response = self.app.post('/tenders/{}/awards/{}/documents?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), upload_files=[('file', 'name.doc', 'content')], status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can add document only in active lot status")


def put_tender_lots_award_document(self):
    response = self.app.post('/tenders/{}/awards/{}/documents?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), upload_files=[('file', 'name.doc', 'content')])
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    self.assertIn(doc_id, response.headers['Location'])

    response = self.app.put('/tenders/{}/awards/{}/documents/{}?acc_token={}'.format(self.tender_id, self.award_id, doc_id, self.tender_token),
                            status=404,
                            upload_files=[('invalid_name', 'name.doc', 'content')])
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location':
            u'body', u'name': u'file'}
    ])

    response = self.app.put('/tenders/{}/awards/{}/documents/{}?acc_token={}'.format(
        self.tender_id, self.award_id, doc_id, self.tender_token), upload_files=[('file', 'name.doc', 'content2')])
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    if self.docservice:
        self.assertIn('Signature=', response.json["data"]["url"])
        self.assertIn('KeyID=', response.json["data"]["url"])
        self.assertNotIn('Expires=', response.json["data"]["url"])
        key = response.json["data"]["url"].split('/')[-1].split('?')[0]
        tender = self.db.get(self.tender_id)
        self.assertIn(key, tender['awards'][-1]['documents'][-1]["url"])
        self.assertIn('Signature=', tender['awards'][-1]['documents'][-1]["url"])
        self.assertIn('KeyID=', tender['awards'][-1]['documents'][-1]["url"])
        self.assertNotIn('Expires=', tender['awards'][-1]['documents'][-1]["url"])
    else:
        key = response.json["data"]["url"].split('?')[-1].split('=')[-1]

    response = self.app.get('/tenders/{}/awards/{}/documents/{}?download={}'.format(
        self.tender_id, self.award_id, doc_id, key))
    if self.docservice:
        self.assertEqual(response.status, '302 Moved Temporarily')
        self.assertIn('http://localhost/get/', response.location)
        self.assertIn('Signature=', response.location)
        self.assertIn('KeyID=', response.location)
        self.assertNotIn('Expires=', response.location)
    else:
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/msword')
        self.assertEqual(response.content_length, 8)
        self.assertEqual(response.body, 'content2')

    response = self.app.get('/tenders/{}/awards/{}/documents/{}'.format(
        self.tender_id, self.award_id, doc_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    self.assertEqual('name.doc', response.json["data"]["title"])

    response = self.app.put('/tenders/{}/awards/{}/documents/{}?acc_token={}'.format(
        self.tender_id, self.award_id, doc_id, self.tender_token), 'content3', content_type='application/msword')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    if self.docservice:
        self.assertIn('Signature=', response.json["data"]["url"])
        self.assertIn('KeyID=', response.json["data"]["url"])
        self.assertNotIn('Expires=', response.json["data"]["url"])
        key = response.json["data"]["url"].split('/')[-1].split('?')[0]
        tender = self.db.get(self.tender_id)
        self.assertIn(key, tender['awards'][-1]['documents'][-1]["url"])
        self.assertIn('Signature=', tender['awards'][-1]['documents'][-1]["url"])
        self.assertIn('KeyID=', tender['awards'][-1]['documents'][-1]["url"])
        self.assertNotIn('Expires=', tender['awards'][-1]['documents'][-1]["url"])
    else:
        key = response.json["data"]["url"].split('?')[-1].split('=')[-1]

    response = self.app.get('/tenders/{}/awards/{}/documents/{}?download={}'.format(
        self.tender_id, self.award_id, doc_id, key))
    if self.docservice:
        self.assertEqual(response.status, '302 Moved Temporarily')
        self.assertIn('http://localhost/get/', response.location)
        self.assertIn('Signature=', response.location)
        self.assertIn('KeyID=', response.location)
        self.assertNotIn('Expires=', response.location)
    else:
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/msword')
        self.assertEqual(response.content_length, 8)
        self.assertEqual(response.body, 'content3')

    response = self.app.post_json('/tenders/{}/cancellations?acc_token={}'.format(self.tender_id, self.tender_token), {'data': {
        'reason': 'cancellation reason',
        'status': 'active',
        "cancellationOf": "lot",
        "relatedLot": self.initial_lots[0]['id']
    }})
    self.assertEqual(response.status, '201 Created')

    response = self.app.put('/tenders/{}/awards/{}/documents/{}?acc_token={}'.format(
        self.tender_id, self.award_id, doc_id, self.tender_token), upload_files=[('file', 'name.doc', 'content3')], status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can update document only in active lot status")


def patch_tender_lots_award_document(self):
    response = self.app.post('/tenders/{}/awards/{}/documents?acc_token={}'.format(
        self.tender_id, self.award_id, self.tender_token), upload_files=[('file', 'name.doc', 'content')])
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    doc_id = response.json["data"]['id']
    self.assertIn(doc_id, response.headers['Location'])

    response = self.app.patch_json('/tenders/{}/awards/{}/documents/{}?acc_token={}'.format(self.tender_id, self.award_id, doc_id, self.tender_token), {"data": {"description": "document description"}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])

    response = self.app.get('/tenders/{}/awards/{}/documents/{}'.format(
        self.tender_id, self.award_id, doc_id))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(doc_id, response.json["data"]["id"])
    self.assertEqual('document description', response.json["data"]["description"])

    response = self.app.post_json('/tenders/{}/cancellations?acc_token={}'.format(self.tender_id, self.tender_token), {'data': {
        'reason': 'cancellation reason',
        'status': 'active',
        "cancellationOf": "lot",
        "relatedLot": self.initial_lots[0]['id']
    }})
    self.assertEqual(response.status, '201 Created')

    response = self.app.patch_json('/tenders/{}/awards/{}/documents/{}?acc_token={}'.format(self.tender_id, self.award_id, doc_id, self.tender_token), {"data": {"description": "document description"}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]["description"], "Can update document only in active lot status")


def check_tender_award(self):
    # get bids
    response = self.app.get('/tenders/{}/bids'.format(self.tender_id))
    self.assertEqual(response.status, "200 OK")
    bids = response.json['data']
    # sort bids by value amount, from lower to higher if reverse is False (all tenders, except esco)
    # or from higher to lower if reverse is True (esco tenders)
    sorted_bids = sorted(bids, key=lambda bid: bid['lotValues'][0]['value'][self.awarding_key], reverse=self.reverse)

    # get awards
    response = self.app.get('/tenders/{}/awards'.format(self.tender_id))
    # get pending award
    award_id = [i['id'] for i in response.json['data'] if i['status'] == 'pending'][0]
    # check award
    response = self.app.get('/tenders/{}/awards/{}'.format(self.tender_id, award_id))
    self.assertEqual(response.status, "200 OK")
    self.assertEqual(response.json['data']['suppliers'][0]['name'], sorted_bids[0]['tenderers'][0]['name'])
    self.assertEqual(response.json['data']['suppliers'][0]['identifier']['id'], sorted_bids[0]['tenderers'][0]['identifier']['id'])
    self.assertEqual(response.json['data']['bid_id'], sorted_bids[0]['id'])

    # cancel award
    self.app.authorization = ('Basic', ('broker', ''))
    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
        self.tender_id, award_id, self.tender_token), {"data": {"status": "unsuccessful"}}, status=403)
    self.assertEqual((response.status, response.content_type), ('403 Forbidden', 'application/json'))
    self.assertEqual(
        response.json['errors'][0]['description'],
        "Can't update award status to unsuccessful, if tender status is active.qualification"
        " and there is no cancelled award with the same bid_id")

    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
        self.tender_id, award_id, self.tender_token), {"data": {"status": "active"}})
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))
    self.assertEqual(response.json['data']['status'], 'active')

    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
        self.tender_id, award_id, self.tender_token), {"data": {"status": "cancelled"}})
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))
    self.assertEqual(response.json['data']['status'], 'cancelled')

    response = self.app.get('/tenders/{}?acc_token={}'.format(self.tender_id, self.tender_token))
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))
    new_award_id = response.json['data']['awards'][-1]['id']
    response = self.app.patch_json('/tenders/{}/awards/{}?acc_token={}'.format(
        self.tender_id, new_award_id, self.tender_token), {"data": {"status": "unsuccessful"}})
    self.assertEqual((response.status, response.content_type), ('200 OK', 'application/json'))

    # get awards
    response = self.app.get('/tenders/{}/awards'.format(self.tender_id))
    # get pending award
    award_id = [i['id'] for i in response.json['data'] if i['status'] == 'pending'][0]
    # check new award
    response = self.app.get('/tenders/{}/awards/{}'.format(self.tender_id, award_id))
    self.assertEqual(response.status, "200 OK")
    self.assertEqual(response.json['data']['suppliers'][0]['name'], sorted_bids[1]['tenderers'][0]['name'])
    self.assertEqual(response.json['data']['suppliers'][0]['identifier']['id'], sorted_bids[1]['tenderers'][0]['identifier']['id'])
    self.assertEqual(response.json['data']['bid_id'], sorted_bids[1]['id'])
