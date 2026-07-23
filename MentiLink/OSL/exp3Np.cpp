#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "Enter number of processes: ";
    cin >> n;

    int at[n], bt[n], pr[n], ct[n], tat[n], wt[n];
    bool completed[n];

    for (int i = 0; i < n; i++) {
        cout << "Enter AT, BT and Priority for P" << i + 1 << ": ";
        cin >> at[i] >> bt[i] >> pr[i];
        completed[i] = false;
    }

    int time = 0;
    int done = 0;

    while (done < n) {
        int index = -1;
        int highest_priority = 9999;

        for (int i = 0; i < n; i++) {
            if (at[i] <= time && completed[i] == false) {
                if (pr[i] < highest_priority) {
                    highest_priority = pr[i];
                    index = i;
                }
            }
        }

        if (index != -1) {
            time = time + bt[index];
            ct[index] = time;
            tat[index] = ct[index] - at[index];
            wt[index] = tat[index] - bt[index];
            completed[index] = true;
            done++;
        } else {
            time++;
        }
    }

    cout << "Process\tAT\tBT\tPR\tCT\tTAT\tWT\n";

    for (int i = 0; i < n; i++) {
        cout << "P" << i + 1 << "\t"
             << at[i] << "\t"
             << bt[i] << "\t"
             << pr[i] << "\t"
             << ct[i] << "\t"
             << tat[i] << "\t"
             << wt[i] << endl;
    }

    return 0;
}