#include <stdio.h>

double sum_array(double *arr, int size) {
    double total = 0.0;
    for (int i = 0; i < size; i++) {
        total += arr[i];

    }
    return total;

}

double one_rep_max(double weight, int reps) {
    double one_rep_max = (weight * reps * 0.0333) + weight;
    return one_rep_max;
}

int main(void) {
    double arr[] = {1.0, 4.0, 45.4, 5.0};
    int size = sizeof(arr) / sizeof(arr[0]);

    sum_array(arr, size);
    return 0;
}