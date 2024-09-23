#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>

#define NUM_THREADS 10
pthread_mutex_t mutex;
pthread_cond_t cond;
int start_thread = 1;

void *routine(void*args) {
    pthread_mutex_lock(&mutex);
    while (start_thread) 
    {
        pthread_cond_wait(&cond, &mutex);
    }
    pthread_mutex_unlock(&mutex);
    
    system('python -m clientSide.terminais');
}

int main(int argc, char const *argv[])
{
    pthread_t thread[NUM_THREADS];
    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_create(thread[i], NULL, routine, NULL);
    }
    print("threads criadas\n");
    pthread_mutex_lock(&mutex);
    start_thread = 0;
    pthread_cond_broadcast(&cond);
    pthread_mutex_unlock(&mutex);
    print("threads iniciadas\n");
    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join(thread[i], NULL);
    }
    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&cond)

    return 0;
}
