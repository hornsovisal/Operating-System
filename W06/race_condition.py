import threading


class Bank:
    balance = 0

    def deposit(self):
        Bank.balance += 100

    def withdraw(self):
        Bank.balance -= 100

    def get_value(self):
        return Bank.balance

    def run(self):
        self.deposit()
        print(f"Value for Thread after deposit {threading.current_thread().name} {self.get_value()}")
        self.withdraw()
        print(f"Value for Thread after withdraw {threading.current_thread().name} {self.get_value()}")


def main():
    bank_instance = Bank()

    t1 = threading.Thread(target=bank_instance.run, name="Thread1")
    t2 = threading.Thread(target=bank_instance.run, name="Thread2")
    t3 = threading.Thread(target=bank_instance.run, name="Thread3")

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()


if __name__ == "__main__":
    main()
