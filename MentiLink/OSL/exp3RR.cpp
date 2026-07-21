#include<iostream>
using namespace std;

int main() {
    int n, bt[10], rt[10], ct[10], tat[10], wt[10];
    int tq;

    cout<<"Enter number of processes: ";
    cin>>n;

    cout<<"Enter Burst Time:\n";
    for(int i=0;i<n;i++) {
        cout<<"P"<<i+1<<": ";
        cin>>bt[i];
        rt[i]=bt[i];
    }

    cout<<"Enter Time Quantum: ";
    cin>>tq;

    int time=0;

    while(true){
        int done=1;

        for(int i=0;i<n;i++){
            if(rt[i]>0){
                done=0;

                if(rt[i]>tq){
                    time+=tq;
                    rt[i]-=tq;
                }
                else{
                    time+=rt[i];
                    ct[i]=time;
                    rt[i]=0;
                }
            }
        }

        if(done==1)
            break;
    }

    for(int i=0;i<n;i++) {
        tat[i]=ct[i];
        wt[i]=tat[i]-bt[i];
    }

    cout<<"\nRound Robin Result\n";
    cout<<"PID\tBT\tCT\tTAT\tWT\n";

    for(int i=0;i<n;i++) {
        cout<<"P"<<i+1<<"\t"
             <<bt[i]<<"\t"
             <<ct[i]<<"\t"
             <<tat[i]<<"\t"
             <<wt[i]<<endl;
    }

    return 0;
}