#include<iostream>
using namespace std;

int main() {
    int pages[] = {7,0,1,2,0,3,0,4};
    int n = 8;
    int frames = 3;

    int f[10], time[10], counter = 0, faults = 0;

    for(int i=0;i<frames;i++){ 
        f[i] = -1; 
        time[i]=-1;
    }

    for(int i=0;i<n;i++) {
        int found = 0;

        for(int j=0;j<frames;j++) {
            if(f[j] == pages[i]) {
                counter++;
                time[j] = counter;
                found = 1;
                break;
            }
        }

        if(found == 0) {
            int pos = 0;
            for(int j=1;j<frames;j++) {
                if(time[j] < time[pos])
                    pos = j;
            }

            f[pos] = pages[i];
            counter++;
            time[pos] = counter;
            faults++;
        }

        cout << "Page " << pages[i] << " -> ";
        for(int j=0;j<frames;j++) cout << f[j] << " ";
        cout << endl;
    }

    cout << "Total Page Faults = " << faults;
}