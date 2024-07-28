
from conf import engine, Session
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship


Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __str__(self):
        return f'Publisher: {self.id}:{self.name}'


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    publisher_id = Column(Integer, ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publisher, backref="books")


class Shop(Base):
    __tablename__ = "shop"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    book = relationship(Book, backref="stock")
    shop_id = Column(Integer, ForeignKey("shop.id"), nullable=False)
    shop = relationship(Shop, backref="stock")
    count = Column(Integer, nullable=False)


class Sale(Base):
    __tablename__ = "sale"
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    date_sale = Column(DateTime, nullable=False)
    stock_id = Column(Integer, ForeignKey("stock.id"), nullable=False)
    stock = relationship(Stock, backref="sale")
    count = Column(Integer, nullable=False)


if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    publisher_input = input("Введите имя или идентификатор издателя: ")

    try:
        publisher_id = int(publisher_input)
        publisher = (
            Session().query(Publisher).filter(Publisher.id == publisher_id).first()
        )
    except ValueError:
        publisher = (
            Session().query(Publisher).filter(Publisher.name == publisher_input).first()
        )

    if publisher is None:
        print("Издатель не найден")
    else:
        sales = (
            Session()
            .query(Sale)
            .join(Stock)
            .join(Stock.shop)
            .join(Book)
            .join(Publisher)
            .filter(Publisher.id == publisher.id)
            .order_by(Sale.date_sale)
            .all()
        )

        for sale in sales:
            print(
                f"{sale.stock.book.title} | {sale.stock.shop.name} | {
                    sale.price} | {sale.date_sale}"
            )

        print(f"Найдено {len(sales)} продаж для издателя {publisher.name}")
