from sqlalchemy import (Column, select, Integer, String, ForeignKey, DECIMAL, create_engine, inspect)
from sqlalchemy.orm import (declarative_base, relationship, Session)

Base = declarative_base()


class Client(Base):
    __tablename__ = 'client_info'
    # definition of attributes
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cpf = Column(String(9), nullable=False, unique=True)
    address = Column(String, nullable=False)

    Account = relationship(
        "Account", back_populates="Client"
    )

    def __repr__(self):
        return f"Client (id = {self.id}, name = {self.name}, cpf = {self.cpf}, address = {self.address})"


class Account(Base):
    __tablename__ = 'account_info'
    # definition of attributes
    id = Column(Integer, primary_key=True)
    account_type = Column(String, nullable=False)
    agency = Column(String, nullable=False)
    number = Column(Integer, nullable=False)
    saldo = Column(DECIMAL, nullable=False)
    id_client = Column(Integer, ForeignKey('client_info.id'), nullable=False)

    Client = relationship(
        "Client", back_populates="Account"
    )

    def __repr__(self):
        return f"""Account (id = {self.id}, type = {self.account_type}, agency = {self.agency}, number = {self.number},
        saldo = {"%.2f" % self.saldo}, id_client = {self.id_client})"""


# Criando a conexão com o banco de dados
engine = create_engine("sqlite://")

# criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# cria um inspetor para analisar o banco de dados
inspector_engine = inspect(engine)
# print(inspector_engine.has_table("account_info"))
# print(inspector_engine.get_table_names())
# print(inspector_engine.default_schema_name)

with Session(engine) as session:
    jonathan = Client(
        name="jonathan melo",
        cpf="123456789",
        address="rua numero um",
        Account=[Account(account_type='Conta Corrente', agency='0001', number=1, saldo=100.90)]
    )
    fernanda = Client(
        name="fernanda silva",
        cpf="987654321",
        address="rua numero dois",
        Account=[Account(account_type='Conta Corrente', agency='0001', number=2, saldo=900.10)]
    )
    claudeir = Client(
        name="claudeir lima",
        cpf="087654321",
        address="rua numero dois",
        Account=[Account(account_type='Conta Corrente', agency='0001', number=3, saldo=900.10)]
    )
    luis = Client(
        name="luis souza",
        cpf="087654301",
        address="rua numero dois",
        Account=[Account(account_type='Conta Corrente', agency='0001', number=4, saldo=900.10)]
    )


session.add_all([jonathan, fernanda, claudeir, luis])

session.commit()

# Recuperando usuarios a partir de filtragem especifica
print("\nOnly jonathan and fernanda")
stmt = select(Client).where(Client.name.in_(['jonathan melo', 'fernanda silva']))
for user in session.scalars(stmt):
    print(user)

# Recuperando todos os usuarios
print("\nAll accounts")
account_stmt = select(Account)
for account in session.scalars(account_stmt):
    print(account)

print("\nCreating a join instruction ")
account_join_client = select(Client.name, Account.account_type, Account.agency, Account.number).join_from(Client, Account)
print(account_join_client)

print("\nFetch all using the join instruction")
connection = engine.connect()
results = connection.execute(account_join_client).fetchall()
for result in results:
    print(result)