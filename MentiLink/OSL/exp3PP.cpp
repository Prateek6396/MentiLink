#include<iostream>
using namespace std;

int main() {
    int n, at[10], bt[10], pr[10], rt[10];
    int ct[10], tat[10], wt[10];

    cout<<"Enter number of processes: ";
    cin>>n;

    cout<<"Enter AT, BT, Priority:\n";
    for(int i=0;i<n;i++) {
        cout<<"P"<<i+1<<": ";
        cin>>at[i]>>bt[i]>>pr[i];
        rt[i]=bt[i];
    }

    int time=0, completed=0;

    while(completed<n){
        int index=-1,max=999;

        for(int i=0;i<n;i++){
            if(at[i]<=time && rt[i]>0 && pr[i]<max){
                max=pr[i];
                index=i;
            }
        }

        if(index==-1){
            time++;
            continue;
        }

        rt[index]--;
        time++;

        if(rt[index]==0){
            completed++;
            ct[index]=time;
            tat[index]=ct[index]-at[index];
            wt[index]=tat[index]-bt[index];
        }
    }

    cout<<"\nPriority Preemptive Result\n";
    cout<<"PID\tAT\tBT\tPR\tCT\tTAT\tWT\n";

    for(int i=0;i<n;i++) {
        cout<<"P"<<i+1<<"\t"
             <<at[i]<<"\t"
             <<bt[i]<<"\t"
             <<pr[i]<<"\t"
             <<ct[i]<<"\t"
             <<tat[i]<<"\t"
             <<wt[i]<<endl;
    }

    return 0;
}