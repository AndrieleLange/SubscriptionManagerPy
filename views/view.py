from datetime import date, datetime
import __init__
from models.database import engine
from models.model import Subscription, Payments
from sqlmodel import Session, select

class SubscriptionService:
    def __init__(self, engine):
        self.engine = engine
    
    def create(self, subscription: Subscription):
        with Session(self.engine) as session: # sessão para conectar com o banco, ele fecha automaticamente a conexão
            existing_subscription = session.exec(select(Subscription).where(Subscription.empresa == subscription.empresa)).first()
            if existing_subscription is not None:
                print('\033[0;31;40mEmpresa já cadastrada\033[0m')
                return False
            session.add(subscription)       # adiciona a inscrição no banco
            session.commit()                # commita a transação, salva 
            print('\033[0;32;40mEmpresa cadastrada com sucesso\033[0m')
            return subscription

    def list_all(self):
        with Session(self.engine) as session:
            statement = select(Subscription) # seleciona tudo da tabela Subscription
            result = session.exec(statement).all() # executa a query
        return result              # retorna todos os resultados

    def delete(self, id: int):
        with Session(self.engine) as session:
            statement = select(Subscription).where(Subscription.id == id)
            subscription = session.exec(statement).one() # exec executa no banco

            try: 
                session.delete(subscription)
            except:
                print('\033[0;31;40mErro ao deletar\033[0m')
                return False
            
            session.commit()
            return subscription

    def _has_pay(self, results):
        for result in results:
            if result.data.month == date.today().month:
                return True
        return False

    def pay(self, subscription: Subscription):
        with Session(self.engine) as session:
            statement = select(Payments).join(Subscription).where(Subscription.empresa == subscription.empresa)
            results = session.exec(statement).all()
 
            if self._has_pay(results):
                question = input('\033[0;32;40mConta já paga esse mês. Deseja pagar a assinatura novamente? (s/n): \033[0m')

                if not question.upper() == 'S':
                    print('\033[0;31;40mPagamento cancelado\033[0m')
                    return
                
            pay = Payments(subscription_id=subscription.id, data=date.today())
            session.add(pay)
            session.commit()
                
            print('\033[0;32;40mPagamento realizado com sucesso\033[0m')

    def _get_last_12_months_native(self):
        today = datetime.now()
        year = today.year
        month = today.month
        last_12_months = []
        for _ in range(12):
            last_12_months.append((month, year))
            month -= 1
            if month == 0:
                month = 12
                year -= 1

        return last_12_months[::-1]

    def total_value(self):
        with Session(self.engine) as session: # busca no banco de dados
            statement = select(Subscription)
            results = session.exec(statement).all()

        total = 0
        for result in results:
            total += result.valor
        return float(total)

    def _get_values_for_month(self, last_12_months):
        with Session(self.engine) as session:
            statement = select(Payments)
            results = session.exec(statement).all()

            value_for_months = []
            for i in last_12_months:
                value = 0
                for result in results:
                    if result.data.month == i[0] and result.data.year == i[1]:
                        value += float(result.subscription.valor)

                value_for_months.append(value)
        return value_for_months

    def gen_chart(self):
        last_12_months = self._get_last_12_months_native()
        values_for_months = self._get_values_for_month(last_12_months)
        last_12_months = list(map(lambda x: x[0], self._get_last_12_months_native()))

        import matplotlib.pyplot as plt
        plt.plot(last_12_months, values_for_months)
        plt.show()


