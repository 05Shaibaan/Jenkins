package dev.shaibaan.calculator;

/** Arithmetic across zero, demonstrated by 05Shaibaan's independent Jenkins jobs. */
public final class SignedCalculator {
    public int add(int left, int right) { return left + right; }
    public int subtract(int left, int right) { return left - right; }

    public static void main(String[] args) {
        SignedCalculator calculator = new SignedCalculator();
        System.out.println("[05Shaibaan CI VERIFIED | Signed Arithmetic | release 1.1.0]");
        System.out.println("12 + (-7) = " + calculator.add(12, -7));
        System.out.println("-3 - 8 = " + calculator.subtract(-3, 8));
    }
}
