#include <stdio.h>
#include <stdlib.h>
#include <time.h>
//�w�����Z�b�g
void resetLayer(float layer[3][5]){
    for(int i=0;i<3;i++){
        for(int j=0;j<5;j++){
            layer[i][j]=0;
        }
    }
}

//w�ɗ������Z�b�g
void randW(float w[4][5][5]){
    srand(time(NULL));
    for(int k=0;k<4;k++){
        for(int j=0;j<5;j++){
            for(int i=0;i<5;i++){
                w[k][i][j]=(double)rand()/RAND_MAX;
            }
        }
    }
}

//���͑w����B��w
void fromInToHide(float layer[3][5],float w[4][5][5],float input[5]){
    for(int j=0;j<5;j++){
        for(int i=0;i<5;i++){
            layer[0][j]=layer[0][j]+w[0][i][j]*input[i];
        }
    }
}

//�B��w�̌v�Z
void hideLayer(float layer[3][5],float w[4][5][5]){
    for(int k=0;k<2;k++){
        for(int j=0;j<5;j++){
            for(int i=0;i<5;i++){
                layer[k+1][j]=layer[k+1][j]+w[k+1][i][j]*layer[k][i];
            }
        }
    }
}
//�B��w����o�͑w
void fromHideToOut(float layer[3][5],float w[4][5][5],float output[5]){
    for(int j=0;j<5;j++){
        for(int i=0;i<5;i++){
            output[j]=output[j]+w[3][i][j]*layer[2][i];
        }
    }
}
//���o�͑w�̏o��
void printio(float io[5]){
    printf("{");
    for(int j=0;j<4;j++){
        printf("%f,",io[j]);
    }
    printf("%f}\n",io[4]);
}

//�B��w�̏o��
void printHide(float hide[3][5]){
    for(int i=0;i<3;i++){
        printf("{");
    for(int j=0;j<4;j++){
        printf("%f,",hide[i][j]);
    }
    printf("%f}\n",hide[i][4]);
    }
}
/*------------------------------------------------------------
                            �ȉ�main�֐�
------------------------------------------------------------*/
int main(int argc[]){
    float layer[3][5]={{0,0,0,0,0},{0,0,0,0,0},{0,0,0,0,0}};
    float w[4][5][5]={{{1,1,1,1,1},{1,1,1,1,1},{1,1,1,1,1},{1,1,1,1,1},{1,1,1,1,1}},{{1,1,1,1,1},{1,1,1,1,1},{1,1,1,1,1},{1,1,1,1,1},{1,1,1,1,1}},{{1,1,1,1,1},{1,1,1,1,1},{1,1,1,1,1},{1,1,1,1,1},{1,1,1,1,1}},{{1,1,1,1,1},{1,1,1,1,1},{1,1,1,1,1},{1,1,1,1,1},{1,1,1,1,1}}};
    float input[5]={0.5,0.2,0.3,0.5,0.4};
    float output[5]={0,0,0,0,0};
    //�w�����Z�b�g
    resetLayer(layer);

    //w�ɗ������Z�b�g
    randW(w);

    //���͑w����B��w
    fromInToHide(layer,w,input);

    //�B��w�̌v�Z
    hideLayer(layer,w);

    //�B��w����o�͑w
    fromHideToOut(layer,w,output);

    //���͑w�̏o��
    printf("���͑w\n");
    printio(input);

    //�B��w�̏o��
    printf("�B��w\n");
    printHide(layer);

    //�o�͑w�̏o��
    printf("�o�͑w\n");
    printio(output);

}