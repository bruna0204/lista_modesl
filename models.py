from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, declarative_base
#configuração base de dados
engine = create_engine('sqlite:///controle_estoque.sqlite3') #nome do banco
db_session = scoped_session(sessionmaker(bind=engine))


#modo declarativo
Base = declarative_base()
Base.query = db_session.query_property()


#Pessoas que tem atividade
class Usuario(Base):
    __tablename__ = 'tab_usuarios'
    id_usuario = Column(Integer, primary_key=True)
    Nome = Column(String(30), nullable=False, index=True )
    profissao = Column(String(70), nullable=False, index=True) #string o tamanho dele
    salario = Column(Integer, nullable=False, index=True) #string o tamanho dele


    def __repr__(self):
        return '<Funcionario: {} {} {} {}>' .format(self.id_usuario, self.profissao, self.Nome, self.salario, )


    def save(self):
        db_session.add(self)
        db_session.commit()

#função para deletar
    def delete(self):
            db_session.delete(self)
            db_session.commit()


    def serialize_usuarios(self):
        dados_usuario = {
            'id_usuarios': self.id_usuario,
            'profissao': self.profissao,
            'Nome': self.Nome,
            'salario': self.salario,
        }
        return dados_usuario



class Livro(Base):
    __tablename__ = 'tab_livros'
    id_livro = Column(Integer, primary_key=True)
    titulo = Column(String(70), nullable=False, index=True)
    autor = Column(String(70), nullable=False, index=True)
    descrisao = Column(String(100), nullable=False, index=True)
    categoria = Column(String(100), nullable=False, index=True)

    def __repr__(self):
        return '<Livros: {} {} {} {}>' .format(self.id_livro, self.titulo, self.categoria, self.descrisao, self.autor)

#função para salvar no banco

    def save(self):
            db_session.add(self)#seção de acesso
            db_session.commit() #salva a informação


#função para deletar
    def delete(self):
            db_session.delete(self)#deletar
            db_session.commit()# salvar

    def serialize_livro(self):
        dados_livros = {
            'id_livro': self.id_livro,
            'titulo': self.titulo,
            'autor': self.autor,
            'descrisao': self.descrisao,
            'categoria': self.categoria,
        }
        return dados_livros




def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()