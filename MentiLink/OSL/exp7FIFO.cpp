#include<iostream>
using namespace std;

int main() {
    int pages[]={7,0,1,2,0,3,0,4};
    int n=8;
    int frames = 3;
    int f[10],index=0,faults=0;
    for(int i=0;i<n;i++){
        f[i]=-1;
    }
    for(int i=0;i<n;i++){
        int found =0;
        for(int j=0;j<frames;j++){
            if(f[j]==pages[i]){
                found=1;
                break;
            }
        }
        if(found==0){
            f[index]=pages[i];
            index=(index+1)%frames;
            faults++;
        }
        cout<<"Pages"<<pages[i]<<"->";
        for(int j=0;j<frames;j++)
            cout<<f[j]<<" ";
        cout<<endl;
    }
    cout<<"Total pages faults= "<<faults;
    return 0;
}