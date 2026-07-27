/* Optional companion to ariane501.py — what C actually does with the
 * Ariane conversion. Build & run:
 *
 *     cc -O2 -o ariane_overflow ariane_overflow.c && ./ariane_overflow
 *
 * Key point: Ada's checked conversion RAISES on out-of-range (loud failure).
 * C gives you neither a check nor a guaranteed wraparound: converting a
 * floating-point value to an integer type that cannot represent it is
 * UNDEFINED BEHAVIOR (C11 6.3.1.4p1). Whatever this program prints for the
 * "direct cast" line is one compiler's choice on one CPU at one optimization
 * level, not a semantics you may rely on. The only portable option is the
 * explicit range check.
 */
#include <stdio.h>
#include <stdint.h>

static int16_t to_int16_checked(double x, int *ok) {
    if (x < INT16_MIN || x > INT16_MAX) {   /* Ada-style guard, made explicit */
        *ok = 0;
        return 0;
    }
    *ok = 1;
    return (int16_t)x;
}

int main(void) {
    /* BH proxy just after t = 36.7 s on the Ariane 5 trajectory model */
    double bh = 40.0 * 36.7 + 23.24 * 36.7 * 36.7;   /* ~ 32769 */
    int ok;

    printf("BH (64-bit double)        : %.1f\n", bh);
    printf("int16 range               : [%d, %d]\n", INT16_MIN, INT16_MAX);

    /* UB: out-of-range double -> int16_t. The result can depend on CPU,
     * compiler, AND optimization level. Measured on one arm64 Apple clang 17:
     * -O0 emits a runtime convert (fcvtzs -> 32769) then truncates to 16 bits,
     * printing -32767; -O2 folds the cast away at compile time (LLVM treats
     * out-of-range fptosi as poison) and what gets printed (-32768 here) is a
     * leftover stack value, not a conversion result at all. The point is
     * exactly that the standard promises nothing. */
    int16_t direct = (int16_t)bh;
    printf("direct cast  (UB in C)    : %d   <- silent garbage, no error signal\n",
           direct);

    int16_t checked = to_int16_checked(bh, &ok);
    printf("checked conversion        : %s (ok=%d)\n",
           ok ? "value accepted" : "REJECTED - out of range, handle explicitly",
           ok);
    printf("checked fallback value    : %d\n", checked);
    return 0;
}
