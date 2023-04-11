from app.infra.repository.address_repository import AddressRepository
from app.services.service_base import ServiceBase


class AddressService(ServiceBase):
    def __init__(self):
        super(AddressService, self).__init__(AddressRepository())

    def insert_address(self, user, data):

        new_address = {
            "user_id": user.id,
            "cep": data['cep'],
            "number": data['number'],
            "district": data['district'],
            "street": data['street'],
            "uf": data['uf']
        }

        stored_address = self.insert(new_address)

        return stored_address

    def update_address(self, address_id, data):
        address_info = {
            "cep": data['cep'],
            "number": data['number'],
            "district": data['district'],
            "street": data['street'],
            "uf": data['uf']
        }

        updated_address = self.update(address_id, address_info)

        return updated_address