#include<iostream>
using namespace std;

void firstfit(int blocksize[], int m, int processSize[], int n){
    int allocation[10];

    for(int i = 0; i < n; i++)
        allocation[i] = -1;

    for(int i = 0; i < n; i++){
        for(int j = 0; j < m; j++){
            if(blocksize[j] >= processSize[i]){
                allocation[i] = j;
                blocksize[j] -= processSize[i];
                break;
            }
        }
    }

    cout << "\nFirst Fit Allocation:\n";
    for(int i = 0; i < n; i++){
        if(allocation[i] != -1)
            cout << "Process " << i+1 << " -> Block " << allocation[i]+1 << endl;
        else
            cout << "Process " << i+1 << " -> Not Allocated\n";
    }
}

int main(){
    int block[] = {100, 500, 200, 300, 600};
    int processSize[] = {212, 417, 112, 426};

    int m = 5;
    int n = 4;

    firstfit(block, m, processSize, n);

    return 0;
}