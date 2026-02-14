import java.util.concurrent.*;

public class ForkJoinDemo {

    // same idea as your slide
    static class SumTask extends RecursiveTask<Integer> {
        static final int THRESHOLD = 1000;

        private int begin;
        private int end;
        private int[] array;

        public SumTask(int begin, int end, int[] array) {
            this.begin = begin;
            this.end = end;
            this.array = array;
        }

        @Override
        protected Integer compute() {
            // base case
            if (end - begin < THRESHOLD) {
                int sum = 0;
                for (int i = begin; i <= end; i++) {
                    sum += array[i];
                }
                return sum;
            } else {
                int mid = (begin + end) / 2;

                SumTask leftTask  = new SumTask(begin, mid, array);
                SumTask rightTask = new SumTask(mid + 1, end, array);

                leftTask.fork();
                rightTask.fork();

                return rightTask.join() + leftTask.join();
            }
        }
    }

    public static void main(String[] args) {
        // make an array (size can be bigger than THRESHOLD so it really splits)
        int n = 20000; // > 1000, so it will fork many times
        int[] arr = new int[n];

        for (int i = 0; i < n; i++) {
            arr[i] = 1; // easy to verify: sum should be 20000
        }

        ForkJoinPool pool = new ForkJoinPool();

        // begin=0, end=n-1 (IMPORTANT because compute loop uses i <= end)
        SumTask task = new SumTask(0, n - 1, arr);

        int result = pool.invoke(task);
        System.out.println("Final Sum = " + result);

        pool.shutdown();
    }
}
