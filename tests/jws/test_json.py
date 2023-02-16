from joserfc.jws import serialize_json, deserialize_json
from joserfc.jwk import RSAKey
from unittest import TestCase
from tests.util import read_key


class TestJSON(TestCase):
    def test_serialize_json(self):
        key = RSAKey.import_key(read_key('openssl-rsa-private.pem'))

        members = {'protected': {'alg': 'RS256'}}

        # flatten
        value = serialize_json(members, b'hello', key)
        self.assertIn('signature', value)
        self.assertNotIn('signatures', value)

        obj = deserialize_json(value, key)
        self.assertEqual(obj.payload, b'hello')

        # complete
        value = serialize_json([members], b'hello', key)
        self.assertNotIn('signature', value)
        self.assertIn('signatures', value)

        obj = deserialize_json(value, key)
        self.assertEqual(obj.payload, b'hello')