//directory management
#include<iostream>
#include<unistd.h>
#include<sys/stat.h>
using namespace std;

int main() {
    char path[100];

    // Create a new directory named MyFolder
    mkdir("MyFolder", 0777);
    cout << "Directory created\n";

    // Move inside MyFolder
    chdir("MyFolder");
    cout << "Changed directory\n";

    // Get current working directory path
    getcwd(path, sizeof(path));
    cout << "Current Path: " << path << endl;

    // Move back to parent directory
    chdir("..");

    // Delete the directory
    rmdir("MyFolder");
    cout << "Directory removed\n";

    return 0;
}