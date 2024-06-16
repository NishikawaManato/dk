#include <stdio.h>
#include <stdlib.h>

int RGBmax(int R,int G, int B){
    if(R>=G){
        if(R>=B){
            return R;
        }else{
            return B;
        }
    }else{
        if(G>=B){
            return G;
        }else{
            return B;
        }
    }
}


int RGBmin(int R,int G, int B){
    if(R>=G){
        if(G>=B){
            return B;
        }else{
            return G;
        }
    }else{
        if(R>=B){
            return G;
        }else{
            return B;
        }
    }
}


int main(void){
    int R,G,B,H,S,V;
    printf("R,G,B\n");
    scanf("%d,%d,%d",&R,&G,&B);
    int max=RGBmax(R,G,B);
    int min=RGBmin(R,G,B);
    if(max==min){
        H=0;
    }else if(max==R){
        H=60*(G-R)/(max-min);
    }else if(max==G){
        H=120+60*(B-G)/(max-min);
    }else{
        H=240+60*(R-B)/(max-min);
    }
    S=max-min;
    V=max;
    printf("(H,S,V)=(%d,%d,%d)",H,S,V);
}