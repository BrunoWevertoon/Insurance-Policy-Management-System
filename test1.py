import datetime

class Customer:
    def __init__(self, name, email, personal_info=None):
        self.name = name
        self.email = email
        self.personal_info = personal_info if personal_info else {}
        self.policy_info = {}

    def update_personal_info(self, name, email):
        self.name = name
        self.email = email

    def view_personal_info(self):
        return {
            'name': self.name,
            'email': self.email
        }

    def add_policy(self, policy):
        self.policy_info[policy.policy_number] = policy.view_policy_details()

    def view_policy_info(self):
        if not self.policy_info:
            return "Este cliente não tem apólices cadastradas."
        return self.policy_info

class Policy:
    def __init__(self, policy_number, customer, coverage_amount, premium):
        self.policy_number = policy_number
        self.customer = customer
        self.coverage_amount = coverage_amount
        self.premium = premium
        self.is_claimed = False
        self.payment_due_date = datetime.datetime.now() + datetime.timedelta(days=30)
        self.risk_evaluation = None

    def file_claim(self):
        self.is_claimed = True

    @classmethod
    def create_policy(cls, policy_number, customer, coverage_amount, premium):
        return cls(policy_number, customer, coverage_amount, premium)

    def view_policy_details(self):
        customer_name = self.customer.name if self.customer else "Cliente não associado"
        return {
            'policy_number': self.policy_number,
            'customer': customer_name,
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

    def avaliar_risco(self):
        fator_arbitrario = 0.1
        self.risk_evaluation = self.coverage_amount * fator_arbitrario / self.premium

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

class Report:
    def __init__(self):
        self.claims_report = []
        self.payments_report = []
        self.customers_statistics = []

    def generate_claims_report(self, claims):
        for claim in claims:
            self.claims_report.append({
                'policy_number': claim.policy.policy_number,
                'customer': claim.policy.customer.name if claim.policy.customer else "Cliente não associado",
                'description': claim.description,
                'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })
        print("Relatório de Sinistros gerado com sucesso.")

    def generate_payments_report(self, policies):
        for policy in policies:
            if policy.premium < policy.coverage_amount:
                self.payments_report.append({
                    'policy_number': policy.policy_number,
                    'customer': policy.customer.name if policy.customer else "Cliente não associado",
                    'amount_paid': policy.premium,
                    'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                })
        print("Relatório de Pagamentos gerado com sucesso.")

    def generate_customers_statistics(self, customers):
        for customer in customers:
            policies_count = len(customer.policy_info)
            self.customers_statistics.append({
                'customer_name': customer.name,
                'email': customer.email,
                'policies_count': policies_count,
            })
        print("Relatório de Estatísticas de Clientes gerado com sucesso.")

class Agent:
    def __init__(self, name, email, assigned_customers=None):
        self.name = name
        self.email = email
        self.assigned_customers = assigned_customers if assigned_customers else []

    def assign_customer(self, customer):
        self.assigned_customers.append(customer)

    def view_assigned_customers(self):
        return [customer.view_personal_info() for customer in self.assigned_customers]

def create_customer():
    name = input("Digite o nome do cliente: ")
    email = input("Digite o email do cliente: ")
    return Customer(name=name, email=email)

def create_agent():
    name = input("Digite o nome do agente: ")
    email = input("Digite o email do agente: ")
    return Agent(name=name, email=email)

def assign_customer_to_agent(agents, customers):
    if not agents:
        print("Não há agentes disponíveis. Por favor, crie um agente primeiro.")
        return
    if not customers:
        print("Não há clientes disponíveis. Por favor, crie um cliente primeiro.")
        return

    print("\nEscolha um agente para atribuir ao cliente:")
    for i, agent in enumerate(agents):
        print(f"{i + 1}. {agent.name}")

    agent_index = int(input("Digite o número correspondente ao agente desejado: ")) - 1

    if 0 <= agent_index < len(agents):
        print("\nEscolha um cliente para atribuir ao agente:")
        for i, customer in enumerate(customers):
            print(f"{i + 1}. {customer.name}")

        customer_index = int(input("Digite o número correspondente ao cliente desejado: ")) - 1

        if 0 <= customer_index < len(customers):
            agents[agent_index].assign_customer(customers[customer_index])
            print(f"Cliente {customers[customer_index].name} atribuído ao agente {agents[agent_index].name}.")
        else:
            print("Índice de cliente inválido.")
    else:
        print("Índice de agente inválido.")

def generate_reports(report, policies, claims, customers):
    print("\nEscolha o tipo de relatório:")
    print("1. Relatório de Sinistros")
    print("2. Relatório de Pagamentos")
    print("3. Estatísticas de Clientes")
    report_choice = input("Digite o número correspondente à opção desejada: ")

    if report_choice == '1':
        report.generate_claims_report(claims)
    elif report_choice == '2':
        report.generate_payments_report(policies)
    elif report_choice == '3':
        report.generate_customers_statistics(customers)
    else:
        print("Opção inválida. Tente novamente.")

def user_interface():
    customers = []  # Lista para armazenar vários clientes
    policies = []   # Lista para armazenar várias apólices
    claims = []     # Lista para armazenar reclamações
    risk_evaluations = []  # Lista para armazenar avaliações de risco associadas a cada apólice
    agents = []     # Lista para armazenar agentes de seguros
    report = Report()  # Instância da classe Report

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
        print("12. Avaliar risco da apólice")
        print("13. Gerar Relatórios")
        print("14. Gerenciar Agentes")
        print("15. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            customers.append(create_customer())
            print("Cliente criado com sucesso.")
        elif choice == '2':
            if not customers:
                print("Não há clientes disponíveis. Por favor, crie um cliente primeiro.")
                continue
            
            print("\nEscolha o cliente para atualizar informações pessoais:")
            for i, customer in enumerate(customers):
                print(f"{i + 0}. {customer.name}")
            customer_index = int(input("Digite o índice do cliente que deseja atualizar: "))
            if 0 <= customer_index < len(customers):
                name = input("Digite o novo nome do cliente: ")
                email = input("Digite o novo email do cliente: ")
                customers[customer_index].update_personal_info(name, email)
                print("Informações pessoais atualizadas com sucesso.")
            else:
                print("Índice de cliente inválido.")
        elif choice == '3':
            if not customers:
                print("Não há clientes disponíveis. Por favor, crie um cliente primeiro.")
                continue
            
            print("\nEscolha o cliente para visualizar informações pessoais:")
            for i, customer in enumerate(customers):
                print(f"{i + 0}. {customer.name}")
            customer_index = int(input("Digite o índice do cliente que deseja visualizar: "))
            if 0 <= customer_index < len(customers):
                print(f"Nome: {customers[customer_index].name}")
                print(f"Email: {customers[customer_index].email}")
            else:
                print("Índice de cliente inválido.")
        elif choice == '4':
            policy_number = input("Digite o número da apólice: ")
            coverage_amount = float(input("Digite a quantidade de cobertura: "))
            premium = float(input("Digite o prêmio: "))
            policy = Policy.create_policy(policy_number, None, coverage_amount, premium)
            policies.append(policy)
            risk_evaluations.append(None)  # Inicialmente, a avaliação de risco é None
            print("Apólice criada com sucesso.")
        elif choice == '5':
            if not customers or not policies:
                print("Primeiro, você precisa criar um cliente e uma apólice.")
                continue
            customer_index = int(input("Digite o índice do cliente: "))
            policy_index = int(input("Digite o índice da apólice: "))
            if 0 <= customer_index < len(customers) and 0 <= policy_index < len(policies):
                policies[policy_index].customer = customers[customer_index]
                customers[customer_index].add_policy(policies[policy_index])
                print("Apólice adicionada ao perfil do cliente.")
            else:
                print("Índice de cliente ou apólice inválido.")
        elif choice == '6':
            if not customers:
                print("Primeiro, você precisa criar um cliente.")
                continue
            customer_index = int(input("Digite o índice do cliente que deseja visualizar as apólices: "))
            if 0 <= customer_index < len(customers):
                policies_info = customers[customer_index].view_policy_info()
                print(policies_info)
            else:
                print("Índice de cliente inválido.")
        elif choice == '7':
            if not policies:
                print("Primeiro, você precisa criar uma apólice.")
                continue
            policy_index = int(input("Digite o índice da apólice que deseja ver os detalhes: "))
            if 0 <= policy_index < len(policies):
                policy_details = policies[policy_index].view_policy_details()
                print(policy_details)
            else:
                print("Índice de apólice inválido.")
        elif choice == '8':
            if not policies:
                print("Primeiro, você precisa criar uma apólice.")
                continue
            policy_index = int(input("Digite o índice da apólice que deseja atualizar a quantidade de cobertura: "))
            if 0 <= policy_index < len(policies):
                new_amount = float(input("Digite a nova quantidade de cobertura: "))
                policies[policy_index].update_coverage_amount(new_amount)
                print("Quantidade de cobertura atualizada com sucesso.")
            else:
                print("Índice de apólice inválido.")
        elif choice == '9':
            if not policies:
                print("Primeiro, você precisa criar uma apólice.")
                continue
            policy_index = int(input("Digite o índice da apólice para registrar uma reclamação: "))
            if 0 <= policy_index < len(policies):
                description = input("Digite a descrição da reclamação: ")
                claim = Claim(policy=policies[policy_index], description=description)
                claim.process_claim()
                claims.append(claim)
            else:
                print("Índice de apólice inválido.")
        elif choice == '10':
            if not policies:
                print("Primeiro, você precisa criar uma apólice.")
                continue
            policy_index = int(input("Digite o índice da apólice para processar o pagamento: "))
            if 0 <= policy_index < len(policies):
                payment_amount = float(input("Digite o valor do pagamento: "))
                policies[policy_index].process_payment(payment_amount)
            else:
                print("Índice de apólice inválido.")
        elif choice == '11':
            if not policies:
                print("Primeiro, você precisa criar uma apólice.")
                continue
            policy_index = int(input("Digite o índice da apólice para enviar o lembrete de pagamento: "))
            if 0 <= policy_index < len(policies):
                policies[policy_index].send_payment_reminder()
            else:
                print("Índice de apólice inválido.")
        elif choice == '12':
            if not policies:
                print("Primeiro, você precisa criar uma apólice.")
                continue
            policy_index = int(input("Digite o índice da apólice para visualizar a avaliação de risco: "))
            if 0 <= policy_index < len(risk_evaluations):
                if risk_evaluations[policy_index] is None:
                    policies[policy_index].avaliar_risco()
                    risk_evaluations[policy_index] = policies[policy_index].risk_evaluation
                print(f"Avaliação de risco: {risk_evaluations[policy_index]}")
            else:
                print("Índice de apólice inválido.")
        elif choice == '13':
            if not policies:
                print("Primeiro, você precisa criar uma apólice.")
                continue
            generate_reports(report, policies, claims, customers)
        elif choice == '14':
            manage_agents(agents, customers)
        elif choice == '15':
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

def manage_agents(agents, customers):
    while True:
        print("\n1. Criar um agente")
        print("2. Atribuir cliente a um agente")
        print("3. Visualizar clientes atribuídos a um agente")
        print("4. Voltar ao menu principal")
        agent_choice = input("Escolha uma opção: ")

        if agent_choice == '1':
            agents.append(create_agent())
            print("Agente criado com sucesso.")
        elif agent_choice == '2':
            assign_customer_to_agent(agents, customers)
        elif agent_choice == '3':
            view_assigned_customers(agents)
        elif agent_choice == '4':
            print("Retornando ao menu principal.")
            break
        else:
            print("Opção inválida. Tente novamente.")

def view_assigned_customers(agents):
    if not agents:
        print("Não há agentes disponíveis.")
        return

    print("\nEscolha um agente para visualizar os clientes atribuídos:")
    for i, agent in enumerate(agents):
        print(f"{i + 1}. {agent.name}")

    agent_index = int(input("Digite o número correspondente ao agente desejado: ")) - 1

    if 0 <= agent_index < len(agents):
        assigned_customers = agents[agent_index].view_assigned_customers()
        print(f"Clientes atribuídos ao agente {agents[agent_index].name}:")
        for customer in assigned_customers:
            print(customer)
    else:
        print("Índice de agente inválido.")

# Executando a interface do usuário
user_interface()
