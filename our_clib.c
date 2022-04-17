#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <string.h>

# define noBuffPrintf(format,...) \
    fprintf(stderr,"[LogFromC ]: " format, __VA_ARGS__)



typedef struct OurStruct
{
    int number;
    char *string;
} OurStruct;

OurStruct *OurStruct_new()
{
    OurStruct *ourStruct = calloc(1, sizeof(OurStruct));
    return ourStruct;
}

void OurStruct_destroy(OurStruct *ourStruct)
{
    free(ourStruct);
    ourStruct = NULL;
}

void OurStruct_display(OurStruct *ourStruct)
{
    noBuffPrintf("OurStruct([number={%i},string={%s}])\n", ourStruct->number, ourStruct->string);
}

int primitive_function(int intArg, char *strArg)
{
    noBuffPrintf("c-side primitive_function received args: [intArg={%i},strArg={%s}]\n", intArg, strArg);
    return 0;
}

int isPrime(int number)
{

    if (number == 1)
    {
        return 0;
    }

    if (number == 2)

    {
        return 1;
    }

    if (number % 2 == 0)

    {
        return 0;
    }

    for (int i = 3; i <= (int)sqrt((double)number); i++)
    {
        if (number % i == 0)
        {
            return 0;
        }
    }
    return 1;
}

int* getFirstNPrimes(int n){
    int *primes = calloc(n,sizeof(int));
    int primesComputed = 0;
    int intToCheck = 2;
    while(primesComputed<n){
        if(isPrime(intToCheck)){
            primes[primesComputed]=intToCheck;
            primesComputed++;
        }
        intToCheck++;
    }
    return primes;
}