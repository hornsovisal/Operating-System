import java.util.concurrent.Semaphore;

class Account {
    String name;
    int balance;
    Semaphore lock;

    Account(String name, int balance) {
        this.name = name;
        this.balance = balance;
        this.lock = new Semaphore(1);
    }
}

class Transfer {

    // Deadlock version
    static void transfer(Account from, Account to, int amount) {
        try {
            System.out.println(Thread.currentThread().getName()
                    + " trying to lock FROM " + from.name);
            from.lock.acquire();
            System.out.println(Thread.currentThread().getName()
                    + " locked FROM " + from.name);

            Thread.sleep(100);

            System.out.println(Thread.currentThread().getName()
                    + " trying to lock TO " + to.name);
            to.lock.acquire();
            System.out.println(Thread.currentThread().getName()
                    + " locked TO " + to.name);

            from.balance -= amount;
            to.balance += amount;

            System.out.println(Thread.currentThread().getName()
                    + " transfer completed");

            to.lock.release();
            from.lock.release();

        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    // Global ordering solution
    static void transferOrdered(Account from, Account to, int amount) {
        Account first;
        Account second;

        if (from.name.compareTo(to.name) < 0) {
            first = from;
            second = to;
        } else {
            first = to;
            second = from;
        }

        try {
            System.out.println(Thread.currentThread().getName()
                    + " trying to lock " + first.name);
            first.lock.acquire();
            System.out.println(Thread.currentThread().getName()
                    + " locked " + first.name);

            Thread.sleep(100);

            System.out.println(Thread.currentThread().getName()
                    + " trying to lock " + second.name);
            second.lock.acquire();
            System.out.println(Thread.currentThread().getName()
                    + " locked " + second.name);

            from.balance -= amount;
            to.balance += amount;

            System.out.println(Thread.currentThread().getName()
                    + " transfer completed");

            second.lock.release();
            first.lock.release();

        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}

public class DeadlockSimulation {

    public static void main(String[] args) throws InterruptedException {

        if (args.length == 0) {
            System.out.println("Usage: java DeadlockSimulation deadlock");
            System.out.println("   or: java DeadlockSimulation ordered");
            return;
        }

        if (args[0].equalsIgnoreCase("deadlock")) {
            runDeadlock();
        } else if (args[0].equalsIgnoreCase("ordered")) {
            runOrdered();
        } else {
            System.out.println("Invalid option.");
            System.out.println("Use: java DeadlockSimulation deadlock");
            System.out.println(" or: java DeadlockSimulation ordered");
        }
    }

    static void runDeadlock() {
        System.out.println("===== DEADLOCK VERSION =====");

        Account account1 = new Account("Account-1", 1000);
        Account account2 = new Account("Account-2", 1000);

        Thread t1 = new Thread(() ->
                Transfer.transfer(account1, account2, 100), "Thread-1");

        Thread t2 = new Thread(() ->
                Transfer.transfer(account2, account1, 200), "Thread-2");

        t1.start();
        t2.start();
    }

    static void runOrdered() throws InterruptedException {
        System.out.println("===== GLOBAL ORDERING SOLUTION =====");

        Account account1 = new Account("Account-1", 1000);
        Account account2 = new Account("Account-2", 1000);

        Thread t1 = new Thread(() ->
                Transfer.transferOrdered(account1, account2, 100), "Thread-1");

        Thread t2 = new Thread(() ->
                Transfer.transferOrdered(account2, account1, 200), "Thread-2");

        t1.start();
        t2.start();

        t1.join();
        t2.join();

        System.out.println("Final balances:");
        System.out.println(account1.name + ": " + account1.balance);
        System.out.println(account2.name + ": " + account2.balance);
    }
}