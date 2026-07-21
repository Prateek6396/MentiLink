//file management
#include<iostream>
#include<fcntl.h>
#include<unistd.h>
#include<string.h>
using namespace std;

int main() {
    int fd;
    char buffer[100];

    // Create a file named demo.txt
    fd = creat("demo.txt", 0777);
    cout << "File created\n";

    // Data to write into file
    char data[] = "Hello OS Lab";

    // Write data into file
    write(fd, data, strlen(data));
    cout << "Data written\n";

    // Close file after writing
    close(fd);

    // Open file in read mode
    fd = open("demo.txt", O_RDONLY);

    // Read data from file
    int n = read(fd, buffer, sizeof(buffer)-1);

    // Add null character to make it printable
    buffer[n] = '\0';

    // Display file content
    cout << "File Content: " << buffer << endl;

    // Close file after reading
    close(fd);

    // Delete the file
    unlink("demo.txt");
    cout << "File deleted\n";

    return 0;
}