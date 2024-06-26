#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
//ハイパボリックタンジェント関数
double tanh(double x){
    double plus = exp(x)+exp(-x);
    double minus = exp(x)-exp(-x);
    return minus/plus;
}

// シグモイド関数
double sigmoid(double x)
{
    return 1.0 / (1.0 + exp(-x));
}

// 層をリセット
void resetLayer(double layer[3][5])
{
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 5; j++)
        {
            layer[i][j] = 0;
        }
    }
}

// wに乱数をセット
void randW(double w[4][5][5])
{
    srand(time(NULL));
    for (int k = 0; k < 4; k++)
    {
        for (int j = 0; j < 5; j++)
        {
            for (int i = 0; i < 5; i++)
            {
                w[k][i][j] = (double)rand() / RAND_MAX;
            }
        }
    }
}

// 入力層から隠れ層
void fromInToHidden(double layer[3][5], double w[4][5][5], double input[5])
{
    for (int j = 0; j < 5; j++)
    {
        for (int i = 0; i < 5; i++)
        {
            layer[0][j] = layer[0][j] + w[0][i][j] * input[i];
        }
    }
}

// 隠れ層の計算
void hideLayer(double layer[3][5], double w[4][5][5])
{
    for (int k = 0; k < 2; k++)
    {
        for (int j = 0; j < 5; j++)
        {
            for (int i = 0; i < 5; i++)
            {
                layer[k + 1][j] = layer[k + 1][j] + w[k + 1][i][j] * sigmoid(layer[k][i]);
            }
        }
    }
}
// 隠れ層から出力層
void fromHiddenToOut(double layer[3][5], double w[4][5][5], double output[5])
{
    for (int j = 0; j < 5; j++)
    {
        for (int i = 0; i < 5; i++)
        {
            output[j] = output[j] + w[3][i][j] * sigmoid(layer[2][i]);
        }
    }
}
// 入出力層の出力
void printio(double io[5])
{
    printf("{");
    for (int j = 0; j < 4; j++)
    {
        printf("%f,", io[j]);
    }
    printf("%f}\n", io[4]);
}

// 隠れ層の出力
void printHidden(double hide[3][5])
{
    for (int i = 0; i < 3; i++)
    {
        printf("{");
        for (int j = 0; j < 4; j++)
        {
            printf("%f,", hide[i][j]);
        }
        printf("%f}\n", hide[i][4]);
    }
}

//wの出力
void printW(double w[4][5][5]){
    printf("w\n");
        for (int k = 0; k < 4; k++)
        {
            for (int i = 0; i < 5; i++)
            {
                printf("{");
                for (int j = 0; j < 4; j++)
                {
                    printf("%f,", w[k][i][j]);
                }
                printf("%f}\n", w[k][i][4]);
            }
        }
}
// 平均二乗誤差
double MSE(double output[5], double t[5])
{
    double answer = 0;
    for (int i = 0; i < 5; i++)
    {
        answer += pow(output[i] - t[i], 2);
    }
    return sqrt(answer / 5);
}

/*------------------------------------------------------------
                            以下main関数
------------------------------------------------------------*/
int main(int argc[])
{
    double layer[3][5] = {{0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}, {0, 0, 0, 0, 0}};
    double w[4][5][5] = {{{1, 1, 1, 1, 1}, {1, 1, 1, 1, 1}, {1, 1, 1, 1, 1}, {1, 1, 1, 1, 1}, {1, 1, 1, 1, 1}}, {{1, 1, 1, 1, 1}, {1, 1, 1, 1, 1}, {1, 1, 1, 1, 1}, {1, 1, 1, 1, 1}, {1, 1, 1, 1, 1}}, {{1, 1, 1, 1, 1}, {1, 1, 1, 1, 1}, {1, 1, 1, 1, 1}, {1, 1, 1, 1, 1}, {1, 1, 1, 1, 1}}, {{1, 1, 1, 1, 1}, {1, 1, 1, 1, 1}, {1, 1, 1, 1, 1}, {1, 1, 1, 1, 1}, {1, 1, 1, 1, 1}}};
    double input[5] ;
    double output[5] = {0, 0, 0, 0, 0};
    double t[5] ;
    int epoch = 0;
    int randInput;
    // 層をリセット
    resetLayer(layer);

    // wに乱数をセット
    randW(w);
    srand(time(NULL));
    do
    {   
        for(int s=0;s<5;s++){
            double ransu=(double)rand()*2/RAND_MAX -1;
            input[s]=ransu;
            t[s]=ransu;
        }
        randInput=rand()%3;
        epoch++;
        // 入力層から隠れ層
        fromInToHidden(layer, w, input);

        // 隠れ層の計算
        hideLayer(layer, w);

        // 隠れ層から出力層
        fromHiddenToOut(layer, w, output);

        // 入力層の出力
        //printf("入力層\n");
        printio(input);

        // 隠れ層の出力
        //printf("隠れ層\n");
        //printHidden(layer);

        // 出力層の出力
        //printf("出力層\n");
        printio(output);

        // 平均二乗誤差の出力
        printf("誤差評価\n");
        printf("%f\n", MSE(output, t));

        // wの出力
        
        // 出力層から隠れ層の逆伝播法
        double delta[4][5];
        for (int i = 0; i < 5; i++)
        {
            for (int j = 0; j < 5; j++)
            {
                delta[3][j] = (output[j] - t[j]);
                w[3][i][j] = w[3][i][j] - (delta[3][j] * sigmoid(layer[2][i]) / (double)(epoch));
            }
        }

        // 隠れ層の逆伝播法
        for (int k = 2; k > 0; k--)
        {

            for (int i = 0; i < 5; i++)
            {
                for (int j = 0; j < 5; j++)
                {
                    double sum = 0;
                    for (int h = 0; h < 5; h++)
                    {
                        sum += delta[k+1][h] * w[k][i][h];
                    }
                    delta[k][j] = ((1 - sigmoid(layer[k][j])) * sigmoid(layer[k][j]) * sum);
                    w[k][i][j] = w[k][i][j] - (delta[k][j] * sigmoid(layer[k - 1][i]) / (double)(epoch));
                }
            }
        }
        for (int i = 0; i < 5; i++)
        {
            for (int j = 0; j < 5; j++)
            {
                double sum = 0;
                for (int h = 0; h < 5; h++)
                {
                    sum += delta[1][h] * w[0][i][h];
                }
                delta[0][j] = ((1 - sigmoid(layer[0][j])) * sigmoid(layer[0][j]) * sum);
                w[0][i][j] = w[0][i][j] - (delta[0][j] * sigmoid(input[i]) / (double)(epoch));
            }
        }
        
        /*
        逆伝播法を導入
        */
    } while (epoch <= 50000);
}
