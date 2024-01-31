import datetime

# Classe base para representar uma pessoa
class Person:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}, Email: {self.email}"

# Classe que herda de Person, representando um cliente
class Customer(Person):
    def __init__(self, name, email, personal_info=None, documents=None):
        super().__init__(name, email)
        self.personal_info = personal_info if personal_info else {}
        self.policy_info = {}
        self.documents = documents if documents else {}

    def update_personal_info(self, name, email):
        self.name = name
        self.email = email

    def view_personal_info(self):
        return {
            'name': self.name,
            'email': self.email,
            'documents': self.documents
        }

    def add_policy(self, policy):
        self.policy_info[policy.policy_number] = policy.view_policy_details()

    def view_policy_info(self):
        if not self.policy_info:
            return "Este cliente não tem apólices cadastradas."
        return self.policy_info

    def update_documents(self, cpf=None, rg=None, endereco=None):
        if cpf:
            self.documents['cpf'] = cpf
        if rg:
            self.documents['rg'] = rg
        if endereco:
            self.documents['endereco'] = endereco

    def __str__(self):
        return super().__str__() + f", Policies: {len(self.policy_info)}"

# Classe que herda de Person, representando um agente
class Agent(Person):
    def __init__(self, name, email, assigned_customers=None):
        super().__init__(name, email)
        self.assigned_customers = assigned_customers if assigned_customers else []

    def assign_customer(self, customer):
        self.assigned_customers.append(customer)

    def view_assigned_customers(self):
        return [customer.view_personal_info() for customer in self.assigned_customers]

    def __str__(self):
        return super().__str__() + f", Assigned Customers: {len(self.assigned_customers)}"

