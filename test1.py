import datetime

class Customer:
    def __init__(self, name, email, personal_info=None):
        self.name = name
        self.email = email
        self.personal_info = personal_info if personal_info else {}
        self.policy_info = {}

    def update_personal_info(self, info):
        self.personal_info.update(info)

    def view_personal_info(self):
        return self.personal_info

    def add_policy(self, policy):
        self.policy_info[policy.policy_number] = policy.view_policy_details()

    def view_policy_info(self):
        return self.policy_info

class Policy:
    def __init__(self, policy_number, customer, coverage_amount, premium):
        self.policy_number = policy_number
        self.customer = customer
        self.coverage_amount = coverage_amount
        self.premium = premium
        self.is_claimed = False
        self.payment_due_date = datetime.datetime.now() + datetime.timedelta(days=30)  # Definindo a data de vencimento do pagamento para 30 dias a partir de agora

    def file_claim(self):
        self.is_claimed = True

    @classmethod
    def create_policy(cls, policy_number, customer, coverage_amount, premium):
        return cls(policy_number, customer, coverage_amount, premium)

    def view_policy_details(self):
        return {
            'policy_number': self.policy_number,
            'customer': self.customer.name,
            'coverage_amount': self.coverage_amount,
            'premium': self.premium,
            'is_claimed': self.is_claimed
        }

    def update_coverage_amount(self, new_amount):
        self.coverage_amount = new_amount

    def process_payment(self, payment_amount):
        if payment_amount < self.premium:
            print("Pagamento insuficiente. Por favor, pague o valor total do prêmio.")
        else:
            self.premium -= payment_amount
            print("Pagamento processado com sucesso.")

    def send_payment_reminder(self):
        if datetime.datetime.now() > self.payment_due_date and self.premium > 0:
            print(f"Lembrete: O pagamento do prêmio de {self.premium} está vencido.")

class Claim:
    def __init__(self, policy, description):
        self.policy = policy
        self.description = description
        self.is_approved = False

    def approve_claim(self):
        self.is_approved = True

    def process_claim(self):
        if self.policy.is_claimed:
            print("O sinistro já foi registrado para esta apólice.")
            return
        self.policy.file_claim()
        self.approve_claim()
        print("Sinistro processado e aprovado.")

def user_interface():
    cliente1 = None
    apolice1 = None
    while True:
        print("\n1. Criar um cliente")
        print("2. Atualizar informações pessoais do cliente")
        print("3. Visualizar informações pessoais do cliente")
        print("4. Criar uma apólice")
        print("5. Adicionar apólice ao perfil do cliente")
        print("6. Visualizar informações da apólice do cliente")
        print("7. Ver detalhes da apólice")
        print("8. Atualizar a quantidade de cobertura")
        print("9. Registrar e processar uma reclamação")
        print("10. Processar pagamento")
        print("11. Enviar lembrete de pagamento")
        print("12. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            name = input("Digite o nome do cliente: ")
            email = input("Digite o email do cliente: ")
            info = input("Digite as informações pessoais no formato 'chave:valor' separadas por vírgulas: ")
            info = dict(item.split(":") for item in info.split(","))
            cliente1 = Customer(name=name, email=email, personal_info=info)
            print("Cliente criado com sucesso.")
        elif choice == '2':
            if cliente1 is None:
                print("Primeiro, você precisa criar um cliente.")
                continue
            info = input("Digite as informações pessoais no formato 'chave:valor' separadas por vírgulas: ")
            info = dict(item.split(":") for item in info.split(","))
            cliente1.update_personal_info(info)
        elif choice == '3':
            if cliente1 is None:
                print("Primeiro, você precisa criar um cliente.")
                continue
            print(cliente1.view_personal_info())
        elif choice == '4':
            if cliente1 is None:
                print("Primeiro, você precisa criar um cliente.")
                continue
            policy_number = input("Digite o número da apólice: ")
            coverage_amount = float(input("Digite a quantidade de cobertura: "))
            premium = float(input("Digite o prêmio: "))
            apolice1 = Policy.create_policy(policy_number, cliente1, coverage_amount, premium)
            print("Apólice criada com sucesso.")
        elif choice == '5':
            if cliente1 is None or apolice1 is None:
                print("Primeiro, você precisa criar um cliente e uma apólice.")
                continue
            cliente1.add_policy(apolice1)
        elif choice == '6':
            if cliente1 is None:
                print("Primeiro, você precisa criar um cliente.")
                continue
            print(cliente1.view_policy_info())
        elif choice == '7':
            if apolice1 is None:
                print("Primeiro, você precisa criar uma apólice.")
                continue
            print(apolice1.view_policy_details())
        elif choice == '8':
            if apolice1 is None:
                print("Primeiro, você precisa criar uma apólice.")
                continue
            new_amount = float(input("Digite a nova quantidade de cobertura: "))
            apolice1.update_coverage_amount(new_amount)
        elif choice == '9':
            if apolice1 is None:
                print("Primeiro, você precisa criar uma apólice.")
                continue
            description = input("Digite a descrição da reclamação: ")
            reclamacao1 = Claim(policy=apolice1, description=description)
            reclamacao1.process_claim()
        elif choice == '10':
            if apolice1 is None:
                print("Primeiro, você precisa criar uma apólice.")
                continue
            payment_amount = float(input("Digite o valor do pagamento: "))
            apolice1.process_payment(payment_amount)
        elif choice == '11':
            if apolice1 is None:
                print("Primeiro, você precisa criar uma apólice.")
                continue
            apolice1.send_payment_reminder()
        elif choice == '12':
            break
        else:
            print("Opção inválida. Tente novamente.")

# Executando a interface do usuário
user_interface()
