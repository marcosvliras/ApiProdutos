from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from src.models import Produto
from src.infra.db.models import Produto as ProdutoTable
from src.infra.db.configs.database import SessionLocal
from src.infra.db.interfaces import RepoInterface


class ProdutoRepo(RepoInterface):

    def __init__(self, db_conn: Session = SessionLocal()) -> None:
        self.db_conn = db_conn

    def create(self, produto: Produto):
        db_produto = ProdutoTable(
            name=produto.name,
            details=produto.details,
            price=produto.price,
            available=produto.available
        ) 

        self.db_conn.add(db_produto)
        self.db_conn.commit()
        self.db_conn.refresh(db_produto)
        self.db_conn.close()
        return db_produto

    def list_all(self):
        produtos = self.db_conn.query(ProdutoTable).all()
        return produtos

    def get(self, product_id: int):
        stmt = select(ProdutoTable).filter_by(id=product_id)

        serie = self.db_conn.execute(stmt).fetchall()
        
        s = []
        for i in serie:
            s.append(i[0])

        return s

    def remove(self, product_id: int):
        stmt = delete(ProdutoTable).where(ProdutoTable.id == product_id)
        self.db_conn.execute(stmt)

        return None