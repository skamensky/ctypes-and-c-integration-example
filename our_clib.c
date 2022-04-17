#include <stdio.h>
#include <stdlib.h>

typedef struct OurStruct{
    int number;
    char *string;
} OurStruct;

OurStruct* OurStruct_new(){
    OurStruct* ourStruct = calloc(1,sizeof(OurStruct));
    return ourStruct;
}

void OurStruct_destroy(OurStruct *ourStruct){
    free(ourStruct);
    ourStruct=NULL;
}

void OurStruct_display(OurStruct *ourStruct){
    printf("OurStruct([number={%i},string={%s}])\n",ourStruct->number,ourStruct->string);
}

int primitive_function(int intArg,char * strArg){
    printf("c-side primitive_function received args: [intArg={%i},strArg={%s}]\n",intArg,strArg);
    return 0;
}