import datetime
import pprint
import pymongo as pyM

client = pyM.MongoClient(
    "mongodb+srv://pymongo:_pymongo_password_@cluster0.uxne4qo.mongodb.net/?retryWrites=true&w=majority")

db = client.bank_DB
bank_accounts = db.bank_accounts

# Criando um modelo para ser seguido posteriormente e armazenando em uma coleção chamada account model
model = {
    # Informações sobre o cliente
    "Titular": "nome do cliente",
    "Endereço": 'endereço do cliente',
    "CPF": "123456789",
    "Data de inscrição": 'data de quando o cliente criou a conta na instituição',
    # Informações sobre a conta do cliente
    "Agencia": "0001",
    "Conta": "1",
    "Tipo de conta": "Conta Corrente",
    "Saldo": 'saldo do cliente'
}

account_model = db.account_model
model_id = account_model.insert_one(model).inserted_id


# inserindo o primeiro documento na coleção bank_accounts
user_01 = {
    # Informações sobre o cliente
    "Titular": "Fernanda da Silva",
    "Endereço": 'Rua dos Pinheiros, 3000',
    "CPF": "187222123-09",
    "Data de inscrição": datetime.datetime.now(),
    # Informações sobre a conta do cliente
    "Agencia": "0001",
    "Conta": "12",
    "Tipo de conta": "Conta Corrente",
    "Saldo": 1277.91
}

user_01_id = bank_accounts.insert_one(user_01).inserted_id
print(user_01_id)

# Adicionando documentos na coleção bank_accounts
insert_3_users = [
    {
        # Informações sobre o cliente
        "Titular": "Jonathan Melo",
        "Endereço": 'Rua dos Pinheiros, 2990',
        "CPF": "992867887-01",
        "Data de inscrição": datetime.datetime.now(),
        # Informações sobre a conta do cliente
        "Agencia": "0002",
        "Conta": "17",
        "Tipo de conta": "Conta Corrente",
        "Saldo": 2881.12
    },
    {
        # Informações sobre o cliente
        "Titular": "Donald Fagen",
        "Endereço": 'Rua dos Pinheiros, 2980',
        "CPF": "273753123-01",
        "Data de inscrição": datetime.datetime.now(),
        # Informações sobre a conta do cliente
        "Agencia": "0002",
        "Conta": "11",
        "Tipo de conta": "Conta Corrente",
        "Saldo": 9921.54
    },
    {
        # Informações sobre o cliente
        "Titular": "Walter Becker",
        "Endereço": 'Rua das Macieiras, 2980',
        "CPF": "998776554-21",
        "Data de inscrição": datetime.datetime.now(),
        # Informações sobre a conta do cliente
        "Agencia": "0004",
        "Conta": "15",
        "Tipo de conta": "Conta Corrente",
        "Saldo": 6623.21
    }
]

users_id = bank_accounts.insert_many(insert_3_users).inserted_ids
print(users_id)

Recuperando docs

print("\nRetornando a primeira ocorrência na coleçao bank_accounts: ")
pprint.pprint(bank_accounts.find_one())

print("\nRetornando uma ocorrência usando um filtro na coleção bank_accounts: ")
pprint.pprint(bank_accounts.find_one({"Titular":'Jonathan Melo'}))

print("\nIterando sobre a coleção: ")
for doc in bank_accounts.find():
    pprint.pprint(doc), print(end='\n')

print("\nRetornando somente os que possuem acima de R$ 5000: ")
for doc in bank_accounts.find({"Saldo": {'$gte': 5000}}):
    pprint.pprint(doc)
