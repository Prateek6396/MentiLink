#include<iostream>
using namespace std;

int main(){
    int n,at[10],bt[10],ct[10],tat[10],wt[10],pid[10];

    cout<<"Enter n:";
    cin>>n;

    cout<<"Enter burst time and arrival time:\n";
    for(int i=0;i<n;i++){
        cout<<"P"<<i+1<<":";
        cin>>at[i]>>bt[i];
        pid[i]=i+1;
    }

    int temp;
    for(int i=0;i<n-1;i++){
        for(int j=0;j<n-i-1;j++){
            if(at[j]>at[j+1]){

                temp=at[j];
                at[j]=at[j+1];
                at[j+1]=temp;

                temp=bt[j];
                bt[j]=bt[j+1];
                bt[j+1]=temp;

                temp=pid[j];
                pid[j]=pid[j+1];
                pid[j+1]=temp;
            }
        }
    }

    ct[0]=at[0]+bt[0];

    for(int i=1;i<n;i++){
        if(ct[i-1]<at[i])
            ct[i]=at[i]+bt[i];
        else
            ct[i]=ct[i-1]+bt[i];
    }

    for(int i=0;i<n;i++){
        tat[i]=ct[i]-at[i];
        wt[i]=tat[i]-bt[i];
    }

    cout<<"\nFCFS\n";
    cout<<"PID\tAT\tBT\tCT\tTAT\tWT\n";

    for(int i=0;i<n;i++){
        cout<<"P"<<pid[i]<<"\t"
            <<at[i]<<"\t"
            <<bt[i]<<"\t"
            <<ct[i]<<"\t"
            <<tat[i]<<"\t"
            <<wt[i]<<endl;
    }

    for(int i=0;i<n;i++){
        cout<<"P"<<pid[i]<<" |";
    }

    cout<<"\n0";
    for(int i=0;i<n;i++){
        cout<<" "<<ct[i];
    }

    return 0;
}