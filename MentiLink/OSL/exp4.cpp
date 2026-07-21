/*with thread in c
#include<stdio.h>
#include<pthread.h>
int flag[2]={0,0};
int turn;

void* process0(void* arg){
    flag[0]=1;
    turn=1;
    while(flag[1] && turn ==1);
    printf("Process 0 in crtical section\n");
    flag[0]=0;
    return NULL;
}

void* process1(voide* arg){
    flag[1]=1;
    turn=0;
    while(flag[0]&&turn==0);
    printf("Process 1 in crticial section\n");
    flag[1]=0;
    return NULL;
}
int main(){
    pthread_t t1,t2;
    pthread_create(&t1,NULL,process0,NULL);
    pthread_create(&t2,NULL,process1,NULL);
    pthread_join(t1,NULL);
    pthread_join(t2,NULL);
    return 0;
}*/

// without thread in c++
/*#include <iostream>
using namespace std;

bool flag[2] = {false, false};
int turn;


void p0() {
    flag[0] = true;
    turn = 1;

    while(flag[1] && turn == 1);

    cout << "Process 0 in critical section\n";

    flag[0] = false;
}

void p1() {
    flag[1] = true;
    turn = 0;

    while(flag[0] && turn == 0);

    cout << "Process 1 in critical section\n";

    flag[1] = false;
}

int main() {
    p0();
    p1();
    p0();
    p1();

    return 0;
}*/