# Classe que representa uma apólice
class Policy:
    def __init__(self, policy_number, customer, coverage_amount, premium):
        self.policy_number = policy_number
        self.customer = customer
        self.coverage_amount = coverage_amount
        self.premium = premium
        self.is_claimed = False
        self.is_canceled = False
        self.payment_due_date = datetime.datetime.now() + datetime.timedelta(days=30)
        self.risk_evaluation = None

    def file_claim(self):
        self.is_claimed = True

    @classmethod
    def create_policy(cls, policy_number, customer, coverage_amount, premium):
        return cls(policy_number, customer, coverage_amount, premium)

    def view_policy_details(self):
        customer_name = self.customer.name if self.customer else "Cliente não associado"
        policy_status = "Cancelada" if self.is_canceled else "Ativa"
        return {
            'policy_number': self.policy_number,
            'customer': customer_name,
            'coverage_amount': self.coverage_amount,
            'premium': self.premium,
            'is_claimed': self.is_claimed,
            'status': policy_status
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
        if self.premium != 0:
            self.risk_evaluation = self.coverage_amount * fator_arbitrario / self.premium
        else:
            print("Prêmio é zero. Não é possível calcular a avaliação de risco.")
            
    def renovar_apolice(self):
        if self.is_canceled:
            print("Não é possível renovar uma apólice cancelada.")
        else:
        # Lógica de renovação da apólice (por exemplo, estender a data de vencimento)
            self.payment_due_date += datetime.timedelta(days=365)
            print("Apólice renovada com sucesso.")
        
    def cancelar_apolice(self):
        if not self.is_claimed:
            self.is_canceled = True
            print("Apólice cancelada com sucesso.")
            self.customer.policy_info[self.policy_number]['status'] = "Cancelada"
        else:
            print("Não é possivel cancelar uma apólice após registro do sinistro")
# Classe que representa uma reclamação
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

# Classe que representa um relatório
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
        return self.claims_report

    def generate_payments_report(self, policies):
        for policy in policies:
            if policy.premium < policy.coverage_amount:
                self.payments_report.append({
                    'policy_number': policy.policy_number,
                    'customer': policy.customer.name if policy.customer else "Cliente não associado",
                    'amount_paid': policy.premium,
                    'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                })
        return self.payments_report

    def generate_customers_statistics(self, customers):
        for customer in customers:
            policies_count = len(customer.policy_info)
            self.customers_statistics.append({
                'customer_name': customer.name,
                'email': customer.email,
                'policies_count': policies_count,
            })
        return self.customers_statistics
# Classe de exceção personalizada
class InsuranceError(Exception):
    pass

# Função para criar um cliente com tratamento de exceções
def create_customer():
    try:
        name = input("Digite o nome do cliente: ")
        email = input("Digite o email do cliente: ")
        return Customer(name=name, email=email)
    except Exception as e:
        raise InsuranceError(f"Erro ao criar cliente: {e}")

# Função para criar um agente com tratamento de exceções
def create_agent():
    try:
        name = input("Digite o nome do agente: ")
        email = input("Digite o email do agente: ")
        return Agent(name=name, email=email)
    except Exception as e:
        raise InsuranceError(f"Erro ao criar agente: {e}")


def assign_customer_to_agent(agents, customers):
    try:
        if not agents:
            raise InsuranceError("Não há agentes disponíveis. Por favor, crie um agente primeiro.")
        if not customers:
            raise InsuranceError("Não há clientes disponíveis. Por favor, crie um cliente primeiro.")

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
                raise InsuranceError("Índice de cliente inválido.")
        else:
            raise InsuranceError("Índice de agente inválido.")
    except InsuranceError as e:
        print(e)


def generate_reports(report, policies, claims, customers):
    try:
        print("\nEscolha o tipo de relatório:")
        print("1. Relatório de Sinistros")
        print("2. Relatório de Pagamentos")
        print("3. Estatísticas de Clientes")
        report_choice = input("Digite o número correspondente à opção desejada: ")

        if report_choice == '1':
            claims_report = report.generate_claims_report(claims)
            print("Relatório de Sinistros:")
            for claim in claims_report:
                print(claim)
        elif report_choice == '2':
            payments_report = report.generate_payments_report(policies)
            print("Relatório de Pagamentos:")
            for payment in payments_report:
                print(payment)
        elif report_choice == '3':
            customers_statistics = report.generate_customers_statistics(customers)
            print("Relatório de Estatísticas de Clientes:")
            for statistic in customers_statistics:
                print(statistic)
        else:
            raise InsuranceError("Opção inválida. Tente novamente.")
    except InsuranceError as e:
        print(e)


def user_interface():
    customers = []  
    policies = []   
    claims = []     
    risk_evaluations = []  
    agents = []     
    report = Report()  

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
        print("16. Portal de Atendimento ao Cliente")
        print("17. Tratamento de Renovações e Cancelamentos")
        print("18. Adicionar Documentos ao Cliente")
        print("19. Visualizar Documentos do Cliente")

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
                print(f"{i + 1}. {customer.name}")
            customer_index = int(input("Digite o índice do cliente que deseja atualizar: ")) - 1
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
                print(f"{i + 1}. {customer.name}")
            customer_index = int(input("Digite o índice do cliente que deseja visualizar: ")) - 1
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
            print("\nLista de Clientes:")
            for i, customer in enumerate(customers):
                print(f"{i + 1}. {customer.name}")
            customer_index = int(input("Digite o número do cliente: ")) - 1
            print("\nLista de Apólices:")
            for i, policy in enumerate(policies):
                policy_details = policy.view_policy_details()
                print(f"{i + 1}. Apólice {policy_details['policy_number']} - Cliente: {policy_details['customer']}, Cobertura: {policy_details['coverage_amount']}, Prêmio: {policy_details['premium']}")
            policy_index = int(input("Digite o número da apólice: ")) - 1
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
            print("\nLista de Clientes:")
            for i, customer in enumerate(customers):
                print(f"{i + 1}. {customer.name}")
            customer_index = int(input("Digite o número do cliente que deseja visualizar as apólices: ")) - 1
            if 0 <= customer_index < len(customers):
                policies_info = customers[customer_index].view_policy_info()
                print(policies_info)
            else:
                print("Índice de cliente inválido.")
        elif choice == '7':
            if not policies:
                print("Primeiro, você precisa criar uma apólice.")
                continue
            print("\nLista de Apólices:")
            for i, policy in enumerate(policies):
                policy_details = policy.view_policy_details()
                print(f"{i + 1}. Apólice {policy_details['policy_number']} - Cliente: {policy_details['customer']}, Cobertura: {policy_details['coverage_amount']}, Prêmio: {policy_details['premium']}")
            policy_index = int(input("Digite o número da apólice que deseja ver os detalhes: ")) - 1
            if 0 <= policy_index < len(policies):
                policy_details = policies[policy_index].view_policy_details()
                print(policy_details)
            else:
                print("Índice de apólice inválido.")
        elif choice == '8':
            if not policies:
                print("Primeiro, você precisa criar uma apólice.")
                continue
            print("\nLista de Apólices:")
            for i, policy in enumerate(policies):
                policy_details = policy.view_policy_details()
                print(f"{i + 1}. Apólice {policy_details['policy_number']} - Cliente: {policy_details['customer']}, Cobertura: {policy_details['coverage_amount']}, Prêmio: {policy_details['premium']}")
            policy_index = int(input("Digite o índice da apólice que deseja atualizar a quantidade de cobertura: ")) - 1
            if 0 <= policy_index < len(policies):
                print("Detalhes da Apólice antes da Atualização:")
                policy_details_before = policies[policy_index].view_policy_details()
                print(policy_details_before)
                new_amount = float(input("Digite a nova quantidade de cobertura: "))
                policies[policy_index].update_coverage_amount(new_amount)
                print("Detalhes da Apólice após a Atualização:")
                policy_details_after = policies[policy_index].view_policy_details()
                print(policy_details_after)
                print("Quantidade de cobertura atualizada com sucesso.")
            else:
                print("Índice de apólice inválido.")
        elif choice == '9':
            if not policies:
                print("Primeiro, você precisa criar uma apólice.")
                continue
            print("\nLista de Apólices:")
            for i, policy in enumerate(policies):
                policy_details = policy.view_policy_details()
                print(f"{i + 1}. Apólice {policy_details['policy_number']} - Cliente: {policy_details['customer']}, Cobertura: {policy_details['coverage_amount']}, Prêmio: {policy_details['premium']}")
            policy_index = int(input("Digite o índice da apólice para registrar uma reclamação: ")) - 1
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
            print("\nLista de Apólices:")
            for i, policy in enumerate(policies):
                policy_details = policy.view_policy_details()
                print(f"{i + 1}. Apólice {policy_details['policy_number']} - Cliente: {policy_details['customer']}, Cobertura: {policy_details['coverage_amount']}, Prêmio: {policy_details['premium']}")
            policy_index = int(input("Digite o índice da apólice para processar o pagamento: ")) - 1
            if 0 <= policy_index < len(policies):
                payment_amount = float(input("Digite o valor do pagamento: "))
                policies[policy_index].process_payment(payment_amount)
            else:
                print("Índice de apólice inválido.")
        elif choice == '11':
            if not policies:
                print("Primeiro, você precisa criar uma apólice.")
                continue
            print("\nLista de Apólices:")
            for i, policy in enumerate(policies):
                policy_details = policy.view_policy_details()
                print(f"{i + 1}. Apólice {policy_details['policy_number']} - Cliente: {policy_details['customer']}, Cobertura: {policy_details['coverage_amount']}, Prêmio: {policy_details['premium']}")
            policy_index = int(input("Digite o índice da apólice para enviar o lembrete de pagamento: ")) - 1
            if 0 <= policy_index < len(policies):
                policies[policy_index].send_payment_reminder()
            else:
                print("Índice de apólice inválido.")
        elif choice == '12':
            if not policies:
                print("Primeiro, você precisa criar uma apólice.")
                continue
            print("\nLista de Apólices:")
            for i, policy in enumerate(policies):
                policy_details = policy.view_policy_details()
                print(f"{i + 1}. Apólice {policy_details['policy_number']} - Cliente: {policy_details['customer']}, Cobertura: {policy_details['coverage_amount']}, Prêmio: {policy_details['premium']}")
            policy_index = int(input("Digite o índice da apólice para visualizar a avaliação de risco: ")) - 1
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
        elif choice == '16':
            customer_email = input("Digite seu e-mail: ")
            authenticated_customer = authenticate_customer(customers, customer_email)
            if authenticated_customer:
                customer_portal(authenticated_customer, policies, claims)
            else:
                print("E-mail não encontrado. Verifique seu e-mail e tente novamente.")
        elif choice == '17':
            if not policies:
                print("Primeiro, você precisa criar uma apólice.")
                continue
            print("\nLista de Apólices:")
            for i, policy in enumerate(policies):
                policy_details = policy.view_policy_details()
                print(f"{i + 1}. Apólice {policy_details['policy_number']} - Cliente: {policy_details['customer']}, Cobertura: {policy_details['coverage_amount']}, Prêmio: {policy_details['premium']}")
                policy_index = int(input("Digite o índice da apólice para tratamento de renovações e cancelamentos: ")) - 1
                if 0 <= policy_index < len(policies):
                    print("\nOpções:")
                    print("1. Renovar Apólice")
                    print("2. Cancelar Apólice")
                    option = input("Digite o número correspondente à opção desejada: ")
                    if option == '1':
                        policies[policy_index].renovar_apolice()
                    elif option == '2':
                        policies[policy_index].cancelar_apolice()
                    else:
                        print("Opção inválida. Tente novamente.")
        elif choice == '18':
            if not customers:
                print("Primeiro, você precisa criar um cliente.")
                continue
            print("\nLista de Clientes:")
            for i, customer in enumerate(customers):
                print(f"{i + 1}. {customer.name}")
                
            customer_index = int(input("Digite o número do cliente para incluir os documentos: ")) - 1
            
            if 0 <= customer_index < len(customers):
                cpf = input("Digite o CPF do cliente: ")
                rg = input("Digite o RG do cliente: ")
                endereco = input("Digite o endereço do cliente: ")
                
                customers[customer_index].update_documents(cpf=cpf, rg=rg, endereco=endereco)
                print("Documentos do cliente incluso com sucesso.")
            else:
                print("Índice de cliente inválido.")
                
        elif choice == '19':
            if not customers:
                print("Primeiro, você precisa criar um cliente.")
                continue
            print("\nLista de Clientes:")
            for i, customer in enumerate(customers):
                print(f"{i + 1}. {customer.name}")
            customer_index = int(input("Digite o número do cliente para visualizar os documentos: ")) - 1
            
            if 0 <= customer_index < len(customers):
                documents = customers[customer_index].view_personal_info()['documents']
                print(f"Documentos do Cliente {customers[customer_index].name}:")
                for key, value in documents.items():
                    print(f"{key.capitalize()}: {value}")
            else:    
                print("Índice de cliente inválido.")
            
def authenticate_customer(customers, email):
    normalized_email = email.lower()  # Converte o e-mail para minúsculas
    for customer in customers:
        if customer.email.lower() == normalized_email:
            return customer
    return None

def customer_portal(customer, policies, claims):
    while True:
        print("\nPortal de Atendimento ao Cliente:")
        print("1. Visualizar Minhas Apólices")
        print("2. Visualizar Minhas Reclamações")
        print("3. Voltar ao Menu Principal")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            view_customer_policies(customer)
        elif choice == '2':
            view_customer_claims(customer, claims)
        elif choice == '3':
            print("Retornando ao Menu Principal.")
            break
        else:
            print("Opção inválida. Tente novamente.")

def view_customer_policies(customer):
    if not customer.policy_info:
        print("Você não tem apólices cadastradas.")
    else:
        print("Suas Apólices:")
        for policy_number, policy_details in customer.policy_info.items():
            print(f"Apólice {policy_number}: {policy_details}")

def view_customer_claims(customer, claims):
    customer_claims = [claim for claim in claims if claim.policy.customer == customer]
    if not customer_claims:
        print("Você não tem reclamações registradas.")
    else:
        print("Suas Reclamações:")
        for claim in customer_claims:
            print(f"Data de Vencimento: {claim.policy.payment_due_date.strftime('%Y-%m-%d')}, Descrição: {claim.description}, Aprovada: {claim.is_approved}")

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
