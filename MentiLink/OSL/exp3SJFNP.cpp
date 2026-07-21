#include<iostream>
using namespace std;

int main() {
    int n, at[10], bt[10], ct[10], tat[10], wt[10], done[10]={0};

    cout<<"Enter number of processes: ";
    cin>>n;

    cout<<"Enter Arrival Time and Burst Time:\n";
    for(int i=0;i<n;i++) {
        cout<<"P"<<i+1<<": ";
        cin>>at[i]>>bt[i];
    }

    int time=0,completed=0;

    while(completed<n){
        int index=-1,min=999;

        for(int i=0;i<n;i++){
            if(at[i]<=time && done[i]==0 && bt[i]<min){
                min=bt[i];
                index=i;
            }
        }

        if(index==-1){
            time++;
            continue;
        }

        time+=bt[index];
        ct[index]=time;
        tat[index]=ct[index]-at[index];
        wt[index]=tat[index]-bt[index];
        done[index]=1;
        completed++;
    }

    cout<<"\nSJF Non-Preemptive Result\n";
    cout<<"PID\tAT\tBT\tCT\tTAT\tWT\n";

    for(int i=0;i<n;i++) {
        cout<<"P"<<i+1<<"\t"
             <<at[i]<<"\t"
             <<bt[i]<<"\t"
             <<ct[i]<<"\t"
             <<tat[i]<<"\t"
             <<wt[i]<<endl;
    }

    return 0;
}