#include<iostream>
using namespace std;

int main() {
    int pages[] = {7,0,1,2,0,3,0,4};
    int n = 8;
    int frames = 3;

    int f[10], faults = 0;

    for(int i=0;i<frames;i++) f[i] = -1;

    for(int i=0;i<n;i++) {
        int found = 0;

        for(int j=0;j<frames;j++) {
            if(f[j] == pages[i]) {
                found = 1;
                break;
            }
        }

        if(found == 0) {
            int pos = -1, farthest = i;

            for(int j=0;j<frames;j++) {
                int k;
                for(k=i+1;k<n;k++) {
                    if(f[j] == pages[k])
                        break;
                }

                if(k == n) {
                    pos = j;
                    break;
                }

                if(k > farthest) {
                    farthest = k;
                    pos = j;
                }
            }

            if(pos == -1) pos = 0;

            f[pos] = pages[i];
            faults++;
        }

        cout << "Page " << pages[i] << " -> ";
        for(int j=0;j<frames;j++) cout << f[j] << " ";
        cout << endl;
    }

    cout << "Total Page Faults = " << faults;
}