from app.infra.entities.order_product import OrderProduct
from app.infra.repository.repository_base import RepositoryBase

class OrderProductRepository(RepositoryBase):

    def __init__(self):
        super(OrderProductRepository, self).__init__(OrderProduct)