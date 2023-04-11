from app.services.service_base import ServiceBase
from flask_login import current_user
from datetime import datetime

from app.infra.repository.order_repository import OrderRepository
from app.services.order_product_service import OrderProductService


class OrderService(ServiceBase):

    __order_product_service: OrderProductService

    def __init__(self):
        super(OrderService, self).__init__(OrderRepository())
        self.__order_product_service = OrderProductService()

    def store_order(self, products):
        order = self.insert(
            {
                "user_id": current_user.id,
                "order_date": datetime.today(),
                "status": "Em Andamento"
            }
        )

        for product in products:
            self.__order_product_service.insert(
                {
                    "order_id": order.id,
                    "product_id": product['id'],
                    "quantity": product['quantity'],
                    "price": product['price'] * product['quantity']
                }
            )

        return order
