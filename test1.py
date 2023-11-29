class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class Policy:
    def __init__(self, policy_number, customer, coverage_amount, premium):
        self.policy_number = policy_number
        self.customer = customer
        self.coverage_amount = coverage_amount
        self.premium = premium
        self.is_claimed = False

    def file_claim(self):
        self.is_claimed = True

class Claim:
    def __init__(self, policy, description):
        self.policy = policy
        self.description = description
        self.is_approved = False

    def approve_claim(self):
        self.is_approved = True

# Exemplo de Uso:
# Criando um cliente
cliente1 = Customer(name="João", email="joao@example.com")

# Criando uma apólice para o cliente
apolice1 = Policy(policy_number="P001", customer=cliente1, coverage_amount=100000, premium=500)

# Registrando uma reclamação para a apólice
reclamacao1 = Claim(policy=apolice1, description="Danos em casa devido a inundação")

# Aprovando a reclamação
reclamacao1.approve_claim()

# Verificando o status da reclamação
print("Status da Reclamação:", "Aprovada" if reclamacao1.is_approved else "Não Aprovada")
