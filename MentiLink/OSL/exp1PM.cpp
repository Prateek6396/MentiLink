//process management
#include<iostream>
#include<unistd.h>
#include<sys/wait.h>
using namespace std;

int main() {

    // Create a new process
    int pid = fork();

    // Child process executes this block
    if(pid == 0) {
        cout << "Child Process Running\n";
        cout << "Child PID: " << getpid() << endl;
    }

    // Parent process executes this block
    else {
        // Parent waits until child finishes
        wait(NULL);

        cout << "Parent Process Running\n";
        cout << "Parent PID: " << getpid() << endl;
    }

    return 0;
}