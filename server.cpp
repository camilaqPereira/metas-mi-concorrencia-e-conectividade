#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <unistd.h>
#include <thread>
#include <iostream>
#include <cstring>
#include <cstdlib>
#include <ctime>


using namespace std;

void sell_a_tickt(int* id, int client) {
    char buffer[1024] = {0};
    cout << "venda realizada com sucesso!"<< endl;
    *id = rand() % 1000;
    sprintf(buffer, "%d", *id);
    send(client, buffer, 1024, 0);
}

int main(int argc, char const *argv[])
{
    srand(time(NULL));
    char buffer[1024] = {0};
    int sale_id = 0;
    int server = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in server_addres;
    server_addres.sin_family = AF_INET;
    server_addres.sin_port = htons(8000);
    server_addres.sin_addr.s_addr = INADDR_ANY;

    bind(server, (struct sockaddr*)&server_addres, sizeof(server_addres));

    listen(server, 0);

    cout << "server on, waiting a client" << endl;
    int client = accept(server, nullptr, nullptr);

    cout << "Client connect" << endl;

    recv(client, buffer, sizeof(buffer), 0);

    if (strcmp(buffer, "comprar") == 0) {
        thread venda (sell_a_tickt, &sale_id, client);
        venda.join();
    }

    cout << "Client sale id: " << sale_id << endl;

    close(server);

    return 0;
}
