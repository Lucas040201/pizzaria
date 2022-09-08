from hashlib import sha1
from werkzeug.utils import secure_filename
import os
import time

from app.infra.repository.product_repository import ProductRepository
from app.services.service_base import ServiceBase


class ProductService(ServiceBase):
    def __init__(self):
        super(ProductService, self).__init__(ProductRepository())

    def insert_product(self, data, file):
        if not self.__validate_info(data, file):
            raise Exception

        product_info = {}
        for info in data:
            product_info[info] = data[info]

        product_info['image'] = self.__hash_image_and_move(file['image'])
        product_info['price'] = float(product_info['price'])
        stored_product = self.insert(product_info)
        return stored_product

    def update_product(self, product_id, data, file):
        if not self.__validate_info(data, file):
            raise Exception

        updated_info = {}

        for info in data:
            updated_info[info] = data[info]

        if not file is None:
            updated_info['image'] = self.__hash_image_and_move(file['image'])

        updated = self.update(product_id, updated_info)
        return updated


    def __hash_image_and_move(self, file):
        filename = file.filename.rsplit('.', 1)[0].lower()
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = str(filename + str(time.time()))
        hashed_filename = sha1(str.encode(filename)).hexdigest()
        hashed_filename = f"{str(hashed_filename)}.{ext}"

        filename = secure_filename(hashed_filename)
        file.save(os.path.join("static/imagem/products/", filename))
        return filename

    def __validate_info(self, data, file):
        product = {
            'product_name': '',
            'price': '',
            'description': '',
            'excerpt': '',
        }

        validated = True

        for info in product:
            if not info in data or not data[info]:
                validated = False
                break

        if not file is None:
            if not 'image' in file or not file['image']:
                return False

        return validated
