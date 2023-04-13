class powerof {
    public static void main(String[] args) {
        int base = 104, exponent = 335174789;

        long result = 1;

        for (; exponent != 0; --exponent) {
            result *= base;
        }

        System.out.println("Answer = " + result);
    }
}