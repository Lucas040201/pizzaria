from app.infra.entities.order import Order
from app.infra.repository.repository_base import RepositoryBase

class OrderRepository(RepositoryBase):

    def __init__(self):
        super(OrderRepository, self).__init__(Order)