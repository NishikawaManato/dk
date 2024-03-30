#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

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
            layer[0][j] = sigmoid(layer[0][j] + w[0][i][j] * input[i]);
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
                layer[k + 1][j] = sigmoid(layer[k + 1][j] + w[k + 1][i][j] * layer[k][i]);
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
            output[j] = sigmoid(output[j] + w[3][i][j] * layer[2][i]);
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
// 平均二乗誤差
double MSE(double output[5], double t[5])
{
    double answer = 0;
    for (int i = 0; i < 5; i++)
    {
        answer = +pow(output[i] - t[i], 2);
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
    double input[5] = {0.5, -0.2, 0.3, -0.5, 0.4};
    double output[5] = {0, 0, 0, 0, 0};
    double t[5] = {0.5, -0.2, 0.3, -0.5, 0.4};
    // 層をリセット
    resetLayer(layer);

    // wに乱数をセット
    randW(w);

    // 入力層から隠れ層
    fromInToHidden(layer, w, input);

    // 隠れ層の計算
    hideLayer(layer, w);

    // 隠れ層から出力層
    fromHiddenToOut(layer, w, output);

    // 入力層の出力
    printf("入力層\n");
    printio(input);

    // 隠れ層の出力
    printf("隠れ層\n");
    printHidden(layer);

    // 出力層の出力
    printf("出力層\n");
    printio(output);

    // 平均に乗誤差の出力
    printf("誤差評価\n");
    printf("%f", MSE(output, t));

    /*
    逆伝播法を導入
    */
}
