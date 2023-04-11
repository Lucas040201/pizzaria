from app.infra.entities.address import Address
from app.infra.repository.repository_base import RepositoryBase


class AddressRepository(RepositoryBase):

    def __init__(self):
        super(AddressRepository, self).__init__(Address)

