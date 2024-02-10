from sqlalchemy import DECIMAL, Column, ForeignKey, Integer, String

from moex_alerter_bot.models import BASE


class Stock(BASE):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    short_name = Column(String(255), unique=True, nullable=False)

    def __repr__(self):
        return f'Stock(id={self.id}, name={self.name}, short_name={self.short_name})'


class StockAnalyze(BASE):
    __tablename__ = 'stock_analyze'

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_id = Column(Integer, ForeignKey('stock.id', ondelete='CASCADE'), nullable=False)
    top_limit = Column(DECIMAL, nullable=False)
    bottom_limit = Column(DECIMAL, nullable=False)

    def __repr__(self):
        return (
            f'StockAnalyze(id={self.id}, stock_id={self.stock_id}, '
            f'top_limit={self.top_limit}, bottom_limit={self.bottom_limit})'
        )
