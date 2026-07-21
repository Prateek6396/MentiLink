#include <iostream>
using namespace std;
int main() {
    int n, m;
    int alloc[10][10], maxm[10][10], need[10][10];
    int avail[10], finish[10] = {0}, safeSeq[10];
    cout << "Enter number of processes: ";
    cin >> n;
    cout << "Enter number of resources: ";
    cin >> m;
    cout << "Enter Allocation matrix:\n";
    for(int i = 0; i < n; i++)
        for(int j = 0; j < m; j++)
            cin >> alloc[i][j];

    cout << "Enter Max matrix:\n";
    for(int i = 0; i < n; i++)
        for(int j = 0; j < m; j++)
            cin >> maxm[i][j];

    cout << "Enter Available resources:\n";
    for(int j = 0; j < m; j++)
        cin >> avail[j];

    // Calculate Need
    for(int i = 0; i < n; i++)
        for(int j = 0; j < m; j++)
            need[i][j] = maxm[i][j] - alloc[i][j];

    int count = 0;

    while(count < n) {
        int found = 0;

        for(int i = 0; i < n; i++) {
            if(finish[i] == 0) {

                int j;
                for(j = 0; j < m; j++) {
                    if(need[i][j] > avail[j])
                        break;
                }

                if(j == m) {//all resources satisfied
                    for(int k = 0; k < m; k++)
                        avail[k] += alloc[i][k];//process finishes releases resources

                    safeSeq[count++] = i;
                    finish[i] = 1;
                    found = 1;
                }
            }
        }

        if(found == 0) {
            cout << "System is NOT in safe state\n";
            return 0;
        }
    }

    cout << "System is SAFE\nSafe sequence: ";
    for(int i = 0; i < n; i++)
        cout << "P" << safeSeq[i] << " ";

    return 0;
}