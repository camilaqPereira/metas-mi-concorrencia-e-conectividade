#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <fstream>
#include <unistd.h>
#include <iostream>
#include <cstring>

using namespace std;

int main(int argc, char const *argv[])
{
    char buffer[1024] = {0};
    char response[1024] = {0};
    int client = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in server_addres;
    server_addres.sin_family = AF_INET;
    server_addres.sin_port = htons(8000);
    server_addres.sin_addr.s_addr = INADDR_ANY;

    connect(client, (struct sockaddr*)&server_addres, sizeof(server_addres));
    cout << "connect at server" << endl;
    cout << "write your msg: ";
    cin.getline(buffer, 1024);
    
    send(client, buffer, strlen(buffer), 0);
    cout << "Msg send to server" << endl;
    
    recv(client, response, 1024, 0);
    close(client);
    cout << "Sale id: " << response << endl;
    

    return 0;
}
