#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
//ƒnƒCƒpƒ{ƒŠƒbƒNƒ^ƒ“ƒWƒFƒ“ƒgŠÖ”
double tanh(double x){
    double plus = exp(x)+exp(-x);
    double minus = exp(x)-exp(-x);
    return minus/plus;
}

// ƒVƒOƒ‚ƒCƒhŠÖ”
double sigmoid(double x)
{
    return 1.0 / (1.0 + exp(-x));
}

// ‘w‚ğƒŠƒZƒbƒg
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

// w‚É—”‚ğƒZƒbƒg
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

// “ü—Í‘w‚©‚ç‰B‚ê‘w
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

// ‰B‚ê‘w‚ÌŒvZ
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
// ‰B‚ê‘w‚©‚ço—Í‘w
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
// “üo—Í‘w‚Ìo—Í
void printio(double io[5])
{
    printf("{");
    for (int j = 0; j < 4; j++)
    {
        printf("%f,", io[j]);
    }
    printf("%f}\n", io[4]);
}

// ‰B‚ê‘w‚Ìo—Í
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

//w‚Ìo—Í
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
// •½‹Ï“ñæŒë·
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
                            ˆÈ‰ºmainŠÖ”
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
    // ‘w‚ğƒŠƒZƒbƒg
    resetLayer(layer);

    // w‚É—”‚ğƒZƒbƒg
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
        // “ü—Í‘w‚©‚ç‰B‚ê‘w
        fromInToHidden(layer, w, input);

        // ‰B‚ê‘w‚ÌŒvZ
        hideLayer(layer, w);

        // ‰B‚ê‘w‚©‚ço—Í‘w
        fromHiddenToOut(layer, w, output);

        // “ü—Í‘w‚Ìo—Í
        //printf("“ü—Í‘w\n");
        printio(input);

        // ‰B‚ê‘w‚Ìo—Í
        //printf("‰B‚ê‘w\n");
        //printHidden(layer);

        // o—Í‘w‚Ìo—Í
        //printf("o—Í‘w\n");
        printio(output);

        // •½‹Ï“ñæŒë·‚Ìo—Í
        printf("Œë·•]‰¿\n");
        printf("%f\n", MSE(output, t));

        // w‚Ìo—Í
        
        // o—Í‘w‚©‚ç‰B‚ê‘w‚Ì‹t“`”d–@
        double delta[4][5];
        for (int i = 0; i < 5; i++)
        {
            for (int j = 0; j < 5; j++)
            {
                delta[3][j] = (output[j] - t[j]);
                w[3][i][j] = w[3][i][j] - (delta[3][j] * sigmoid(layer[2][i]) / (double)(epoch));
            }
        }

        // ‰B‚ê‘w‚Ì‹t“`”d–@
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
        ‹t“`”d–@‚ğ“±“ü
        */
    } while (epoch <= 50000);
}
