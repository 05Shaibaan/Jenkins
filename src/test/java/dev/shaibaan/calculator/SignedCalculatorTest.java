package dev.shaibaan.calculator;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

class SignedCalculatorTest {
    private final SignedCalculator calculator = new SignedCalculator();

    @Test void addsPositiveAndNegativeOperands() {
        assertEquals(5, calculator.add(12, -7));
    }

    @Test void subtractsAcrossZero() {
        assertEquals(11, calculator.subtract(-3, 8));
    }
}
