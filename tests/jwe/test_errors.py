from unittest import TestCase
from joserfc import jwe
from joserfc.jwk import OctKey
from joserfc.registry import HeaderParameter
from joserfc.errors import InvalidKeyTypeError, InvalidKeyLengthError
from tests.base import load_key


class TestJWEErrors(TestCase):
    def test_dir_with_invalid_key_type(self):
        key = load_key("ec-p256-private.pem")
        protected = {"alg": "dir", "enc": "A128CBC-HS256"}
        self.assertRaises(
            InvalidKeyTypeError,
            jwe.encrypt_compact,
            protected, b"i", key,
        )

        protected = {"alg": "A128KW", "enc": "A128CBC-HS256"}
        self.assertRaises(
            InvalidKeyTypeError,
            jwe.encrypt_compact,
            protected, b"i", key,
        )

        protected = {"alg": "ECDH-ES+A128KW", "enc": "A128CBC-HS256"}
        self.assertRaises(
            InvalidKeyTypeError,
            jwe.encrypt_compact,
            protected, b"i", "secret",
        )

        protected = {"alg": "PBES2-HS256+A128KW", "enc": "A128CBC-HS256"}
        self.assertRaises(
            InvalidKeyTypeError,
            jwe.encrypt_compact,
            protected, b"i", key,
            algorithms=["PBES2-HS256+A128KW", "A128CBC-HS256"]
        )

    def test_rsa_with_invalid_key_type(self):
        key = load_key("ec-p256-private.pem")
        protected = {"alg": "RSA-OAEP", "enc": "A128CBC-HS256"}
        self.assertRaises(
            InvalidKeyTypeError,
            jwe.encrypt_compact,
            protected, b"i", key,
        )

    def test_invalid_alg(self):
        protected = {"alg": "INVALID", "enc": "A128CBC-HS256"}
        self.assertRaises(
            ValueError,
            jwe.encrypt_compact,
            protected, b"i", "secret"
        )

    def test_invalid_key_length(self):
        protected = {"alg": "dir", "enc": "A128CBC-HS256"}
        self.assertRaises(
            InvalidKeyLengthError,
            jwe.encrypt_compact,
            protected, b"i", "secret"
        )
        protected = {"alg": "A128KW", "enc": "A128CBC-HS256"}
        self.assertRaises(
            InvalidKeyLengthError,
            jwe.encrypt_compact,
            protected, b"i", "secret"
        )

    def test_extra_header(self):
        key = OctKey.generate_key(256)
        protected = {"alg": "dir", "enc": "A128CBC-HS256", "custom": "hi"}
        self.assertRaises(
            ValueError,
            jwe.encrypt_compact,
            protected, b"i", key
        )

        registry = jwe.JWERegistry(strict_check_header=False)
        jwe.encrypt_compact(protected, b"i", key, registry=registry)

        registry = jwe.JWERegistry(header_registry={
            "custom": HeaderParameter("Custom", "str")
        })
        jwe.encrypt_compact(protected, b"i", key, registry=registry)

    def test_strict_check_header_with_more_header_registry(self):
        key = load_key("ec-p256-private.pem")
        protected = {"alg": "ECDH-ES", "enc": "A128CBC-HS256", "custom": "hi"}
        self.assertRaises(
            ValueError,
            jwe.encrypt_compact,
            protected, b"i", key
        )
        registry = jwe.JWERegistry(strict_check_header=False)
        jwe.encrypt_compact(protected, b"i", key, registry=registry)