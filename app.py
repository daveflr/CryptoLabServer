from os.path import join

from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import hashlib
import os

app = Flask(__name__)
api = Api(app)
CORS(app)

malespin = {
    'a': 'e',
    'i': 'o',
    'b': 't',
    'f': 'g',
    'p': 'm',
    'A': 'E',
    'I': 'O',
    'B': 'T',
    'F': 'G',
    'P': 'M'
}


def encode(text):
    counter = 0
    list_str = list(text)
    for letter in text:
        space = 0
        for key, value in malespin.items():
            if letter == key:
                list_str[counter] = value
                break
            elif letter == value:
                list_str[counter] = key
                break
            space += 1
        counter += 1
    return ''.join(list_str)


xcrypt_code = {
    'e': 'w',
    'a': 'k',
    'o': 'x',
    's': 'ñ',
    'r': 'j',
    'n': 'z',
    'i': 'f',
    'd': 'h',
    'l': 'q',
    'c': 'y',
    't': 'v',
    'u': 'g',
    'm': 'b'
}


def xcrypt(text):
    counter = 0
    list_str = list(text)
    for letter in text:
        space = 0
        for key, value in xcrypt_code.items():
            if letter == key or letter.upper() == key.upper():
                list_str[counter] = value
                break
            elif letter == value or letter.upper() == value.upper():
                list_str[counter] = key
                break
            space += 1
        counter += 1
    return ''.join(list_str)


class Encode(Resource):
    @staticmethod
    def get():
        method = request.args.get('method')
        text = request.args.get('text')

        if method == 'MD5':
            text = hashlib.md5(text.encode()).hexdigest()
        elif method == 'SHA-1':
            text = hashlib.sha1(text.encode()).hexdigest()
        elif method == 'SHA-256':
            text = hashlib.sha256(text.encode()).hexdigest()
        elif method == 'SHA-512':
            text = hashlib.sha512(text.encode()).hexdigest()
        elif method == 'Malespin':
            text = encode(text)
        elif method == 'XCrypt':
            text = xcrypt(text)

        return {'method': method, 'text': text}, 200


class Decode(Resource):
    @staticmethod
    def get():
        method = request.args.get('method')
        text = request.args.get('text')
        return {'method': method, 'text': text}, 200


api.add_resource(Encode, '/encode')
api.add_resource(Decode, '/decode')

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
