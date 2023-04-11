from app.services.service_base import ServiceBase
from app.infra.repository.order_product_repository import OrderProductRepository


class OrderProductService(ServiceBase):
    def __init__(self):
        super(OrderProductService, self).__init__(OrderProductRepository())