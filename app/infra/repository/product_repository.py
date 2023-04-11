from app.infra.entities.product import Product
from app.infra.repository.repository_base import RepositoryBase


class ProductRepository(RepositoryBase):

    def __init__(self):
        super(ProductRepository, self).__init__(Product)
