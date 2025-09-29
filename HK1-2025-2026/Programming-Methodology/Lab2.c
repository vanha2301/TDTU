#include <stdio.h>
#include <math.h>

long long ucln(long long a, long long b) {
    while (b) {
        long long t = a % b;
        a = b;
        b = t;
    }
    return a < 0 ? -a : a;
}

int nt(long long n) {
    if (n < 2) return 0;
    if (n % 2 == 0) return n == 2;
    for (long long i = 3; i * i <= n; i += 2) {
        if (n % i == 0) return 0;
    }
    return 1;
}

long long luythua(long long a, long long b) {
    long long r = 1;
    for (long long i = 0; i < b; i++) r *= a;
    return r;
}

void bai1() {
    long long n, s = 0;
    printf("Nhap n: ");
    scanf("%lld", &n);
    for (long long i = 2; i <= n; i += 2) s += i;
    printf("Tong so chan 1..%lld = %lld\n", n, s);
}

void bai2() {
    long long n, s = 0;
    printf("Nhap n: ");
    scanf("%lld", &n);
    for (long long i = 1; i <= n; i += 2) s += i;
    printf("Tong so le 1..%lld = %lld\n", n, s);
}

void bai3() {
    long long a;
    printf("Nhap a: ");
    scanf("%lld", &a);
    for (int i = 1; i <= 10; i++) {
        printf("%lld x %d = %lld\n", a, i, a * i);
    }
}

void bai4() {
    long long n, s = 0;
    printf("Nhap n: ");
    scanf("%lld", &n);
    for (long long i = 1; i <= n; i++) s += i;
    printf("Tong 1..%lld = %lld\n", n, s);
}

void bai5() {
    long long n;
    printf("Nhap n: ");
    scanf("%lld", &n);
    if (n < 0) n = -n;
    long long cuoi = n % 10;
    long long dau = n;
    while (dau >= 10) dau /= 10;
    printf("Chu so dau = %lld, cuoi = %lld\n", dau, cuoi);
}

void bai6() {
    long long n, s = 0;
    printf("Nhap n: ");
    scanf("%lld", &n);
    if (n < 0) n = -n;
    if (n == 0) s = 0;
    while (n > 0) {
        s += n % 10;
        n /= 10;
    }
    printf("Tong chu so = %lld\n", s);
}

void bai7() {
    long long n, p = 1;
    printf("Nhap n: ");
    scanf("%lld", &n);
    if (n < 0) n = -n;
    if (n == 0) p = 0;
    while (n > 0) {
        p *= n % 10;
        n /= 10;
    }
    printf("Tich chu so = %lld\n", p);
}

void bai8() {
    long long n, r = 0;
    printf("Nhap n: ");
    scanf("%lld", &n);
    int am = n < 0;
    if (am) n = -n;
    while (n > 0) {
        r = r * 10 + n % 10;
        n /= 10;
    }
    if (am) r = -r;
    printf("So dao nguoc = %lld\n", r);
}

void bai9() {
    long long n;
    int d = 0;
    printf("Nhap n: ");
    scanf("%lld", &n);
    if (n == 0) d = 1;
    if (n < 0) n = -n;
    while (n > 0) {
        d++;
        n /= 10;
    }
    printf("So chu so = %d\n", d);
}

int main() {
    int chon;
    do {
        printf("\nMenu:\n");
        printf("1. Bai 1\n");
        printf("2. Bai 2\n");
        printf("3. Bai 3\n");
        printf("4. Bai 4\n");
        printf("5. Bai 5\n");
        printf("6. Bai 6\n");
        printf("7. Bai 7\n");
        printf("8. Bai 8\n");
        printf("9. Bai 9\n");
        printf("0. Thoat\n");
        printf("Chon bai: ");
        if (scanf("%d", &chon) != 1) return 0;

        switch (chon) {
            case 1: bai1(); break;
            case 2: bai2(); break;
            case 3: bai3(); break;
            case 4: bai4(); break;
            case 5: bai5(); break;
            case 6: bai6(); break;
            case 7: bai7(); break;
            case 8: bai8(); break;
            case 9: bai9(); break;
            case 0: printf("Ket thuc.\n"); break;
            default: printf("Khong hop le.\n");
        }
    } while (chon != 0);

    return 0;
}
